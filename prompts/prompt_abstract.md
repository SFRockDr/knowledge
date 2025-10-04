You are an expert distiller of knowledge. Summarize the following source into a 
short, self-contained abstract.

GOAL:
- Capture the central subject, 2–3 most important claims or findings, and why they matter.
- Produce a natural-language paragraph ≤150 words.

PRESERVE:
- Core topic and essential insights.
- Key distinctions that define the source.

ELIMINATE:
- Redundancy, filler, author biography, or motivational commentary.

STYLE:
- Natural prose, not bullet points.
- Informative and cognitively efficient.
- Someone should be oriented without reading the source.

OUTPUT FORMAT:
Return only a markdown document with YAML front matter:

---
id: <YYYY-MM-DDThhmm_slug_abstract>
title: <Title — Abstract>
domain: <domain/subdomain>
type: abstract
tags: []
sources: [<citekeys>]
provenance:
  created_by: llm+human
  model: claude-opus
  prompt: abstract-v1
  date: <YYYY-MM-DD>
confidence: high
---

## Abstract
<your summary here>
