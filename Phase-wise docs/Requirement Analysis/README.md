# Phase 02 - Requirement Analysis

## Functional Requirements

- Accept username, user ID, age, weight, fitness goal, and workout intensity.
- Validate profile values before generating a plan.
- Generate and save a seven-day workout plan.
- Accept feedback and generate a revised plan without deleting the original.
- Display stored users and plans to an administrator.

## Non-Functional Requirements

- Provide responsive Jinja2 pages.
- Handle missing API keys, invalid input, and Gemini failures gracefully.
- Keep secrets in environment variables.
- Persist records through SQLAlchemy.