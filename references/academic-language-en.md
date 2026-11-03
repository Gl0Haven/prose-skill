# English research-article language: stance, tense, sentences, phrases

本文件管英文论文的用词造句，依据是对已发表论文的语料研究（主要是 Hyland 等人对顶刊的统计）和编辑指南。
整体写法见 [academic-method.md](academic-method.md)，英文学术文体的其他要求见 [genre-academic-en.md](genre-academic-en.md)。
证据标记：[实测] 语料统计；[规范] 教材、编辑或期刊指南；[推断] 综合判断，没有直接测量。

## 1. 立场：判断要敢下，强度和证据相称

顶级电子工程期刊（每领域影响因子前五，1965–2015，Hyland & Jiang 2016）的实际情况 [实测]：
- 每万词限定语（hedges）126、强调语（boosters）95、作者自称 86。"we"从 47 升到 71，"I"几乎为零。
  电子工程是四个领域里唯一四类立场标记都在增加的。"硬科学不用限定语"不成立。
- 最常用的限定语是 may，could 在增加；强调语以 show、must、establish、prove 为主，用在结果和证明上，不用在主观评价上。
- 二语作者限定语种类少、断言更强（Hyland & Milton 1997）；中文期刊的英文摘要比英文期刊的限定语明显少（Hu & Cao 2011）[实测]。
  所以中国作者常见的问题不是"太谨慎"，而是把中文语境里的笃定直接搬进英文。

动词强度阶梯（排序是综合判断 [推断]，各级用词有语料依据）：

| 强度 | 用词 | 什么时候用 |
|---|---|---|
| 1 | may, could, might; is consistent with; appears to | 解释机制、推广到没测过的条件 |
| 2 | suggest, indicate | 数据指向 X，但还有其他解释 |
| 3 | show, find, observe, report | 从表或图里直接读出来的结果，实证结论默认用这一级 |
| 4 | demonstrate, confirm, establish | 重复、受控或独立验证过；confirm 只在事先有预期时用 |
| 5 | prove, guarantee | 只用于定理和确定性的界，不用于准确率 |

- 限定语放在解释和推广上，强调语只放在论文真正确立的东西上（推出的界、经检验的差距）。一个论断最多一处限定。
- 结果的说服力来自名词而不是形容词：动词后面跟一个可度量的名词（error、latency、parameters、PSNR），
  比名词前面加一个褒义形容词可信。
- "significantly"只在做了统计检验时用，并写出是什么检验。

## 2. 时态和语态

各节的时态惯例 [规范]（工程类论文的分节统计还没人做过）：

| 部分 | 默认 | 说明 |
|---|---|---|
| 摘要 | 论文本身的内容和结论用现在时；叙述已完成的实验可以用过去时 | 一篇摘要内保持一种用法 |
| 引言 | 普遍事实和本文做什么用现在时；"has been widely studied"用现在完成时；某一篇前人工作用过去时 | 贡献列表用现在时 |
| 相关工作 | 某篇工作做了什么用过去时（X proposed），某方法是什么用现在时（X uses） | 同一段内保持一致 |
| 方法 | 方法的定义用现在时（The encoder maps …），实验里的具体选择用过去时（We used a batch size of 32） | |
| 实验与结果 | 跑了什么、观察到什么用过去时；表和图显示什么用现在时（Table 2 shows …） | |
| 讨论与结论 | 解释用现在时，观察用过去时，机制推测加情态动词 | |

语态按"这句话的主题是谁"选：
- 句子讲的是步骤或对象，用被动没问题（"Images were resized to 224 × 224"）。
- 句子讲的是作者的选择、主张或结果，用"we"或者让方法本身作主语（"The module reduces latency by …"）。
- 实测：科学论文里被动小句约占 30%，近三成集中在方法部分；要求作者多用主动的期刊，被动比例是 26%，不要求的是 34%（Leong 2014）。
  "is shown in Fig.""can be noted that"这类被动词块在电子工程论文里大幅减少；中国作者比英语母语作者更多用被动词块（Pan 等 2016）[实测]。

## 3. 句子构造与衔接

- **名词短语压缩是学术英语的常态**：复杂度来自名词短语内部的修饰语，不来自从句链（Biber & Gray 2010）[实测]。
  中国作者偏爱动词和从句框架，母语作者偏爱名词和介词框架（"the effect of X on Y""as a function of"）[实测]。
  句子是"动词 + that 从句 + 动词短语"的形状时，试试名词化写法；但压缩到读者看不出修饰关系时，补介词或拆开。
- **旧信息在前，新信息在后**（Gopen & Swan）：句首放上文已出现的对象（数据集、基线），句尾放数字或新事实。
  句子不要以"in this paper""as shown above"这种弱尾巴收束。
- **"this + 名词"**：前一句很长、"this"指整个命题时，写"This result""This gap""This non-smoothness"，不写光秃秃的"This is"。
  后面的名词同时也是一次评价 [规范，有实测依据]。
- **连接副词要节制**：中国博士生的连接副词总量多于已发表论文，33 个过度使用、25 个使用不足，集中依赖少数几个，转折类问题最大（Lei 2012）[实测]。
  2015 年电子工程顶刊每万词句首 However 4.8 次、Thus 4.3 次，是四个领域里最少的 [实测]。
  做法：每段最多一个附加类连接词（Moreover / Furthermore / In addition）；按逻辑关系选连接词；下一句已经用共享名词开头时，连接词可以省掉。
  Additionally 和 notably 同时也是大模型高频词。
- **句长**：没有研究给出工程论文的最佳句长 [缺口]。编辑指南的经验线是超过两个主句或 25 词就考虑拆开；摘要的可读性测试只当烟雾报警器用。
  摘要可读性 130 年来持续下降（70 万篇摘要，Plavén-Sigray 等 2017）[实测]，增长的主要是通用科学行话。
- **宣传词和大模型高频词**：PubMed 摘要里 novel、robust、innovative、unprecedented 等褒义词从约 2% 升到 17.5%（Vinkers 2015）；
  2024 年 delves 是基线的 28 倍、underscores 13.8 倍、showcasing 10.7 倍（Kobak 2025）；arXiv CS 摘要里 realm、intricate、showcasing、pivotal 在 2023 年后急升（Liang 2024）[实测]。
  审稿人可能把这些词读成机器润色的痕迹。换成普通动词或数字。

## 4. 中国作者的常见问题

有实测的只有三类：词块结构偏动词和从句、连接副词过量、断言过强。其余来自编辑服务的经验 [规范]，
"the proposed method""respectively""It can be seen"是否被中国作者过度使用，没有找到测量 [推断]。

| 问题 | 改法 | 例（构造） |
|---|---|---|
| 冠词缺失或误用 | the 指特定或已提及；a/an 首次提到的可数单数；泛指复数和不可数不加 | "We feed image into network" → "We feed the image into the network" |
| 可数性 | data、evidence、information、research、equipment、feedback 不加 s | "Many researches show the datas" → "Many studies show that the data" |
| 话题—评论语序，结论在后 | 先给结论或目的，再补背景 | "For denoising, many methods…, so we estimate it" → "We estimate the noise level, which most denoising methods assume to be known." |
| 主语缺失 | 补主语，或用被动让对象作主语 | "Is trained for 90 epochs" → "The network is trained for 90 epochs" |
| 解释部分用被动 | 解释和主张用主动 | "It is suggested by the results that…" → "The results suggest that the module helps, but only on small objects." |
| 段内时态漂移 | 按第 2 节，一种功能一种时态 | "Smith et al. [3] propose… The model achieved…" → "Smith et al. [3] proposed a transformer that achieved…" |
| 悬垂修饰语 | 引导短语后的第一个名词必须是它的施动者 | "Using Adam, the learning rate was set to 1e-4" → "Using Adam, we set the learning rate to 1e-4" |
| 连串并列、逗号连接两个句子 | 一句一个意思，用句号或 so | "The model is small, it runs in real time, therefore…, moreover…" → 拆成两句 |
| 同义词成对、空名词 | 删掉成对词中的一个 | "help and assist in the improvement of" → "improves" |
| It can be seen from Fig. 3 that | 直接说图显示了什么 | → "Fig. 3 shows that …" |
| 反复的 the proposed method 而没有数字 | 给方法起名，之后用名字；写出比较的量 | → "X lowers the mean error from 4.1 to 3.6 relative to the strongest baseline" |
| respectively 误用 | 只在两个有序列表一一对应且相邻时用 | "Accuracy is 91.2% respectively on CIFAR-10" → 去掉 respectively |
| which / that | 限制性用 that 不加逗号；非限制性用 ", which" | |
| 过度断言 | 换成度量 | "completely solves overfitting" → "reduces the train–test gap from 9.0 to 2.3 points" |

自查顺序（每句朗读时依次问）：施动者是不是语法主语？主张是不是在第一个分句里？可数名词标了没有？这一段是否用了不止一个连接词？
是不是一个数字或一个具名对象在承担说服？

## 5. 按功能组织的表达（选用，不照抄）

组织方式参照 Manchester Academic Phrasebank 的功能分区。原则：右栏的写法不是"错"，而是信息量低、被过度使用或带宣传色彩。
标记：[L2] 二语作者常见，[LLM] 大模型高频词表上有，[HYPE] 有实测上升的宣传词。X 方法，Y 数值，D 数据集，T 任务。

| 功能 | 推荐 | 少用 |
|---|---|---|
| 背景 | T underlies [具体应用]: [一个带数字或标准的事实]。 / [应用] requires T at Y latency. / T is difficult because [具体原因]. | In recent years, T has attracted more and more attention. [L2]；T plays a pivotal/crucial role. [LLM]；In the realm of T [LLM] |
| 缺口 | Methods in group A assume [条件]; this fails when [情形]. / It remains unclear whether … / To our knowledge, no prior method handles [情形] without [代价].（检索之后才写） | Existing methods still have many shortcomings. [L2]；There is no research on …（绝对化）；cannot well solve [L2] |
| 目的与贡献 | We address [问题] by [机制]. / X differs from [最接近的前人工作] in [一点]. / 贡献逐条写成可检验的陈述，每条带证据名词（一个界、一个数据集、一组消融） | we propose a novel and effective … [HYPE][L2]；We delve into … [LLM]；a comprehensive framework that showcases … [LLM] |
| 方法 | We use [组件] to [功能]. / The encoder maps x to z ∈ R^d.（定义用现在时） / We follow the protocol of [12]. | It is worth noting that …；The proposed method is composed of …（重复）；非顺序内容用 Firstly/Secondly |
| 结果 | X achieves Y on D, compared with Y0 for the strongest baseline. / Table 2 shows … / Removing the module lowers Y by Z. | significantly outperforms（没有检验）；demonstrate the superiority of [HYPE]；remarkable/impressive performance [HYPE][L2]；fully prove |
| 比较 | Compared with B, X reduces error by Y at equal parameters. / X matches B on D1 but trails it on D2. / Under the same training budget and data, … | our method is the best [L2]；surpasses all state-of-the-art methods；Under the premise of … [L2] |
| 局限 | X was tested only on D; whether it holds for [其他领域] remains open. / The gain disappears when [条件]. / We did not evaluate [方面]. | Our method has some limitations.（没内容）[L2]；Due to the limit of space [L2] |
| 意义与结论 | These results suggest that [与数据相称的结论]. / A practical consequence is that [部署层面的事实]. / Future work could test whether … | underscore the pivotal importance of [LLM]；opens a new era [HYPE]；provides valuable insights for the community；we will further study more deeply [L2] |
| 衔接 | However / In contrast / Instead（转折）；Therefore / As a result（因果）；For example / In particular（举例）；This + 名词 | 连用 Moreover / Furthermore / In addition / Additionally；Besides [L2]；It is noteworthy that；Last but not least |

参考书各自的用处：Phrasebank 适合按功能查表达，但跨学科、容易诱导照抄；Swales & Feak《Academic Writing for Graduate Students》讲 move 分析和数据评述；
Glasman-Deal《Science Research Writing》从范文反推每节的语法和词汇，正适合配合本技能的范文卡片；Wallwork 的书基于审稿退稿意见和约 6000 篇非母语论文的错误，适合句子层面修补。

## 来源
- Hyland & Jiang 2016, 2017, 2018（顶刊立场、自称、连接、词块的历时语料）；Hyland & Milton 1997；Hu & Cao 2011；Lei 2012；Gao 2016
- Pan, Reppen & Biber 2016（中国电信领域作者的词块）；Bychkovska & Lee 2017；Biber & Gray 2010；Leong 2014（被动比例）
- Plavén-Sigray et al. 2017（eLife，摘要可读性）；Vinkers et al. 2015（BMJ）；Kobak et al. 2025（Sci. Adv.）；Liang et al. 2024
- Gopen & Swan 1990；Swales & Feak；Glasman-Deal；Wallwork；Manchester Academic Phrasebank；IEEE Author Center；EditorWorld、Elsevier、AJE 语言编辑指南
