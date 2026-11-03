# prose

我写论文、专利、周报和给导师的邮件时，常让 Claude 起草或润色，改出来的东西经常"每句都对，合起来什么也没说"。
这个 Claude Code 技能就是为了治这个毛病写的。

它先判断你在写什么，论文、专利、周报、README 和邮件各有一套规范。
论文里该留的被动句和限定语，放进周报就是废话。去 AI 味时，它按七层查问题，从词汇、句式一直到内容和长文一致性，
并守住一条底线：不新增事实，不改数字、限定和归因，缺内容就标出来请作者补，不替作者编。

结构问题单独成了一份规则，比如一个标题下只有一句话、"从技术层面看……从应用层面看……"的切片式写法、整页的
"**标签**：内容"列表。每条规则都注明了依据：有人机对照统计的标"实测"，来自写作规范的标"规范"，只是编辑经验的标"观察"。
很多流传的"AI 特征"其实站不住，比如句长均匀、用被动、用设问，这些在中文语料里人写得一样多甚至更多，所以没有收进来。

`scripts/check_prose.py` 能扫出表面模式。命中只说明这里值得看一眼，不能拿来判断是不是 AI 写的。

写论文的部分，整体思路来自 Mensh & Kording、Gopen & Swan、Whitesides、Williams、Peyton Jones 这些人的写作方法，
用词造句的依据来自对顶刊论文的语料统计，中文部分对照了现行国标和几本核心期刊的投稿须知。具体到某本期刊、
某位导师怎么要求，通用规则写不全，所以它会给每个人建一份写作档案（默认在 `~/.claude/prose-profile/`，不在技能目录里）。
你改过它的稿子、说过"以后都这样"、指定过范文，它会记下来；同一条出现两次或者你明确要求过，才会问你要不要定成规则。
档案是普通的 Markdown 文件，随时可以打开改。这个思路借自 NeurIPS 2024 的 CIPHER（从用户修改里学习偏好）。

## 用法

把整个目录放到 `~/.claude/skills/prose`，在 Claude Code 里说"帮我润色这段""去 AI 味"之类的话就会触发。脚本也可以单独跑：

```bash
python ~/.claude/skills/prose/scripts/check_prose.py draft.md --genre academic-en
```

`--genre` 可选 academic-en、academic-zh、patent、report、technical、letter、essay。

写作档案用 `scripts/profile.py` 管理，第一次用先运行 `python ~/.claude/skills/prose/scripts/profile.py init`。

规则文件以中文为主，英文写作那几份用英文写。技能里提到的 `ieee-paper`、`report2ppt` 等是我本地的其他技能，没有的话忽略即可。

## English

A Claude Code skill for writing and revising Chinese and English prose. It picks the genre first, then diagnoses
AI-style writing on seven layers without adding facts or changing numbers, hedges, or attributions. Each rule is tagged
by evidence (measured, style guide, or editor observation). The checker script flags places to look at, not authorship.
