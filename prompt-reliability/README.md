# Prompt Reliability

First iteration implemented: **10 paraphrase pairs** (P01-P10) in `paraphrase_pairs.md`, covering
the phrasings that move answers in practice - polarity flips, leading framings, register shifts,
distractor context, option ordering, and anchoring. An answer that changes under paraphrase was
retrieval luck, not knowledge.

## Protocol

1. Run both variants of each pair 3 times per model, recording model version, date, temperature.
2. Score each pair 0/1/2 per the scale in `paraphrase_pairs.md` (consistent with `results/RUBRIC.md`):
   2 = substantively identical, 1 = same substance/different emphasis, 0 = materially different.
3. Record runs as P01-P10 rows in `results/scoring.csv` and re-run `analysis/analyze_scores.py`.

P07 (unit conversion) is a deliberate baseline pair that any competent model should pass; if it
scores below 2, suspect the protocol before the model.

## Planned extension

The original design - 5 paraphrases per question rather than pairs, measuring stability across the
full fan - remains the goal; pairs are the minimum publishable unit and the pair scores tell us
which question types deserve the full 5-way treatment first.
