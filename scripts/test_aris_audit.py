#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aris_audit.py 回归测试：用固定 fixture 跑 extract 与 drift，断言关键输出。"""
import json, subprocess, sys, tempfile, textwrap
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "aris_audit.py"

FIXTURE_DRAFT = textwrap.dedent("""\
本模型在 2024 年的准确率达到了 92%，显著优于基线。
测试表明，所有用户都认为新界面更加友好。
这只是个普通句子没有数字也没有断言词。
""")

def run(args):
    return subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True, text=True, timeout=30,
    )

def test_extract_produces_ledger():
    with tempfile.TemporaryDirectory() as td:
        draft = Path(td) / "draft.md"
        draft.write_text(FIXTURE_DRAFT, encoding="utf-8")
        out = Path(td) / "sub" / "out" / "ledger.md"
        r = run(["extract", "--draft", str(draft), "--output", str(out)])
        assert r.returncode == 0, r.stderr
        text = out.read_text(encoding="utf-8")
        assert "Claim Ledger" in text, "缺少台账标题"
        assert "⚠️" in text, "证据列未标 ⚠️"
        assert "C1" in text and "C2" in text, "应识别到至少 2 条候选声明"
        assert "92%" in text, "数字声明 92% 应被识别"
        print("  [PASS] extract 生成台账骨架，含 ⚠️ 与 2 条候选声明")

def test_extract_parent_mkdir():
    """P2-1 验证：--output 父目录不存在时自动创建"""
    with tempfile.TemporaryDirectory() as td:
        draft = Path(td) / "draft.md"
        draft.write_text(FIXTURE_DRAFT, encoding="utf-8")
        deep = Path(td) / "a" / "b" / "c" / "ledger.md"
        r = run(["extract", "--draft", str(draft), "--output", str(deep)])
        assert r.returncode == 0, r.stderr
        assert deep.exists(), f"深度嵌套输出文件未创建: {deep}"
        print("  [PASS] --output 父目录自动创建")

def test_extract_stdout_no_output_flag():
    with tempfile.TemporaryDirectory() as td:
        draft = Path(td) / "draft.md"
        draft.write_text(FIXTURE_DRAFT, encoding="utf-8")
        r = run(["extract", "--draft", str(draft)])
        assert r.returncode == 0, r.stderr
        assert "Claim Ledger" in r.stdout, "stdout 应有台账"
        print("  [PASS] 无 --output 时打印到 stdout")

def test_drift_detects_new_claim():
    """成稿比 ledger 多一条声明 -> 应出现在漂移 A"""
    with tempfile.TemporaryDirectory() as td:
        draft = Path(td) / "finished.md"
        ledger = Path(td) / "ledger.md"
        draft.write_text("新声明：本模型准确率达到了 95%，超越所有基线。\n", encoding="utf-8")
        ledger.write_text(
            "| # | 声明 | 证据 | 强度 | 缺口 |\n"
            "|---|---|---|---|---|\n"
            "| C1 | 旧声明 | ⚠️ | 待评 | ⚠️ |\n",
            encoding="utf-8",
        )
        r = run(["drift", "--draft", str(draft), "--ledger", str(ledger)])
        assert r.returncode == 0, r.stderr
        assert "95%" in r.stdout, "漂移 A 应含新增声明 95%"
        print("  [PASS] drift 检测成稿新增声明")

def test_nonexistent_draft_fails_cleanly():
    r = run(["extract", "--draft", "/no/such/file.md"])
    assert r.returncode != 0
    assert "找不到" in r.stderr
    print("  [PASS] 找不到文件时干净报错")

def test_nonutf8_fails_cleanly():
    """GBK 等非 UTF-8 字节 -> 退出码 3 + ERR-ENCODING，提示另存 UTF-8"""
    with tempfile.TemporaryDirectory() as td:
        bad = Path(td) / "bad.txt"
        bad.write_bytes("中文声明数据错误非UTF8编码".encode("gbk"))
        r = run(["extract", "--draft", str(bad)])
        assert r.returncode != 0, r.stderr
        assert "UTF-8" in r.stderr
        print("  [PASS] 非 UTF-8 文件干净报错（P2-2）")

def test_drift_weak_claim_strengthened():
    """台账弱声明被成稿强化 -> 漂移 B"""
    with tempfile.TemporaryDirectory() as td:
        draft = Path(td) / "finished.md"
        ledger = Path(td) / "ledger.md"
        draft.write_text("数据显示，新方案性能绝对提升，比旧方案更快。\n", encoding="utf-8")
        ledger.write_text(
            "| # | 声明 | 证据 | 强度 | 缺口 |\n"
            "|---|---|---|---|---|\n"
            "| C1 | 新方案性能比旧方案提升 | ⚠️ | 弱 | 缺对照实验 |\n",
            encoding="utf-8",
        )
        r = run(["drift", "--draft", str(draft), "--ledger", str(ledger)])
        assert r.returncode == 0, r.stderr
        assert "B" in r.stdout or "强化" in r.stdout or "弱" in r.stdout, \
            "漂移 B 应识别弱声明被强化"
        print("  [PASS] drift 检测弱声明被强化")

def test_extract_detects_claim_after_heading():
    """P1-1 回归：标题行（无句末标点）后的声明不应被静默丢弃"""
    with tempfile.TemporaryDirectory() as td:
        draft = Path(td) / "draft.md"
        draft.write_text("## 核心结论\n本地部署比云端快 3 倍。\n", encoding="utf-8")
        out = Path(td) / "ledger.md"
        r = run(["extract", "--draft", str(draft), "--output", str(out)])
        assert r.returncode == 0, r.stderr
        text = out.read_text(encoding="utf-8")
        assert "3 倍" in text or "快 3 倍" in text, \
            "标题后的关键声明应被识别为候选声明，而非整句丢弃"
        print("  [PASS] 标题后的声明不被静默丢弃（P1-1）")

def test_gate_fails_on_open_claims():
    """台账有未验证声明 -> gate 必须非零退出（严格闭环硬闸门）"""
    with tempfile.TemporaryDirectory() as td:
        ledger = Path(td) / "ledger.md"
        ledger.write_text(
            "| # | 声明 | 证据 | 强度 | 缺口 |\n"
            "|---|---|---|---|---|\n"
            "| C1 | 已验证声明 | exp/log.txt L12 | 强 | 无 |\n"
            "| C2 | 未验证声明 | ⚠️ | 待评 | ⚠️ |\n",
            encoding="utf-8",
        )
        r = run(["gate", "--ledger", str(ledger)])
        assert r.returncode != 0, "存在未验证声明时 gate 应通过非零退出阻止收口"
        assert r.returncode == 10, f"gate 未闭环应返回退出码 10，实际 {r.returncode}"
        assert "未闭环" in r.stderr, "gate 报错应明确提示未闭环"
        print("  [PASS] gate 在存在未验证声明时阻止收口（退出码10）")

def test_gate_passes_when_closed():
    """所有声明已验证或显式降级 -> gate 退出码 0"""
    with tempfile.TemporaryDirectory() as td:
        ledger = Path(td) / "ledger.md"
        ledger.write_text(
            "| # | 声明 | 证据 | 强度 | 缺口 |\n"
            "|---|---|---|---|---|\n"
            "| C1 | 已验证声明 | exp/log.txt L12 | 强 | 无 |\n"
            "| C2 | 已降级声明 | ⚠️ | 弱 | 已降级：缺压测，措辞改为'可能' |\n",
            encoding="utf-8",
        )
        r = run(["gate", "--ledger", str(ledger)])
        assert r.returncode == 0, r.stderr
        assert "PASSED" in r.stdout
        print("  [PASS] gate 在全部闭环时通过")

def test_extract_table_claim():
    """表格单元格内的数字声明不应被漏检（复杂格式识别不全修复）"""
    with tempfile.TemporaryDirectory() as td:
        draft = Path(td) / "draft.md"
        draft.write_text(
            "## 指标\n| 指标 | 数值 |\n|---|---|\n| 准确率 | 本模型准确率达 95% |\n| 延迟 | 普通 |\n",
            encoding="utf-8")
        out = Path(td) / "ledger.md"
        r = run(["extract", "--draft", str(draft), "--output", str(out)])
        assert r.returncode == 0, r.stderr
        text = out.read_text(encoding="utf-8")
        assert "95%" in text, "表格单元格内的 95% 声明应被识别"
        print("  [PASS] extract 识别表格单元格声明")

def test_extract_bold_claim():
    """加粗内的断言不应被漏检"""
    with tempfile.TemporaryDirectory() as td:
        draft = Path(td) / "draft.md"
        draft.write_text("**我们的方案比基线快 2 倍。**\n", encoding="utf-8")
        out = Path(td) / "ledger.md"
        r = run(["extract", "--draft", str(draft), "--output", str(out)])
        assert r.returncode == 0, r.stderr
        assert "2 倍" in out.read_text(encoding="utf-8"), "加粗声明应被识别"
        print("  [PASS] extract 识别加粗声明")

def test_extract_json_output():
    """--json 输出合法 JSON 数组，便于程序/CI 消费"""
    with tempfile.TemporaryDirectory() as td:
        draft = Path(td) / "draft.md"
        draft.write_text("本模型准确率达 92%。\n", encoding="utf-8")
        r = run(["extract", "--draft", str(draft), "--json"])
        assert r.returncode == 0, r.stderr
        data = json.loads(r.stdout)
        assert isinstance(data, list) and len(data) >= 1
        assert "92%" in data[0]["claim"]
        print("  [PASS] extract --json 输出合法 JSON 数组")

def test_is_dir_fails():
    """目录当文件传入 -> 退出码 2 + ERR-IS-DIR"""
    with tempfile.TemporaryDirectory() as td:
        r = run(["extract", "--draft", td])
        assert r.returncode == 2, f"目录应返回2，实际 {r.returncode}: {r.stderr}"
        assert "ERR-IS-DIR" in r.stderr
        print("  [PASS] 目录当文件传入干净报错（退出码2）")

def test_binary_fails():
    """二进制文件（含 NUL）-> 退出码 3 + ERR-BINARY"""
    with tempfile.TemporaryDirectory() as td:
        bad = Path(td) / "bad.bin"
        bad.write_bytes(b"\x00\x01\x02not-text")
        r = run(["extract", "--draft", str(bad)])
        assert r.returncode == 3, f"二进制应返回3，实际 {r.returncode}"
        assert "ERR-BINARY" in r.stderr
        print("  [PASS] 二进制文件干净报错（退出码3）")

def test_empty_fails():
    """空文件 -> 退出码 4 + ERR-EMPTY"""
    with tempfile.TemporaryDirectory() as td:
        e = Path(td) / "empty.md"
        e.write_text("", encoding="utf-8")
        r = run(["extract", "--draft", str(e)])
        assert r.returncode == 4, f"空文件应返回4，实际 {r.returncode}"
        assert "ERR-EMPTY" in r.stderr
        print("  [PASS] 空文件干净报错（退出码4）")

def test_too_large_fails():
    """超大文件（超 --max-bytes）-> 退出码 7 + ERR-TOO-LARGE"""
    with tempfile.TemporaryDirectory() as td:
        big = Path(td) / "big.md"
        big.write_text("x" * 500, encoding="utf-8")
        r = run(["extract", "--draft", str(big), "--max-bytes", "100"])
        assert r.returncode == 7, f"超大文件应返回7，实际 {r.returncode}"
        assert "ERR-TOO-LARGE" in r.stderr
        print("  [PASS] 超大文件被保护拒绝（退出码7）")

def test_mark_custom():
    """--mark 自定义缺口标记：extract 与 gate 共用判据"""
    with tempfile.TemporaryDirectory() as td:
        draft = Path(td) / "draft.md"
        draft.write_text("本模型准确率达 92%。\n", encoding="utf-8")
        ledger = Path(td) / "ledger.md"
        r = run(["extract", "--draft", str(draft), "--output", str(ledger), "--mark", "✗"])
        assert r.returncode == 0, r.stderr
        text = ledger.read_text(encoding="utf-8")
        assert "✗" in text and "⚠️" not in text, "应改用自定义标记 ✗"
        r2 = run(["gate", "--ledger", str(ledger), "--mark", "✗"])
        assert r2.returncode == 10, f"自定义标记应判未闭环(10)，实际 {r2.returncode}"
        print("  [PASS] --mark 自定义标记 extract/gate 共用")

if __name__ == "__main__":
    tests = [
        test_extract_produces_ledger,
        test_extract_parent_mkdir,
        test_extract_stdout_no_output_flag,
        test_drift_detects_new_claim,
        test_drift_weak_claim_strengthened,
        test_nonexistent_draft_fails_cleanly,
        test_nonutf8_fails_cleanly,
        test_extract_detects_claim_after_heading,
        test_gate_fails_on_open_claims,
        test_gate_passes_when_closed,
        test_extract_table_claim,
        test_extract_bold_claim,
        test_extract_json_output,
        test_is_dir_fails,
        test_binary_fails,
        test_empty_fails,
        test_too_large_fails,
        test_mark_custom,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} passed")
    sys.exit(0 if passed == len(tests) else 1)
