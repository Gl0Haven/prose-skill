# prose

A Claude Code skill for writing and revising Chinese and English prose, with a de-AI branch.

- Picks a genre first (academic EN/ZH, patent, report/slides, technical docs, letters, essays) and applies its rules.
- De-AI workflow: seven-layer diagnosis (vocabulary, sentence patterns, structure, content, formatting, residue, long-document consistency), hard boundaries (no new facts, meaning preserved), three delivery modes.
- Structure rules: heading levels, one-sentence sections, "aspects/dimensions" slicing, bold-label lists.
- Evidence labels throughout: measured / style-guide / observed.
- `scripts/check_prose.py` flags surface patterns; every hit is a prompt to inspect, not proof of AI authorship.

## Install

Copy this folder to `~/.claude/skills/prose`.

```bash
python ~/.claude/skills/prose/scripts/check_prose.py draft.md --genre academic-en
```

Rules are written in Chinese; English-specific files are in English.
