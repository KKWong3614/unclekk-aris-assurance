# UncleKK ARIS 对抗式声明审计 · Adversarial Claim Audit

> 把 ARIS 论文的"保证层 + 跨模型对抗协作"提炼成可复用工作流——用异族 reviewer 挑刺 + 三阶段声明审计，治"看似成立但证据不足"的长程失败。适用于文章/报告/分析/科研草稿的质量兜底。
>
> A reusable workflow distilled from the ARIS paper's "guarantee layer + cross-model adversarial collaboration": heterologous reviewers challenge the drafts and a three-stage claim audit cures the long-horizon failure mode of "plausible but evidence-poor conclusions." Use it as a quality gate for articles, reports, analyses, and research drafts.

源自论文 ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration (arXiv 2605.03042)。 把"长程任务中最隐蔽的失败模式——看似成立但证据不足的结论"变成可执行的检查流程： (1) 对抗式编排——executor 推进，来自不同模型家族的 reviewer 审阅中间产物并要求修改； (2) 三阶段声明审计——完整性验证 → 结果到声明映射 → 声明审计，产出 claim ledger 与证据缺口报告； (3) 持久化 research wiki + 自改进循环（落地为 LLM Wiki）。 适用：写公众号长文/技术报告前兜底结论、做研究/分析怕"编得太顺"、任何需要"结论可追溯"的深度产出。 触发词：声明审计、对抗审查、证据核查、ARIS、claim audit、结论有没有证据、长文质检。

Based on the paper *ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration* (arXiv 2605.03042), this skill turns the most insidious failure mode of long-horizon tasks — conclusions that look sound but lack evidence — into an executable review flow: (1) Adversarial orchestration — an executor drives progress while reviewers from different model families examine intermediate artifacts and demand revisions; (2) Three-stage claim audit — completeness verification → result-to-claim mapping → claim audit, producing a claim ledger and an evidence-gap report; (3) Persistent research wiki + self-improvement loop (implemented as an LLM Wiki). Use it to gate conclusions before writing long-form articles or technical reports, when doing research/analysis work and fearing "fabrication that flows too smoothly," or for any deep deliverable that needs "traceable conclusions." Trigger words: 声明审计 / 对抗审查 / 证据核查 / ARIS / claim audit / 结论有没有证据 / 长文质检.

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
├── SKILL.md      # 技能主文件（含 frontmatter）
├── README.md     # 本文件
├── LICENSE       # MIT 许可证
├── references/   # 参考文档（如有）
├── scripts/      # 可执行脚本（如有）
└── templates/    # 模板（如有）
```

## 版本 Version

当前版本：`1.4.0`
Current version: `1.4.0`

## 许可证 License

[MIT](LICENSE) © 2026 KK大叔 (UncleKK)
