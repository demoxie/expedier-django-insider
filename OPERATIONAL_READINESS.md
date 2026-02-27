# Operational Readiness — Incidence Search

## Blast Radius Analysis

| Component | Impact | Mitigation |
|-----------|--------|------------|
| New API endpoint | Staff users only | `IsAdminUser` permission; no public exposure |
| New DB table | No schema changes to existing tables | Additive migration; independent table |
| Frontend | New page only | No changes to existing UI routes |
| Database load | Additional read queries | Indexed fields; paginated responses; rate limiting |

**Conclusion:** Blast radius is minimal. The feature is entirely additive with no modifications to existing code paths.

---

## Rollout Strategy

### Phase 1: Internal Testing
- Deploy to staging
- Staff QA with seed data
- Verify all filters with edge cases

### Phase 2: Gradual Rollout
- Deploy behind feature flag (optional)
- Monitor for 24h before broader access
- Check query latency baseline

### Phase 3: Full Rollout
- Remove feature flag
- Announce to staff users
- Begin 48-hour monitoring period

---

## Rollback Plan

1. **Revert the PR** — all changes are in one commit
2. **Migrate down** — `python manage.py migrate incidences zero`
3. **No data loss** — incidence data is new; no existing data is modified
4. **Time to rollback** — < 5 minutes

---

## Monitoring & Observability

### Structured Logging
Every search request is logged with:
- `query_params` — what the user searched for
- `result_count` — number of results returned
- `elapsed_ms` — query execution time
- `user_id` — who performed the search

### Key Metrics to Watch
| Metric | Threshold | Action |
|--------|-----------|--------|
| P95 latency | > 500ms | Add database indexes or optimize query |
| Error rate | > 1% | Check logs, investigate root cause |
| Zero-result rate | > 50% | Review filter UX, check data quality |

### Alerting Recommendations
- Alert on 5xx error rate > 0.5% for `/api/incidences/`
- Alert on P95 latency > 1s
- Dashboard: search volume, top query terms, status distribution

---

## Security Considerations

- **Authentication** — Session-based auth required; no anonymous access
- **Authorization** — `IsAdminUser` ensures only staff can search
- **Input validation** — All filter values validated by django-filter and DRF serializers
- **Rate limiting** — 120 requests/minute for authenticated users
- **No SQL injection** — ORM-based queries; no raw SQL
- **UUID PKs** — Prevents ID enumeration

---

## Performance Considerations

### Current Indexes
- `fingerprint` — UNIQUE index (exact lookup)
- `status` — B-tree index
- `first_seen` — B-tree index
- `last_seen` — B-tree index
- `(status, -last_seen)` — Composite index

### Future Optimizations (if needed)
- GIN trigram index on `title` for faster `icontains` (requires Postgres)
- Query result caching with Redis (TTL: 30s)
- Materialized view for aggregated stats
