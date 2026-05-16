# Changelog

## 2026-05-15

### docs(db): add comprehensive code annotations (#24)

Add detailed inline documentation explaining each component of the database layer:
- **Connection handling**: get_db() purpose and row_factory
- **Schema initialization**: Explains each table and its columns

## 2026-05-13

### feat(db): add prompt CRUD operations with version history (#22)

- Add CRUD functions for prompts: create_prompt, get_prompt, get_all_prompts, update_prompt, delete_prompt
- Add get_prompt_versions to retrieve version history
- Update creates version history entry in prompt_versions table

## 2026-05-12

### feat(db): add SQLite setup with prompt optimizer schema (#18)

- Adds SQLite database with schema for prompt optimization and active learning pipeline
- Creates `db.py` with tables for models, prompts, prompt_versions, experiments, metrics, datasets
- Initializes `prompt_lab.db` database file

## 2026-05-11

### fix: correct changelog date conversion to EST (#14)

Python's strftime on an aware datetime doesn't respect the TZ env var. Added astimezone() call and tzset() to properly convert UTC merge dates to America/New_York.

## 2026-05-11

### feat: add Makefile for dev environment management (#15)

Common targets:
- `make install` creates venv + installs deps
- `make dev-install` includes Sphinx

## 2026-05-09

### feat: auto docs and changelog generation (#4)

- Adds a GitHub workflow that generates changelog and rebuilds Sphinx docs on merge to `main`
- Creates a separate PR with the generated changes for manual review
- Populates the Sphinx config (`docs/conf.py`, `docs/index.rst`)

## 2026-05-08

### feat: add auto docs and changelog generation (#4)

Adds a GitHub workflow that generates a changelog entry and rebuilds Sphinx docs on merge to main, then opens a PR for review.

## 2026-05-08

### feat: add CI check to enforce single-commit PRs (#3)

Add a workflow to check that commits are squashed before merge to main.

## 2026-05-08

### feat: make learning diary entries collapsible (#2)

Make each date in the README a collapsible section.

## 2025-11-25

### feat: initial project setup (#1)

Set up a standard project: project goals, virtual environment, source/test folders, conventional commit validation.
