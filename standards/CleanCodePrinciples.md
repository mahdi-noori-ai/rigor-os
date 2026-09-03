# Clean Code Principles (Pragmatic)

Do not treat these as dogma. Prefer the project's existing style when it conflicts.

## KISS / YAGNI

Ship the simplest design that meets today's requirements. No speculative layers.

## DRY

Remove duplication that has **one reason to change**. Do not abstract two similar lines into a framework.

## SOLID (where useful)

- Single responsibility at module/service level — not every function.
- Depend on interfaces when the app already uses DI/ports.
- Do not apply all five letters to a 40-line script.

## Naming

Names that match sibling code. Prefer clear names over comments.

## Comments

Short comments for invariants, non-obvious adapters, `# TODO(owner):`. No large commented-out blocks.

## Modules

Small cohesive units, explicit dependencies, understandable control flow.

## Dead code

Delete unused code in the same change only if it is clearly created by this work or the user asked. Do not "clean the repo" unsolicited.

## Technical debt

If you take a shortcut, note it in the completion report. Do not hide it.
