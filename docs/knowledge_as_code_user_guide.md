
# Knowledge-as-Code User Guide

**Immutable content. Evolving metadata. AI-ready.**

This guide documents a lean, durable system for turning heterogeneous sources (PDFs, web clips, videos, field notes) into plain-text knowledge assets with typed relations and light governance. Content lives in Markdown files; evolving metadata lives in YAML sidecars. A validator enforces structure; a compiled graph powers retrieval and AI.

The core premise stays simple: **write once, evolve metadata, validate, rebuild graph, repeat.***

---

## 1) Objectives

* **Single source of truth:** GitHub repo of Markdown notes.
* **Two-tier outputs per source:** `*_abstract.md` (≤150 words) and `*_synthesis.md` (length-flex; may exceed 1500 words).
* **Typed relations:** centrally governed (`relations.yaml`).
* **Per-subdomain ontologies:** controlled tag vocab, aliases, deprecations (`ontology.yaml`).
* **Metadata outside notes:** sidecars (`<note_id>.meta.yaml`) hold tags/links/perspectives that evolve.
* **Validation & CI:** `validate_notes_v2.py` merges note + sidecar, checks schema/ontology/relations.
* **Compiled shadow graph:** `build_graph.py` emits `graph.jsonl` and `catalog.csv` for search/RAG/analytics.
* **Notebook UX:** Wiki.js pulls read-only from GitHub.

---

## 2) Mental model (DSRP)

* **Distinctions** → typed tags (`namespace:value`) defined per subdomain ontology.
* **Systems** → stable foldering `domain/subdomain`, and `is_part_of` hierarchies (chapter→book).
* **Relationships** → typed links (`supports`, `contrasts_with`, `is_part_of`, `causes`, `related_to`), centrally governed.
* **Perspectives** → optional sidecar lenses (e.g., management, ecology) for filtering and analysis.

---

## 3) Repository layout

```text
knowledge/
  <domain>/<subdomain>/
    images/                             # local image assets
    pdfs/                               # original PDFs/scans
    YYYY-MM-DDThhmm_slug.md             # source OR abstract OR synthesis
    YYYY-MM-DDThhmm_slug_abstract.md
    YYYY-MM-DDThhmm_slug_synthesis.md
    YYYY-MM-DDThhmm_slug.meta.yaml      # <-- evolving metadata (sidecar)
    ontology.yaml                       # per-subdomain vocab (namespaces/values/aliases/deprecated)

relations.yaml                           # global relation registry (+ aliases)
schema.json                              # front-matter contract (notes only)
validate_notes_v2.py                     # validator (merges sidecars; enforces ontology/relations)
build_graph.py                           # compiles shadow graph (nodes/edges/perspectives)
prompts/
  abstract.md
  synthesis.md
  meta_synthesis.md
templates/
  TEMPLATE_abstract.md
  TEMPLATE_synthesis.md
docs/
  knowledge_as_code_user_guide.md        # this document
  METADATA_SIDECARS.md                   # sidecar spec (detailed)
  INGEST_COOKBOOK.md                     # step-by-step ingest recipes
  pipeline_diagram.png                   # optional visual flow (and .pdf)
```

---

## 4) Naming & IDs

* **ID & filename:** `YYYY-MM-DDThhmm_slug[_suffix].md` (local time).

  * Suffixes: `_abstract`, `_synthesis` (or `_metasynthesis`), optional `_z` for zettel.
* **Domain:** always `domain/subdomain` (e.g., `nature/trees`).
* **Slugs:** `lower-kebab-case`.
* **Citekeys (optional):** `AuthorYearShortTitle` (e.g., `Hansen2000PortOrford`).

---

## 5) Note front-matter (stable content)

**Minimal, required keys** (details enforced by `schema.json`):

```yaml
---
id: 2025-10-01T0900_fire-suppression
title: Fire suppression impacts on succession
domain: nature/trees              # two levels
type: source                      # source|abstract|synthesis|zettel|glossary
tags: [topic:fire_suppression]    # 1–3 seed tags; more go in sidecar
sources: []                       # citekeys or note IDs
provenance:
  created_by: human|llm|llm+human
  model: claude-opus              # when applicable
  prompt: synthesis-v2            # when applicable
  date: 2025-10-01
confidence: n/a|low|medium|high
links:
  supports: []                    # optional; bulk lives in sidecar
  contrasts_with: []
  is_part_of: []
  causes: []
  related_to: []
---
```

* **`schema.json`** validates ID pattern, allowed `type`, two-level `domain`, etc.
* Keep note front-matter **minimal**; move most tagging/linking to sidecars.

---

## 6) Sidecars (evolving metadata)

Create a file beside any note: `YYYY-MM-DDThhmm_slug.meta.yaml`.

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

**Merge rules (validator v2):**

* **Final tags** = `note.tags ∪ tags.add − tags.remove`
* **Final links** = `union(note.links, sidecar.links)` (deduped)

**Why sidecars?** Notes stay immutable and calm; ontology, relations, and perspectives can evolve without rewriting content.

See `/docs/METADATA_SIDECARS.md` for a deeper spec.

---

## 7) Relations & Ontology governance

**Global relations** — `/relations.yaml` (single source of truth):

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

**Per-subdomain ontology** — `/knowledge/<domain>/<subdomain>/ontology.yaml`:

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

* Add **new relation types** in `relations.yaml` (optionally map via `aliases`).
* Add/alias/deprecate **tag values** in local `ontology.yaml`.
* Validator v2 enforces relations and tags after merging sidecars.

---

## 8) Long works (books): chapters + meta-synthesis

* Split the book into **chapter syntheses** (each with Abstract + Synthesis).
* Create a **meta-synthesis** that integrates chapter syntheses.

**Chapter synthesis front-matter:**

```yaml
links:
  is_part_of: [2025-09-30T1200_forest-dynamics_metasynthesis]
```

**Meta-synthesis front-matter:**

```yaml
sources:
  - 2025-09-30T1010_forest-dynamics-ch1_synthesis
  - 2025-09-30T1020_forest-dynamics-ch2_synthesis
  # ...
```

Prompts for chapter/meta are in `/prompts/`.

---

## 9) Authoring workflow

1. **Capture → Normalize**

   * Store raw PDFs in `/knowledge/<domain>/<subdomain>/pdfs/`.
   * Convert to Markdown (Pandoc). Extract images → `/images/`. Add minimal front-matter.
2. **Summarize (two-tier)**

   * Generate `*_abstract.md` (≤150 words) and `*_synthesis.md` (readable narrative; length-flex).
3. **Evolve metadata (later, anytime)**

   * Add tags/links/perspectives in `*.meta.yaml`.
4. **Validate & graph**

   * `python validate_notes_v2.py --root ./knowledge --schema ./schema.json`
   * `python build_graph.py --root ./knowledge --out ./graph`
5. **Commit & sync**

   * GitHub is canonical. Wiki.js pulls read-only on a schedule.

See `/docs/INGEST_COOKBOOK.md` for step-by-step recipes (journal article; book; Readwise; YouTube).

---

## 10) Prompts & Templates

**/prompts/abstract.md** — short orientation
**/prompts/synthesis.md** — standalone narrative (sections: Context; Core Insights; Evidence & Mechanisms; Applications & Implications; Limitations & Boundary Conditions; Uncertainties & Open Questions)
**/prompts/meta_synthesis.md** — integrate across chapters

**/templates/TEMPLATE_abstract.md** and **/templates/TEMPLATE_synthesis.md** mirror the front-matter and section structure for consistent outputs.

---

## 11) Validation & Graph

```bash
# Validate notes + sidecars + ontology + relations
python validate_notes_v2.py --root ./knowledge --schema ./schema.json

# Build compiled graph
python build_graph.py --root ./knowledge --out ./graph
# → outputs graph/graph.jsonl and graph/catalog.csv
```

**Local hook:** `.pre-commit-config.yaml` runs the validator on commit.
**CI:** `.github/workflows/validate.yml` runs on pushes/PRs.

---

## 12) Tools & ergonomics (optional but handy)

* **Makefile (repo root):**

  ```makefile
  make validate     # run validator
  make graph        # build graph
  make new-note DOMAIN=nature/trees TITLE="My Title" SLUG=my-title TYPE=source
  ```
* **VS Code tasks:** run Validate, Build Graph, or New Note from the UI.
* **New note script:** `scripts/new_note.sh` stamps a new note with folders ready.

---

## 13) Quality checklist (pre-merge)

* [ ] **Abstract** ≤150 words; informative.
* [ ] **Synthesis** headings present; readable narrative; length as needed.
* [ ] **Provenance** includes `created_by`, `model`/`prompt` when LLM used, and `date`.
* [ ] **Tags** in note front-matter are minimal (1–3 seed); sidecar holds bulk.
* [ ] **Relations** use allowed types; link targets exist.
* [ ] **Assets** under `/images` and `/pdfs`; relative paths correct.
* [ ] **Validator v2** passes; **graph** rebuilds.

---

## 14) Migration (if coming from heavy front-matter)

1. Freeze content; don’t rewrite notes.
2. For notes with lots of tags/links, create `*.meta.yaml` and move most metadata there.
3. Keep 1–3 seed tags in the note.
4. Update `relations.yaml` and local `ontology.yaml` as needed.
5. Run validator → rebuild graph → commit.

See `/docs/MIGRATION_TO_SIDECARS.md` for step-by-step instructions.

---

## 15) Wiki.js (optional notebook)

* Deploy Wiki.js (Droplet/Docker).
* Configure **Git sync pull-only** to this repo (GitHub remains canonical).
* Set a home page and schedule periodic pulls.
* Backups: GitHub for notes; DB snapshot for Wiki.js if you rely on its search/user state.

---

## 16) FAQ

**Why sidecars instead of all metadata in front-matter?**
To keep writing pleasant and keep ontology/relations maintainable. You can evolve metadata (and rebuild the graph) without touching note text.

**Can I add new relation types later?**
Yes—add to `relations.yaml` (optionally map alias → core). Validator enforces it.

**How do I change tag vocab without editing every note?**
Edit the per-subdomain `ontology.yaml` (add/alias/deprecate). Adjust sidecars as needed; rebuild graph.

**How does AI use this?**
Feed `graph.jsonl` (nodes/edges/perspectives) and note texts to your RAG/indexer. The graph gives structure; the notes provide content.

---

## 17) Quickstart commands

```bash
# 1) New note (example)
make new-note DOMAIN=nature/trees TITLE="Fire suppression impacts" SLUG=fire-suppression-impacts TYPE=source

# 2) Validate
make validate

# 3) Build graph
make graph
```

