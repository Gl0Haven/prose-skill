# 文体：技术文档（README、spec、交接、协议、提交信息、注释）

读者要照着做。好的技术文档让人不用猜：每个名词有定义，每个步骤可执行，每个数字有来源。
格式是技术文本里测得最强的 AI 信号：每万词 markdown 标记人类 8 处、AI 90 处，要点列表 3 对 28，
"✅"在 AI 文本里多 167 倍（Pangram）[实测]。

## README
顺序：它是什么（一句）→ 能做什么、不能做什么 → 怎么装、怎么跑（可复制的命令）→ 输入输出格式 →
已知限制。示例比描述有用。改了技能或代码的行为，README 同步改。

典型 AI README：emoji 小标题（🚀 Getting Started、✨ Features）、每条都是"**⚡ Blazing Fast**：……"式加粗标签加抽象好处、
标题全部首字母大写、"Contributions are welcome!"、没有一个数字、一条命令或一个限制、把计划中的功能写成已有。
- 每个形容词换成一个数字、一条命令或一个可观察的行为；标题用句首大写（sentence case）；不用 emoji 标题；
  徽章不超过 4–5 个；写一行"Limitations"；加粗只用于字面的 API 名。
- 改前：`## 🚀 Getting Started` / "Get up and running in seconds with our powerful, blazing-fast CLI!"
- 改后：`## Install`，然后 `pip install foo`、`foo run data/ --out results/  # 10k 张样例在一张 4090 上 38 s`，
  再一行"Requires Python 3.10+. Windows is untested."（数字须实测）

## spec 与给实现方的计划
- 用祈使句和确定语气（"读取 X，输出 Y"），不用"可以考虑""建议"。
- 每个符号、字段、阈值、计数都有定义和来源；计数从实际文件算出。
- 引用的函数、配置键、路径先在仓库里核对存在。
- 写清范围：允许改什么、禁止碰什么、遇到什么情况停下。
- 不用空模板小节（Overview / Goals / Non-goals / Risks / Future Work 各两条），把标题换成这份设计要回答的具体问题；没有内容的小节删掉。
- 交给 Codex 的计划同时满足 `bridge-handoff` 模板。

## 交接（handoff）
在做什么 → 当前假设 → 已改文件与关键 `file:line` → 已验证 / 未验证 → 下一步。
写给明天的自己或另一个模型，不写给领导：不渲染进度，只写状态。

## 提交信息与 PR 描述
- 首行说做了什么：祈使句、具体、50 字符以内、不加句号；正文说为什么，以及没验证什么（Beams；Linux 内核要求先写促成改动的问题）[规范]。
- 不写"更新代码""Update utils.py""修复问题"；不用 emoji；不用一串过去时的要点复述 diff（"Added…/Updated…/Improved…"）；
  "improved"后面要有度量。
- 改前："Update train.py / - Added gradient clipping / - Modified learning rate / - Improved stability"
- 改后："Clip gradient norm at 1.0 in train loop" + 空行 + "Loss went NaN around step 3k on the 4-GPU run (runs/0412).
  Clipping fixes it; lr unchanged. Not checked on the single-GPU path."
- PR 描述：先写问题和审阅者要做的决定，点名文件和计数，写清跑了什么、没跑什么；删掉空的模板小节。
  维护者对 AI 写的 PR 描述的主要抱怨是：冗长、复述代码里一眼能看到的细节、缺少理解改动所需的整体框架 [观察]。
- AI 协助的提交按项目规则标注（Linux 内核用 `Assisted-by`，AI 不得代加 `Signed-off-by`）；本机提交按全局指令加 Co-Authored-By。

## 注释与 docstring
- 注释说"为什么这样做"、单位、不变量和不显然的约束，不复述代码在做什么（`# Increment counter` 删掉）。
- 不在第一句重复类名或函数名，不写"This class will…"，用现在时（Google API 注释规范）[规范]。
- docstring 只写签名里看不出的信息：`"""Read the .mat at path; returns (N, 2, T) float32 I/Q, channel-first."""`
- `img = img / 255.0  # 传感器 8 bit；模型按 [0,1] 训练，不做 mean/std 归一化` 比 `# Normalize the image to [0, 1]` 有用。

## 风格
短句，主动语态，术语一致；列表用于步骤和并列项；不用修辞，不用形容词评价自己的代码（powerful、seamless、robust、blazing fast）；
不用 hype 和催促语气，少用"just、simple、easy"（DigitalOcean、Google 文档规范）[规范]。

## 来源
Pangram, Signs of AI writing；Wikipedia: Signs of AI writing；Chris Beams, How to Write a Git Commit Message；
Linux kernel, Submitting patches；Conventional Commits；Google developer style guide（API reference comments、headings）；
DigitalOcean docs voice and tone；Kenton Varda（via Simon Willison）、NixOS discourse、Pydantic OSS panel 关于 AI PR 描述的讨论。
