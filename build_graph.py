#!/usr/bin/env python3
"""
Compile notes + sidecars into graph.jsonl and catalog.csv
Usage: python build_graph.py --root ./knowledge --out ./graph
"""
import argparse, re, sys, json, csv
from pathlib import Path
import yaml

FM_RE = re.compile(r'^---\s*\n(.*?)\n---\s*', re.DOTALL)

def extract_front_matter(text: str):
    m = FM_RE.match(text)
    if not m: return None
    return yaml.safe_load(m.group(1)) or {}

def walk_notes(root: Path):
    for p in root.rglob("*.md"):
        if p.name.lower().startswith("ontology."): continue
        yield p

def sidecar_for(note_path: Path):
    return note_path.with_name(note_path.stem + ".meta.yaml")

def load_sidecar(note_path: Path, note_id: str):
    sc = sidecar_for(note_path)
    if sc.exists():
        data = yaml.safe_load(sc.read_text(encoding="utf-8")) or {}
        if data.get("id") and data["id"] != note_id:
            print(f"WARNING: sidecar id mismatch for {note_path.name}", file=sys.stderr)
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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    gj = (out / "graph.jsonl").open("w", encoding="utf-8")
    catf = (out / "catalog.csv").open("w", newline="", encoding="utf-8")
    writer = csv.writer(catf); writer.writerow(["id","type","domain","title","tags"])

    for note in walk_notes(root):
        text = note.read_text(encoding="utf-8")
        fm = extract_front_matter(text)
        if not isinstance(fm, dict) or "id" not in fm: continue
        sc = load_sidecar(note, fm["id"])
        tags = merge_tags(fm.get("tags", []), sc)
        links = merge_links(fm.get("links", {}), (sc.get("links") or {}))
        perspectives = sc.get("perspectives") or []

        node = {"id": fm["id"], "type": fm.get("type"), "domain": fm.get("domain"),
                "title": fm.get("title"), "tags": tags, "confidence": fm.get("confidence")}
        gj.write(json.dumps({"node": node}) + "\n")
        writer.writerow([node["id"], node["type"], node["domain"], node["title"], ";".join(tags)])

        for rel, targets in (links or {}).items():
            for dst in targets:
                gj.write(json.dumps({"edge":{"src": fm["id"], "rel": rel, "dst": dst}}) + "\n")

        for p in perspectives:
            gj.write(json.dumps({"perspective":{"id": fm["id"], **p}}) + "\n")

    gj.close(); catf.close()
    print(f"Wrote {out/'graph.jsonl'} and {out/'catalog.csv'}")

if __name__ == "__main__":
    main()
