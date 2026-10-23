# 文体：信函（邮件、cover letter、审稿回复）

读者读第一段就决定要不要认真读下去。第一句说事，第二句说你需要对方做什么。

## 邮件（导师、合作者、编辑、甲方）
- 主题行 = 事由 + 动作 + 时限，日后能搜到（"[请审阅] TIFS 修回稿，周五前"；"【周报】频域分支 Rank-1 +4.1，需您定是否追加 MSMT17"）。
- 开门见山（BLUF）：问候之后的一两句就是请求或答案，不铺垫"打扰您了"（MIT CommLab）[规范]。
- 一封邮件只办一件事；正文不超过两段，更长的内容考虑约个会 [规范]。多件事才分条编号。
- 结尾写清谁在什么时候做什么，而不是"如有问题随时联系"。附件在正文里点名。
- 每一句感谢或道歉都对应一件具体的事，各一句就够。

### 典型 AI 邮件
- 套话开头和结尾：I hope this message finds you well；I wanted to reach out；Please don't hesitate to reach out；
  Thank you so much for your time and consideration [观察，Wikipedia 把前两种与 "Best regards" 一起列为粘贴信件的特征]。
- 刻意热情（thrilled to）、空泛大词（fostering a strong sense of community）、凑三项、格式过于整齐、没有一处只有写信人才知道的细节 [观察]。
- 收件人判断邮件是 AI 写的，主要因为"过于正式或机械"（59%）和"用词不自然"（50%）[转引的调查，未核实]。
- 单独出现一个套话不说明问题，几种同时出现才是信号。

### 中文邮件的分寸
中文商务和师生邮件里，称呼、问候、落款是礼仪，删光反而失礼（2026 年还有学生邮件"无称呼无落款"引发的讨论）。
保留一个称呼、一句与具体事项挂钩的感谢、一个简单落款；删掉的是"打扰了、万分感谢、不胜感激、祝您工作顺利身体健康"这类连串堆叠。

- 改前："尊敬的老师，您好！打扰您了。我是您的学生 XX，希望您最近一切顺利。想和您汇报一下我最近的研究进展，取得了一些阶段性成果，
  具体内容见附件。如有任何问题，请随时联系我，万分感谢您的指导，祝您工作顺利、身体健康！"
- 改后（数字示意）："X 老师好，频域分支在 val 上 Rank-1 从 63.5% 提到 67.6%（三个 seed 的均值，见附件表 1），遮挡子集没有增益。
  请您在周四组会前定：是否追加 MSMT17 验证（我倾向追加，约 2 天 GPU）。其余细节见附件。 XX"
- English before: "I hope this email finds you well. I wanted to reach out regarding the dataset. Please don't hesitate to reach out
  if you have any questions." After: "Could you confirm by Friday whether we can use split B for the final table?
  The split-A numbers are attached; split B changes Rank-1 by 0.3 points."
- 英文称呼：Dear Prof. X / Dear Editor；结尾 Best regards 可以用，前面不要再堆一句客套。

## Cover letter
三段：投什么、为什么适合这本刊（对应期刊的 aims and scope）、核心贡献与证据（两三句，带数字）。
加上必需的声明（原创、未一稿多投、利益冲突）。不复述摘要，不自夸，不用 thrilled / excited。

## 审稿回复
逐点回复交 `nature-response`。语言要求：
- 每条先概括审稿人的关切，再回答，再指出改动位置（页、行、节）。
- 同意就直接改并说明改了什么；不同意要给证据，语气平和，不争辩、不讨好。
- 感谢只在开头说一次，不在每条前面重复"感谢审稿人的宝贵意见"；不写"You are absolutely right"。
- 回复里的数字和正文、图表一致；审稿回复里的限定和否定措辞一字不随意改动。
