# 声明审计报告样例 · Sample Claim Audit Report

> 这是一份**成品样例**，展示阶段 1→2→3 跑完后 `claim_audit_report.md` 长什么样。
> 背景：一篇 800 字技术分析，主张"本地部署比云端快 3 倍 / 准确率 92% / 适用于所有生产环境 / 百万级并发稳定"。
> This is a **finished sample** showing what `claim_audit_report.md` looks like after stages 1→2→3.

---

## 0. 审计元信息 (Audit Metadata)

| 项 | 值 |
|----|----|
| 待审产物 | `references/example-final.md`（800 字技术分析） |
| Reviewer | 异族子 agent（executor 闭源 / reviewer 开源） |
| 对抗轮数 | 2 轮（第 2 轮 reviewer 无异议） |
| 降级路径 | 无（标准路径，异族模型可用） |
| 关联证据 | `references/results.tsv` · `references/evolution-log.md` |

## 1. 阶段1 — 完整性验证 (Integrity Verification)

| # | 检查项 | 结果 |
|---|--------|------|
| I1 | 性能对比是否有原始 benchmark 日志 | ❌ 缺 `exp/benchmark_*.txt` |
| I2 | 准确率是否有评测数据文件 | ❌ 缺 `exp/eval_*.csv` |
| I3 | "生产环境/并发"是否有压测记录 | ❌ 无任何证据 |

> 结论：三项关键证据全缺，必须先补或降级，不得直接放行。
> Verdict: all three key pieces of evidence are missing; must supplement or downgrade before passing.

## 2. 阶段2 — Claim Ledger（声明台账摘要） (Result-to-Claim Mapping)

| # | 声明 | 证据 | 强度 | 缺口 |
|---|---|---|---|---|
| C1 | 本地部署比云端快 3 倍（120ms→40ms） | exp/benchmark_0902.txt L12 | 强 | 无 |
| C2 | 准确率 92%，优于旧方案 | exp/eval_0902.csv L5 | 强 | 无 |
| C3 | 适用于所有生产环境 | ⚠️ | 弱 | 已降级：仅小流量验证 |
| C4 | 百万级并发稳定 | ⚠️ | 弱 | ❌ 缺压测，且成稿凭空新增 |

## 3. 阶段3 — 声明审计结果 (Claim Auditing)

### 必须改项（P0 · 未改不许 Finish） (Must-fix)

- **[P0-1] C4「百万级并发稳定」**：成稿新增、台账无对应、无任何证据 → 属幻觉/漂移。
  - 处置：删除该句，或补压测数据后入台账。
- **[P0-2] C3「适用于所有生产环境」**：证据缺口未闭环。
  - 处置：已降级为"适用于多数生产环境"，措辞必须同步改，否则 gate 不通过。

### 建议改项（P1 · 建议采纳） (Suggested-fix)

- **[P1-1] C1「快 3 倍」**：样本量仅 1 次 benchmark，建议补充多次均值与方差，避免"单次好看"。
- **[P1-2] 全文**：补充"本结论基于 X 数据集 / Y 环境"的范围声明，防止读者过度泛化。

### 漂移复核（drift 产出） (Drift Review)

- A 类（成稿有、台账无）：C4「百万级并发稳定」→ 已并入 P0-1。
- B 类（弱声明被强化）：C2 成稿加了"绝对领先业界"，但"绝对"无依据 → 改为"领先旧方案"。

## 4. 收口判定 (Closure Verdict)

```
gate --ledger references/example-ledger-closed.md  →  ✅ PASSED
所有 P0 已闭合，审计通过，允许 Finish。
```

> 未闭环情况下 `gate` 会返回非零退出码并列出 C1/C2/C3，从机制上阻止带缺口发稿。
> If not closed, `gate` returns a non-zero exit code and lists the open claims, mechanically blocking publication with gaps.

---
*本样例对应最小运行示例 `quickstart-minimal-example.md` 与 `example-*.md` 文件。*
