#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aris_audit.py — ARIS 对抗式声明审计 · 前置自审脚本（light 模式，零交互）

子命令：
  extract  阶段2：喂草稿.md -> 生成 Claim Ledger 台账骨架（证据列留空标 ⚠️，可用 --mark 自定义）
  drift    阶段3：喂成稿 + ledger.md -> 输出漂移清单（成稿有台账无 / 弱声明被强化）
  gate     收口闸门：台账仍有未验证声明 -> 退出码 10，禁止 Finish（严格闭环硬保障）

设计约束：
  - 零交互：所有选项走 flag，无 input() 询问
  - 默认 light 模式（纯规则启发式，不调 LLM、不联网、零依赖）
  - 证据缺口留空标 ⚠️，绝不追问
  - 定位是"前置自审、降缺口"，不替代 Hermes + SenseNova 异族审

错误处理：所有可预期错误都带「错误码 + 退出码 + 一行修复提示」，见 AuditError。
常见退出码：2=文件不存在/是目录，3=编码或二进制，4=空文件，7=文件过大，10=gate 未闭环。

仅依赖 Python 标准库。
"""

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_MAX_BYTES = 5 * 1024 * 1024  # 5MB：超大文档默认拒绝，防卡死
MAX_LINE_CHARS = 20000               # 单行超长截断，防正则灾难


# ---------- 错误处理（统一错误体系 · 错误码 + 退出码 + 修复提示） ----------
class AuditError(Exception):
    """统一错误：带错误码、友好中文消息、可操作修复提示、退出码。

    用法：raise FileNotFound("...", fix="...") ；在命令里 except AuditError 后调 _die(e)。
    """
    CODE = "ERR-UNKNOWN"
    EXIT = 1

    def __init__(self, message, fix=None):
        self.message = message
        self.fix = fix
        super().__init__(message)

    def render(self):
        parts = [f"[aris_audit] ❌ {self.CODE}：{self.message}"]
        if self.fix:
            parts.append(f"    🔧 修复：{self.fix}")
        parts.append(f"    （错误码 {self.CODE} · 退出码 {self.EXIT}）")
        return "\n".join(parts)


class FileNotFound(AuditError):
    CODE, EXIT = "ERR-FILE-NOT-FOUND", 2


class IsDirectory(AuditError):
    CODE, EXIT = "ERR-IS-DIR", 2


class NotUtf8(AuditError):
    CODE, EXIT = "ERR-ENCODING", 3


class BinaryFile(AuditError):
    CODE, EXIT = "ERR-BINARY", 3


class EmptyFile(AuditError):
    CODE, EXIT = "ERR-EMPTY", 4


class TooLarge(AuditError):
    CODE, EXIT = "ERR-TOO-LARGE", 7


def _die(e):
    """统一错误出口：打印友好提示到 stderr，按错误类型退出对应码。"""
    print(e.render(), file=sys.stderr)
    sys.exit(e.EXIT)


def read_doc(path, max_bytes=DEFAULT_MAX_BYTES):
    """统一安全读取：覆盖目录/二进制/空/超大/编码边界，返回 UTF-8 文本。"""
    p = Path(path)
    if not p.exists():
        raise FileNotFound(
            f"找不到文件：{path}",
            fix=f"检查路径是否拼写正确；建议改用绝对路径，如 D:/work/{p.name} 或 /home/you/{p.name}")
    if p.is_dir():
        raise IsDirectory(
            f"传入的是目录而非文件：{path}",
            fix="请传入具体的 .md 文件路径（含扩展名），不要传目录")
    size = p.stat().st_size
    if size == 0:
        raise EmptyFile(
            f"文件为空（0 字节）：{path}",
            fix="文件还没有内容，请先写入草稿 / 成稿后再审计")
    if size > max_bytes:
        mb = max_bytes / 1024 / 1024
        raise TooLarge(
            f"文件过大（{size / 1024 / 1024:.1f}MB > 上限 {mb:.0f}MB）：{path}",
            fix=f"超大文档建议按章节拆分审计；或加 --max-bytes {int(size)} 临时调大上限")
    try:
        raw = p.read_bytes()
    except OSError as e:
        raise FileNotFound(f"无法读取文件：{path}（{e}）")
    if b"\x00" in raw:
        raise BinaryFile(
            f"文件疑似二进制（含 NUL 字节）：{path}",
            fix="请传入纯文本 / Markdown 文件，而非 .docx / .pdf / .png 等二进制格式")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise NotUtf8(
            f"文件不是 UTF-8 编码，无法读取：{path}",
            fix="在编辑器里「另存为 → 编码选择 UTF-8」后重试")


# ---------- 文本切分 ----------
TABLE_SEP = re.compile(r"^\s*\|?[\s:\-|]+\|?\s*$")  # 表格分隔行 |---|---|


def split_sentences(text):
    # 去掉 fenced code 与 html 块，避免把代码当声明
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    # 按中英文句末标点切分（保留标点）
    raw = re.split(r"(?<=[。！？!?；;])", text)
    out = []
    for s in raw:
        for line in s.split("\n"):
            line = line.strip()
            if not line:
                continue
            # 表格分隔行跳过
            if TABLE_SEP.match(line):
                continue
            # 表格数据行：拆单元格，逐单元格检测（修复"表格内声明漏检"）
            if line.startswith("|"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                for cell in cells:
                    if cell and not re.match(r"^C\d+$", cell):
                        out.append(cell)
                continue
            # 剥离 markdown 标题/引用/列表/加粗/有序列表前缀，避免污染声明或触发哨兵丢弃
            line = re.sub(r"^\s*#{1,6}\s+", "", line)
            line = re.sub(r"^\s*>\s*", "", line)
            line = re.sub(r"^\s*[-*+]\s+", "", line)
            line = re.sub(r"^\s*\*{1,2}\s*", "", line)   # 行首加粗 **x**
            line = re.sub(r"\*{1,2}", "", line)           # 行内加粗
            line = re.sub(r"^\s*\d+[.)]\s+", "", line)
            # 超长行截断，防正则灾难（稳定性保护）
            if len(line) > MAX_LINE_CHARS:
                line = line[:MAX_LINE_CHARS]
            if line:
                out.append(line)
    return out


# 声明标记（中文 + 英文常见断言词）
CLAIM_MARKERS = [
    "比", "优于", "快", "慢", "高", "低", "多", "少", "证明", "表明", "显示", "说明",
    "结论", "因此", "所以", "从而", "必然", "一定", "所有", "都", "最高", "最低",
    "第一", "领先", "超越", "提升", "下降", "增加", "减少", "达到", "约为", "倍",
    "准确率", "精度", "效果", "性能", "F1", "BLEU", "显著", "可达", "高达",
]
# 强化词（用于检测"弱声明被强化"）
STRENGTHEN_MARKERS = ["更", "最", "绝对", "必然", "远超", "领先", "第一", "完全",
                      "彻底", "一定", "毫无", "碾压", "吊打", "秒杀"]
# 弱强度标记
WEAK_MARKERS = ["弱", "⚠️", "❌", "无", "缺", "未", "待补", "不足", "存疑"]

NUM_RE = re.compile(r"\d")


def is_candidate_claim(sent):
    if len(sent) < 8:
        return False
    # 跳过 markdown 结构行
    if sent[:1] in "#>|*-":
        return False
    if sent.endswith("？") or sent.endswith("?"):
        return False
    # 含数字 或 含断言标记 -> 视为候选声明
    if NUM_RE.search(sent):
        return True
    for m in CLAIM_MARKERS:
        if m in sent:
            return True
    return False


def normalize(s):
    return re.sub(r"\s+", "", re.sub(r"[^\w一-鿿]", "", s))


def tokenize(s):
    return set(re.findall(r"[a-zA-Z]+|[一-鿿]", normalize(s)))


def jaccard(a, b):
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


# ---------- extract（阶段2） ----------
# 声明已"显式闭环"的标记（即使暂无证据，作者也已决定降级/删除）
CLOSED_MARKERS = ["降级", "删除", "已决", "decided", "drop", "downgrade"]


def cmd_extract(args):
    try:
        text = read_doc(args.draft, args.max_bytes)
    except AuditError as e:
        _die(e)
    sents = split_sentences(text)
    claims = [s for s in sents if is_candidate_claim(s)]
    mark = args.mark

    if args.json:
        data = [{"id": f"C{i}", "claim": c, "evidence": "", "strength": "待评", "gap": ""}
                for i, c in enumerate(claims, 1)]
        out = json.dumps(data, ensure_ascii=False, indent=2)
        print(out)
        return

    lines = []
    lines.append("# Claim Ledger（声明台账骨架 · 由 aris_audit extract 生成）")
    lines.append("")
    lines.append(f"> 阶段2产物：以下为候选声明，证据列留空标 {mark}，请人工 / 异族审补全。"
                 "本骨架为前置自审，不替代 Hermes+SenseNova 异族审。")
    lines.append("")
    lines.append("| # | 声明(原文句子) | 证据来源(文件/行/截图) | 支撑强度 | 缺口 |")
    lines.append("|---|---|---|---|---|")
    for i, c in enumerate(claims, 1):
        c_safe = c.replace("|", "｜")
        lines.append(f"| C{i} | {c_safe} | {mark} | 待评 | {mark} |")
    lines.append("")
    out = "\n".join(lines)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out, encoding="utf-8")
        print(f"[aris_audit] 已生成台账骨架 -> {args.output}"
              f"（{len(claims)} 条候选声明，证据列留空标 {mark}）")
    else:
        print(out)


# ---------- ledger 解析 ----------
def parse_ledger(content):
    rows = []
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        if not re.match(r"^C\d+$", cells[0]):
            continue
        cid, claim, evidence, strength, gap = cells[0], cells[1], cells[2], cells[3], cells[4]
        rows.append({
            "id": cid, "claim": claim, "evidence": evidence,
            "strength": strength, "gap": gap,
            "weak": any(w in strength or w in evidence or w in gap for w in WEAK_MARKERS),
        })
    return rows


# ---------- drift（阶段3） ----------
def cmd_drift(args):
    try:
        final_text = read_doc(args.draft, args.max_bytes)
        ledger_text = read_doc(args.ledger, args.max_bytes)
    except AuditError as e:
        _die(e)
    final_sents = split_sentences(final_text)
    final_claims = [s for s in final_sents if is_candidate_claim(s)]
    ledger = parse_ledger(ledger_text)
    ledger_norm = [(r["claim"], tokenize(r["claim"])) for r in ledger]

    # 类型A：成稿有、台账无
    drift_a = []
    for s in final_claims:
        ns = tokenize(s)
        if not ns:
            continue
        covered = False
        for _, lt in ledger_norm:
            if not lt:
                continue
            if lt <= ns or jaccard(ns, lt) >= args.threshold:
                covered = True
                break
        if not covered:
            drift_a.append(s)

    # 类型B：弱声明被强化
    drift_b = []
    for r in ledger:
        if not r["weak"]:
            continue
        base = tokenize(r["claim"])
        matched = None
        for s in final_claims:
            if r["claim"] in s or (base and base <= tokenize(s)):
                matched = s
                break
        if not matched:
            continue
        base_m = sum(1 for m in STRENGTHEN_MARKERS if m in r["claim"])
        matched_m = sum(1 for m in STRENGTHEN_MARKERS if m in matched)
        if matched_m > base_m:
            drift_b.append((r["id"], r["claim"], matched))

    if args.json:
        data = {
            "scan": {"final_claims": len(final_claims), "ledger_rows": len(ledger)},
            "drift_A_new_claim": drift_a,
            "drift_B_strengthened": [
                {"id": cid, "base": base_c, "strengthened": matched}
                for cid, base_c, matched in drift_b
            ],
        }
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    out = []
    out.append("# 声明漂移清单（由 aris_audit drift 生成 · 阶段3前置自审）")
    out.append("")
    out.append(f"> 扫描成稿候选声明 {len(final_claims)} 条，台账条目 {len(ledger)} 条。"
               f"以下为疑似漂移，请人工 / 异族审复核。本清单不替代 Hermes+SenseNova 异族审。")
    out.append("")
    out.append(f"## A. 成稿有、台账无（疑似幻觉/漂移）：{len(drift_a)} 条")
    out.append("")
    if drift_a:
        for s in drift_a:
            out.append(f"- ⚠️ {s}")
    else:
        out.append("- 无（成稿声明均能在台账中找到对应）")
    out.append("")
    out.append(f"## B. 弱声明被强化（台账标弱、成稿措辞更绝对）：{len(drift_b)} 条")
    out.append("")
    if drift_b:
        for cid, base_c, matched in drift_b:
            out.append(f"- ⚠️ [{cid}] 原声明：「{base_c}」 -> 成稿强化为：「{matched}」")
    else:
        out.append("- 无（弱声明未在成稿中被强化）")
    out.append("")

    result = "\n".join(out)
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result, encoding="utf-8")
        print(f"[aris_audit] 已生成漂移清单 -> {args.output}")
    else:
        print(result)


# ---------- gate（严格闭环硬闸门 · 规则5/6） ----------
def _row_closed(r, mark="⚠️"):
    """一行声明是否视为已闭环：已补证据，或已显式降级/删除。"""
    blob = f"{r['evidence']} {r['strength']} {r['gap']}"
    if any(m in blob for m in CLOSED_MARKERS):
        return True
    # 证据列不再是缺口标记且不是空/缺，视作已补证据
    ev = r["evidence"].strip()
    if mark not in ev and ev not in ("", "缺", "无", "待补"):
        return True
    return False


def cmd_gate(args):
    """收口前硬校验：台账里仍有未验证声明 -> 退出码 10，禁止 Finish。"""
    try:
        ledger_text = read_doc(args.ledger, args.max_bytes)
    except AuditError as e:
        _die(e)
    ledger = parse_ledger(ledger_text)
    if not ledger:
        print("[aris_audit] ⚠️ 台账为空（没有 C 开头的声明行）。"
              "请先运行 `extract` 生成台账，再审计。", file=sys.stderr)
        sys.exit(1)

    open_rows = [r for r in ledger if not _row_closed(r, args.mark)]
    if open_rows:
        ids = ", ".join(r["id"] for r in open_rows)
        print(
            f"[aris_audit] ❌ 审计未闭环（gate FAILED · 退出码 10）："
            f"台账中仍有 {len(open_rows)} 条声明缺少证据（{ids}）。\n"
            f"    请对每条三选一后重试：\n"
            f"      1) 补证据：在「证据来源」列填入 文件:行号 或 截图路径\n"
            f"      2) 降级措辞：把「支撑强度」改为「弱」，并在「缺口」列写「已降级：…」\n"
            f"      3) 删除：直接从成稿中移除该声明\n"
            f"    仍不确定？运行 `python scripts/aris_audit.py drift --draft 成稿.md --ledger {args.ledger}` 复核成稿与台账是否一致。",
            file=sys.stderr,
        )
        sys.exit(10)
    print(f"[aris_audit] ✅ 审计闭环校验通过（gate PASSED）："
          f"台账 {len(ledger)} 条声明均已验证或已显式降级/删除，可以收口。")


# ---------- CLI ----------
def build_parser():
    p = argparse.ArgumentParser(
        description="ARIS 对抗式声明审计 · 前置自审脚本（light 模式，零交互）")
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("extract", help="阶段2：草稿 -> Claim Ledger 台账骨架（证据留空标 ⚠️）")
    pe.add_argument("--draft", required=True, help="草稿 markdown 路径")
    pe.add_argument("--output", help="输出台账路径（默认打印到 stdout）")
    pe.add_argument("--mode", default="light", choices=["light"],
                    help="自审模式，默认 light（纯规则启发式）")
    pe.add_argument("--mark", default="⚠️", help="缺口标记符，默认 ⚠️（extract 与 gate 共用）")
    pe.add_argument("--json", action="store_true", help="输出 JSON 数组，便于程序/CI 消费")
    pe.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES,
                    help=f"草稿大小上限（字节），默认 {DEFAULT_MAX_BYTES}（5MB），超限报错 ERR-TOO-LARGE")
    pe.set_defaults(func=cmd_extract)

    pd = sub.add_parser("drift", help="阶段3：成稿 + ledger -> 漂移清单")
    pd.add_argument("--draft", required=True, help="成稿（finished）markdown 路径")
    pd.add_argument("--ledger", required=True, help="extract 生成的 ledger.md 路径")
    pd.add_argument("--output", help="输出漂移清单路径（默认打印到 stdout）")
    pd.add_argument("--mode", default="light", choices=["light"],
                    help="自审模式，默认 light（纯规则启发式）")
    pd.add_argument("--json", action="store_true", help="输出 JSON 对象，便于程序/CI 消费")
    pd.add_argument("--threshold", type=float, default=0.6,
                    help="成稿声明与台账声明的 Jaccard 相似度阈值，默认 0.6")
    pd.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES,
                    help=f"文件大小上限（字节），默认 {DEFAULT_MAX_BYTES}（5MB）")
    pd.set_defaults(func=cmd_drift)

    pg = sub.add_parser("gate", help="收口闸门：台账仍有未验证声明 -> 退出码 10（严格闭环）")
    pg.add_argument("--ledger", required=True, help="extract 生成的 ledger.md 路径")
    pg.add_argument("--mark", default="⚠️", help="缺口标记符，需与 extract 一致，默认 ⚠️")
    pg.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES,
                    help=f"文件大小上限（字节），默认 {DEFAULT_MAX_BYTES}（5MB）")
    pg.set_defaults(func=cmd_gate)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
