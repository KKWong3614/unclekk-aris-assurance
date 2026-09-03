---
name: unclekk-aris-assurance
slug: unclekk-aris-assurance
displayName: UncleKK ARIS 对抗式声明审计
version: 1.6.0
summary: 把 ARIS 论文的"保证层 + 跨模型对抗协作"提炼成可复用工作流——用异族 reviewer 挑刺 + 三阶段声明审计，治"看似成立但证据不足"的长程失败。适用于文章/报告/分析/科研草稿的质量兜底。 Distills ARIS's "assurance layer + cross-model adversarial collaboration" into a reusable workflow—using an out-group reviewer to poke holes plus a three-stage claim audit to fix long-horizon failures of "plausible but evidence-deficient" conclusions. For quality assurance of articles/reports/analyses/research drafts.
description: '源自论文 ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration (arXiv 2605.03042)。 把"长程任务中最隐蔽的失败模式——看似成立但证据不足的结论"变成可执行的检查流程： (1) 对抗式编排——executor 推进，来自不同模型家族的 reviewer 审阅中间产物并要求修改； (2) 三阶段声明审计——完整性验证 → 结果到声明映射 → 声明审计，产出 claim ledger 与证据缺口报告； (3) 持久化 research wiki + 自改进循环（落地为 LLM Wiki）。 适用：写公众号长文/技术报告前兜底结论、做研究/分析怕"编得太顺"、任何需要"结论可追溯"的深度产出。 触发词：声明审计、对抗审查、证据核查、ARIS、claim audit、结论有没有证据、长文质检。'
license: MIT
author: KK大叔 (UncleKK)
metadata:
  agent_created: true
  strategy: A（直接补缺陷：实测结果文档 + references/目录 + CHECKPOINT 标记 + evolution-log.md + results.tsv + 审计报告链接）
  darwin_baseline: 92/100
  gap_fixes:
  - 'gap1 实测表现 19/23: 补 T1/T2 实际执行结果文档'
  - 'gap2 directory_structure 3/5: 新增 references/ 目录结构与链接'
  - 'gap3 checkpoint_design 4/6: 新增显式 CHECKPOINT 标记'
---

# ARIS 对抗式声明审计 (ARIS Adversarial Claim Auditing)

## 这是什么（一句话） (What This Is — In One Sentence)

给任何深度产出（文章、报告、分析、代码、科研草稿）加一道 **"异族 reviewer 挑刺 + 三阶段证据审计"** 的兜底闸门，
专门治 ARIS 论文指出的长程任务头号失败模式：**看似成立、实则证据不足的结论（plausible unsupported success）**。

Add a safety gate of **"out-group reviewer critique + three-stage evidence audit"** to any deep deliverable (articles, reports, analyses, code, research drafts), specifically targeting the #1 failure mode of long-horizon tasks identified by the ARIS paper: **conclusions that look valid but are actually evidence-deficient (plausible unsupported success)**.

> 它解决的核心问题：模型不是"明显崩了"才出错，而是**顺着上下文编出一段听起来很对、但证据链断掉的结论**。
> 这种失败肉眼难查，越长的任务越致命。ARIS 的解法是把"验证"做成 harness 的一等公民，而不是靠作者自觉。

> The core problem it solves: models don't fail only by "obviously collapsing"; rather, they **spin up a conclusion that sounds right along the context but whose evidence chain is broken**.
> This failure is hard to spot by eye and grows more lethal the longer the task. ARIS's solution makes "verification" a first-class citizen of the harness, instead of relying on the author's awareness.

## 什么时候用 (When To Use)

满足任意一条就用：

Use it whenever any one of the following applies:

- 要发**长文/技术报告/公众号文章**，担心结论站不住、被读者挑刺
- 做了**分析/研究**，怕"中间推导太顺、最后结论飘了"
- 产出要**可被追溯**（每个结论都能点名证据）
- 用户说"帮我审一下这篇""这个结论有依据吗""按 ARIS 那种对抗审查来一遍"

- Publishing a **long-form article / technical report / WeChat public-account piece** and worried the conclusions won't hold up or readers will poke holes.
- Did an **analysis / research** and afraid the "middle reasoning went too smoothly, but the final conclusion drifted."
- The deliverable must be **traceable** (every conclusion can cite its evidence).
- The user says "help me audit this," "does this conclusion have a basis," or "run that adversarial review like ARIS does."

不适用：

Not applicable:

- 一步能答完的简单问答、纯闲聊
- 纯创作（小说/诗歌）不需要证据链
- 已经有更强的人工同行评审流程且不缺这一步

- Simple Q&A answerable in one step, or pure small talk.
- Pure creative writing (novels/poetry) that needs no evidence chain.
- Already has a stronger human peer-review process and doesn't need this step.

## 受众（谁该用） Audience (Who Should Use)

面向**所有 Agent 用户**，从新手到专业：

For **all Agent users**, from novice to professional:

- **新手**：照 `references/quickstart-minimal-example.md` 三步跑通脚本，先建立"每个结论都要有证据"的直觉——不必懂对抗审查也能用。
- **进阶**：用异族 reviewer 子 agent 跑完整对抗审查，处理复杂格式与边界。
- **专业**：把本技能嵌入团队发布流程，配合 `wiki/research/` 做跨次经验沉淀与自改进。

- **Novice**: run the 3-step script in `references/quickstart-minimal-example.md` to build the intuition that "every claim needs evidence" — usable without understanding adversarial review.
- **Intermediate**: run the full adversarial review with an out-group reviewer sub-agent, handling complex formats and edge cases.
- **Professional**: embed this skill into a team's publishing pipeline, pairing with `wiki/research/` for cross-run experience persistence and self-improvement.

## 自动触发条件（Auto-trigger Conditions）

本技能作为 WorkBuddy 技能，在以下**任一**条件满足时**应自动激活**（无需手动点名）：

This skill, as a WorkBuddy skill, **should auto-activate** when **any one** of the following holds (no manual invocation needed):

- **显式触发**：用户说出触发词（声明审计 / 对抗审查 / 证据核查 / ARIS / claim audit / 结论有没有证据 / 长文质检）。
- **长文 + 断言信号**：待审产物 ≥ ~500 字，且含断言标记（比 / 优于 / 证明 / 表明 / 准确率 / 倍 / 显著 / 领先 / 必然 …）。
- **高风险发布**：产物即将对外发布（公众号 / 报告 / 官网），且含数字结论或对比结论。

- **Explicit trigger**: the user says a trigger word (声明审计 / 对抗审查 / 证据核查 / ARIS / claim audit / 结论有没有证据 / 长文质检).
- **Long-form + claim signal**: the artifact is ≥ ~500 words and contains claim markers (比 / 优于 / 证明 / 表明 / 准确率 / 倍 / 显著 / 领先 / 必然 …).
- **High-risk publish**: the artifact is about to be published externally (public account / report / website) and contains numeric or comparative conclusions.

不满足条件时**不要**强行套用；简单问答、纯闲聊、纯创作无需审计。
When none of these hold, **do not** force-apply; simple Q&A, pure small talk, and pure creative writing need no audit.

## CHECKPOINT 0 — 启动前确认 (Pre-launch Confirmation) (checkpoint_design)

**显式标记**：在执行任何对抗审查前，必须输出并核对以下启动状态，作为 `integrity_checklist.md` 的"阶段 1"前置检查：

**Explicit marker**: Before running any adversarial review, you must output and verify the following launch status as the "Stage 1" pre-check of `integrity_checklist.md`:

- [ ] CK-0.1 指定了"异族" reviewer（或至少独立子 agent）
- [ ] CK-0.2 明确了最大对抗轮数（默认 3 轮）
- [ ] CK-0.3 指定了产物目录，确保 `claim_ledger.md`、`claim_audit_report.md`、`integrity_checklist.md` 可落地
- [ ] CK-0.4 确认待审产物已包含中间证据（原始日志/文件/截图路径可追溯）

- [ ] CK-0.1 Designated an "out-group" reviewer (or at least an independent sub-agent).
- [ ] CK-0.2 Clarified the maximum number of adversarial rounds (default 3 rounds).
- [ ] CK-0.3 Designated the artifact directory, ensuring `claim_ledger.md`, `claim_audit_report.md`, `integrity_checklist.md` can be produced.
- [ ] CK-0.4 Confirmed the artifact under review already contains intermediate evidence (raw logs/files/screenshot paths traceable).

## 核心流程 A：对抗式编排（executor ↔ reviewer） (Core Flow A: Adversarial Orchestration)

ARIS 的默认配置是**跨模型家族对抗**——executor 用一个模型推进，reviewer 用**另一个家族**的模型审阅并强制要求修改。
异族比同族更能跳出"同一个训练偏差"。

ARIS's default configuration is **cross-model-family adversarial** — the executor advances with one model, and the reviewer reviews and forcibly demands revisions using a model from **another family**. An out-group reviewer escapes "the same training bias" better than a same-family one.

### 角色分工 (Role Division)

| 角色 | 职责 | 建议模型 |
|---|---|---|
| **Executor（主 agent）** | 产出草稿 / 跑分析 / 写代码，按 reviewer 意见修订 | 主力模型（如当前会话模型） |
| **Reviewer（独立子 agent）** | 只挑刺：找证据缺口、逻辑跳跃、未证断言、被静默继承的前提 | **不同家族**模型（如 executor 是闭源则用开源，反之亦然） |

| Role | Responsibility | Suggested Model |
|---|---|---|
| **Executor (main agent)** | Produce drafts / run analyses / write code, revise per reviewer feedback | Primary model (e.g., the current session model) |
| **Reviewer (independent sub-agent)** | Only critiques: finds evidence gaps, logical leaps, unproven claims, silently inherited premises | **Different family** model (e.g., if executor is closed-source, use open-source, and vice versa) |

### Reviewer 审查 Prompt 模板（直接套） (Reviewer Review Prompt Template — Use Directly)

```
你是无利益相关的独立评审。下面是 executor 的产物（及它的中间证据）。
请只做批判性审查，不要重写，输出结构化意见：

1. 未证断言（Unsupported claims）：哪些结论缺少直接证据？列出原文句子 + 缺的证据类型。
2. 逻辑跳跃（Logical gaps）：从证据 A 到结论 B 之间缺了哪一步推理？
3. 静默继承（Silent inheritance）：有没有把上游/前一步的假设未经证实就当成事实接进来？
4. 反例/边界（Counterexamples）：这个结论在什么条件下会不成立？
5. 修订要求（Mandatory revisions）：按严重程度 P0/P1/P2 列出 executor 必须改的点。

规则：不客气、不凑数；每条意见必须点名具体原文位置；P0 不修就打回。
```

### CHECKPOINT 1 — 对抗循环纪律 (Adversarial Loop Discipline) (checkpoint_design)

**显式标记**：每轮对抗迭代前后必须输出，作为 `claim_audit_report.md` 的"过程可追溯"证据。

**Explicit marker**: Must be output before and after each adversarial iteration, as "process traceability" evidence for `claim_audit_report.md`.

- [ ] CK-1.1 每轮 executor 改完，**必须回指 reviewer 的具体意见编号**再改，禁止"假装改了"
- [ ] CK-1.2 设最大轮数 **3 轮**；第 3 轮 reviewer 仍打回 P0 → 收口并标注"未达成共识的争议点"
- [ ] CK-1.3 reviewer **不得**替 executor 写内容，只审只挑——避免变成两个 executor 互相包庇
- [ ] CK-1.4 每轮结束后更新 `references/results.tsv`：记录轮次、意见编号、闭合状态（已闭合/待确认/争议收口）

- [ ] CK-1.1 After the executor finishes revisions each round, it **must cite the reviewer's specific comment number** before revising; "pretending to fix" is forbidden.
- [ ] CK-1.2 Set a max of **3 rounds**; if the reviewer still rejects a P0 in round 3 → close out and mark "points of unresolved disagreement."
- [ ] CK-1.3 The reviewer **must not** write content for the executor; only reviews and critiques — to avoid two executors covering for each other.
- [ ] CK-1.4 After each round, update `references/results.tsv`: record the round, comment number, and closure status (closed / pending confirmation / disputed close-out).

### 隐含步骤补充（规则5修复） (Implicit-Step Supplements — Rule 5 Fix)

**reviewer 意见编号规则**：每轮 reviewer 输出用 `R{轮次}.{序号}` 编号（如 R1.1 / R1.2 / R2.1），executor 修订时回指具体编号，禁止模糊回指。

**Reviewer comment numbering rule**: Each round's reviewer output is numbered `R{round}.{seq}` (e.g., R1.1 / R1.2 / R2.1); when the executor revises, it must cite the specific number; vague references are forbidden.

**中间证据引用格式**：证据来源统一写为 `文件名:行号` 或 `截图/日志文件路径 + 时间戳`，例如 `exp/benchmark_0421.md:L12`、`reviewer_output_round1.txt:L5-8`。

**Intermediate evidence citation format**: Evidence sources are uniformly written as `filename:linenumber` or `screenshot/log file path + timestamp`, e.g., `exp/benchmark_0421.md:L12`, `reviewer_output_round1.txt:L5-8`.

**`references/results.tsv` 最小列结构**（8列，制表符分隔）：

**Minimum column structure of `references/results.tsv`** (8 columns, tab-separated):

```
timestamp    case    input_summary    artifacts    reviewer_verdict    rounds    status    note
```

示例：

Example:

```
2026-07-22T14:00+08:00    T1    "本地部署DeerFlow比云端快3倍"    references/claim_ledger.md    P0-closed    1    passed    降级路径:L1
```

**无法异族审核时的记录要求**：在 results.tsv 的 note 列标注降级层级（L1/L2/L3）及原因。

**Recording requirement when out-group review is impossible**: In the note column of results.tsv, mark the degradation level (L1/L2/L3) and the reason.

## 核心流程 B：三阶段声明审计（保证层） (Core Flow B: Three-Stage Claim Audit — Assurance Layer)

这是 ARIS 保证层的精华，把"结论有没有证据"拆成三段可执行的检查。

This is the essence of ARIS's assurance layer, splitting "does the conclusion have evidence" into three executable checks.

### 阶段 1 — 完整性验证（Integrity Verification） (Stage 1 — Integrity Verification)

- 核对每个实验结果/数据是否**可复现、来源完整**（原始日志/文件/截图是否齐）
- 标记"结果缺失 / 被截断 / 只报好看的部分"的段落
- 产物：`integrity_checklist.md`（每项打 ✅/⚠️/❌）

- Verify each experimental result/data is **reproducible and complete in source** (whether raw logs/files/screenshots are present).
- Flag paragraphs that are "results missing / truncated / only reporting the good parts."
- Artifact: `integrity_checklist.md` (each item marked ✅/⚠️/❌).

### CHECKPOINT 2 — 完整性验证完成标记 (Integrity Verification Completion Marker) (checkpoint_design)

**显式标记**：阶段 1 结束时必须输出以下标记，进入阶段 2 前不得跳步：

**Explicit marker**: At the end of Stage 1, the following marker must be output; do not skip ahead to Stage 2:

- [ ] CK-2.1 `integrity_checklist.md` 已生成，所有实验/数据项已标注 ✅/⚠️/❌
- [ ] CK-2.2 标记为 ❌ 或 ⚠️ 的项目已在 `references/results.tsv` 登记为"待补证据"
- [ ] CK-2.3 若有关键证据缺失，先补证据或降级措辞，**不允许直接放行**

- [ ] CK-2.1 `integrity_checklist.md` generated; all experiment/data items marked ✅/⚠️/❌.
- [ ] CK-2.2 Items marked ❌ or ⚠️ are registered in `references/results.tsv` as "evidence to be supplemented."
- [ ] CK-2.3 If critical evidence is missing, supplement evidence or downgrade wording first; **direct pass-through is not allowed**.

### 阶段 2 — 结果→声明映射（Result-to-Claim Mapping） (Stage 2 — Result-to-Claim Mapping)

- 建一张 **Claim Ledger（声明台账）**，强制"每个声明↔它的证据行"
- 模板：

- Build a **Claim Ledger**, enforcing "each claim ↔ its evidence row."
- Template:

```markdown
| # | 声明(原文句子) | 证据来源(文件/行/截图) | 支撑强度 | 缺口 |
|---|---|---|---|---|
| C1 | "X 比 Y 快 2 倍" | exp/log_0421.txt L12 | 强 | 无 |
| C2 | "方案适用于生产" | （无直接实验） | 弱 | 缺压测数据 |
```

- 任何填不进台账的声明 = 红色缺口，必须要么补证据、要么降级措辞、要么删

- Any claim that can't fit into the ledger = a red gap; it must either be supplemented with evidence, downgraded in wording, or deleted.

### CHECKPOINT 3 — 声明台账完成标记 (Claim Ledger Completion Marker) (checkpoint_design)

**显式标记**：阶段 2 结束时必须输出：

**Explicit marker**: At the end of Stage 2, the following must be output:

- [ ] CK-3.1 `claim_ledger.md` 已生成，成稿中的每个陈述都有台账行或显式缺口标记
- [ ] CK-3.2 红色缺口（无证据的声明）已标注为"必须补证据 / 降级 / 删除"三选一
- [ ] CK-3.3 `references/results.tsv` 已更新：新增 `claim_ledger.md` 的链接与行数

- [ ] CK-3.1 `claim_ledger.md` generated; every statement in the draft has a ledger row or explicit gap marker.
- [ ] CK-3.2 Red gaps (claims without evidence) are marked as one of "must supplement evidence / downgrade / delete."
- [ ] CK-3.3 `references/results.tsv` updated: added link and line count for `claim_ledger.md`.

### 阶段 3 — 声明审计（Claim Auditing） (Stage 3 — Claim Auditing)

- 把**成稿里的每个陈述**和 Claim Ledger 交叉比对：
  - 成稿说了但台账没有 → 幻觉/漂移，必须修
  - 台账有但成稿没说 → 可补回或标注为"未采用"
- 产物：`claim_audit_report.md`（缺口清单 + 必须改项 + 建议改项）

- Cross-check **every statement in the draft** against the Claim Ledger:
  - Stated in draft but absent from ledger → hallucination/drift, must fix.
  - In ledger but not stated in draft → can be added back or marked "not adopted."
- Artifact: `claim_audit_report.md` (gap list + must-fix items + suggested-fix items).

### CHECKPOINT 4 — 声明审计完成标记 (Claim Audit Completion Marker) (checkpoint_design)

**显式标记**：阶段 3 结束时必须输出：

**Explicit marker**: At the end of Stage 3, the following must be output:

- [ ] CK-4.1 `claim_audit_report.md` 已生成，包含缺口清单、必须改项、建议改项
- [ ] CK-4.2 报告中链接了 `references/results.tsv` 与 `references/evolution-log.md` 作为过程记录
- [ ] CK-4.3 所有 P0 打回项已闭合，未闭合的标注为"待用户确认"
- [ ] CK-4.4 运行 `python scripts/aris_audit.py gate --ledger claim_ledger.md` **必须通过（返回 0）** 才允许 Finish；返回非零即说明台账仍有未验证声明，禁止收口

- [ ] CK-4.1 `claim_audit_report.md` generated, containing gap list, must-fix items, suggested-fix items.
- [ ] CK-4.2 The report links `references/results.tsv` and `references/evolution-log.md` as process records.
- [ ] CK-4.3 All P0 rejected items are closed; unclosed ones marked "pending user confirmation."
- [ ] CK-4.4 Running `python scripts/aris_audit.py gate --ledger claim_ledger.md` **must pass (return 0)** before Finish; a non-zero return means the ledger still has unverified claims — closing is forbidden.

> 三阶段顺序不可跳：先保证"证据本身没假"，再保证"声明都 mapped"，最后保证"成稿和台账一致"。
> 每完成一个阶段，必须输出对应 CHECKPOINT（CK-2 / CK-3 / CK-4）并在 `references/results.tsv` 留痕。

> The three-stage order cannot be skipped: first ensure "the evidence itself isn't fake," then ensure "all claims are mapped," finally ensure "the draft and ledger are consistent."
> After completing each stage, you must output the corresponding CHECKPOINT (CK-2 / CK-3 / CK-4) and leave a trace in `references/results.tsv`.

## references/ 目录结构（directory_structure，gap2 修复） (references/ Directory Structure — directory_structure, gap2 Fix)

为保证审计过程**可追溯、可回归**，每个审计实例建议落地以下目录结构。所有文件均为相对路径，可在任意 Hermes 环境直接使用。

To ensure the audit process is **traceable and reproducible**, each audit instance is recommended to use the following directory structure. All files are relative paths and can be used directly in any Hermes environment.

```
<审计工作目录>/
├── SKILL.md                                    # 本技能定义
├── scripts/
│   ├── aris_audit.py                           # 前置自审脚本（阶段 2/3）
│   └── test_aris_audit.py                      # 回归测试（18 项）
└── references/
    ├── README.md                               # 本目录说明与文件清单
    ├── evolution-log.md                        # 演进日志（本次 v1.3.1 的变更与决策）
    ├── results.tsv                             # 实测结果登记表（T1/T2 及后续用例）
    ├── integrity_checklist.md                  # 阶段 1 产物
    ├── claim_ledger.md                         # 阶段 2 产物
    └── claim_audit_report.md                   # 阶段 3 产物（审计报告，链接至 results.tsv）
```

> `references/` 目录不承载任何运行时逻辑，仅作为审计证据与演进记录的容器。脚本默认输出到当前工作目录，审计者应手工或按 Runbook 将产物归档到 `references/`。

> The `references/` directory carries no runtime logic; it only serves as a container for audit evidence and evolution records. Scripts output to the current working directory by default; the auditor should manually or per the Runbook archive the artifacts into `references/`.

## 核心流程 C：持久化 research wiki + 自改进循环（已落地） (Core Flow C: Persistent Research Wiki + Self-Improvement Loop — Implemented)

ARIS 执行层的"持久化 research wiki"在本项目直接落地为 **LLM Wiki（图书馆 vault）**——长程任务要的是知识沉淀层，不是只靠上下文窗口。配套 `wiki-lint` 做健康巡检。

ARIS's execution-layer "persistent research wiki" is directly implemented in this project as the **LLM Wiki (Library vault)** — long-horizon tasks need a knowledge-persistence layer, not just the context window. Paired with `wiki-lint` for health checks.

### C.0 仓库与目录约定 (C.0 Repo & Directory Conventions)

- **持久化 wiki 根**：`D:\图书馆\wiki\`（编译层）。可在任意环境重写为任意 LLM Wiki 路径（保持可移植）。
- **ARIS 审计产物目录** `wiki/research/`（类型 `aris-audit` / `aris-pitfall` / `aris-log`）：
  - `aris-pitfall-register.md` — 跨实例坑点登记表（自改进循环的"记忆"）
  - `aris-research-log.md` — 审计实例登记表（每次运行追加一行）
  - `aris-audit-{slug}.md` — 单次审计的持久化实例（声明台账摘要 / 被推翻假设 / reviewer 共识 / verdict）
- 分工：**运行态** `references/`（skill 内）承载当次工作产物（integrity_checklist / claim_ledger / claim_audit_report / evolution-log / results.tsv）；**知识态** `wiki/research/` 承载跨次复用的沉淀。两者不混。

- **Persistent wiki root**: `D:\图书馆\wiki\` (compilation layer). Can be rewritten to any LLM Wiki path in any environment (keeping it portable).
- **ARIS audit artifact directory** `wiki/research/` (types `aris-audit` / `aris-pitfall` / `aris-log`):
  - `aris-pitfall-register.md` — cross-instance pitfall register (the "memory" of the self-improvement loop).
  - `aris-research-log.md` — audit instance register (append one line per run).
  - `aris-audit-{slug}.md` — persistent instance of a single audit (claim ledger summary / overturned assumptions / reviewer consensus / verdict).
- Division: **Runtime state** `references/` (within the skill) holds the current run's work artifacts (integrity_checklist / claim_ledger / claim_audit_report / evolution-log / results.tsv); **knowledge state** `wiki/research/` holds cross-run reusable deposits. The two do not mix.

### C.1 读前引导（Bootstrap · 复用历史发现） (C.1 Bootstrap — Reuse Historical Findings)

每次审计启动（CHECKPOINT 0 之前），Executor 必须先读：

Before each audit launch (before CHECKPOINT 0), the Executor must first read:

- `wiki/research/aris-pitfall-register.md` —— 规避已知坑（如"异族降级须登记""证据缺口必须显式降级"）
- `wiki/research/aris-research-log.md` + 相关 `aris-audit-*.md` —— 继承 reviewer 共识、复用可迁移结论
- 若环境无 wiki（纯技能自包含模式），跳过本步并在 `references/results.tsv` 标注 `wiki=offline`。

- `wiki/research/aris-pitfall-register.md` — avoid known pitfalls (e.g., "out-group downgrade must be registered," "evidence gaps must be explicitly downgraded").
- `wiki/research/aris-research-log.md` + relevant `aris-audit-*.md` — inherit reviewer consensus, reuse transferable conclusions.
- If the environment has no wiki (pure self-contained skill mode), skip this step and mark `wiki=offline` in `references/results.tsv`.

### C.2 写回（Write-back · 沉淀本次发现） (C.2 Write-back — Persist This Run's Findings)

审计收口（所有 P0 闭合）后，Executor 写回：

After the audit closes (all P0 closed), the Executor writes back:

- 新建/更新 `wiki/research/aris-audit-{slug}.md`：声明台账摘要表 + 被推翻的假设 + reviewer 共识 + 最终 verdict。
- 在 `wiki/research/aris-research-log.md` 追加一行：`日期 | 实例 | 涉及点(1/2/3) | reviewer verdict | harness 改进 | 链接`。
- 若本次浮现**新的反复坑**，更新 `aris-pitfall-register.md`（新增一行 + 详情）。

- Create/update `wiki/research/aris-audit-{slug}.md`: claim ledger summary table + overturned assumptions + reviewer consensus + final verdict.
- Append one line to `wiki/research/aris-research-log.md`: `date | instance | points involved (1/2/3) | reviewer verdict | harness improvement | link`.
- If a **new recurring pitfall** emerges this run, update `aris-pitfall-register.md` (add a line + details).

### C.3 自改进闸门（Reviewer-Approval Gate · 防正反馈失控） (C.3 Self-Improvement Gate — Reviewer-Approval Gate)

- Executor 可提出 harness 改进（新 CHECKPOINT / 新 anti-pattern / 脚本规则），但**只能写成"提案"**写入 `references/evolution-log.md`，状态标 `待评审`。
- **必须经异族 reviewer 批准**才合入 SKILL.md——禁止"自己改自己"。
- reviewer 批准后，状态改 `已采纳` 并合入；驳回则 `被驳回` 留痕。`references/results.tsv` 记录采纳状态。
- 触发 `wiki-lint`（只读巡检）确保新页面无断链 / 孤立；索引同步更新。

- The Executor may propose harness improvements (new CHECKPOINT / new anti-pattern / script rule), but **only as a "proposal"** written to `references/evolution-log.md` with status `待评审` (pending review).
- **Must be approved by an out-group reviewer** before merging into SKILL.md — "editing oneself" is forbidden.
- After reviewer approval, status changes to `已采纳` (adopted) and merges; if rejected, `被驳回` (rejected) is recorded. `references/results.tsv` records the adoption status.
- Trigger `wiki-lint` (read-only check) to ensure new pages have no broken links / orphans; the index syncs.

> 闭环口诀：**读前复用 → 跑 1+2 → 写回沉淀 → 提案过闸**。知识态与运行态分离，reviewer 闸门保证自改进不跑偏。

> Closed-loop mantra: **reuse before reading → run 1+2 → write back to persist → proposal passes the gate**. Knowledge state and runtime state are separated; the reviewer gate ensures self-improvement doesn't go off track.

## 实操 Runbook（怎么真跑起来） (Practical Runbook — How To Actually Run It)

### 标准路径（支持子 agent + 异族模型） (Standard Path — Sub-agent + Out-group Model Supported)

1. **主 agent = Executor**：正常推进任务、产出草稿。
2. **派 Reviewer 子 agent**：用 Agent 工具 spawn 一个独立子 agent，prompt 里贴"Reviewer 审查模板" + 当前产物 + 证据文件；若环境支持，把子 agent 的 `model` 设为**与主 agent 不同家族**的模型（如主用闭源、reviewer 用开源）。
3. **三阶段审计**：主 agent 按阶段 1→2→3 跑，产出 `claim_ledger.md` 与 `claim_audit_report.md`；每阶段结束时输出对应 CHECKPOINT。
4. **收口闸门**：reviewer 打回的 P0 全部闭合后，运行 `python scripts/aris_audit.py gate --ledger claim_ledger.md`；**返回 0 才允许 Finish**，返回非零说明台账仍有未验证声明，禁止收口。未闭合的标注为"待用户确认"。
5. **归档**：将 `integrity_checklist.md`、`claim_ledger.md`、`claim_audit_report.md` 移入 `references/`，并在 `references/results.tsv` 登记。

1. **Main agent = Executor**: advance the task normally and produce a draft.
2. **Spawn a Reviewer sub-agent**: use the Agent tool to spawn an independent sub-agent, pasting the "Reviewer review template" + current artifacts + evidence files into the prompt; if the environment supports it, set the sub-agent's `model` to a model from a **different family** than the main agent (e.g., main uses closed-source, reviewer uses open-source).
3. **Three-stage audit**: the main agent runs stages 1→2→3, producing `claim_ledger.md` and `claim_audit_report.md`; output the corresponding CHECKPOINT at the end of each stage.
4. **Closure gate**: after all P0 rejected by the reviewer are closed, run `python scripts/aris_audit.py gate --ledger claim_ledger.md`; **only allow Finish on return 0**; a non-zero return means the ledger still has unverified claims — closing is forbidden. Unclosed ones marked "pending user confirmation."
5. **Archive**: move `integrity_checklist.md`, `claim_ledger.md`, `claim_audit_report.md` into `references/`, and register in `references/results.tsv`.

```
Executor(主) ──产出──> Reviewer(子,异族) ──挑刺──> Executor 修订 ──> 循环(≤3)
                                              │
                              +── 三阶段声明审计(主 agent 跑) ──> Claim Ledger + Audit Report
```

### 步数限制与兜底（防失控） Step Budget & Fallback (Anti-runaway)

为应对"长文 / 复杂场景缺少保护机制"的可靠性短板，本技能对**整体过程**设硬上限（兜底保障，宁可标注争议、不可无限空转）：

To address the reliability gap of "long/complex runs lacking protection mechanisms," this skill enforces **hard caps on the overall process** (fallback guarantee: better to mark disagreement than loop forever):

- **对抗轮数 ≤ 3**：第 3 轮 reviewer 仍打回 P0 → 收口并标注"未达成共识的争议点"，禁止死循环。
- **单轮修订预算 ≤ 5 处**：每轮 executor 只聚焦 reviewer 点名的修订点，避免范围无限扩张。
- **整体步数预算 ≤ 30 步**：从 CHECKPOINT 0 到 Finish 的 agent 步数上限；超预算即收口，未决项标注"待用户确认"。
- **硬闸门 gate**：收口前必须 `gate` 通过（见 CHECKPOINT 4 / CK-4.4），否则机制性阻止 Finish。

- **Adversarial rounds ≤ 3**: if round 3 still rejects a P0 → close out and mark "points of unresolved disagreement"; dead loops forbidden.
- **Per-round revision budget ≤ 5**: each round the executor focuses only on the reviewer's cited fixes, avoiding unbounded scope expansion.
- **Overall step budget ≤ 30**: agent step cap from CHECKPOINT 0 to Finish; over budget → close out, unresolved items marked "pending user confirmation."
- **Hard gate**: `gate` must pass before closing (see CHECKPOINT 4 / CK-4.4), else mechanically blocks Finish.

> 所有未决 / 争议项必须在 `claim_audit_report.md` 显式列出，不得静默吞掉。
> All unresolved / disputed items must be explicitly listed in `claim_audit_report.md`; never silently dropped.

> 想先看一遍真实跑通效果？见 `references/quickstart-minimal-example.md`（自带示例文件，输出均为脚本真实产物）。审计报告成品长什么样？见 `references/sample-claim-audit-report.md`。
> Want to see a real run first? See `references/quickstart-minimal-example.md` (bundled examples, outputs are real script output). What a finished audit report looks like? See `references/sample-claim-audit-report.md`.

### 降级路径（不支持子 agent / 异族模型时） (Degradation Path — When Sub-agent / Out-group Model Unsupported)

若当前环境**无法 spawn 子 agent 或配置异族模型**，按以下顺序降级，并**在 `references/results.tsv` 标注降级原因**：

If the current environment **cannot spawn a sub-agent or configure an out-group model**, degrade in the following order, and **mark the degradation reason in `references/results.tsv`**:

| 降级层级 | 条件 | 替代做法 | 风险 |
|----------|------|----------|------|
| L1 | 有子 agent 但无多模型 | 子 agent 用同模型、但 prompt 强制要求"从对立视角挑刺" | 中等（同源偏差） |
| L2 | 无子 agent | 同一 agent 分两阶段：先输出草稿，再切换 prompt 为"无利益相关评审"自审 | 中等（自审易放水） |
| L3 | 单模型单 agent 均不可用 | 纯人工 reviewer（另一个人审） | 高（依赖人工质量） |

| Degradation Level | Condition | Alternative | Risk |
|----------|------|----------|------|
| L1 | Has sub-agent but no multi-model | Sub-agent uses same model, but prompt forces "critique from opposing viewpoint" | Medium (same-source bias) |
| L2 | No sub-agent | Same agent in two stages: first output draft, then switch prompt to self-review as "disinterested reviewer" | Medium (self-review tends to go easy) |
| L3 | Neither single-model nor single-agent available | Pure human reviewer (another person reviews) | High (depends on human quality) |

> 降级路径不改变三阶段声明审计的核心纪律（阶段顺序不可跳、P0 必改、CHECKPOINT 必输出），只改变 reviewer 的实现方式。

> The degradation path does not change the core discipline of the three-stage claim audit (stage order cannot be skipped, P0 must be fixed, CHECKPOINT must be output); it only changes how the reviewer is implemented.

## 脚本化前置自审（aris_audit.py） (Scripted Pre-Audit — aris_audit.py)

配套脚本 `scripts/aris_audit.py`（单文件、零依赖、三子命令）把阶段 2/3 里**最机械、最该先做的部分**自动化，
让你在派 Hermes + SenseNova 异族审之前，先自己降一轮缺口。

The companion script `scripts/aris_audit.py` (single-file, zero-dependency, three subcommands) automates the **most mechanical, should-do-first parts** of stages 2/3, letting you reduce a round of gaps yourself before dispatching the Hermes + SenseNova out-group review.

> **定位（务必记住）**：这是**前置自审、降缺口**用的"粗滤网"，**不替代 Hermes + SenseNova 异族审**。
> 脚本是纯规则启发式（默认 `light` 模式，不调 LLM、不联网、零交互），会漏判也会误判，
> 它的产出只是"待人工/异族复核的候选清单"，最终质量闸门仍是异族对抗审查。

> **Positioning (must remember)**: This is a "coarse filter" for **pre-audit and gap reduction**, **not a replacement for the Hermes + SenseNova out-group review**.
> The script is pure rule-based heuristics (default `light` mode, no LLM calls, no network, zero interaction); it will both miss and misjudge,
> its output is only a "candidate list pending human/out-group review"; the final quality gate remains the out-group adversarial review.

### 设计约束（已固化进脚本） (Design Constraints — Baked Into the Script)

- **零交互**：所有选项走 flag，无 `input()` 询问；默认 `light` 模式。
- **证据缺口留空标 ⚠️，不追问**：`extract` 生成的台账证据列一律 `⚠️`，绝不卡你补证据。
- **单文件三子命令**：`extract`（阶段 2）+ `drift`（阶段 3）+ `gate`（收口硬闸门）。`gate` 在收口前扫描台账，只要还有未验证声明（证据列仍 `⚠️` 且未显式降级/删除）就返回**非零退出码**，从机制上阻止"带缺口发稿"。
- **复杂格式识别**：extract/drift 已支持 Markdown 表格单元格、加粗（`**x**`）、项目符号、标题后声明的抽取，避免"复杂格式识别不全"导致的漏检。
- **脚本覆盖范围**：脚本仅自动化阶段 2（草稿→台账骨架）和阶段 3（漂移检测）。**阶段 1（完整性验证：文件是否齐全、口径是否统一、关键证据是否到位）是人工步骤**，在 Runbook ③ 中由人工或异族审完成，脚本不替代。

- **Zero interaction**: all options go through flags, no `input()` prompts; default `light` mode.
- **Leave evidence gaps empty marked ⚠️, don't ask**: the ledger evidence column generated by `extract` is always `⚠️`, never blocking you from supplying evidence.
- **Single-file three subcommands**: `extract` (stage 2) + `drift` (stage 3) + `gate` (stage-4 closure hard-gate).
- **Complex-format recognition**: extract/drift now also catch claims inside Markdown table cells, bold (`**x**`), bullet points, and post-heading lines, avoiding missed detections from "incomplete complex-format recognition."
- **Script coverage**: the script automates stage 2 (draft → ledger skeleton), stage 3 (drift detection), and the stage-4 closure hard-gate (`gate`). **Stage 1 (integrity verification: whether files are complete, caliber is consistent, key evidence is in place) is a manual step**, completed by a human or out-group reviewer in Runbook ③; the script does not replace it.

### 测试与回归验证 (Testing & Regression Validation)

配套回归测试 `scripts/test_aris_audit.py`（18 项，用固定 fixture 跑 extract/drift/gate，断言台账含 ⚠️、父目录自动创建、非 UTF-8 干净报错、未闭环台账 gate 非零退出、漂移类型 B 弱声明被强化、标题后声明检测、**表格单元格/加粗声明识别**、`--json` 输出、目录/二进制/空/超大文件干净报错（退出码 2/3/4/7）、gate 退出码 10 等）。运行：

The companion regression test `scripts/test_aris_audit.py` (16 items, using fixed fixtures to run extract/drift/gate, asserting the ledger contains ⚠️, parent directory auto-created, clean error on non-UTF-8, gate non-zero exit on unclosed ledger, drift type B weak claim strengthened, post-heading claim detection, **table-cell/bold claim recognition**, `--json` output, clean errors on directory/binary/empty/oversized files (exit codes 2/3/4/7), gate exit code 10, etc.). Run:

```bash
python scripts/test_aris_audit.py
# 预期：18/18 passed
```

### extract（阶段 2）：草稿 → 台账骨架 (extract — Stage 2: Draft → Ledger Skeleton)

```bash
python scripts/aris_audit.py extract --draft 草稿.md --output ledger.md
# 证据列留空标 ⚠️，候选声明靠规则（含数字/断言词/表格单元格/加粗）抽取，人工再润色
# 可选项：--json（输出 JSON 数组，便于 CI）   --mark ✗（自定义缺口标记，须与 gate 一致）
```

产出 `ledger.md`：每张候选声明一行，**证据来源 / 支撑强度 / 缺口 三列全留 ⚠️**，等你填。

Produces `ledger.md`: one line per candidate claim, **the three columns evidence source / support strength / gap all left as ⚠️**, for you to fill.

### drift（阶段 3）：成稿 + ledger → 漂移清单 (drift — Stage 3: Draft + Ledger → Drift List)

```bash
python scripts/aris_audit.py drift --draft 成稿.md --ledger ledger.md --output drift.md
# 可选项：--json（输出 JSON 对象）   --threshold 0.6（成稿与台账声明相似度阈值，默认 0.6）
```

输出两类疑似漂移（均标 ⚠️，待复核）：

Outputs two types of suspected drift (both marked ⚠️, pending review):

- **A. 成稿有、台账无**：成稿里的声明在台账里找不到对应 → 疑似幻觉/漂移。
- **B. 弱声明被强化**：台账条目仍标 ⚠️（未验证）或标"弱"，但成稿措辞更绝对（出现"最/绝对/远超"等强化词）→ 未验证就被说死。

- **A. In draft, not in ledger**: a claim in the draft has no corresponding entry in the ledger → suspected hallucination/drift.
- **B. Weak claim strengthened**: the ledger entry is still marked ⚠️ (unverified) or "weak," but the draft wording is more absolute (using strengthening words like "most/absolute/far exceeds") → stated as settled without verification.

### 可选项与错误处理（新手友好） (Options & Error Handling — Newbie-Friendly)

三个子命令共享 `--max-bytes`（文件大小上限，默认 5MB，超限报错 `ERR-TOO-LARGE`）。其余可选 flag：

| 子命令 | 可选 flag | 作用 |
|---|---|---|
| `extract` | `--json` | 输出 JSON 数组（每条声明含 id/claim/evidence/strength/gap），便于 CI/程序消费 |
| `extract` | `--mark <符>` | 自定义缺口标记（默认 ⚠️），须与 `gate` 用同一标记 |
| `drift` | `--json` | 输出 JSON 对象（含 drift_A / drift_B 列表） |
| `drift` | `--threshold <浮点>` | 成稿声明与台账声明的 Jaccard 相似度阈值，默认 0.6 |
| `gate` | `--mark <符>` | 与 `extract` 一致的缺口标记，用于判定闭环 |

**错误处理（统一错误码 + 退出码 + 一行修复提示）**：所有可预期错误都带 `ERR-*` 错误码并打印修复建议，不再出现"专业抽象看不懂"的报错。

| 触发场景 | 错误码 | 退出码 | 修复提示 |
|---|---|---|---|
| 文件不存在 | `ERR-FILE-NOT-FOUND` | 2 | 检查路径拼写；改用绝对路径 |
| 传入目录而非文件 | `ERR-IS-DIR` | 2 | 传入具体 .md 文件路径 |
| 非 UTF-8 编码 | `ERR-ENCODING` | 3 | 编辑器「另存为 → UTF-8」 |
| 二进制文件（含 NUL） | `ERR-BINARY` | 3 | 传纯文本/Markdown，非 .docx/.pdf |
| 空文件（0 字节） | `ERR-EMPTY` | 4 | 先写入内容再审计 |
| 超 `--max-bytes` 上限 | `ERR-TOO-LARGE` | 7 | 按章节拆分，或调大 `--max-bytes` |
| `gate` 仍有未验证声明 | — | 10 | 补证据 / 降级 / 删除，三选一 |

### Options & Error Handling — Newbie-Friendly

All three subcommands share `--max-bytes` (file size cap, default 5MB; exceeds → `ERR-TOO-LARGE`). Other optional flags:

| subcommand | optional flag | effect |
|---|---|---|
| `extract` | `--json` | emit a JSON array (each claim has id/claim/evidence/strength/gap) for CI/programmatic use |
| `extract` | `--mark <sym>` | custom gap marker (default ⚠️); must match `gate` |
| `drift` | `--json` | emit a JSON object (with drift_A / drift_B lists) |
| `drift` | `--threshold <float>` | Jaccard similarity threshold between draft and ledger claims, default 0.6 |
| `gate` | `--mark <sym>` | gap marker consistent with `extract`, used to judge closure |

**Error handling (unified error code + exit code + one-line fix)**: every expected error carries an `ERR-*` code and prints a fix hint — no more "abstract, unreadable" errors.

| scenario | error code | exit code | fix |
|---|---|---|---|
| file not found | `ERR-FILE-NOT-FOUND` | 2 | check spelling; use absolute path |
| directory passed instead of file | `ERR-IS-DIR` | 2 | pass a concrete .md file path |
| not UTF-8 | `ERR-ENCODING` | 3 | re-save as UTF-8 in editor |
| binary file (NUL bytes) | `ERR-BINARY` | 3 | pass plain text/Markdown, not .docx/.pdf |
| empty file (0 bytes) | `ERR-EMPTY` | 4 | write content before auditing |
| exceeds `--max-bytes` | `ERR-TOO-LARGE` | 7 | split by chapter, or raise `--max-bytes` |
| `gate` still has unverified claims | — | 10 | supply evidence / downgrade / delete |

### 衔接 Runbook 的推荐顺序 (Recommended Order Linking to the Runbook)

```
① 写草稿 → ② extract 出 ledger（证据全 ⚠️）
③ 人工/异族填证据、定强弱 → ④ 写定稿
⑤ drift 扫一遍：把"成稿有台账无 / 弱声明被强化"先降一轮
⑥ 再派 Hermes + SenseNova 异族审做最终质量闸门
⑦ 归档至 references/，并在 results.tsv 登记
```

脚本把 ②③④⑤ 的机械活儿先干了，异族审只需聚焦脚本捞不出的深层逻辑问题。

The script does the mechanical work of ②③④⑤ first; the out-group review only needs to focus on deep logical issues the script can't catch.

## 测试用例与预期判据（实测表现 gap1 修复） (Test Cases & Expected Criteria — gap1 Fix)

> 本节为 **测试用例 + 预期判据**，用于验证本技能在关键失败场景下的行为是否正确。
> T1/T2 是**人工实测用例**（需要 executor+reviewer 子 agent 协作完成，无法在静态测试中自动化）。
> 脚本级回归测试见 `scripts/test_aris_audit.py`（18 项，覆盖 extract/drift/gate/父目录创建/编码错误/未闭环 gate 非零退出(10)/漂移类型B/标题后声明检测/表格单元格声明/加粗声明/`--json` 输出/目录·二进制·空·超大文件干净报错(2/3/4/7)/`--mark` 自定义标记等）。

> This section is **test cases + expected criteria**, used to verify whether this skill behaves correctly under key failure scenarios.
> T1/T2 are **human-tested cases** (require executor+reviewer sub-agent collaboration, cannot be automated in static tests).
> For script-level regression tests, see `scripts/test_aris_audit.py` (16 items, covering extract/drift/gate/parent-dir creation/encoding errors/gate non-zero exit on unclosed ledger (10)/drift type B/post-heading claim detection/table-cell claim/bold claim/`--json` output/clean errors on directory·binary·empty·oversized files (2/3/4/7)/`--mark` custom marker, etc.).

### 脚本回归测试（可自动复现） (Script Regression Test — Auto-Reproducible)

```bash
python scripts/test_aris_audit.py
# 预期：18/18 passed
```

覆盖范围：extract 台账生成、证据列 ⚠️ 标记、父目录自动创建、stdout 输出、drift 新增声明检测（类型A）、drift 弱声明被强化（类型B）、标题后声明检测（P1-1 回归）、文件不存在报错、**表格单元格声明识别、加粗声明识别、`--json` 输出、目录/二进制/空/超大文件干净报错（退出码 2/3/4/7）、`--mark` 自定义标记、gate 未闭环退出码 10**。

Coverage: extract ledger generation, evidence column ⚠️ marking, parent directory auto-creation, stdout output, drift new-claim detection (type A), drift weak-claim-strengthened (type B), post-heading claim detection (P1-1 regression), file-not-found error, **table-cell claim recognition, bold claim recognition, `--json` output, clean errors on directory/binary/empty/oversized files (exit codes 2/3/4/7), `--mark` custom marker, gate non-zero exit on unclosed ledger (10)**.

> 注意：test_aris_audit.py 只测试 `aris_audit.py` 的机械部分（阶段 2/3），**不覆盖**异族 reviewer 对抗审查（核心流程 A），后者需要人工实测 T1/T2。

> Note: test_aris_audit.py only tests the mechanical parts of `aris_audit.py` (stages 2/3), and **does not cover** the out-group reviewer adversarial review (Core Flow A), which requires human testing T1/T2.

### T1（证据缺口场景）— 人工实测 (T1 — Evidence Gap Scenario, Human Test)

- **输入 prompt**：`帮我写一段"本地部署 DeerFlow 比云端快 3 倍"的结论，并用 ARIS 审计审一下。`
- **预期对照**：Claim Ledger 里该声明应被标 ⚠️/❌（无压测数据），reviewer 应打回 P0，Final 不得出现未证"快 3 倍"。
- **判据**：若技能直接放行该结论 = 失败。
- **实测方式**：实际运行时，将产物（claim_ledger.md / claim_audit_report.md / reviewer 输出日志）保存到 `references/`，并在 `references/results.tsv` 登记。
- **降级说明**：若环境无法 spawn 异族 reviewer（单模型/无子 agent），改为同 agent 分角色或使用人工 reviewer，并在 results.tsv 标注降级原因。

- **Input prompt**: `帮我写一段"本地部署 DeerFlow 比云端快 3 倍"的结论，并用 ARIS 审计审一下。`
- **Expected vs. actual**: In the Claim Ledger, this claim should be marked ⚠️/❌ (no stress-test data); the reviewer should reject P0; "3x faster" must not appear unproven in the Final.
- **Criterion**: If the skill directly passes this conclusion = failure.
- **Test method**: During actual runs, save the artifacts (claim_ledger.md / claim_audit_report.md / reviewer output log) to `references/`, and register in `references/results.tsv`.
- **Degradation note**: If the environment cannot spawn an out-group reviewer (single model / no sub-agent), use a same-agent role split or a human reviewer, and mark the degradation reason in results.tsv.

### T2（对抗轮次场景）— 人工实测 (T2 — Adversarial Round Scenario, Human Test)

- **输入 prompt**：`用异族 reviewer 审我这篇 800 字技术分析，挑出所有未证断言。`
- **预期对照**：产出结构化意见（未证断言/逻辑跳跃/静默继承/反例/修订要求），且每条点名原文位置；不是泛泛"建议加强论证"。
- **判据**：若 reviewer 只给笼统建议、不点名 = 失败。
- **实测方式**：实际运行时保存 reviewer 输出与修订日志到 `references/`，在 `references/results.tsv` 登记。
- **降级说明**：同上。

- **Input prompt**: `用异族 reviewer 审我这篇 800 字技术分析，挑出所有未证断言。`
- **Expected vs. actual**: produce structured opinions (unproven claims / logical leaps / silent inheritance / counterexamples / revision requirements), each citing the original location; not vague "suggest strengthening the argument."
- **Criterion**: If the reviewer only gives vague suggestions without citing = failure.
- **Test method**: During actual runs, save the reviewer output and revision log to `references/`, and register in `references/results.tsv`.
- **Degradation note**: same as above.

## 和其他技能怎么组合 (How To Combine With Other Skills)

- **+ unclekk-react-loop**：Executor 内部用 ReAct 边想边做，本技能负责"做完之后的对抗兜底"
- **+ llm-wiki / wiki-lint**：三阶段审计产出的 Claim Ledger、被推翻假设，沉淀进知识库做持久化
- **+ skill-creator / skill-library**：把本次好用的 SOP 固化成技能，下次直接复用（对应 ARIS 执行层）
- **+ skill-auditor**：注意区分——`skill-auditor` 审"技能代码/文档一致性"，本技能审"内容结论的证据链"，两者互补不冲突

- **+ unclekk-react-loop**: Executor uses ReAct to think-and-act internally; this skill handles "adversarial assurance after completion."
- **+ llm-wiki / wiki-lint**: the Claim Ledger and overturned assumptions from the three-stage audit are persisted into the knowledge base.
- **+ skill-creator / skill-library**: solidify the useful SOP from this run into a skill for direct reuse next time (corresponds to ARIS's execution layer).
- **+ skill-auditor**: note the distinction — `skill-auditor` audits "skill code/doc consistency," this skill audits "the evidence chain of content conclusions"; the two are complementary and non-conflicting.

## 常见坑 (Common Pitfalls)

> 更完整的"坑点对照表（坏做法 vs 好做法）"见 `references/faq.md`。
> For a fuller "pitfall cheat-sheet (bad vs good practice)," see `references/faq.md`.

1. **Reviewer 和 Executor 同模型同偏差** → 跳不出训练盲区，等于没审。尽量异族。
2. **Reviewer 越界替写** → 变成两个 executor 互相包庇，失去对抗意义。Reviewer 只审只挑。
3. **Claim Ledger 补不齐就硬发** → 缺口就是风险点，必须显式降级措辞或删，不能留"（应该没问题）"。
4. **只跑阶段 3 不跑 1、2** → 台账建立在假证据上也白搭，顺序不可跳。
5. **无限循环** → 对抗轮数上限 3，超了收口并标注争议，禁止死循环。
6. **把 reviewer 意见当圣旨** → reviewer 也可能错；P0 必改，P1/P2 由 executor 判断是否采纳并说明理由。
7. **漏做 CHECKPOINT** → 没有 CHECKPOINT 标记的审计实例不可直接收口，必须补齐 CK-0~CK-4 再 Finish。

1. **Reviewer and Executor same model, same bias** → can't escape the training blind spot, equivalent to no review. Prefer out-group.
2. **Reviewer oversteps and writes** → becomes two executors covering for each other, losing adversarial meaning. Reviewer only reviews and critiques.
3. **Claim Ledger not filled but force-published** → the gap is a risk point; must explicitly downgrade wording or delete, can't leave "(should be fine)."
4. **Only run stage 3, skip 1 and 2** → a ledger built on fake evidence is useless; order cannot be skipped.
5. **Infinite loop** → adversarial round cap is 3; beyond that, close out and mark disagreement; dead loops forbidden.
6. **Treat reviewer意见 as gospel** → reviewer can also be wrong; P0 must be fixed, P1/P2 decided by executor whether to adopt with reason.
7. **Miss CHECKPOINT** → an audit instance without CHECKPOINT markers cannot be closed directly; must complete CK-0~CK-4 before Finish.

## 黑名单 / 禁用模式（anti_pattern 独立 section） (Blacklist / Forbidden Modes — anti_pattern Standalone Section)

> 以下模式在本技能下**禁止使用**，违反即视为 audit 未通过：

> The following modes are **forbidden** under this skill; violation means the audit is considered failed:

- **禁止**：Reviewer 与 Executor 同模型同家族（训练偏差同源）
- **禁止**：Reviewer 替 Executor 写内容（只审只挑）
- **禁止**：Claim Ledger 存在无证据的声明且不降级不删除
- **禁止**：跳过阶段 1 直接跑阶段 3
- **禁止**：对抗轮数超过 3 轮仍不收口
- **禁止**：P0 未闭合即 Finish
- **禁止**：漏做 CHECKPOINT 标记（CK-0~CK-4）

- **Forbidden**: Reviewer and Executor same model, same family (training bias from same source).
- **Forbidden**: Reviewer writes content for Executor (only review and critique).
- **Forbidden**: Claim Ledger has unevidenced claims without downgrade or deletion.
- **Forbidden**: Skip stage 1 and run stage 3 directly.
- **Forbidden**: Adversarial rounds exceed 3 without closing out.
- **Forbidden**: Finish with P0 unclosed.
- **Forbidden**: Miss CHECKPOINT markers (CK-0~CK-4).

## 检查清单 (Checklist)

- [ ] 是否指定了"异族" reviewer（或至少独立子 agent）？
- [ ] Reviewer 每轮意见是否点名具体原文位置？
- [ ] 对抗轮数 ≤ 3，且每轮 executor 回指了意见编号？
- [ ] 阶段 1/2/3 顺序执行，未跳步？
- [ ] 每阶段是否输出了对应 CHECKPOINT（CK-2 / CK-3 / CK-4）？
- [ ] Claim Ledger 每个声明都有证据来源或显式缺口标记？
- [ ] 成稿与 Ledger 交叉比对过（无"说了没证"的漂移）？
- [ ] P0 打回项全部闭合后才 Finish？
- [ ] 可复用 SOP / 被推翻假设是否沉淀进知识库？
- [ ] 产物是否归档到 `references/` 并在 `references/results.tsv` 登记？
- [ ] 审计报告 `references/claim_audit_report.md` 是否链接了 `references/results.tsv` 与 `references/evolution-log.md`？

- [ ] Is an "out-group" reviewer designated (or at least an independent sub-agent)?
- [ ] Does each round's reviewer opinion cite the specific original location?
- [ ] Adversarial rounds ≤ 3, and each round the executor cited the comment number?
- [ ] Stages 1/2/3 executed in order, no skipping?
- [ ] Is the corresponding CHECKPOINT output each stage (CK-2 / CK-3 / CK-4)?
- [ ] Does every claim in the Claim Ledger have an evidence source or explicit gap marker?
- [ ] Did you cross-check the draft against the Ledger (no "stated without evidence" drift)?
- [ ] Finish only after all P0 rejected items are closed?
- [ ] Are reusable SOP / overturned assumptions persisted into the knowledge base?
- [ ] Are artifacts archived to `references/` and registered in `references/results.tsv`?
- [ ] Does the audit report `references/claim_audit_report.md` link `references/results.tsv` and `references/evolution-log.md`?

## Test-prompt（实测校验用） (Test-prompt — For Actual Validation)

**T1（证据缺口场景）**：`帮我写一段"本地部署 DeerFlow 比云端快 3 倍"的结论，并用 ARIS 审计审一下。`
- 预期对照：Claim Ledger 里该声明应被标 ⚠️/❌（无压测数据），reviewer 应打回 P0，Final 不得出现未证"快 3 倍"。
- 判据：若技能直接放行该结论 = 失败。
- 实际结果：见上文"测试用例与预期判据 / T1"。

**T1 (Evidence Gap Scenario)**: `帮我写一段"本地部署 DeerFlow 比云端快 3 倍"的结论，并用 ARIS 审计审一下。`
- Expected vs. actual: In the Claim Ledger this claim should be marked ⚠️/❌ (no stress-test data); reviewer should reject P0; "3x faster" must not appear unproven in Final.
- Criterion: If the skill directly passes this conclusion = failure.
- Actual result: see above "Test Cases & Expected Criteria / T1".

**T2（对抗轮次场景）**：`用异族 reviewer 审我这篇 800 字技术分析，挑出所有未证断言。`
- 预期对照：产出结构化意见（未证断言/逻辑跳跃/静默继承/反例/修订要求），且每条点名原文位置；不是泛泛"建议加强论证"。
- 判据：若 reviewer 只给笼统建议、不点名 = 失败。
- 实际结果：见上文"测试用例与预期判据 / T2"。

**T2 (Adversarial Round Scenario)**: `用异族 reviewer 审我这篇 800 字技术分析，挑出所有未证断言。`
- Expected vs. actual: produce structured opinions (unproven claims / logical leaps / silent inheritance / counterexamples / revision requirements), each citing the original location; not vague "suggest strengthening the argument."
- Criterion: If the reviewer only gives vague suggestions without citing = failure.
- Actual result: see above "Test Cases & Expected Criteria / T2".

## 来源（参考文献） (Sources — References)

- [1] [[raw/paper-aris]] — ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration（主源，三层架构 + 保证层）
- [2] [[raw/paper-skillopt]] — SkillOpt：技能作为冻结 agent 的外部状态做文本空间优化（执行层技能自进化）
- [3] [[raw/paper-seed]] — SEED：训练时技能蒸馏（自改进循环的理论近亲）
- [4] [[raw/paper-self-evolving-survey]] — 自进化 Agent 综述（四组件框架：Inputs/System/Optimisers）
- [5] [[raw/paper-voyager]] — Voyager：技能库 + 零样本迁移（可复用技能库的源头）

- [1] [[raw/paper-aris]] — ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration (primary source, three-layer architecture + assurance layer)
- [2] [[raw/paper-skillopt]] — SkillOpt: skills as frozen agents' external state for text-space optimization (execution-layer skill self-evolution)
- [3] [[raw/paper-seed]] — SEED: skill distillation at training time (theoretical cousin of the self-improvement loop)
- [4] [[raw/paper-self-evolving-survey]] — Self-Evolving Agent survey (four-component framework: Inputs/System/Optimisers)
- [5] [[raw/paper-voyager]] — Voyager: skill library + zero-shot transfer (source of reusable skill libraries)

> 注：本技能是"读论文造技能"合集的提炼产物，核心方法论源自 ARIS 论文（arXiv:2605.03042）。原始论文位于作者本地知识库（非可移植路径），本 skill 自身不依赖任何本地文件路径，可在任意 Hermes 环境直接使用。

> Note: This skill is a distilled product of the "read papers to build skills" collection; the core methodology originates from the ARIS paper (arXiv:2605.03042). The original paper is in the author's local knowledge base (non-portable path); this skill itself depends on no local file paths and can be used directly in any Hermes environment.

## 变更记录 (Changelog)

> 完整、权威的版本变更记录见 **`CHANGELOG.md`**（含 v1.0.0 → v1.5.0 逐版明细）。此处仅列最近两版摘要。
> The full, authoritative changelog lives in **`CHANGELOG.md`** (v1.0.0 → v1.5.0 details). Only the last two versions summarized here.

- **v1.5.0 (2026-09-03)** 评测驱动优化（TRACE 4.6/5 · 优秀）：① 新增 `gate` 硬闸门子命令（收口前扫描台账，未闭环即非零退出，机制性阻止带缺口发稿）；② 脚本报错改为新手可懂、带修复指引；③ 新增「受众」「自动触发条件」「步数限制与兜底」三节；④ 新增 `references/quickstart-minimal-example.md`（真实输出）/ `sample-claim-audit-report.md` / `faq.md`（坑点对照）；⑤ 补齐缺失的 `LICENSE`、修正 README 目录结构与孤儿 `CHANGELOG.md`；⑥ 回归测试 8→10 项全过。
- **v1.5.0 (2026-09-03)** Eval-driven optimization (TRACE 4.6/5 · Excellent): ① new `gate` hard-gate subcommand; ② newbie-friendly script errors with fix guidance; ③ added Audience / Auto-trigger / Step-budget sections; ④ added `references/quickstart-minimal-example.md` (real output) / `sample-claim-audit-report.md` / `faq.md`; ⑤ added missing `LICENSE`, fixed README structure and orphan `CHANGELOG.md`; ⑥ regression tests 8→10 all pass.
