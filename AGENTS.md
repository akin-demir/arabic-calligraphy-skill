# Development rules

Preserve Unicode input. Never reverse or manually reshape Arabic before Pango.
Never promote authenticity without recorded independent calligrapher review.
Keep reference-only styles unavailable to the renderer. Do not silently substitute fonts.
Run `PYTHONPATH=src python -m unittest discover -s tests -v` before commits.
Use Conventional Commits on feature branches. Do not publish releases automatically.
Rendering must work offline and never fetch user-provided URLs or run document code.
