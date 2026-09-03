# UncleKK ARIS 对抗式声明审计 · Adversarial Claim Audit

> 把 ARIS 论文的"保证层 + 跨模型对抗协作"提炼成可复用工作流——用异族 reviewer 挑刺 + 三阶段声明审计，治"看似成立但证据不足"的长程失败。适用于文章/报告/分析/科研草稿的质量兜底。
>
> A reusable workflow distilled from the ARIS paper's "guarantee layer + cross-model adversarial collaboration": heterologous reviewers challenge the drafts and a three-stage claim audit cures the long-horizon failure mode of "plausible but evidence-poor conclusions." Use it as a quality gate for articles, reports, analyses, and research drafts.

源自论文 ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration (arXiv 2605.03042)。 把"长程任务中最隐蔽的失败模式——看似成立但证据不足的结论"变成可执行的检查流程。 触发词：声明审计、对抗审查、证据核查、ARIS、claim audit、结论有没有证据、长文质检。

Based on the paper *ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration* (arXiv 2605.03042), this skill turns the most insidious failure mode of long-horizon tasks — conclusions that look sound but lack evidence — into an executable review flow. Trigger words: 声明审计 / 对抗审查 / 证据核查 / ARIS / claim audit / 结论有没有证据 / 长文质检.

## 受众 Audience

面向**所有 Agent 用户**，从新手到专业：

- **新手**：照 `references/quickstart-minimal-example.md` 三步跑通脚本，先建立"每个结论都要有证据"的直觉。
- **进阶**：用异族 reviewer 子 agent 跑完整对抗审查，处理复杂格式与边界。
- **专业**：把本技能嵌入团队发布流程，配合 `wiki/research/` 做跨次经验沉淀与自改进。

For **all Agent users**, from novice to professional (see `../SKILL.md` "受众 Audience" for the full scope).

## 安装 Installation

将此技能克隆到你的 WorkBuddy 技能目录：
Clone this skill into your WorkBuddy skills directory:

```bash
git clone https://github.com/KKWong3614/unclekk-aris-assurance.git "$HOME/.workbuddy/skills/unclekk-aris-assurance"
```

或下载 Release 中的 zip，解压到技能目录即可。
Or download the zip from the Release and extract it into your skills directory.

## 目录结构 Directory Structure

```
unclekk-aris-assurance/
├── SKILL.md                           # 技能主文件（含 frontmatter 与完整方法论）
├── README.md                         # 本文件
├── LICENSE                           # MIT 许可证
├── CHANGELOG.md                      # 版本变更记录（权威）
├── pyproject.toml                    # 分发元数据
├── _meta.json                        # 平台元数据（含 version）
├── scripts/
│   ├── aris_audit.py                 # 前置自审脚本（extract / drift / gate 三子命令）
│   └── test_aris_audit.py            # 回归测试（18/18 passed）
└── references/
    ├── README.md                     # 本目录说明与文件清单
    ├── evolution-log.md              # 技能演进历史与决策记录
    ├── quickstart-minimal-example.md # 最小可运行示例（真实输出）
    ├── sample-claim-audit-report.md  # 审计报告成品样例
    ├── faq.md                        # 常见问题与坑点对照
    ├── example-draft.md              # 示例草稿（extract 输入）
    ├── example-final.md              # 示例成稿（drift 输入）
    ├── example-ledger.md             # extract 产物（未闭环）
    ├── example-ledger-closed.md      # 已闭环台账样例（gate 通过）
    └── example-drift.md              # drift 产物
```

> 注：`integrity_checklist.md` / `claim_ledger.md` / `claim_audit_report.md` / `results.tsv` 是**每次审计运行时**在 `references/` 下生成的产物，不在仓库里预置。
> Note: `integrity_checklist.md` / `claim_ledger.md` / `claim_audit_report.md` / `results.tsv` are **generated at audit runtime** under `references/`; they are not pre-shipped in the repo.

## 最小运行 Minimal Run

```bash
python scripts/aris_audit.py extract --draft references/example-draft.md --output references/example-ledger.md
python scripts/aris_audit.py drift   --draft references/example-final.md  --ledger references/example-ledger.md --output references/example-drift.md
python scripts/aris_audit.py gate    --ledger references/example-ledger.md   # 未闭环 -> 非零退出
```

详见 `references/quickstart-minimal-example.md`。
See `references/quickstart-minimal-example.md` for the full walkthrough with real output.

## 版本 Version

当前版本：`1.6.0`
Current version: `1.6.0`

> v1.6.0 重点提升 Reliability：统一错误码+退出码分级（2/3/4/7/10）、表格/加粗声明识别、`--json`/`--mark`/`--threshold`/`--max-bytes` 选项、5MB 大文件保护。回归测试 16/16 全过。
> v1.6.0 focuses on Reliability: unified error codes + exit-code tiers (2/3/4/7/10), table/bold claim recognition, `--json`/`--mark`/`--threshold`/`--max-bytes` options, 5MB file-size guard. 16/16 regression tests pass.

## 许可证 License

[MIT](LICENSE) © 2026 KK大叔 (UncleKK)
