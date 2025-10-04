Here’s a **step-by-step “cookbook” workflow** for ingesting different asset types into your Knowledge-as-Code system. Each follows the same **capture → normalize → summarize → (atomize optional) → link** pipeline, but tuned for the quirks of the source.

---

# 1) Scientific Journal Article (PDF)

**Example**: Ecology journal article, ~15 pages.

**Steps**

1. **Capture**

   * Save PDF → `/knowledge/nature/trees/pdfs/2025-10-01_ecology-fire-suppression.pdf`.
   * Drop a raw copy in `/inbox/` until processed.

2. **Normalize**

   * Run Pandoc → Markdown.
   * Extract figures/tables → `/nature/trees/images/`.
   * Create base file:
     `2025-10-01T0900_fire-suppression.md` with YAML stub (`type: source`, provenance).

3. **Summarize**

   * **Abstract.md** (≤150 words).
   * **Synthesis.md** (800–1500 words, structured).
   * Include study design, evidence, and limitations.

4. **Atomize (optional)**

   * Extract zettels for each claim (e.g., “Fire suppression alters successional trajectories”).
   * Link each to synthesis with `is_part_of`.

5. **Link & Ontology**

   * Add `tags:` → `topic:fire_suppression`, `ecosystem:chaparral`.
   * `links:` → `supports` or `contrasts_with` earlier notes.

---

# 2) Book (PDF, 400 pages)

**Example**: *Forest Dynamics: An Ecological Perspective*.

**Steps**

1. **Capture**

   * Save book PDF → `/knowledge/nature/trees/pdfs/forest-dynamics.pdf`.

2. **Normalize**

   * Split PDF → chapter PDFs (tools: `pdftk`, `qpdf`).
   * Convert each chapter → Markdown.
   * Store as `/nature/trees/forest-dynamics/ch1.md` … `/chN.md`.

3. **Summarize (per chapter)**

   * For each chapter: create `chX_synthesis.md` and `chX_abstract.md`.
   * Use chapter title in IDs.

4. **Meta-Synthesis**

   * Run meta-synthesis across all chapters → `forest-dynamics_metasynthesis.md`.
   * Chapters `is_part_of` meta; meta `sources:` includes chapters.

5. **Atomize (optional)**

   * Pull atomic zettels only from key chapters (don’t over-split).

6. **Link & Ontology**

   * Local ontology for `topic:succession`, `topic:disturbance`.
   * Cross-link with other works (e.g., articles on fire suppression).

---

# 3) Readwise Article

**Example**: Saved via Readwise from *The Atlantic* (~2000 words).

**Steps**

1. **Capture**

   * Export from Readwise → Markdown/CSV.
   * Save raw file in `/inbox/2025-10-01_fire-ecology-readwise.md`.

2. **Normalize**

   * Strip Readwise formatting.
   * Add YAML stub with `source_url`, `author`, `date_original`.
   * Save to `/nature/trees/2025-10-01T0940_fire-ecology.md`.

3. **Summarize**

   * **Abstract.md**: short digest of article.
   * **Synthesis.md**: richer write-up, 600–1000 words.

4. **Atomize (optional)**

   * Likely not needed unless article is dense.

5. **Link & Ontology**

   * Tag as `source_type:article`, add topical tags.
   * `related_to:` academic paper syntheses.

---

# 4) YouTube Video (Lecture/Interview)

**Example**: 45-min talk on forest management.

**Steps**

1. **Capture**

   * Download transcript (`yt-dlp --write-auto-sub`).
   * Save video (optional) → `/nature/trees/videos/2025-10-01_forest-management.mp4`.
   * Transcript → `/inbox/2025-10-01_forest-management-transcript.txt`.

2. **Normalize**

   * Clean transcript (remove timestamps, filler).
   * Convert to Markdown: `2025-10-01T1000_forest-management.md`.
   * YAML stub: `source_type:video`, `source_url`, `speaker`.

3. **Summarize**

   * **Abstract.md**: ≤150 words — “what the talk is about.”
   * **Synthesis.md**: distill into structured, flowing write-up (1000+ words if necessary).

4. **Atomize (optional)**

   * Pull zettels for each major insight/claim from the talk.

5. **Link & Ontology**

   * Add topical tags (`topic:management`, `driver:fire`).
   * `related_to:` papers or books on same subject.

---

## 🔑 Observations Across All Workflows

* **Normalize always** → everything ends up Markdown + YAML + assets in local folder.
* **Summarize consistently** → Abstract + Synthesis, no matter the length.
* **Atomize optional** → only when it adds value.
* **Ontology links** → keep simple, just enough for retrieval and navigation.
* **Meta-synthesis** only for long works (books, multi-part series).

---

Would you like me to now **diagram this as a unified pipeline** (flowchart from source type → normalized markdown → Abstract/Synthesis → optional zettels/meta → Wiki.js/GitHub)?
