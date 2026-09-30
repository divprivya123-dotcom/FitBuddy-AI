# Phase 06 - Project Testing

## Test Areas

- Start the application and verify the home page and `/docs`.
- Submit valid and invalid profile values.
- Verify plan generation and SQLite persistence.
- Submit feedback and verify that a revised plan is stored while the original remains available.
- Verify missing-key and Gemini-failure handling.
- Verify `/view-all-users` displays stored records.

## Manual Test Command

```powershell
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000` and exercise the application workflow.