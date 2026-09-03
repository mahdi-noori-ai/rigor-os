# Skill: Observability

```
Name: observability
Domain: reliability
Purpose: Understand production failures
Trigger: New services, error paths, jobs, incident follow-up
Do Not Trigger: Tiny UI copy changes
```

## Minimum

- Structured JSON logs
- `trace_id` / `span_id` when OpenTelemetry or request ID middleware exists
- Errors logged with exception + safe context (no secrets)
- Health/readiness endpoints for deploy

## Metrics

Low-cardinality labels only (route template, status class — not user id).

## Tracing

Propagate context across HTTP and task queues.

## Don't

- `print()` debugging left in
- Log entire request bodies with PII
