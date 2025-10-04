Here’s a tight, opinionated toolkit that fits your “immutable content + evolving metadata” setup, on Mac + iPhone, with GitHub as the source of truth.

# 1) Hosting (for Wiki.js)

## Recommendation (simple + durable): **DigitalOcean droplet + Wiki.js**

* **Why**: one-click image maintained by the Wiki.js team; straightforward backups; you control the box. ([docs.requarks.io][1])
* **DB**: use **PostgreSQL** (preferred by Wiki.js; unlocks native search modules). If you later need scale/backup SLAs, migrate DB to DO Managed PG. ([docs.requarks.io][2])
* **How** (quick path):

  1. Create a small droplet (2vCPU/2GB is plenty to start).
  2. Pick the **Wiki.js Marketplace** image; finish setup via web UI. ([docs.requarks.io][1])
  3. Point your domain → droplet; enable HTTPS (Let’s Encrypt).
  4. Connect **Git sync** (pull-only) to your GitHub repo.

### Alternative (more control, still simple): **Docker Compose on a droplet**

* Use the official `docker-compose.yml` (Wiki.js + Postgres) and follow DigitalOcean’s Compose guide. This makes upgrades/restore predictable. ([docs.requarks.io][3])

### Cloud alternatives

* Render / Fly.io / Railway can run Wiki.js containers, but DO’s one-click image is the least friction path for solo ops.

# 2) Mac tooling (edit, validate, convert)

## Editor

* **VS Code** with:

  * **YAML** (Red Hat) — schema-aware YAML editing.
  * **markdownlint** + **Markdown All in One** — fast, consistent MD.
  * **Better TOML / JSON** (optional) if you dabble in other configs.

## Term essentials (Homebrew installs)

```bash
# package manager
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# conversion & media
brew install pandoc poppler qpdf imagemagick  # PDF→MD, text/figure extraction, image ops
# parsing & search
brew install yq jq ripgrep fd                  # YAML/JSON ops, fast search/listing
# python + hooks
brew install python pre-commit                 # local venvs + commit hooks
# git / GH
brew install git gh                            # CLI + auth for GitHub
# optional
brew install yt-dlp graphviz fzf
```

* **Pandoc** is your normalize workhorse; Homebrew keeps it updated. ([Homebrew Formulae][4])
* **yq** (mikefarah) is the right CLI for YAML queries/patching (great for ontology edits & sidecars). ([GitHub][5])

## Python (to run your validator & graph build)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip pyyaml jsonschema
# then:
python validate_notes_v2.py --root ./knowledge --schema ./schema.json
python build_graph.py --root ./knowledge --out ./graph
```

## Nice-to-haves

* **BBEdit** (macOS-native, great for big files/regex).
* **Tower** or **Fork** (GUI Git) if you want a visual client alongside CLI.

# 3) iPhone workflow (edit on the go)

## Git client

* **Working Copy** (best-in-class Git on iOS; integrates with Files + other editors). Use it to clone/pull/push your repo and open Markdown directly. ([Apple][6])

## Markdown editor options (pair with Working Copy)

* **iA Writer** — clean MD editor; commonly used with Working Copy via the Files provider (open the repo folder from Working Copy and edit in iA). ([decoding.io][7])
* **Textastic** — code-friendly editor if you want YAML/MD with syntax cues (works well via Files/Working Copy).
* (You asked to leave Obsidian out; this stack doesn’t require it.)

# 4) Everyday tasks → minimal commands

**Validate notes + sidecars**

```bash
pre-commit run --all-files          # if you installed the hook
# or
python validate_notes_v2.py --root ./knowledge --schema ./schema.json
```

**Rebuild the graph**

```bash
python build_graph.py --root ./knowledge --out ./graph
```

**Edit ontology with safety checks**

```bash
# list namespaces
yq '.namespaces' knowledge/nature/trees/ontology.yaml
# preview adding a tag value
yq -Y '.controlled_values.topic += ["range_change"]' -i knowledge/nature/trees/ontology.yaml
git diff
```

**Quick PDF → Markdown (normalize)**

```bash
# rough text + keep images nearby
pdftotext -layout input.pdf -
pandoc input.pdf -o output.md
```

# 5) Backup & upgrades

* **Backups**: source of truth is GitHub. If using Postgres on the droplet, add a weekly `pg_dump` cron or move to a managed PG later.
* **Upgrades**:

  * DO one-click image → follow in-app notices.
  * Docker Compose → pull new images & `docker compose up -d`.
* **Wiki.js requirements recap**: current docs favor **PostgreSQL**, and note the `pg_trgm` extension for search features; the official Docker docs include a complete compose example. ([docs.requarks.io][2])

---

## TL;DR stack

* **Hosting**: DigitalOcean Wiki.js image on a small droplet → Git pull from GitHub. ([docs.requarks.io][1])
* **Mac**: VS Code + YAML/MD extensions; Homebrew: `pandoc yq jq ripgrep fd python pre-commit`. ([Homebrew Formulae][4])
* **iPhone**: Working Copy for Git; iA Writer/Textastic for editing. ([Apple][6])

This combo keeps your authoring joyful, ontology ops surgical, and operations boring—in the best possible way.

[1]: https://docs.requarks.io/install/digitalocean?utm_source=chatgpt.com "Install on DigitalOcean - Wiki.js"
[2]: https://docs.requarks.io/install/requirements?utm_source=chatgpt.com "Requirements - Wiki.js - requarks.io"
[3]: https://docs.requarks.io/install/docker?utm_source=chatgpt.com "Docker - Wiki.js - requarks.io"
[4]: https://formulae.brew.sh/formula/pandoc?utm_source=chatgpt.com "pandoc"
[5]: https://github.com/mikefarah/yq?utm_source=chatgpt.com "mikefarah/yq: yq is a portable command-line YAML, JSON, ..."
[6]: https://apps.apple.com/us/app/git-client-working-copy/id896694807?utm_source=chatgpt.com "Git client — Working Copy on the App Store"
[7]: https://decoding.io/2023/12/using-ia-writer-as-an-end-to-end-writing-system/?utm_source=chatgpt.com "Using iA Writer as an end-to-end writing system - Decoding.io"
