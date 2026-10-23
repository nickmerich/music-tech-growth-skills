# Contributing

The best contributions come from events that actually happened.

## Add a skill

1. Create `skills/<name>/SKILL.md` with `name` and `description` frontmatter.
2. Write `UNKNOWN: ask <who>` instead of guessing.
3. Add it to the table in `README.md`.
4. Run `python3 scripts/validate_skills.py`.

## Improve a skill

- Keep each `SKILL.md` under 500 lines. Move detail into `references/` or `assets/`.
- `name` must match the folder name: lowercase, numbers, single hyphens.
- `description` says what it does **and when to use it**, in under 1,024 characters.
- Write plainly. No em dashes, no hype words, no invented numbers.

## Share a lesson

Open an issue titled `Lesson: <what happened>` with: what you tried, headcount (verified or estimated, say which), what broke, what you'd change. Lessons that hold up get folded into the relevant skill.

## Never commit

Participant names, emails, phone numbers, waivers, medical info, emergency contacts, unpublished photos, contracts, or sponsor pricing someone asked you to keep private.
