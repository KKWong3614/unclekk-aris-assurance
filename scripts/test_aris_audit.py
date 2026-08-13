#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aris_audit.py 回归测试：用固定 fixture 跑 extract 与 drift，断言关键输出。"""
import subprocess, sys, tempfile, textwrap
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
    with tempfile.TemporaryDirectory() as td:
        bad = Path(td) / "bad.txt"
        bad.write_bytes(b"\xff\xfe" + b"not utf-8" + b"\x00")
        r = run(["extract", "--draft", str(bad)])
        assert r.returncode != 0
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
