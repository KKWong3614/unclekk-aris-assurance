# 最小运行示例 · Minimal Runnable Example

> 本示例用本技能自带的 `references/example-draft.md` 与 `references/example-final.md` 实跑，输出均为脚本真实产物，可直接复现。
> This example runs on the bundled `references/example-draft.md` and `references/example-final.md`; all outputs below are real script output and fully reproducible.

## 三步跑通 (Three Steps)

```bash
# ① 阶段2：草稿 -> 台账骨架（证据列留空标 ⚠️）
python scripts/aris_audit.py extract --draft references/example-draft.md --output references/example-ledger.md

# ② 阶段3：成稿 + 台账 -> 漂移清单（待人工/异族复核）
python scripts/aris_audit.py drift --draft references/example-final.md --ledger references/example-ledger.md --output references/example-drift.md

# ③ 收口闸门：台账仍有未验证声明 -> 非零退出，禁止 Finish
python scripts/aris_audit.py gate --ledger references/example-ledger.md
```

## ① extract 的真实产出 (Real output of extract)

`references/example-ledger.md`：

```
# Claim Ledger（声明台账骨架 · 由 aris_audit extract 生成）

| # | 声明(原文句子) | 证据来源(文件/行/截图) | 支撑强度 | 缺口 |
|---|---|---|---|---|
| C1 | 本地部署比云端快 3 倍，延迟从 120ms 降到 40ms。 | ⚠️ | 待评 | ⚠️ |
| C2 | 我们的准确率达到了 92%，显著优于旧方案。 | ⚠️ | 待评 | ⚠️ |
| C3 | 这个方案适用于所有生产环境。 | ⚠️ | 待评 | ⚠️ |
```

> 三条候选声明都被抽出，证据列统一标 `⚠️`——这就是要你补/降级/删除的"红色缺口"。
> All three candidate claims are extracted; the evidence column is uniformly `⚠️` — these are the "red gaps" you must supplement, downgrade, or delete.

## ② drift 的真实产出 (Real output of drift)

`references/example-drift.md`（成稿在 ① 的台账基础上做了两处改动）：

```
## A. 成稿有、台账无（疑似幻觉/漂移）：1 条
- ⚠️ 新结论：本系统在百万级并发下依然稳定。

## B. 弱声明被强化（台账标弱、成稿措辞更绝对）：1 条
- ⚠️ [C2] 原声明：「我们的准确率达到了 92%，显著优于旧方案。」 -> 成稿强化为：「我们的准确率达到了 92%，显著优于旧方案，绝对领先业界。」
```

> A 类 = 成稿凭空多出的声明（未进台账，疑似幻觉）；B 类 = 台账本就未验证（⚠️），成稿却把它说得更绝对。**两类都必须在收口前处理。**
> Type A = a claim appearing in the draft but absent from the ledger (possible hallucination); Type B = a ledger claim still unverified (⚠️) yet stated more absolutely in the draft. **Both must be resolved before closing.**

## ③ gate 的真实产出 (Real output of gate)

未闭环时（默认台账，3 条皆 ⚠️）：

```
[aris_audit] ❌ 审计未闭环（gate FAILED）：台账中仍有 3 条声明缺少证据（C1, C2, C3）。
    请对每条三选一后重试：
      1) 补证据：在「证据来源」列填入 文件:行号 或 截图路径
      2) 降级措辞：把「支撑强度」改为「弱」，并在「缺口」列写「已降级：…」
      3) 删除：直接从成稿中移除该声明
    仍不确定？运行 `python scripts/aris_audit.py drift --draft 成稿.md --ledger references/example-ledger.md` 复核成稿与台账是否一致。
```

补完证据 / 显式降级后（见 `references/example-ledger-closed.md`）：

```
[aris_audit] ✅ 审计闭环校验通过（gate PASSED）：台账 3 条声明均已验证或已显式降级/删除，可以收口。
```

> `gate` 是**硬代码闸门**：只要台账里还有未验证声明，它就返回非零退出码，从机制上阻止"带缺口发稿"。
> `gate` is a **hard-code gate**: as long as any unverified claim remains in the ledger, it returns a non-zero exit code, mechanically preventing "publishing with gaps."

## 一句话总结 (One-line summary)

```
写草稿 → extract 出台账(全⚠️) → 人工/异族补证据 → drift 扫一遍 → gate 通过 → 才允许 Finish
```

完整方法论见 `../SKILL.md`；审计报告成品样例见 `sample-claim-audit-report.md`；常见坑与对照见 `faq.md`。
