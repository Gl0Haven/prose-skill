# English language layer

Readers process English sentences by position. Put what they already know first and the
new, important information last; give each sentence one clear subject and an active verb.
Most fixes follow from that.

## Position (Gopen & Swan, "The Science of Scientific Writing")
- Topic position (sentence start): the old information that links back to what came before.
- Stress position (sentence end): the new information you want emphasized.
- Keep grammatical subject and its verb close; do not bury the verb after a 20-word subject.
- One sentence, one main point. A sentence that needs two stress positions should be two sentences.

## Verbs over nouns
Turn nominalizations back into verbs.
- "performed an analysis of" → "analyzed"; "achieved an improvement in" → "improved"
- "is dependent on" → "depends on"; "make a comparison" → "compare"
Prefer a concrete verb to "is / has / provides / enables / allows" when one exists.

## Concision (Orwell, Strunk)
- Cut words that do not change the meaning: "in order to" → "to", "due to the fact that" → "because",
  "a large number of" → "many", "it is important to note that" → delete.
- Never use a long word where a short one will do; never use jargon where plain English is exact.
- If a sentence survives deletion of a word, delete it.

## Voice
Active voice by default in general prose. In academic methods and results sections the
passive is acceptable when the actor is obvious or irrelevant ("The images were cropped
to 256 × 256"); follow `journal-paper-revision`, which sets IEEE style to passive-leaning.
Do not use passive to hide who made a claim or a decision.

## Hedging and claims
Calibrate, do not decorate. One hedge per claim at most, placed where the uncertainty is.
- Overclaim: "proves", "clearly demonstrates", "guarantees", "significantly" (without a test)
- Over-hedge: "may possibly suggest", "could potentially"
- Calibrated: "suggests", "is consistent with", "under the evaluated protocol"

## Paragraphs
Open with the point; end where the point is made. Do not close every paragraph with a
summary sentence. Vary paragraph length with content.

## Parallelism and lists
Parallel items take the same grammatical form. Use a list only for items that are truly
parallel and that readers will scan; arguments belong in prose.

## Word choice
- Same thing, same word. Elegant variation ("the model… the network… the architecture…" for one object) confuses.
- Prefer specific nouns: "three datasets" over "various datasets".
- Avoid intensifiers and empty adverbs: very, really, highly, extremely, truly, essentially.

## Punctuation
- No em-dash as a universal connector; use a comma, colon, parentheses, or a new sentence. At most one dash pair per paragraph;
  in IEEE/Nature prose default to commas and parentheses. Rates are model-specific (per 1,000 words: GPT-4.1 10.6,
  Claude Opus 4.6 9.1, DeepSeek V3 7.0, Gemini 2.5 Pro 3.5, GPT-5.4 1.4; human essays 0.3–17, mean 3.2) [M, single-author preprint],
  and newer models avoid dashes, so dash-free comma-and-period monotony is becoming its own sign. Spaced dashes ("works — mostly")
  break Microsoft/Chicago style.
- Colons: no colon at the end of a heading or before a figure, table, or code block; before a list only when the lead-in
  refers to it ("the following"). No empty lead-in sentence plus colon.
- Exclamation marks: almost never in formal writing.
- Quotes and invisible characters: curly vs straight quotes prove nothing on their own (Word and macOS make curly quotes).
  Before submitting LaTeX, code, or patent text, grep for U+2018/2019/201C/201D, U+00A0 and U+202F (narrow no-break space,
  seen in some OpenAI outputs) and replace U+202F with a normal space, never delete it. Keep intentional ties (`Fig.~\ref`).
- No →, ✅, or • in running prose; use words and real list syntax.
- Headings: sentence case unless the venue says otherwise; no emoji.
- Semicolons: in IEEE manuscripts, none in prose (see `journal-paper-revision`). Elsewhere, sparingly.
- No contractions in academic and formal writing.

## Chinglish and LLM-ese (for Chinese authors writing English)
- Chinglish openers and connectors: "With the development of X, …", "In recent years, … has attracted more and more attention",
  "play an important role in", "Firstly/Secondly/Finally" chains, "so … therefore", "although … but", "it can be seen that".
- Topic-comment sentences ("As for the dataset, it is collected …"), comma splices, missing or extra articles,
  light verb + noun ("carry out analysis", "put forward a method", "obtain good effect").
- LLM-ese on top: delve/crucial/testament vocabulary, inflated register, symmetric triplets, flatter syntax than a human translator.
- Fixes: S-V-O with the agent as subject; known information first, new information last; one idea per sentence; real verbs;
  start at the gap instead of the opener formula. When writing English from a Chinese draft, first reduce the Chinese to a
  claim list, then write English from the list rather than translating paragraph by paragraph; keep numbers frozen.

## Rhythm
Read it aloud. Three sentences of the same length in a row sound mechanical; a short
sentence after a long one lands the point.
