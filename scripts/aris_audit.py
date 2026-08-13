#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aris_audit.py — ARIS 对抗式声明审计 · 前置自审脚本（light 模式，零交互）

子命令：
  extract  阶段2：喂草稿.md -> 生成 Claim Ledger 台账骨架（证据列留空标 ⚠️）
  drift    阶段3：喂成稿 + ledger.md -> 输出漂移清单（成稿有台账无 / 弱声明被强化）

设计约束：
  - 零交互：所有选项走 flag，无 input() 询问
  - 默认 light 模式（纯规则启发式，不调 LLM、不联网、零依赖）
  - 证据缺口留空标 ⚠️，绝不追问
  - 定位是"前置自审、降缺口"，不替代 Hermes + SenseNova 异族审

仅依赖 Python 标准库。
"""

import argparse
import re
import sys
from pathlib import Path

# ---------- 文本切分 ----------
def split_sentences(text):
    # 去掉 fenced code 与 html 块，避免把代码当声明
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    # 按中英文句末标点切分（保留标点）
    raw = re.split(r"(?<=[。！？!?；;])", text)
    out = []
    for s in raw:
        # 再按换行切分：标题行（无句末标点）否则会与下句合并，
        # 合并后以 '#' 开头被 is_candidate_claim 整句丢弃，导致标题后的关键声明漏检（P1-1）
        for line in s.split("\n"):
            line = line.strip()
            # 剥离 markdown 标题/引用/列表/有序列表前缀，避免污染声明或触发哨兵丢弃
            line = re.sub(r"^\s*#{1,6}\s+", "", line)
            line = re.sub(r"^\s*>\s*", "", line)
            line = re.sub(r"^\s*[-*+]\s+", "", line)
            line = re.sub(r"^\s*\d+[.)]\s+", "", line)
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
                      "彻底", "一定", "毫无", "碾压", "吊打", "远超", "秒杀"]
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
def cmd_extract(args):
    draft = Path(args.draft)
    if not draft.exists():
        sys.exit(f"[aris_audit] 找不到草稿: {args.draft}")
    try:
        text = draft.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        sys.exit(f"[aris_audit] 文件非 UTF-8 编码，无法读取: {args.draft} ({e})")
    sents = split_sentences(text)
    claims = [s for s in sents if is_candidate_claim(s)]

    lines = []
    lines.append("# Claim Ledger（声明台账骨架 · 由 aris_audit extract 生成）")
    lines.append("")
    lines.append("> 阶段2产物：以下为候选声明，证据列留空标 ⚠️，请人工 / 异族审补全。"
                 "本骨架为前置自审，不替代 Hermes+SenseNova 异族审。")
    lines.append("")
    lines.append("| # | 声明(原文句子) | 证据来源(文件/行/截图) | 支撑强度 | 缺口 |")
    lines.append("|---|---|---|---|---|")
    for i, c in enumerate(claims, 1):
        c_safe = c.replace("|", "｜")
        lines.append(f"| C{i} | {c_safe} | ⚠️ | 待评 | ⚠️ |")
    lines.append("")
    out = "\n".join(lines)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out, encoding="utf-8")
        print(f"[aris_audit] 已生成台账骨架 -> {args.output}"
              f"（{len(claims)} 条候选声明，证据列留空标 ⚠️）")
    else:
        print(out)


# ---------- ledger 解析 ----------
def parse_ledger(path):
    rows = []
    try:
        content = Path(path).read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        sys.exit(f"[aris_audit] 台账文件非 UTF-8 编码，无法读取: {path} ({e})")
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
    draft = Path(args.draft)
    ledger_path = Path(args.ledger)
    if not draft.exists():
        sys.exit(f"[aris_audit] 找不到成稿: {args.draft}")
    if not ledger_path.exists():
        sys.exit(f"[aris_audit] 找不到台账: {args.ledger}")
    try:
        final_text = draft.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        sys.exit(f"[aris_audit] 文件非 UTF-8 编码，无法读取: {args.draft} ({e})")
    final_sents = split_sentences(final_text)
    final_claims = [s for s in final_sents if is_candidate_claim(s)]
    ledger = parse_ledger(ledger_path)
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
            if lt <= ns or jaccard(ns, lt) >= 0.6:
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
    pe.set_defaults(func=cmd_extract)

    pd = sub.add_parser("drift", help="阶段3：成稿 + ledger -> 漂移清单")
    pd.add_argument("--draft", required=True, help="成稿（finished）markdown 路径")
    pd.add_argument("--ledger", required=True, help="extract 生成的 ledger.md 路径")
    pd.add_argument("--output", help="输出漂移清单路径（默认打印到 stdout）")
    pd.add_argument("--mode", default="light", choices=["light"],
                    help="自审模式，默认 light（纯规则启发式）")
    pd.set_defaults(func=cmd_drift)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
