# prose

prose 是一个 Claude Code 技能，用于中英文文稿的起草、改写和审阅。它先判定文体，再按该文体的规范写作；
处理 AI 起草的稿件时，它按分层诊断去除 AI 写作痕迹，同时保证事实、数字、限定和归因不变。
技能还为每位使用者维护一份写作档案，从使用者的修改和反馈中积累个人与期刊层面的写作偏好。

## 功能

### 分文体写作

技能覆盖七类文体，每类有独立的规范文件，中英文分别有语言层规范。

| 文体 | 典型文稿 | 规范文件 |
|---|---|---|
| 英文学术 | 期刊与会议论文、摘要、rebuttal | `genre-academic-en.md`、`academic-language-en.md` |
| 中文学术 | 期刊论文、学位论文、综述、开题报告 | `genre-academic-zh.md` |
| 专利 | 说明书、权利要求书、交底书 | `genre-patent.md` |
| 汇报 | 幻灯片文字、周报、组会材料 | `genre-report.md` |
| 技术文档 | README、设计文档、交接说明、提交信息、注释 | `genre-technical.md` |
| 信函 | 邮件、cover letter、审稿回复 | `genre-letter.md` |
| 随笔与科普 | 博客、科普文章、序言、个人陈述 | `genre-essay.md` |

### 期刊论文写作

`academic-method.md` 给出期刊论文的整体写法，中英文论文通用，内容包括：
- 核心贡献的确定；
- 引言的"共识背景、带代价的缺口、本文回答"结构；
- 写作与修改顺序；
- 各部分的职能；
- Nature 系、IEEE Transactions 与 CVPR 类会议的差异；
- 投稿前自查清单。

该部分综合了 Mensh & Kording、Gopen & Swan、Whitesides、Williams、Peyton Jones、Widom、Freeman、Lipton & Steinhardt 等人的写作方法。

`academic-language-en.md` 处理英文论文的用词造句，内容包括：
- 论断强度与证据的匹配；
- 各节的时态与语态；
- 句子构造与衔接；
- 中国作者的常见问题；
- 按功能组织的表达对照。

该部分依据 Hyland 等人对顶级期刊的语料统计。

中文部分对照现行国家标准（GB/T 7713.2—2022、GB/T 7713.1—2006、GB/T 6447—2025）和《计算机学报》《软件学报》《自动化学报》《电子与信息学报》等期刊的投稿须知。

### 去 AI 味

使用者要求"去 AI 味""降 AI 率"或审阅 AI 起草的稿件时，技能进入专门流程（`deai.md`）。
- 诊断：从词汇、句式、篇章与结构、内容、格式、残留、长文一致性七个层面查找问题。
- 交付：提供三种模式，分别是红笔报告、改写、只改指定问题类型。
- 专项规则：标题与段落结构（`structure.md`），开头、结尾、语气、比喻与量化（`tone.md`），起草阶段的预防与改后评价方法（`prevention.md`）。
- 硬性边界：不新增事实，不改动数字、限定语和归因；内容缺失处标注请作者补充，不代为编造。
- 去 AI 味与 AIGC 检测分数是两回事。技能不使用同义词替换、故意错字、来回翻译等降低检测分数的手段。

### 写作档案

通用规范无法覆盖每位作者、每本期刊和每位导师的具体要求，这部分由写作档案在使用中积累（`learning.md`）。
- 存放：档案默认位于 `~/.claude/prose-profile/`，与技能目录分离，个人内容不会随技能一起分享。
- 起草前：技能读取与当前文体、期刊、章节相符的规则、期刊卡片、范文结构卡片和作者本人的样稿。
- 交付后：技能从使用者的修改、导师与审稿意见以及明确指示中归纳偏好，先记为候选观察。同一观察在两篇不同文稿中出现，或使用者明确要求过，才询问是否升为规则。
- 学习期刊或范文：使用者指定期刊或范文后，技能按模板建立期刊卡片和范文结构卡片。卡片只记录结构和写法要点，不保存原文。
- 编辑与维护：档案为普通 Markdown 文件，可直接编辑；每次写入前自动备份。

该机制参考了 CIPHER（Gao 等，NeurIPS 2024，arXiv:2404.15269）从用户修改中推断偏好的方法，晋升门槛参考了 self-learning-skills（MIT）。

### 检查脚本

`scripts/check_prose.py` 按内容、结构、AI 痕迹、文体、排版、可读性六组报告可疑位置。
- 结构：一句话小节、标题过密、维度切片式行文。
- AI 痕迹：先否后立句式、背景式开头、升华式结尾。
- 排版：中文里混用半角标点、中英文之间的空格不统一。
- 文体专项：周报套话、README 宣传用语、论文图题下结论等。

命中项只提示需要人工判断的位置，不作为文稿由 AI 生成的证据。

## 安装

将本仓库克隆到 Claude Code 的技能目录。

```bash
git clone https://github.com/Gl0Haven/prose-skill ~/.claude/skills/prose
```

脚本只依赖 Python 3.8 及以上的标准库；读取 `.docx` 时需要额外安装 `python-docx`。

## 使用

在 Claude Code 中提出写作或改写请求即可触发，例如"润色这段引言""把这封邮件改得简洁一些""检查这篇稿子的 AI 痕迹"。
首次使用写作档案前，先运行初始化命令。

```bash
python ~/.claude/skills/prose/scripts/profile.py init
```

常用命令如下表。

| 命令 | 作用 |
|---|---|
| `check_prose.py FILE --genre G` | 检查文稿，G 为 academic-en、academic-zh、patent、report、technical、letter、essay 之一 |
| `profile.py context --genre G --venue V --section S --lang L` | 列出当前写作任务适用的规则、期刊卡片、范文卡片和样稿 |
| `profile.py diff DRAFT FINAL` | 列出初稿与定稿之间改动的句子，供归纳偏好 |
| `profile.py observe` / `promote` / `retire` | 记录观察、升为规则、停用规则 |
| `profile.py stats FILE ...` | 统计作者本人文字的句长、段长、人称、限定语等习惯 |
| `profile.py list` | 查看档案概况和待确认条目 |

档案位置可用环境变量 `PROSE_PROFILE_DIR` 修改。

## 目录结构

```
prose/
├── SKILL.md                 技能入口：文体判定、写作步骤、档案读写时机
├── references/              各文体、语言层、去 AI 味、论文写作和学习机制的规范
├── scripts/
│   ├── check_prose.py       文稿检查
│   └── profile.py           写作档案管理
└── profile-template/        写作档案的初始模板
```

## 依据与局限

规范文件中的每条规则都标注了依据类型：
- "实测"：有人机对照统计或语料研究；
- "规范"：来自写作指南、期刊或国家标准的明文；
- "观察"：编辑经验或综合判断，尚无测量支持。

部分流传较广的"AI 特征"在语料中不成立，因此未被收录，例如句长均匀、使用被动语态、使用设问。

已知局限：
- 期刊要求会更新，具体篇幅与格式以目标期刊当前的作者指南为准。
- 检查脚本基于表面模式，无法判断立场、证据和论证质量。
- 写作档案的学习效果取决于使用者提供修改和反馈的频率。

规则文件以中文为主，英文写作相关的文件使用英文。技能中提到的 `ieee-paper`、`journal-paper-revision`、`nature-writing`、`report2ppt` 等为配套技能，未安装时可忽略。

## English summary

prose is a Claude Code skill for drafting, revising and reviewing Chinese and English documents. It identifies the genre
first and applies the rules for that genre. Supported genres are academic papers, patents, reports, technical documents,
letters and essays.
Its journal-writing guidance synthesizes established methods (Mensh & Kording, Gopen & Swan, Whitesides, Williams,
Peyton Jones) with corpus studies of research articles and current Chinese national standards. A de-AI workflow
diagnoses AI-style writing on seven layers without adding facts or changing numbers, hedges or attributions. A per-writer
profile, stored outside the skill directory, learns preferences from the writer's edits and feedback. A preference becomes
a rule only after it recurs or the writer confirms it. Every rule is tagged by its evidence: measured, style guide,
or editorial observation.
