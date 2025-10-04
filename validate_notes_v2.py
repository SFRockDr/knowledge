#!/usr/bin/env python3
"""
Validate front-matter against schema.json, merge with sidecars, enforce ontology and relations.
Usage: python validate_notes_v2.py --root ./knowledge --schema ./schema.json
"""
import argparse, json, os, re, sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator

FM_RE = re.compile(r'^---\s*\n(.*?)\n---\s*', re.DOTALL)
TAG_RE = re.compile(r'^([a-z0-9_]+):([A-Za-z0-9_]+)$')

def extract_front_matter(text: str):
    m = FM_RE.match(text)
    if not m: return None
    return yaml.safe_load(m.group(1)) or {}

def walk_notes(root: Path):
    for p in root.rglob("*.md"):
        if p.name.lower().startswith("ontology."): continue
        yield p

def load_schema(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_relations(root: Path):
    for c in [root / "relations.yaml", root.parent / "relations.yaml", Path("relations.yaml")]:
        if c.exists():
            data = yaml.safe_load(c.read_text(encoding="utf-8")) or {}
            return set(data.get("allowed", [])), (data.get("aliases") or {})
    return set(["supports","contrasts_with","is_part_of","causes","related_to"]), {}

def domain_dir_for(root: Path, domain_value: str):
    return root.joinpath(*domain_value.split("/")) if domain_value else root

def load_local_ontology(domain_dir: Path):
    p = domain_dir / "ontology.yaml"
    if p.exists():
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        return set(data.get("namespaces", [])), {k:set(v or []) for k,v in (data.get("controlled_values", {}) or {}).items()}, (data.get("aliases") or {}), (data.get("deprecated") or {})
    return set(), {}, {}, {}

def collect_ids(root: Path):
    ids = set()
    for p in walk_notes(root):
        fm = extract_front_matter(p.read_text(encoding="utf-8")) or {}
        if "id" in fm: ids.add(fm["id"])
    return ids

def sidecar_for(note_path: Path):
    return note_path.with_name(note_path.stem + ".meta.yaml")

def load_sidecar(note_path: Path, fm: dict):
    sc = sidecar_for(note_path)
    if sc.exists():
        data = yaml.safe_load(sc.read_text(encoding="utf-8")) or {}
        return data
    return {}

def merge_tags(note_tags, sc):
    add = ((sc.get("tags") or {}).get("add") or [])
    remove = ((sc.get("tags") or {}).get("remove") or [])
    final = set(note_tags or []) | set(add)
    final -= set(remove)
    return sorted(final)

def merge_links(note_links, sc_links):
    final = {}
    keys = set((note_links or {}).keys()) | set((sc_links or {}).keys())
    for k in keys:
        nv = set((note_links or {}).get(k, []) or [])
        sv = set((sc_links or {}).get(k, []) or [])
        final[k] = sorted(nv | sv)
    return final

def validate_tags(tags, namespaces, controlled, aliases):
    errs = []
    if not tags: return errs
    for t in tags:
        m = TAG_RE.match(t)
        if not m:
            errs.append(f"  tag '{t}': invalid format (namespace:value)"); continue
        ns, val = m.group(1), m.group(2)
        if namespaces and ns not in namespaces:
            errs.append(f"  tag '{t}': unknown namespace '{ns}'"); continue
        # alias resolution
        if isinstance(aliases.get(ns, {}), dict):
            val = aliases[ns].get(val, val)
        allowed = controlled.get(ns)
        if allowed and val not in allowed:
            errs.append(f"  tag '{ns}:{val}': not in controlled values")
    return errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--schema", required=True)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    schema = load_schema(Path(args.schema))
    validator = Draft7Validator(schema)
    allowed_rel, rel_aliases = load_relations(root)
    all_ids = collect_ids(root)

    total = bad = 0
    for note in walk_notes(root):
        total += 1
        rel = note.relative_to(root)
        fm = extract_front_matter(note.read_text(encoding="utf-8"))
        if not isinstance(fm, dict):
            print(f"[FAIL] {rel}\n  Missing or invalid front matter"); bad += 1; continue

        schema_errs = [f"  {e.message}" for e in validator.iter_errors(fm)]

        sc = load_sidecar(note, fm)
        tags_final = merge_tags(fm.get("tags", []), sc)
        links_final = merge_links(fm.get("links", {}), (sc.get("links") or {}))

        namespaces, controlled, aliases, deprecated = load_local_ontology(domain_dir_for(root, fm.get("domain","")))
        tag_errs = validate_tags(tags_final, namespaces, controlled, aliases)

        link_errs = []
        for relname, targets in (links_final or {}).items():
            core_rel = rel_aliases.get(relname, relname)
            if core_rel not in allowed_rel:
                link_errs.append(f"  links.{relname}: relation not allowed"); continue
            for t in targets:
                if t not in all_ids:
                    link_errs.append(f"  links.{core_rel}: target '{t}' not found")

        errs = schema_errs + tag_errs + link_errs
        if errs:
            print(f"[FAIL] {rel}")
            for e in errs: print(e)
            bad += 1
        else:
            print(f"[OK]   {rel}")

    print(f"\nChecked {total} notes. {bad} file(s) with issues.")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
