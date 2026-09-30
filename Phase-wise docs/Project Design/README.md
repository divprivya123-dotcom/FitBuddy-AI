# Phase 03 - Project Design

## Architecture

```text
Browser -> FastAPI routes -> Validation and Gemini service
                         -> SQLAlchemy database
                         -> Jinja2 templates
```

## Main Components

- `app/main.py`: application entry point and template setup.
- `app/routes.py`: page and form request handlers.
- `app/schemas.py`: request validation models.
- `app/models.py` and `app/database.py`: persistence layer.
- `app/gemini_client.py` and generators: AI plan creation and revision.
- `templates/` and `static/`: user interface.