# MyNotes AI v1.1.0

This release turns MyNotes AI from a web-first AI planning app into a Windows desktop-ready portfolio project.

## Highlights

- Added a Tauri v2 desktop shell for `MyNotes AI`.
- Added a FastAPI sidecar packaging path with PyInstaller.
- Added Windows release scripts for web build, backend sidecar build, Tauri build, and SHA256 checksum generation.
- Added GitHub Actions release automation for `v*` tags.
- Kept all existing AI planning, daily review, local RAG, TXT/MD upload, source citations, and planner evaluation features.

## Assets

- `MyNotes-AI-v1.1.0-windows-x64.msi`
- `MyNotes-AI-v1.1.0-windows-x64.sha256`

## Notes

The installer is unsigned in this phase. Windows may show a SmartScreen warning until a future signed release.
