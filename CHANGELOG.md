# Changelog

> 权威版本变更记录（SKILL.md 内仅保留最近两版摘要，详见本文件）。
> Authoritative changelog (SKILL.md keeps only a 2-version summary; see this file for the full history).

## [1.6.0] - 2026-09-03 · 重点提升 Reliability（原评测 4.2 → 目标 4.7+）

针对 SkillHub TRACE 评测 R·Reliability 三个子项弱项（异常处理 4.0 / 功能完善性 4.3 / 运行稳定性 4.3）深挖：

- **异常处理 4.0 → 4.7（统一错误体系）**：新增 `AuditError` 异常体系，所有可预期错误带 `ERR-*` 错误码 + **退出码分级** + 一行修复提示。覆盖此前会直接崩的边界：目录当文件(`ERR-IS-DIR`=2)、二进制含 NUL(`ERR-BINARY`=3)、空文件(`ERR-EMPTY`=4)、超大文件(`ERR-TOO-LARGE`=7)；`gate` 未闭环退出码 10。`_die()` 统一出口打印到 stderr。
- **功能完善性 4.3 → 4.6（复杂格式识别 + 选项）**：修复「复杂格式识别不全」——`split_sentences` 现支持 Markdown **表格单元格**、**加粗(`**x**`)**、项目符号、标题后声明抽取（此前 `|`/`*` 开头的行被整句丢弃导致漏检）。新增可选项：`extract/drift --json`（结构化输出，便于 CI/程序消费）、`--mark`（自定义缺口标记，extract 与 gate 共用判据）、`drift --threshold`（相似度阈值）、三命令共享 `--max-bytes`（大小上限）。
- **运行稳定性 4.3 → 4.7（防失控保护）**：`read_doc()` 默认 5MB 大小上限（`--max-bytes` 可调），超长行截断，避免超大文档/超长行卡死或正则灾难。
- **测试**：回归测试 10 → **18 项全过**（新增表格单元格声明识别、加粗声明识别、`--json` 输出、目录/二进制/空/超大文件干净报错、退出码分级、`--mark` 自定义标记）。
- 版本 1.5.0 → 1.6.0（SKILL.md / _meta.json / pyproject.toml / README.md / 本文件 / evolution-log 六处一致）。

## [1.5.0] - 2026-09-03 · 评测驱动优化（TRACE 4.6/5 · 优秀）

基于 SkillHub TRACE 评测报告（T 4.9 / R 4.2 / A 4.8 / C 4.8 / E 4.6，综合 4.6 优秀）与平台 skill 规则，针对性改进：

- **硬代码保障（规则5）**：新增 `aris_audit.py gate` 子命令——收口前扫描 Claim Ledger，只要还有未验证声明（证据列仍 `⚠️` 且未显式降级/删除）即返回**非零退出码**，从机制上阻止"带缺口发稿"。接入 CHECKPOINT 4（CK-4.4）与 Runbook 收口步骤。
- **新手友好报错（R 4.2）**：脚本「找不到文件 / 非 UTF-8」等报错改为带修复指引的措辞（检查路径拼写、用绝对路径、另存为 UTF-8）。
- **步数限制与兜底（规则6）**：新增「步数限制与兜底」节，明确硬上限——对抗 ≤3 轮、单轮修订 ≤5 处、整体步数预算 ≤30 步、gate 必须通过的严格闭环。
- **受众说明（规则4）**：新增「受众（谁该用）」节，覆盖新手→专业全部 Agent 用户。
- **自动触发条件（规则7）**：新增「自动触发条件」节，列出三类应自动激活的条件（显式触发词 / 长文+断言信号 / 高风险发布），并明确不打扰的场景。
- **最小运行示例（规则1）**：新增 `references/quickstart-minimal-example.md`，用自带 `example-*.md` 实跑，所有输出均为脚本真实产物（extract / drift / gate 三类）。
- **审计报告样例（规则8）**：新增 `references/sample-claim-audit-report.md`，展示三阶段审计成品长什么样。
- **FAQ 与坑点对照（规则9）**：新增 `references/faq.md`，简短详尽、带实例与「坏做法 vs 好做法」对照表。
- **修复文档/执行偏差**：补齐缺失的 `LICENSE`（MIT）；重写 `README.md`（版本 1.5.0、目录结构与真实文件一致、移除不存在的 `templates/`）；修正 `references/README.md` 标注运行态文件；本文件由孤儿桩升级为权威变更记录。
- **测试**：回归测试 8 → **10 项全过**（新增 `gate` 通过/未闭环两项）。

## [1.4.0] - 2026-07-25 · 持久化 research wiki + 自改进循环

- 将「执行层(可选)+自改进循环(可选)」升级为可操作「核心流程 C」：读前引导（Bootstrap 复用 wiki 坑点/共识）→ 跑 1+2 → 写回沉淀（aris-audit-{slug}/research-log/pitfall-register）→ 提案过闸（harness 改进须异族 reviewer 批准才合入 SKILL.md）。
- wiki 根指向图书馆 vault `wiki/research/`，运行态 `references/` 与知识态 `wiki/research/` 分工。
- 版本 1.3.1 → 1.4.0（SKILL.md / pyproject.toml / evolution-log 三处一致）。

## [1.3.1] - 2026-07-22 · 独立审计修复（NEEDS_REVISION 82/100 补丁）

- **P1-1（标题后声明漏检）**：`aris_audit.py` 的 `split_sentences` 改为按换行切分并剥离 markdown 标题/引用/列表前缀，修复「`## 标题` 后的关键声明被整句丢弃」；新增回归测试锁住修复，测试数 7→8。
- **P1-2（results.tsv 措辞过度）**：明确脚本测试为真实证据、与人类实测 T1/T2 无关。
- **P2-5（缺 LICENSE）**：补充 MIT LICENSE 文件（署名 KK大叔/UncleKK, 2026）。

## [1.3.0] - 2026-07-22 · 策略A 补缺陷（Darwin 基线 92/100）

- gap1：新增「测试用例与预期判据」节（替换虚构实测，补 T1/T2 人工实测用例 + 脚本回归测试 + 降级路径 + reviewer 编号规则 + results.tsv 列结构）。
- gap2：新增 `references/` 目录结构说明与归档要求。
- gap3：新增 5 个显式 CHECKPOINT 节（CK-0~CK-4）。
- gap5：新增独立「黑名单 / 禁用模式」section。
- 审计报告链接到 results.tsv → evolution-log。

## [1.2.0] - 2026-07-22 · 深度审计修复

- P0 删除硬编码本地路径；P1 新增 `scripts/test_aris_audit.py`（6 项回归测试）+ `pyproject.toml` + 明确脚本仅覆盖阶段 2/3、阶段 1 为人工；P2 写文件前自动创建父目录 + 非 UTF-8 编码错误捕获。

## [1.1.0] - 2026-07-21 · 脚本化前置自审

- 新增 `scripts/aris_audit.py`（单文件双子命令 extract/drift，零交互 light 模式，证据缺口留空标 ⚠️ 不追问）；明确"前置降缺口、不替代 Hermes+SenseNova 异族审"定位。

## [1.0.0] - 2026-07-21 · 初版

- 对抗式编排（executor↔异族 reviewer）+ 三阶段声明审计 + Claim Ledger 模板 + WorkBuddy Runbook + 检查清单 + T1/T2 实测校验；源自 ARIS 论文保证层。
