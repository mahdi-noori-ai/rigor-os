# Skill: Impact Analysis

```
Name: impact-analysis
Domain: coordination
Purpose: Find all consumers before changing a surface
Trigger: API, auth, schema, shared components, events, env vars
Do Not Trigger: Isolated private helper with a single caller (still grep once)
```

## Procedure

1. Name the change (endpoint, field, table, token format).
2. Grep serializers, schemas, TS types, clients, tests, docs, jobs.
3. List domains: BE, FE, DB, CI, mobile if any.
4. Order implementation so contract and consumers land together.
5. Tests for each consumer or an explicit "out of scope" note.

## Example

API response field rename → serializer, OpenAPI, frontend type, display component, fixture, API test, changelog.
