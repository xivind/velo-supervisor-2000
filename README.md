# velo-supervisor-2000
Velo Supervisor 2000 is a program to keep track of lifetime and service intervals of bicycle components, based on activity data from Strava.

**Which version do these instructions cover?** The setup, layout and release instructions below describe the `dev` branch and the next release. They are not what the current release (v0.5.0) uses. If you run v0.5.0 today, follow the README on the [`master` branch](https://github.com/xivind/velo-supervisor-2000/blob/master/README.md) (or at the [v0.5.0 tag](https://github.com/xivind/velo-supervisor-2000/blob/v0.5.0/README.md)).

This software is under active development. Use it at your own risk, as there may be issues with data integrity. We do our best to solve bugs and make improvements, but cant promise you any support. See the [project board](https://github.com/users/xivind/projects/2/views/1) for a complete list of issues.

**Join the work, either by forking the repo and contribute with PRs or simply by submitting <a href="https://github.com/xivind/velo-supervisor-2000/issues" class="text-decoration-none">issues</a>. Please prefix suggestions for improvements with FEATURE REQUEST. We will review them and remove the prefix when decided how to follow up. Bug reports should be prefixed with BUG.**

## Setup and configuration
Starting files are in `config/`. Keep your own copies outside the repo, and dont share the Strava tokens with anyone.

- **Step 1:** Copy `config/template_db.sqlite` to a place outside the repo. This is your database
- **Step 2:** Copy `config/strava_tokens.example.json`, rename it (e.g. to `strava_tokens.json`) and fill in your own data. [See this tutorial](https://developers.strava.com/docs/getting-started/) on how to obtain the oauth-data from Strava. **Important:** the tutorial's example authorization URL uses `scope=read`, which is not enough. Replace it with `scope=read,activity:read_all,activity:write,profile:read_all`. The `profile:read_all` scope is required for the app to detect bikes that dont have any recorded rides yet
- **Step 3:** Copy `config/config.json.example` to `config.json` and update it with the paths to your database file and Strava tokens. Where it goes depends on how you run the program:
  - Local: `config.json` in the project root (it is in .gitignore, so it will not be synced to remote)
  - Docker: `/data/config.json` inside the container, set by the environment variable `VELO_SUPERVISOR_CONFIG`
- **Step 4 (local):** Install [uv](https://docs.astral.sh/uv/) and run `uv sync` from the project root. This creates a virtual Python 3.12 environment in `.venv` and installs the packages from `uv.lock`. Start the program from the project root with `uv run uvicorn velo_supervisor.main:app --log-config config/uvicorn_log_config.ini`. It serves on http://localhost:8000
- **Step 4 (Docker):** The `Dockerfile` is in the project root. The script `scripts/create-container-vs2000.sh` builds the image and starts a container, and is meant as inspiration, so modify it to your liking. The container runs as UID 1000, so the folder mounted on `/data` (database, `config.json` and logs) must be writable by that user. The Strava tokens are mounted on `/secrets`. A health check calls `/health` every 10 minutes and reports unhealthy if an error was logged in the last 24 hours or the database cant be read
- **Step 5:** On startup the program will call Stravas APIs and get the last 200 rides and related bikes, but since this is the first time you run the program, you need to manually fetch all ride data and all bikes. This is done by navigating to the `CONFIG` tab and click the button `Get all rides`
- **Step 6:** You are all set and can now register your first components. The rest will hopefully be self explanatory

### Upgrading and database migration
Some releases change the database schema. These are marked as breaking changes in the [release notes](https://github.com/xivind/velo-supervisor-2000/releases). Backup the database first, then run the migration script from the project root:

```bash
python -m velo_supervisor.db_migration
```

The script does not read `config.json`. It searches the home folders of the current user for the database and asks you to confirm, or to enter the path manually. Release notes also say when you need to clear the browser cache (Ctrl + Shift + R) after updating the server.

### Knowledge graph (graphify)
This repo tracks a [graphify](https://github.com/Graphify-Labs/graphify) knowledge graph of the codebase in `graphify-out/` (committed to git). The git hook that keeps it auto-updated on commit is **not** included by cloning, because `.git/hooks/` is never tracked by git. After cloning, run this once to get the same behavior locally:

```bash
graphify hook install
```

This installs a post-commit hook that rebuilds `graph.json`/`GRAPH_REPORT.md` from changed code (AST-only, no LLM cost). Doc/template/image content still needs a manual update after those change. Run `graphify . --update` (or ask Claude Code to run `/graphify --update`), since that step needs either a Gemini API key or an LLM-capable session.

## Bugs
There are still some bugs scattered around. If you find any, please submit them as an <a href="https://github.com/xivind/velo-supervisor-2000/issues" class="text-decoration-none">issue</a>.

## Tests
Run `uv run pytest` locally. Calculation behaviour is pinned by characterisation tests on a synthetic dataset with a fixed clock. Expected-result files are never overwritten by tooling. For changes near the calculations, `scripts/integrity/compare.py --ref master --db <copy>` compares the results against `master` on a local copy of real data (never committed). See [tests/README.md](tests/README.md) for details.

## CI/CD
The workflow `.github/workflows/tests.yml` runs on every push and pull request, with three jobs:
- `test`: `uv run pytest` with coverage
- `lint`: `ruff check` and `ruff format --check` on `tests/` and `scripts/`. App modules join as Stage 4 rewrites them
- `docker`: builds the image, starts it on a throwaway `/data`, and requires `/health` to return 200, a clean footer version and UID 1000

Dependabot opens weekly, grouped updates for GitHub Actions and uv dependencies, targeting `dev`. They go through CI like any other change.

## Versioning, branches and releases
Velo Supervisor 2000 uses <a href="https://semver.org/" class="text-decoration-none">Semantic Versioning Specification (SemVer)</a>. The version comes from the git tag (hatch-vcs), so there is no version file to edit.

Work is done on feature branches off `dev`, merged into `dev` by pull request. `master` and `staging` accept changes only through pull requests, admins included. Required CI checks are switched on for `staging` after the next dev to staging merge, and for `master` at the switch-over. Changes flow `dev` to `staging` for testing and quality assurance, then `staging` to `master`.

To release, go to the [Releases page](https://github.com/xivind/velo-supervisor-2000/releases) and:
1. Click **Draft a new release**
2. Type the new tag `vX.Y.Z` and select `master` as target. GitHub creates the tag on publish
3. Click **Generate release notes**. They are categorised by `.github/release.yml`. Label pull requests `breaking-change` when a migration is required, so they are listed as such
4. Edit the notes, then publish

## Changelog
See the [Releases page](https://github.com/xivind/velo-supervisor-2000/releases) for release notes for every version. To see whats coming, check out the [project board](https://github.com/users/xivind/projects/2/views/1). Items marked as P0 are planned for the next release.
