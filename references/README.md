# references/

审计证据与演进记录的容器。本目录不承载任何运行时逻辑（脚本默认输出到当前工作目录，需按 Runbook 归档到此）。

| 文件 | 类型 | 用途 |
|------|------|------|
| README.md | 文档 | 本目录说明与文件清单 |
| evolution-log.md | 文档 | 技能演进历史与决策记录 |
| quickstart-minimal-example.md | 文档 | 最小可运行示例（真实脚本输出） |
| sample-claim-audit-report.md | 文档 | 审计报告成品样例 |
| faq.md | 文档 | 常见问题与坑点对照 |
| example-draft.md | 示例 | extract 的草稿输入 |
| example-final.md | 示例 | drift 的成稿输入 |
| example-ledger.md | 示例 | extract 产物（未闭环） |
| example-ledger-closed.md | 示例 | 已闭环台账（gate 通过） |
| example-drift.md | 示例 | drift 产物 |

> 以下为**每次审计运行时**由 Executor 生成并归档的产物（不在仓库预置）：
> The following are **generated per audit run** by the Executor and archived here (not pre-shipped):

| 文件 | 阶段 | 用途 |
|------|------|------|
| integrity_checklist.md | 阶段1 | 完整性验证产物（✅/⚠️/❌） |
| claim_ledger.md | 阶段2 | 声明台账 |
| claim_audit_report.md | 阶段3 | 声明审计报告（链接 results.tsv / evolution-log） |
| results.tsv | 全程 | 实测结果登记表（T1/T2 及后续用例） |
