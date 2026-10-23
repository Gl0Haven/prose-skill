# AI 腔速查清单（中英文）

本表只管表层（词汇、句式、篇章、格式、残留）。内容层的毛病（无立场、虚假平衡、迎合、空泛论证、
编造细节）和完整的诊断改写流程见 [deai.md](deai.md)。

用法：命中不等于必须改。单个词出现一次通常没问题，密集出现才是 AI 腔。改的原则是删掉或换成具体内容，
不是换同义词。★ 标记为本人产物中多次出现或中文语料实测有区分度的条目。

## 1. 套话与填充
- 中：值得注意的是、需要指出的是、值得一提的是、综上所述★、总体而言★、综观★、总而言之、众所周知、
  不难看出、显而易见、可以清晰地看到★、不可否认、事实上（句首独立成分）、说白了★、旨在、
  扮演着……角色、至关重要、不可或缺、具有重要意义★
- 英：it is worth noting, it should be noted that, notably, importantly, crucially, in conclusion, at its core,
  when it comes to, in today's / in an era of, plays a crucial role, it goes without saying, that being said

## 2. 拔高、宣传与空泛因果
- 中：为后续……提供了基础支持★、标志着……的重要转变★、开辟了新的道路、推动了……的发展、取得了长足进步、
  赋能、闭环、底层逻辑、抓手、颠覆、重塑、生态（作比喻时）
- 英：pivotal, groundbreaking, paves the way, sheds light on, opens new avenues, holds promise,
  marks a turning point, underscores the importance, testament to, rich tapestry, evolving landscape,
  enduring legacy, transformative, has the potential to revolutionize
- 学术英文的过度宣称：demonstrates / proves / establishes / guarantees（证据不够时）、significantly（没做检验时）、
  novel / for the first time / to the best of our knowledge（重复使用）

## 3. 英文高频词（按模型年代，词表会过时）
Kobak 等对 1500 万篇 PubMed 摘要的统计：delves 28 倍、underscores 13.8 倍、showcasing 10.7 倍；
异常高频的风格词里三分之二是动词。Wikipedia 编辑社区按年代整理：
- GPT-4 时期：additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate, interplay,
  landscape, meticulously, pivotal, underscore, tapestry, testament, vibrant
- GPT-4o 时期：align with, enhance, fostering, highlighting, showcasing
- 2026 起：challenge, clearer, dependable, foster, leverage, multifaceted, practical, prioritize, quietly, steady
- 只在高密度时才提示的常用学术词：crucial, significant, comprehensive, robust, key, effective, novel, various。

## 4. 句式套路
- 先否后立★：不是 X，而是 Y / not X, but Y / It's not X, it's Y / Y rather than X。人类多否定真实存在的误解，
  AI 多否定不存在的前提。改：直接说 Y。（中文实测 R 3.4）
- 句末挂分词（英文）：", highlighting…", ", ensuring…", ", reflecting…", ", paving the way for…"（约为人类 5 倍）
- 系动词回避：serves as / stands as / represents / boasts / features 代替 is / has；中文"作为……而存在"。
- 凑三项：实际只有两项也写成三项。
- 虚假范围：from X to Y, from A to B 串连不相干的两端。
- 同义词轮换：同一事物轮流叫"模型 / 网络 / 架构"，同一动作轮流用"指出 / 表示 / 提到"。
- 译文句式★（中文实测 R 2.6–5.3）：过长前置定语、"当……时"从句、"对于……来说"、句首"然而，"、"这意味着"复述句。
- 冒号引出★：用一个空转句加冒号引出列表或结论（"核心结论先给你："）（R 3.8–9.4）。
- 拟人化的理想化比喻：数据告诉我们、结果揭示了、"智慧的导师"。

## 5. 篇章
- 维度切片★："从技术层面看……从应用层面看……从产业层面看……"、"在 A 方面……在 B 方面……"、"On the X front / From a X perspective / In terms of"。
  维度是通用格子、彼此无关、分量相同；改成按因果和主次组织（[structure.md](structure.md) 第 3 节）。
- 套路开头和结尾："随着……的快速发展""In today's fast-paced world"；"未来可期""the future looks bright"（[tone.md](tone.md)）。
- 对称收尾★：每节结尾配一句同模板总结（"……回答的是'能否 X'的问题"）。
- 复述式总结和预告式开头："本节将介绍……""如上所述……""In this section, we…"。
- 段首无指代的评论句★：段落第一句是评价（"这一点至关重要。"），却没有指明"这"指什么（R 4.4）。
- 序数词充当小标题★："第一，……第二，……"代替真正的结构（R 3.1）。
- 挑战与展望套路："尽管面临诸多挑战，……前景广阔" / Despite these challenges… Future outlook。

## 6. 格式
加粗泛滥、"**标签**：内容"式列表、emoji、标题层级过多、一个标题下只有一两句、能写成段落的内容写成表格、
英文正文标题首字母全大写（title case）、破折号当万能连接（中文实测 R 3.0；各模型差异约 40 倍）、
→ ✅ • 等符号代替文字（✅ 在 AI 文本里多 167 倍）、全半角标点混用。每万词 markdown 标记人类 8、AI 90 [实测]。

## 7. 对话与工具残留
- 聊天口吻："以下是……""希望对你有帮助""如需进一步……请告诉我"、Here are…, Certainly!, Great question!,
  I hope this helps, You're absolutely right
- 知识边界声明：截至我的知识、based on available information, not widely documented
- 工具标记：`contentReference[oaicite:0]`、`turn0search0`、`[cite: 1]`、`[span_1](start_span)`、`【85†L261-269】`、`[attached_file:1]`

## 不是 AI 痕迹（别误改）
句长与段长是否均匀、被动语态、设问与反问（人类用得更多）、句内排比、真有先后的"首先……其次"、
中文"进行 + 动词"（是文病，但不是 AI 痕迹）、完美语法、平淡文风。详见 [deai.md](deai.md) 第 4 节。

## 文体宽严
| 条目 | 学术论文 | 专利 | 汇报 / PPT | 技术文档 | 随笔 |
|---|---|---|---|---|---|
| 被动语态 | 方法与结果部分可用 | 允许 | 少用 | 少用 | 少用 |
| 限定语 | 与证据挂钩的保留 | 不用模糊限定 | 少用 | 少用 | 少用 |
| 列表 | 少用，论证写成段落 | 按法定格式 | 可以多用 | 步骤可用 | 不用 |
| 路标句（本节、首先） | 长文可用 | 按模板 | 不用 | 可用 | 不用 |
| 修辞、意象 | 不用 | 禁用 | 少用 | 不用 | 可用，但要具体 |
| 第一人称判断 | 用 we，不用 I | 禁用 | 可用 | 可用 | 可用 |
