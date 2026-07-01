# ChunkVault

Initial FastAPI project structure for ChunkVault.

## MVP scope

- Register and log in
- Upload files
- Split files into chunks
- Encrypt chunks
- Store chunk metadata in SQLite
- List files
- Download and rebuild files
- Delete files
- Audit logs

## Project layout

```text
app/
  api/          FastAPI route modules
  core/         chunking, encryption, hashing, B2 storage, rebuild helpers
  services/     upload, download, delete, and audit workflows
  templates/    simple FastAPI HTML templates
tests/          core behavior tests
scripts/        database and maintenance helpers
data/           staging and temporary restore folders
docs/           architecture, threat model, restore flow
```
