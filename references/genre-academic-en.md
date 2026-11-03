# Genre: English academic writing

Readers: reviewers and specialists who skim first and judge fast. They want the
contribution, the evidence, and the boundary, in that order. Workflow, venue rules,
LaTeX checks, and claim-evidence mapping live in `ieee-paper` and
`journal-paper-revision`; Nature-family drafting in `nature-writing` / `nature-polishing`.
This file sets the prose standard those skills assume.

Read with it: [academic-method.md](academic-method.md) for the whole-paper approach (one contribution,
the context → gap → answer arc, writing order, what each section does, venue differences), and
[academic-language-en.md](academic-language-en.md) for stance, tense, sentence construction, Chinese-L1
issues and the function-organised phrase table. Before drafting, run `profile.py context` (see
[learning.md](learning.md)) to load the writer's own rules, venue card and exemplar cards.

## Voice
Formal, precise, direct. No contractions, no first-person singular, no rhetorical
questions. Use active "we" for the authors' choices, claims and results: in top EE journals
"we" rose from 47 to 71 per 10k words between 1965 and 2015 [M]. Passive is fine for routine
procedure where the actor is irrelevant (methods, setup).

## Each section has one job
- Abstract: context → gap → mechanism → strongest measured result with its protocol → meaning and boundary. No citations, no unsupported novelty.
- Introduction: shared context → gap with its cost → the core idea → evidence summary → refutable contributions with section pointers.
- Related work: grouped by family and by limitation, not a list of summaries. Each group ends on the assumption this work relaxes.
- Method: intuition and a small example before the general formalism; reproducible; give the design rationale where a reader would ask "why this choice".
- Results: ordered by the argument; each paragraph opens with a question and ends with its answer; isolate the source of the gain (ablation, error analysis); report failures.
- Conclusion: contribution, key evidence, boundary. No new claims, no future-work wish list.
Details and sources for each are in academic-method.md section 3.

## Claims
- Match the verb to the evidence (see `journal-paper-revision` claim calibration).
- Numbers in text, tables, captions, and abstract come from one source and match the code and configs.
- Quoted results from other papers are reference rows, not same-protocol comparisons; say so.
- Modest gains get plain magnitudes: "improves CER by 0.25 points", not "significantly improves".
- State limitations that bound the claims, not unrelated weaknesses.

## Paragraph craft
- Topic sentence carries the claim; the rest is evidence. If the claim is in the last sentence, move it up.
- Link sentences by repeating the key term at the start of the next sentence (old → new), not with "Furthermore".
- One paragraph, one point, typically 4–8 sentences.

## Titles
- State the method or the result in plain nouns. Nature Portfolio: 15 words or fewer, no punctuation or puns [G].
  IEEE titles follow the venue template; still drop words the paper does not measure.
- AI tells: "X: A Novel Framework for Y", "Towards …", "Unlocking the Power of …", "Rethinking …: A Comprehensive …",
  "Leveraging … for Enhanced …". In one small study, ChatGPT-4.0 titles had colons in 100% of cases vs 30% of human titles,
  and were longer (median 16 vs 12.5 words) [M, n=50]. The template phrases themselves are unmeasured [A].
- Before: "DeepSig: A Novel Transformer-Based Framework for Robust and Efficient Modulation Recognition".
  After: "Modulation recognition with a 0.4M-parameter transformer under 5 dB SNR".
- Before: "Towards Unlocking the Potential of Frequency Cues for Deepfake Detection".
  After: "Frequency-domain cues improve cross-dataset deepfake detection".

## Abstracts
- The frame to break: "In this paper, we propose a novel framework, XNet, for robust Y. Specifically, we introduce A and B.
  Extensive experiments on three benchmark datasets demonstrate that XNet significantly outperforms state-of-the-art methods,
  paving the way for future research." Each slot is common in pre-LLM ML abstracts; the tell is every slot filled with no number.
- Replace with: problem with a number → what was done → the single strongest result with a number and a named baseline → one honest limit.
  "Cross-dataset accuracy of Y drops by 18 points when training and test devices differ. We replace the shared backbone with
  per-device normalization … On 4 held-out devices, accuracy rises from 71.3% to 82.6% (3 seeds, s.d. 0.4); gains vanish below 10 dB SNR."
- Delete "novel" (Nature: "We report a mechanism", not "a novel mechanism"), "extensive", "significantly" without a test,
  "state-of-the-art" without a named baseline, "paving the way". Post-2022 abstract vocabulary shift includes
  across, additionally, comprehensive, crucial, enhancing, insights, notably, particularly [M]; these are density signals only.
- Venue limits: Nature Communications ≤150 words, no references or abbreviations, final sentence "Here we show …" in present tense [G];
  IEEE 150–250 words, one paragraph, no equations, self-contained (verify in the current Author Center) [G].

## Keywords
3–4 distinct terms (IEEE: from the IEEE Thesaurus, alphabetical; verify) naming task, modality, method family, data type.
Not 8–12 broad words ("deep learning, framework, performance") that repeat the title.

## Figure and table captions
- Describe, do not advertise. A caption gives a short standalone title, what each panel shows, n, what bars and error bars mean,
  and the symbol key in words (Nature: "blue circles", not a symbol; avoid "top/left") [G]. A summary sentence of the key finding
  is allowed by some guides (Caltech), so make it a measured fact, not an adjective.
- AI tells: "Performance comparison … clearly demonstrating the superiority of our approach"; "Comprehensive ablation study
  showcasing the crucial role of each component"; "Visualization results. Our method produces cleaner …" [A].
- After: "Figure 3. Top-1 accuracy on held-out devices. a, Per-dataset accuracy; bars show the mean of three seeds, error bars s.d.
  b, Accuracy against SNR; shaded bands show min to max over seeds. Blue circles, proposed; grey squares, ResNet-18 baseline."
- After: "TABLE II. Ablation on the validation split. Each row removes one component; other settings fixed. Mean accuracy (%) over three seeds."
- Keep the claim in Results ("Removing the fusion module lowers accuracy by 4.1 points (Table II)"), where it can cite evidence.
- IEEE: "Fig. 1." below the figure; table captions above, Roman numerals.

## Forbidden in this genre
Buzzwords (delve, leverage, showcase, crucial, seamless, comprehensive, notably, moreover as filler),
negative parallelisms, rule-of-three padding, em-dash chains, prose semicolons (IEEE), title-case
headings where the venue uses sentence case, summary sentences at the end of every paragraph.
