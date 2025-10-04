# Knowledge-as-Code (KaC) — **Bootstrap Context for Future Sessions**

*A single document you can paste at the start of a new chat so I can instantly re-establish context and execute without backtracking.*

---

## 0) Working style (important)

* **Tone & output**: concise, analytical, structured; focus on insight & execution.
* **Bias to action**: propose concrete next steps, small diffs, and checklists.
* **Guardrails**: don’t over-engineer; sustainability and joy of curation > theoretical purity.

---

## 1) Mission in one line

Create a **Git-first, plain-text** knowledge system where **content is immutable** (Markdown notes) and **metadata evolves** (sidecar YAML), validated by CI, and compiled into a **graph** that humans and AIs can use.

---

## 2) Core design decisions (non-negotiables)

* **Two-level domain hierarchy**: `domain/subdomain` (e.g., `nature/trees`).
* **Immutable content**: `source.md`, `*_abstract.md` (≤150 words), `*_synthesis.md` (length-flex; may exceed 1500 words), optional zettels.
* **Evolving metadata outside notes**: `*.meta.yaml` (tags/links/perspectives).
* **Typed relations** (governed, not ad-hoc): `supports | contrasts_with | is_part_of | causes | related_to` (+ aliases in `relations.yaml`).
* **Per-subdomain ontology**: `ontology.yaml` with namespaces, controlled values, aliases, deprecations.
* **Validated & rebuildable**: `validate_notes_v2.py` merges note+sidecar and enforces schema/ontology/relations; `build_graph.py` emits `graph.jsonl`/`catalog.csv`.
* **GitHub is canonical**; **Wiki.js** optionally pulls read-only as the online notebook.

---

## 3) DSRP mental model (how we think)

* **D – Distinctions** → typed tags (`namespace:value`) in local ontology.
* **S – Systems** → foldering + `is_part_of` hierarchies (chapter ↔ book meta-synthesis).
* **R – Relationships** → typed links (governed in `relations.yaml`); curated via sidecars.
* **P – Perspectives** → sidecar `perspectives:` (e.g., management, ecology) to filter/compare.

---

## 4) Expected repository layout

```
/knowledge/
  <domain>/<subdomain>/
    images/                               # assets referenced by notes
    pdfs/                                 # originals for provenance
    YYYY-MM-DDThhmm_slug.md               # source or abstract or synthesis
    YYYY-MM-DDThhmm_slug_abstract.md
    YYYY-MM-DDThhmm_slug_synthesis.md
    YYYY-MM-DDThhmm_slug.meta.yaml        # evolving metadata (sidecar)
    ontology.yaml                         # per-subdomain vocab

/relations.yaml                            # global relation registry (+ aliases)
/schema.json                               # front-matter contract (notes only)
/validate_notes_v2.py                      # validator (merges sidecars)
/build_graph.py                            # compiles graph.jsonl + catalog.csv

/prompts/
  abstract.md
  synthesis.md
  meta_synthesis.md

/templates/
  TEMPLATE_abstract.md
  TEMPLATE_synthesis.md

/docs/
  knowledge_as_code_user_guide.md          # full guide (this project’s SOP)
  METADATA_SIDECARS.md                     # detailed sidecar spec
  INGEST_COOKBOOK.md                       # PDF article, book→chapters, Readwise, YouTube
  pipeline_diagram.(png|pdf)               # optional visual flow
```

---

## 5) Naming & IDs

* **Filename/ID**: `YYYY-MM-DDThhmm_slug[_suffix].md`

  * Suffixes: `_abstract`, `_synthesis` (or `_metasynthesis`), optional `_z` (zettel).
* **Domain**: always two segments.
* **Slug**: `lower-kebab-case`.
* **Citekeys (optional)**: `AuthorYearShortTitle`.

---

## 6) Note front-matter (stable content)

Minimal required keys (see `schema.json` for patterns/enums):

```yaml
---
id: 2025-10-01T0900_fire-suppression
title: Fire suppression impacts on succession
domain: nature/trees
type: source            # source|abstract|synthesis|zettel|glossary
tags: [topic:fire_suppression]   # 1–3 seed tags; bulk tagging happens in sidecar
sources: []             # citekeys or note IDs
provenance:
  created_by: human|llm|llm+human
  model: claude-opus          # when LLM used
  prompt: synthesis-v2        # when LLM used
  date: 2025-10-01
confidence: n/a|low|medium|high
links:
  supports: []
  contrasts_with: []
  is_part_of: []
  causes: []
  related_to: []
---
```

---

## 7) Sidecar schema (evolving metadata)

Beside any note: `YYYY-MM-DDThhmm_slug.meta.yaml`

```yaml
id: 2025-10-01T0900_fire-suppression_synthesis

tags:
  add:    [topic:succession, driver:fire_suppression]
  remove: []

links:
  supports:       [2025-09-30T1010_forest-dynamics-ch1_synthesis]
  contrasts_with: []
  is_part_of:     []
  causes:         []
  related_to:     []

perspectives:
  - name: management
    notes: Prioritize prescribed burns where ladder fuels exist.
  - name: ecology
    notes: Successional reset intervals shift with climate.
```

**Merge rules (validator v2)**

* `final_tags = note.tags ∪ add − remove`
* `final_links = union(note.links, sidecar.links)` (deduped)

---

## 8) Governance files

**`/relations.yaml`** (single source of truth for relation types)

```yaml
allowed: [supports, contrasts_with, is_part_of, causes, related_to]
aliases:
  contradicts: contrasts_with
  correlates_with: related_to
display:
  supports: "supports"
  contrasts_with: "contrasts with"
  is_part_of: "is part of"
  causes: "causes"
  related_to: "related to"
```

**`/knowledge/<domain>/<subdomain>/ontology.yaml`** (per-subdomain)

```yaml
namespaces: [species, topic, driver, region, technique]
controlled_values:
  species: [Chamaecyparis_lawsoniana, Sequoia_sempervirens]
  topic: [range_change, disease_dynamics, succession]
  driver: [fire_suppression, drought, pathogen]
  region: [Pacific_Northwest, Northern_California]
  technique: [wet_in_wet, glazing, drybrush]
aliases:
  species:
    Port_Orford_cedar: Chamaecyparis_lawsoniana
deprecated:
  topic: [legacy_term]
```

**Rules**

* Add new relation types in `relations.yaml` (optionally with aliases).
* Add/alias/deprecate tag values in local `ontology.yaml`.
* Never rewrite note text for ontology changes—use sidecars & rebuild the graph.

---

## 9) Long works (books): chapters + meta-synthesis

* Chapters: Abstract + Synthesis per chapter.
* Meta-synthesis: integrates all chapters.

```yaml
# Chapter synthesis front-matter
links: { is_part_of: [2025-09-30T1200_forest-dynamics_metasynthesis] }

# Book meta-synthesis front-matter
sources:
  - 2025-09-30T1010_forest-dynamics-ch1_synthesis
  - 2025-09-30T1020_forest-dynamics-ch2_synthesis
```

---

## 10) Operations — commands you can assume are available

```bash
# Validate notes + sidecars + ontology + relations
python validate_notes_v2.py --root ./knowledge --schema ./schema.json

# Compile shadow graph for AI/queries (rebuild anytime)
python build_graph.py --root ./knowledge --out ./graph
# → graph/graph.jsonl (nodes/edges/perspectives), graph/catalog.csv

# (Optional) Makefile shortcuts
make validate
make graph
make new-note DOMAIN=nature/trees TITLE="My Title" SLUG=my-title TYPE=source
```

**VS Code tasks** (optional)

* “KaC: Validate”, “KaC: Build Graph”, “KaC: New Note” (wired to the same commands).

---

## 11) Artifacts I (assistant) expect to have access to

*(If missing, I’ll ask you to upload them at session start.)*

* `/schema.json`
* `/relations.yaml`
* `/validate_notes_v2.py`
* `/build_graph.py`
* `/knowledge/<domain>/<subdomain>/ontology.yaml` (at least one example)
* `/prompts/abstract.md`, `/prompts/synthesis.md`, `/prompts/meta_synthesis.md`
* `/templates/TEMPLATE_abstract.md`, `/templates/TEMPLATE_synthesis.md`
* *(Optional)* `/Makefile`, `/.vscode/tasks.json`, `/scripts/new_note.sh`
* *(Docs)* `/docs/knowledge_as_code_user_guide.md`, `/docs/METADATA_SIDECARS.md`, `/docs/INGEST_COOKBOOK.md`

---

## 12) Capture → Normalize → Summarize → Evolve → Validate → Graph (SOP)

1. **Capture**: put raw PDFs under `/pdfs/`; images under `/images/`.
2. **Normalize**: Pandoc → Markdown; add minimal front-matter; keep provenance.
3. **Summarize (2-tier)**: Abstract (≤150 words) + Synthesis (readable narrative; length-flex).
4. **Evolve metadata**: add tags/links/perspectives in `*.meta.yaml` (assistive suggestions OK; human approves).
5. **Validate**: run the validator (locally and in CI).
6. **Graph**: rebuild compiled graph for AI & queries.
7. **Sync**: commit/push (Wiki.js pulls read-only).

---

## 13) Quick “asks” the assistant may make at session start

* “Please upload `relations.yaml` and the active subdomain’s `ontology.yaml` so I can validate typed relations and tags.”
* “Please upload `schema.json`, `validate_notes_v2.py`, and `build_graph.py` (or confirm they’re in the repo).”
* “Upload one example note and its `*.meta.yaml` so I can run a dry-run validation and propose improvements.”
* “If you want UI triggers, upload the `Makefile` and `.vscode/tasks.json`.”

---

## 14) Common tasks I can do quickly

* Draft or refine **ontology.yaml** (namespaces/values/aliases).
* Suggest **sidecar diffs** (tags/links/perspectives) for a batch of notes.
* Diagnose **validation errors** and output exact line-level fixes.
* Propose **DSRP-aware queries** (e.g., contrasts within a topic).
* Generate or adjust **prompt/templates** per domain.
* Configure **pre-commit** and **CI** snippets if missing.

---

## 15) Quality checklist (pre-merge)

* Abstract ≤150 words; Synthesis has headings and reads as a standalone.
* Provenance filled (created_by, model/prompt when applicable, date).
* Note front-matter has only seed tags; sidecar contains bulk.
* Relations are allowed and targets exist.
* Assets under `/images` and `/pdfs`; relative paths correct.
* Validator v2 passes; graph rebuilds cleanly.

---

## 16) Optional: Wiki.js

* Pull-only Git sync to this repo; GitHub remains canonical.
* SSL via Let’s Encrypt; periodic pulls; optional DB snapshot if you use built-in search/user state.

---

### End of Bootstrap

**How to use:** Paste this doc at the top of a new session and say, “Use this KaC bootstrap.” I’ll confirm artifacts present/missing, request any uploads, run validation/graph, and continue execution with minimal back-and-forth.
