# duodata-sync-action template

Drop these files into the **root** of `datastack-cloud/duodata-semantic-view-mappings`:

```
.github/workflows/sync-from-google-sheets.yml
scripts/sync_sheet.py
scripts/render_xlsx.py
```

## Setup

1. In the new repo, **Settings -> Actions -> General -> Workflow permissions**: select
   **Read and write permissions** so the workflow can push the regenerated MD back.
2. Trigger once manually: **Actions -> Sync from Google Sheets -> Run workflow**.

## What it does

- Fetches the workbook via `https://docs.google.com/spreadsheets/d/<SHEET_ID>/export?format=xlsx`
  (works for "Anyone with the link" sheets, no auth).
- Renders to `duodata_semantic_view_mappings.md` using `scripts/render_xlsx.py`
  (the structure-aware renderer: contiguous non-empty regions become separate
  tables, single-cell header rows become `###` headings, empty columns trimmed).
- Commits and pushes to `main` only if the file actually changed.

## Configuration

- `env.SHEET_ID` in the workflow holds the Google Sheets ID. Move it to
  `vars.SHEET_ID` (repo Variables) if you'd prefer not to keep it in the YAML.
- `env.OUTPUT_PATH` controls the output filename.
- Schedule: `cron: "0 12 * * *"` (daily at 12:00 UTC). Adjust or delete the
  `schedule:` block for manual-only runs.

## If the sheet is later made private

The export endpoint will return HTML/403. You'll need to switch to the Google
Sheets API with a service account:

1. Create a GCP service account, enable Sheets + Drive APIs, generate a JSON key.
2. Share the sheet with the service account's email (Viewer).
3. Store the JSON in a repo secret (e.g. `GOOGLE_SERVICE_ACCOUNT_JSON`).
4. Replace `fetch_xlsx` in `scripts/sync_sheet.py` with a Drive `files.export`
   call (mimeType `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`)
   using `google-api-python-client`.

Ping back if you want me to write that variant.
