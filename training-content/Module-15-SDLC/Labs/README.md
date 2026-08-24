# Module 15: SDLC -- Lab Setup

## Prerequisites

- No software installation required.
- A text editor for writing user stories and SDLC artefacts.
- Access to `Labs/starter-code/` for the flawed SDLC documents.

## Running the Starter Code

This is a document-based lab. There is no application to run.

1. Read `Project/BRIEF.md` for the full exercise instructions.
2. Open the files in `Labs/starter-code/` -- they contain draft user stories, an SDLC methodology
   recommendation, and an environment design with deliberate errors.
3. Work through each issue listed in `lab-exercises.md`.

## Verifying Your Fixes

Compare your corrected artefacts against `Project/CHECKLIST.md`:

- User stories: follow "As a / I want / So that" format with clear acceptance criteria.
- Methodology selection: justified with trade-offs for the FoodExpress context.
- Environment design: dev, test, staging, and production environments defined with access controls.

## Expected Behavior

- User stories are independent, negotiable, and testable (INVEST criteria).
- SDLC methodology choice is appropriate for a sustain engineering team (not greenfield dev).
- Environment design prevents test data from reaching production.
- Sprint / iteration structure accounts for on-call rotations and incident response time.

## Troubleshooting

**User stories too large:** Stories that span multiple sprints should be split. Look for "and" in the
"I want" clause -- each "and" is usually a separate story.

**Methodology justification too brief:** Compare at least two options (e.g., Scrum vs. Kanban) against
the team constraints in `BRIEF.md` before choosing one.
