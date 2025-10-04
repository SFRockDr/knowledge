# Knowledge-as-Code Methodology

*Personal Notebook Edition (Wiki.js + GitHub)*

---

## 1. Core Principles

* **Single source of truth**: All knowledge lives as plain Markdown + YAML in a GitHub repo.
* **Durability**: Plaintext + Git history = future-proof, portable.
* **Simplicity over standards**: Only adopt the conventions you actually use.
* **Two-level domain hierarchy**: Every note belongs to `/domain/subdomain/`.
* **Provenance always**: Every note records source(s), authorship, and if/when an LLM touched it.
* **Human oversight**: AI assists in summarization and linking, but you approve/correct.
* **Notebook + Code**: Wiki.js is the user-friendly web notebook; GitHub is the canonical store.

---

## 2. Repository Structure

```
/knowledge
  /nature/
    /trees/
      /images/         # images for this subdomain
      /pdfs/           # PDFs or scans
      2025-09-30_slug.md
      2025-09-30_slug_abstract.md
      2025-09-30_slug_synthesis.md
    /fungi/
      /images/
      /pdfs/
  /art/
    /urban_sketching/
    /watercolor_techniques/
  /mindfulness/
    /zazen/
  /inbox/              # capture dropbox, unprocessed
  /ontology.md         # global relations schema
  /<domain>/<subdomain>/ontology.md  # local vocabularies
  schema.json
  validate_notes.py
```

**Rules**

* All notes belong to exactly one subdomain.
* Assets live in that subdomain’s `images/` or `pdfs/`.
* IDs use the format:

  ```
  YYYY-MM-DDThhmm_slug_suffix.md
  ```

  e.g., `2025-09-30T1033_fire-suppression_synthesis.md`.

---

## 3. Workflow

### Step 1 — Capture / Aggregate

* Dump raw sources into `/inbox/`:

  * Readwise exports (Markdown/CSV).
  * PDFs, articles, field notes.
  * Images (maps, sketches, figures).
* Naming convention optional here — just get material in.
* Move images/PDFs into `/domain/subdomain/images/` or `/pdfs/` as soon as you know where they belong.

---

### Step 2 — Normalize

### Front‑matter Contract (Required)

Add this near “Normalize” so authors know exactly what’s required.

```yaml
# Required keys
id: YYYY-MM-DDThhmm_slug(_abstract|_synthesis|_z)
title: ...
domain: <domain/subdomain>     # always 2 levels
type: abstract|synthesis|source|glossary   # (zettel optional: zettel)
tags: []                        # typed: namespace:value (from local ontology)
sources: []                     # citekeys or note IDs
provenance: {created_by: human|llm+human, model: claude-opus, prompt: <name>, date: YYYY-MM-DD}
confidence: high|medium|low
links:
  supports: []                  # allowed relations (global):
  contrasts_with: []            # supports | contrasts_with | is_part_of | causes | related_to
  is_part_of: []
  causes: []
  related_to: []
```

Also see `schema.json` and `validate_notes.py` for enforcement.


### Naming & Citekeys

- **IDs/filenames:** `YYYY-MM-DDThhmm_slug_suffix.md`  (suffix = `abstract|synthesis|z`).
- **Slugs:** lower‑kebab‑case.
- **Citekeys (suggested):** `AuthorYearShortTitle` (e.g., `Hansen2000PortOrford`).



* Run a small **Pandoc wrapper script** or do it manually:

  * Convert all PDFs/HTML → Markdown.
  * Insert YAML stub:

    ```yaml
    ---
    id: 2025-09-30T1033_slug
    title: <source title>
    domain: nature/trees
    type: source
    tags: []
    sources: []
    provenance:
      created_by: human
      imported_from: <file/url>
      date: 2025-09-30
    confidence: n/a
    ---
    ```
  * Store normalized Markdown in the proper subdomain folder.
  * Rewrite image references to point to local `/images/`.

**Goal:** Every raw artifact has a clean, consistent Markdown representation + YAML front matter.

---

### Step 3 — Summarize (two levels)

### Prompts & Templates

Provide deterministic inputs for the LLM and consistent outputs for authors:

```
/prompts/
  abstract.md
  synthesis.md
  meta_synthesis.md   # for books
/templates/
  TEMPLATE_abstract.md
  TEMPLATE_synthesis.md
```
Note: *Synthesis may exceed 1,500 words when essential information warrants it.*


### Books: Chapter + Meta‑Synthesis Pattern

Use chapter‑level syntheses and a book‑level meta‑synthesis.

```yaml
# Chapter synthesis
links: { is_part_of: [<book_metasynthesis_id>] }

# Book meta-synthesis
sources: [<chapter_synthesis_id_1>, <chapter_synthesis_id_2>, ...]
```



Use an advanced LLM (e.g. Anthropic Claude Opus) with templates.

1. **Abstract (≤150 words)**

   * Short, high-level overview of the source.
   * Filename: `slug_abstract.md`.

2. **Synthesis (800–1500 words)**

   * Structured analysis: context, evidence, mechanisms, implications, open questions.
   * Filename: `slug_synthesis.md`.

**Provenance**:

```yaml
provenance:
  created_by: llm+human
  model: claude-opus
  prompt: synthesis-v2
  date: 2025-09-30
```

---

### Step 4 — Atomization (Optional Zettels)

* You **may skip this step** if Abstract + Synthesis is enough.
* Zettels = one idea per file (`slug_z.md`), atomic, highly linkable.
* Pros: fine-grained graph, useful for RAG chunking.
* Cons: overhead — may not be necessary if you’re not actively managing 10k+ notes.

**Recommendation**:

* Start without zettels.
* If Synthesis files get too dense, use LLM to propose zettels and extract selectively.

---

### Evolving Metadata (No Note Edits Required)
- Most tagging/linking happens in sidecars: `<note_id>.meta.yaml`.
- Relations are governed by `relations.yaml` (repo root).
- Controlled vocab & aliases live in per-subdomain `ontology.yaml`.
- Rebuild the shadow graph anytime: `python build_graph.py --root ./knowledge --out ./graph`.


## Validation Hooks (Automate It)

**Pre-commit**

```yaml
# .pre-commit-config.yaml
repos:
- repo: local
  hooks:
  - id: validate-notes
    name: Validate notes
    entry: python validate_notes.py --root ./knowledge --schema ./schema.json
    language: system
    files: \.md$
```

**GitHub Action**

```yaml
# .github/workflows/validate.yml
name: validate
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install pyyaml jsonschema
      - run: python validate_notes.py --root ./knowledge --schema ./schema.json
```


## Wiki.js Git Sync (Minimum Setup)

1. Deploy Wiki.js (Droplet or managed).
2. Settings → **Git** → choose Pull‑only (GitHub remains canonical).
3. Add repo URL + read‑only PAT.
4. Content directory = `/` (or `/knowledge` if you mirror the path).
5. Enable auto‑pull on a schedule (e.g., hourly).
6. Set a default home page (e.g., `/knowledge/README`).


## Quality Checklist (Pre‑merge)

- [ ] Abstract ≤150 words and informative.
- [ ] Synthesis contains required headings; length flexes as needed.
- [ ] Provenance present (`created_by`, model, prompt, date).
- [ ] Tags exist in local ontology; relations are valid; links resolve.
- [ ] Assets under `/domain/subdomain/{images,pdfs}/` with relative paths.
- [ ] `validate_notes.py` passes.


## References & Aids

- **Ingest Cookbook:** `INGEST_COOKBOOK.md` (PDF article, Book→chapters, Readwise, YouTube).
- **Pipeline Diagram:** see `/docs/pipeline_diagram.png` (and `.pdf`) for the end‑to‑end flow.



* **Global ontology.md** = relation types + schema.
* **Local ontology.md** per subdomain = controlled vocab for tags (`species:`, `technique:`, `topic:`).
* **Typed links** in YAML:

  ```yaml
  links:
    supports: [2025-09-29T0831_fire-suppression-effects_synthesis]
    contrasts_with: []
    is_part_of: []
    causes: []
    related_to: []
  ```
* Auto-suggest links with LLM → review and approve.
* Validate tags/relations with `validate_notes.py`.

---

## 4. Authoring & Notebook (Wiki.js)

* **Wiki.js** runs as your **online notebook**.
* It syncs with the GitHub repo:

  * Markdown is the source of truth.
  * You can edit in Wiki.js’s UI or push/pull via Git.
* Use Wiki.js to:

  * Browse by domain/subdomain.
  * Search.
  * Draft new notes directly (saved as Markdown).

**Benefit**: one web-accessible, backed-up master copy. No local vs. remote drift.

---

## 5. Sustainability Practices

* **Keep it simple**:

  * Two-level domain hierarchy.
  * Only the relations you use (supports, contrasts_with, is_part_of, causes, related_to).
  * Only tags that help retrieval.

* **Daily/weekly maintenance**:

  * Clear `/inbox/`.
  * Normalize new items.
  * Run `validate_notes.py` to catch drift.

* **LLM assist**:

  * Use Claude Opus for Abstracts + Syntheses.
  * Optionally for link suggestions.
  * Always record provenance.

* **Backups**:

  * GitHub is canonical.
  * Periodic repo clone/zip as extra safeguard.

---

## 6. What’s Optional

* **Zettels**: only if needed.
* **Complex ontologies**: keep global relations fixed; expand local vocab slowly.
* **Automated pipelines**: start manual, add scripts once the pattern is solid.

---

## 7. Example File Set (Trees / Chamaecyparis)

```
/nature/trees/
  /images/chamaecyparis_range_map.png
  /pdfs/zobel1985.pdf
  2025-09-30T1033_chamaecyparis-lawsoniana.md
  2025-09-30T1033_chamaecyparis-lawsoniana_abstract.md
  2025-09-30T1033_chamaecyparis-lawsoniana_synthesis.md
  ontology.md
```

---

## 8. Why This Works

* **Scalable**: domain/subdomain keeps growth tidy.
* **Durable**: Markdown + Git → no vendor lock-in.
* **Flexible**: Wiki.js provides an online notebook; GitHub provides versioned master.
* **Manageable**: validation script keeps ontology/tags clean without heavy standards.
* **Sustainable**: simple enough to maintain; extensible if you want to add zettels, RAG pipelines, or analytics later.

