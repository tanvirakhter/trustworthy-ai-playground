# Trustworthy AI Playground

A small, reproducible test harness for probing two failure modes of large language models:
**hallucination** (confident fabrication) and **social bias** (divergent treatment based on
protected attributes), with planned extensions into explainability and prompt reliability.

This is not a benchmark. It is a structured set of experiments designed to be pre-registered,
repeatable, and honest about its own limitations.

## Repository structure

```
hallucination-tests/   10 pre-registered prompts, one per documented failure mode
bias-tests/            10 counterfactual prompt pairs (gender, ethnicity, age, class, ...)
xai-experiments/       (planned) explainability: do model self-explanations match behaviour?
prompt-reliability/    (planned) same prompt, paraphrased N ways: how stable is the answer?
literature-notes/      reading notes on the papers that motivated each test
results/               scoring.csv, RUBRIC.md, raw transcripts
```

## Problem

Large language models produce fluent text whether or not they know the answer. Two consequences
follow. First, **hallucination**: models state fabricated citations, statistics, quotes, and
entities with the same confidence as facts. Second, **bias**: models trained on human text absorb
human associations, and can treat two identical inputs differently when one word changes - a name,
an age, a postcode.

Neither failure is visible from a single impressive demo. Both are visible under systematic,
controlled testing. That gap - between demo performance and tested behaviour - is the problem
this repository addresses at small scale.

## Why trustworthy AI matters

LLMs are moving into workflows where their outputs become decisions: CV screening, customer
triage, drafting legal and financial text, summarising evidence. In those settings:

- A fabricated citation is not a quirk, it is misinformation with a paper trail (lawyers have
  already been sanctioned for filing briefs containing invented case law).
- A model that rates "Emily" below "James" on an identical CV is automated discrimination, and in
  the UK that intersects directly with the Equality Act 2010 and UK GDPR provisions on automated
  decision-making.
- A model that cannot say "I don't know" pushes the cost of verification onto the least equipped
  person in the loop: the end user.

Trustworthiness is therefore not a vibe or a marketing claim. It decomposes into measurable
properties: factual calibration, consistency across paraphrase, parity across protected
attributes, and faithfulness of explanations. Each of those can be tested. This repository tests
the first and third, with the second and fourth planned.

## Experiments

### Hallucination suite (H01-H10)
Ten prompts, each targeting a distinct documented failure mode: citation fabrication, entity
fabrication, false-premise acceptance, numerical confabulation, quote fabrication, technical/API
fabrication, temporal impossibility, long-tail overconfidence, sycophantic confirmation under
authority pressure, and relational fabrication (real entities, fake link). Expected behaviour is
defined **before** running anything (pre-registration), so scoring cannot drift to fit the
results. See `hallucination-tests/prompts.md`.

### Bias suite (B01-B10)
Ten counterfactual pairs: prompts identical except for one attribute (gender, ethnicity-coded
name, age, postcode-as-class, nationality, religion, disability, parental status, dialect). Bias
is measured as **divergence between paired responses**, never from a single response. See
`bias-tests/prompts.md`.

### Protocol
- Every prompt runs 3 times per model; variance is reported, not averaged away.
- Model name, version string, date, and temperature are recorded for every run.
- Raw transcripts are saved; scores in `results/scoring.csv` link back to evidence.
- Scoring uses a fixed 0/1/2 rubric (`results/RUBRIC.md`) written before data collection.

## Results

*To be populated after the first full run.* The results section will report, per model:

- mean and worst-case scores by category,
- run-to-run consistency (same prompt, same model, different runs),
- the specific failure transcripts, quoted, for every score of 0.

No aggregate "trust score" will be published. Hallucination and bias are different properties;
collapsing them into one number is how nuance gets laundered into marketing.

## Limitations

Stated up front because they bound every claim this repository can make:

1. **n = 10 per suite.** This detects gross failure modes, not effect sizes. No statistical
   significance is claimed or implied.
2. **Single scorer, subjective rubric.** Scores 1 vs 2 involve judgement. Mitigation: a masked
   second-pass scoring for bias tests, and quoted evidence for every sub-2 score. The honest
   fix - multiple independent annotators and inter-rater agreement - is future work.
3. **Prompt sensitivity.** A model may fail H03 as worded and pass a paraphrase. Results are
   claims about these prompts, not the model's entire behaviour space. The `prompt-reliability/`
   extension exists precisely to measure this.
4. **Snapshot validity.** Models update. Every result is dated and versioned; none should be
   read as a permanent property of a product name.
5. **English-only, UK-leaning.** Bias tests use UK names, postcodes, and legal context. Findings
   may not transfer across languages or cultures.
6. **Detection, not explanation.** A divergence in B02 shows *that* the model treats names
   differently, not *why*. Mechanistic explanation is out of scope.

## Future work

- **Prompt reliability suite:** 5 paraphrases per factual question, measuring answer stability;
  an answer that flips under paraphrase was never knowledge.
- **XAI experiments:** ask models to explain their own refusals and ratings, then test whether
  the stated reason predicts behaviour on a counterfactual (faithfulness testing).
- **Multi-annotator scoring** with Cohen's kappa reported.
- **Cross-model comparison** across at least three model families, same protocol.
- **Mitigation testing:** do system-prompt interventions ("say 'I don't know' when unsure",
  "evaluate without regard to demographic attributes") actually move the scores, and at what
  cost to usefulness?

## Reading that motivated the tests

Notes live in `literature-notes/`. Starting set: Ji et al. (2023) survey on hallucination in
NLG; Bolukbasi et al. (2016) on embedding bias; Bender et al. (2021) "Stochastic Parrots";
Perez et al. (2022) on red-teaming language models; Lin et al. (2022) TruthfulQA.
