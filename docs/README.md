# Knowledge-as-Code (KaC) — Personal Notebook (GitHub + Wiki.js)

A lean, durable method for turning heterogeneous sources (PDFs, Readwise clips, videos, field notes) into **plain-text Markdown knowledge assets** with YAML metadata, typed links, and optional retrieval later. **GitHub** is the canonical store; **Wiki.js** is the online notebook view.

---

## Authoring flow
1) Create source + Abstract + Synthesis (minimal tags).
2) Create/modify sidecar to add tags/links/perspectives.
3) Validate, build graph, commit, push (Wiki.js will pull).


## What you get
- **Git-first, Markdown canonical** notes (immutable content).
- **Evolving metadata in sidecars**: `<note_id>.meta.yaml` holds tags, typed links, and perspectives.
- **Two-tier outputs** per source: `*_abstract.md` (≤150 words), `*_synthesis.md` (length-flex; can exceed 1500 words if needed).
- **Typed relations** governed centrally in `relations.yaml`; local vocabularies in per-subdomain `ontology.yaml`.
- **Validator v2** merges notes + sidecars and enforces schema/ontology/relations.
- **Compiled shadow graph** (`graph.jsonl`, `catalog.csv`) for search/RAG/analytics.
- **Wiki.js** pulls read-only from GitHub for an always-online notebook.


---

## 10-minute Quickstart

1. **Clone** this repo and open a terminal at the root.

2. **Create folders** (example domains):

```
knowledge/
  nature/trees/{images,pdfs}/
  nature/fungi/{images,pdfs}/
  art/watercolor_techniques/{images,pdfs}/
  mindfulness/zazen/{images,pdfs}/
  inbox/
```

3. **Install deps** (Python 3.10+):

```bash
python -m venv .venv && source .venv/bin/activate
pip install pyyaml jsonschema
```

4. **Drop a PDF** into `knowledge/inbox/` (e.g., a journal article).

5. **Normalize → Markdown** (quick Pandoc example):

```bash
# move original asset
mv knowledge/inbox/article.pdf knowledge/nature/trees/pdfs/2025-10-01_article.pdf

# convert PDF to MD (Pandoc must be installed)
pandoc knowledge/nature/trees/pdfs/2025-10-01_article.pdf -o knowledge/nature/trees/2025-10-01T0900_fire-suppression.md
```

Add YAML front matter to the top (see “Front matter” below).

6. **Create Abstract + Synthesis**
   Use the prompt templates in `/prompts/` (or copy from this README) with your LLM (e.g., Claude Opus). Save as:

```
knowledge/nature/trees/2025-10-01T0900_fire-suppression_abstract.md
knowledge/nature/trees/2025-10-01T0900_fire-suppression_synthesis.md
```

7. **Validate**:

```bash
python validate_notes.py --root ./knowledge --schema ./schema.json
```

Fix any errors (tags outside ontology, missing fields, bad links).

8. **Commit + push** to GitHub.
9. **Configure Wiki.js** to sync from this repo (read-only PAT). Browse/edit online.

You’re live.

---

## Repository layout

```
knowledge/
  <domain>/<subdomain>/
    images/                          # local image assets
    pdfs/                            # original PDFs/scans
    YYYY-MM-DDThhmm_slug.md          # source OR abstract OR synthesis
    YYYY-MM-DDThhmm_slug_abstract.md
    YYYY-MM-DDThhmm_slug_synthesis.md
    YYYY-MM-DDThhmm_slug.meta.yaml   # <-- sidecar (tags/links/perspectives)
    ontology.yaml                    # local vocab (namespaces/values/aliases/deprecated)
relations.yaml                       # allowed relation types (+ aliases)
schema.json                          # front-matter contract (notes only)
validate_notes_v2.py                 # validator (merges sidecars)
build_graph.py                       # compiles shadow graph for AI/query
prompts/                             # abstract/synthesis/meta prompt templates
docs/pipeline_diagram.(png|pdf)      # optional visual flow

```

---

## Conventions

### IDs & filenames

```
YYYY-MM-DDThhmm_slug_suffix.md
suffix ∈ {abstract, synthesis}  # (zettel optional: z)
```

### Note types

`type: abstract | synthesis | source | glossary`  *(zettel optional)*

### Domain

`domain: nature/trees`  (always two levels)

### Relations (global, fixed)

```
supports | contrasts_with | is_part_of | causes | related_to
```

### Tags (local, controlled)

Typed tags like `species:Chamaecyparis_lawsoniana`, `topic:range_change`.
Allowed namespaces and values are defined per subdomain in `ontology.yaml|md`.

---

## Front matter (reference)

**Minimal source note**

```yaml
---
id: 2025-10-01T0900_fire-suppression
title: Fire suppression impacts on succession
domain: nature/trees
type: source
tags: []
sources: []           # citekeys or IDs of originals if applicable
provenance:
  created_by: human
  imported_from: knowledge/nature/trees/pdfs/2025-10-01_article.pdf
  date: 2025-10-01
confidence: n/a
---
```

**Abstract**

```yaml
---
id: 2025-10-01T0900_fire-suppression_abstract
title: Fire suppression impacts on succession — Abstract
domain: nature/trees
type: abstract
tags: [topic:fire_suppression]
sources: [2025-10-01T0900_fire-suppression]
provenance: {created_by: llm+human, model: claude-opus, prompt: abstract-v1, date: 2025-10-01}
confidence: high
---
```

**Synthesis**

```yaml
---
id: 2025-10-01T0900_fire-suppression_synthesis
title: Fire suppression impacts on succession — Synthesis
domain: nature/trees
type: synthesis
tags: [topic:succession, driver:fire_suppression]
sources: [2025-10-01T0900_fire-suppression]
links:
  supports: []
  contrasts_with: []
  is_part_of: []     # chapters → meta-synthesis, etc.
  causes: []
  related_to: []
provenance: {created_by: llm+human, model: claude-opus, prompt: synthesis-v2, date: 2025-10-01}
confidence: medium
---
```

---

## Prompts (drop into `/prompts/`)

**Abstract (`prompts/abstract.md`)**

```
Summarize into ≤150 words… [full template from earlier message]
```

**Synthesis (`prompts/synthesis.md`)**

```
Transform the source into a readable standalone synthesis… 
Sections: Context; Core Insights; Evidence & Mechanisms; Applications & Implications; 
Limitations & Boundary Conditions; Uncertainties & Open Questions.
[full template from earlier]
```

**Meta-synthesis (`prompts/meta_synthesis.md`)** *(for books)*
Integrates multiple chapter syntheses into one narrative. [template from earlier]

*(You can paste the previously agreed versions directly.)*

---

## Ontology

**Global (`ontology.md`)**

* Defines the five relation types and schema rules (kept stable).

**Local (`knowledge/<domain>/<subdomain>/ontology.yaml`)**

```yaml
namespaces: [species, topic, driver, region, technique]   # per subdomain
controlled_values:
  species: [Chamaecyparis_lawsoniana, Sequoia_sempervirens]
  topic: [range_change, disease_dynamics]
aliases:
  species:
    Port_Orford_cedar: Chamaecyparis_lawsoniana
deprecated:
  topic: [legacy_term]
```

---

## Validation & Graph

# Validate notes + sidecars + ontology + relations
```bash
python validate_notes_v2.py --root ./knowledge --schema ./schema.json
```

# Build the compiled graph (JSONL + CSV)
```
python build_graph.py --root ./knowledge --out ./graph
```

- Optional local hook:
  - `.pre-commit-config.yaml` runs `validate_notes_v2.py` on every commit.
- CI:
  - `.github/workflows/validate.yml` runs the same command on PRs/pushes.

---


## Sidecars & typed links (immutable content, evolving metadata)
- Keep note front-matter minimal (id, title, type, domain, sources, 1–3 seed tags).
- Put most **tags/links/perspectives** in `<note_id>.meta.yaml`.
- **Relations** are restricted to those in `relations.yaml` (add new types there).
- Tags/links/perspectives now live in `*.meta.yaml` files beside notes.
- **Local ontologies** live in `knowledge/<domain>/<subdomain>/ontology.yaml` and govern tag namespaces/values.
- Validation merges note + sidecar; the compiled graph is rebuilt anytime without editing note text.

- Validate notes + sidecars:
  ```bash
  python validate_notes_v2.py --root ./knowledge --schema ./schema.json
  ```

---

## Cookbook (ingest workflows)

See `INGEST_COOKBOOK.md` for the step-by-step recipes covering:

* Scientific article (PDF)
* Book → chapters → meta-synthesis
* Readwise article
* YouTube video (transcript)

---

## Optional features

* **Zettels (atomic notes)**: Only if it helps. Use suffix `_z.md`, link with `is_part_of`.
* **RAG index**: A small script can chunk by headings, embed with metadata (`id, domain, type, tags, confidence`), and serve retrieval. Keep separate from core authoring.
* **Versioning**: When re-running summaries with newer models, increment `version` and keep prior text in Git history.

---

## Operating with Wiki.js (online notebook)

* Deploy Wiki.js (self-host or managed).
* Configure **Git sync** to the repo (read-only token).
* Edit in Wiki.js *or* locally + push. Git remains canonical.
* Backups are automatic via Git; optionally export Wiki.js DB snapshots.

---

## Quality checklist (pre-merge)

* [ ] Abstract ≤150 words, informative.
* [ ] Synthesis contains all sections (headings present; length can flex).
* [ ] Provenance completed (who/when/model/prompt).
* [ ] Tags exist in local ontology; relations are valid; links resolve.
* [ ] Assets stored under `/domain/subdomain/{images,pdfs}/` and paths rewritten.

---

## FAQ

**Do I need zettels?**
No. Start with Abstract + Synthesis. Add zettels only when they clearly improve retrieval or cross-linking.

**What if the source is very long (e.g., a book)?**
Split into chapter syntheses + one meta-synthesis. Chapters use `is_part_of` to point to the book-level ID; the meta-synthesis lists chapters in `sources`.

**Must I follow any external standards?**
No. This is optimized for **sustainability and utility**, not conformance.

---

## Roadmap (optional)

* `normalize.py` (Pandoc wrapper), `summarize.py` (LLM calls), `link_suggest.py` (suggest relations).
* `.pre-commit-config.yaml` and GitHub Action to enforce validation.
* `retag_notes.py` to align tags using `aliases`/`deprecated`.

