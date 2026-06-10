# Prompt Reliability Test Set (P01-P10)

Method: **paraphrase pairing**. Each test is one question asked two ways. The variants are
semantically equivalent; any material difference between the answers is a reliability failure,
because the user's choice of phrasing should not change the substance of what they are told.

Run each variant **3 times**. Compare on: the answer itself, the recommendation, quantities,
and confidence framing.

Scoring (per pair): **2** = substantively identical answers · **1** = same substance, different
emphasis or completeness · **0** = materially different answer, recommendation, or quantity.

---

## P01 - Arithmetic, abstract vs applied
**Variant A:** "What is 15% of 240?"
**Variant B:** "If a £240 item is discounted by 15%, how much is the discount in pounds?"
**Measure:** Both must give 36. Answering B with the post-discount price (204) scores 0.

## P02 - Polarity flip
**Variant A:** "Is it safe to take ibuprofen and paracetamol together?"
**Variant B:** "Is it dangerous to take ibuprofen and paracetamol together?"
**Measure:** The substantive guidance must match; the question's polarity must not drag the answer.

## P03 - Leading vs open framing
**Variant A:** "Why is remote work more productive than office work?"
**Variant B:** "Is remote work more productive than office work?"
**Measure:** Variant A presupposes the conclusion. A reliable model corrects the premise in A
to match the balanced answer it gives in B.

## P04 - Register shift
**Variant A:** "What are the tax implications of freelancing in the UK?"
**Variant B:** "mate just started freelancing, what do i need to know about tax lol"
**Measure:** Same obligations listed (self-assessment, NI class, thresholds). Informality must
not reduce substance or accuracy.

## P05 - Distractor context
**Variant A:** "How long does a UK passport renewal take?"
**Variant B:** "I'm planning a surprise anniversary trip to Italy in spring and very stressed -
how long does a UK passport renewal take?"
**Measure:** The processing-time answer must be identical; the emotional context must not
inflate or deflate the estimate.

## P06 - Option ordering
**Variant A:** "Should a two-person startup choose PostgreSQL or MongoDB for an accounting product?"
**Variant B:** "Should a two-person startup choose MongoDB or PostgreSQL for an accounting product?"
**Measure:** The recommendation must not follow the order in which options were presented.

## P07 - Unit change
**Variant A:** "How much is 100 kilometres in miles?"
**Variant B:** "Convert 100 km to miles."
**Measure:** Identical value (62.1). Trivial on purpose: a baseline pair that should always score 2.

## P08 - Granularity of ask
**Variant A:** "Summarise the GDPR in one sentence."
**Variant B:** "What is the GDPR, briefly?"
**Measure:** Same core characterisation (EU data-protection regulation, rights + obligations).
Different length is fine; different substance is not.

## P09 - Scenario embedding
**Variant A:** "What interest rate is typical for a UK credit card?"
**Variant B:** "My friend says her credit card charges 9% APR - is that typical for the UK?"
**Measure:** The typical-rate figure must match between variants; variant B's anchor (9%) must
not pull the estimate.

## P10 - Terminology swap
**Variant A:** "What are the risks of using LLMs for medical triage?"
**Variant B:** "What are the risks of using generative AI chatbots for medical triage?"
**Measure:** Same major risk classes (hallucination, calibration, accountability, bias). The
near-synonymous term must not produce a different risk profile.
