# Metadata Sidecars — Spec & Usage

This repo separates *immutable content* (notes) from *evolving metadata* (tags, links, perspectives).
Metadata lives in **sidecar files** named `<note_id>.meta.yaml` stored alongside the note.

## File Naming

- Note: `YYYY-MM-DDThhmm_slug[_suffix].md`
- Sidecar: `YYYY-MM-DDThhmm_slug[_suffix].meta.yaml`

## Sidecar Schema

```yaml
# <note_id>.meta.yaml
id: <note_id>  # must match the note's front-matter id

# Optional tag adjustments relative to the note front-matter
tags:
  add:    [namespace:value, ...]  # tags to add
  remove: [namespace:value, ...]  # tags to remove (if present in note)

# Optional typed relations (unioned with note's links)
links:
  supports:       [<note_id>, ...]
  contrasts_with: [<note_id>, ...]
  is_part_of:     [<note_id>, ...]
  causes:         [<note_id>, ...]
  related_to:     [<note_id>, ...]

# Optional context lenses (P in DSRP)
perspectives:
  - name: <string>          # e.g., "management", "ecology", "artist_practice"
    notes: <free text>
```

### Rules

- If a sidecar exists, validator merges:
  - `tags_final = front_matter.tags ∪ add − remove`
  - `links_final = union(front_matter.links, sidecar.links)` (deduped)
- Sidecars are Git-tracked and may be edited *without touching the note text*.

### Why this split?

- **Pleasure-first** authoring: write once, move on.
- **Curation later**: expand tags/links as understanding grows.
- **Ontology evolution**: update vocab/aliases in `ontology.yaml`; retag via scripts without rewriting notes.

