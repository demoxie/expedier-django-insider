# PR: Implement Incidence Search Feature (Vertical Slice)

## Summary
Implements a complete Incidence Search feature allowing staff users to search and filter incidences by title, fingerprint, status, first_seen, and last_seen date ranges. Includes backend API, frontend UI, tests, and operational readiness artifacts.

---

## Design Decisions

### Backend
1. **django-filter over manual QuerySet chaining** — Declarative, composable, and auto-generates DRF schema documentation. Trade-off: adds a dependency, but it's a mature, widely-adopted library.
2. **UUID primary key** — Prevents enumeration attacks and is safe for external exposure. Trade-off: slightly larger than integer PKs, but negligible for this data volume.
3. **ReadOnlyModelViewSet** — Restricts the API surface to list + retrieve. Write operations belong in a separate, more controlled endpoint.
4. **TextChoices enum for status** — Validates at the Python layer before hitting the DB. Extensible by simply adding new choices.
5. **Composite index on (status, -last_seen)** — Optimizes the most common query pattern (filter by status, order by recency).
6. **Request-level logging** — Every search request is logged with query params, result count, elapsed time, and user ID for observability.

### Frontend
1. **Debounced text search (300ms)** — Reduces API load while keeping the UI responsive.
2. **URL-independent filter state** — Filters live in React state. Extension: sync to URL params for shareable links.
3. **Vanilla CSS with design tokens** — No CSS framework dependency. Full control over the premium dark-mode design.
4. **Error handling with retry** — Auth errors are surfaced clearly with a retry button.

---

## Trade-offs

| Decision | Benefit | Cost |
|----------|---------|------|
| SQLite default (Postgres via env) | Zero-config local dev | No trigram GIN index for title search |
| Session auth (not JWT) | Leverages Django admin login | Requires cookie-based auth; no stateless API |
| Client-side debounce only | Simple implementation | No server-side query caching |
| Page-based pagination | DRF default, well-understood | Less efficient than cursor-based for large datasets |

---

## Hypothesis Tree

If the search feature is slow or produces incorrect results, investigate in this order:

1. **Query performance** → Check if indexes are being used (EXPLAIN ANALYZE)
   - If full table scan → ensure `db_index=True` fields and composite index exist
   - If text search is slow → consider adding Postgres GIN trigram index
2. **Filter correctness** → Run the 13 filter-specific tests
   - If date range is wrong → check timezone handling (all times are UTC)
   - If status filter returns unexpected results → verify enum validation
3. **API latency** → Check the structured log (elapsed_ms field)
   - If > 500ms → profile the ORM query, check N+1 issues
   - If network latency → check CORS, proxy config
4. **Frontend display** → Check browser console for JS errors
   - If data loads but table is empty → check response shape (count, results)
   - If filters don't trigger → check debounce timer, onChange handlers

---

## First-Hour Plan (Post-Deploy)

| Time | Action |
|------|--------|
| 0–5 min | Verify deployment: hit `/api/incidences/` with curl, check 200 + correct JSON shape |
| 5–10 min | Verify auth: confirm 403 for unauthenticated, 200 for staff |
| 10–20 min | Smoke test each filter parameter individually via the UI |
| 20–30 min | Check structured logs for query latency baseline |
| 30–45 min | Test with realistic data volume (1000+ records), verify pagination |
| 45–60 min | Monitor error rates, check for any unexpected 500s |

---

## Extension Strategy

1. **Full-text search** → Replace `icontains` with Postgres `SearchVector` + `SearchRank` for relevance scoring
2. **Cursor-based pagination** → Swap to `CursorPagination` for consistent performance on large datasets
3. **URL-synced filters** → Sync React filter state to `window.location.search` for shareable links
4. **Export to CSV** → Add a `/api/incidences/export/` endpoint with streaming response
5. **Real-time updates** → Add WebSocket channel for live incidence feed
6. **Advanced analytics** → Add aggregation endpoint for status distribution, trend charts

---

## Launch Criteria

- [ ] All 33 backend tests pass
- [ ] All 13 frontend tests pass
- [ ] Staff-only access enforced (manual verification)
- [ ] All 7 filter parameters work correctly
- [ ] Page load time < 2s for 1000 records
- [ ] Structured logging captures all search requests
- [ ] No console errors in the frontend

---

## 48-Hour Follow-Up Plan

### Day 1 (0–24h)
- Monitor search latency P50/P95 from structured logs
- Check for any 500 errors in the Django error log
- Verify no unexpected query patterns (full table scans)
- Collect initial user feedback on filter UX

### Day 2 (24–48h)
- Review query patterns and add indexes if needed
- Address any bug reports from Day 1
- Document any edge cases discovered in production
- Plan next iteration (full-text search, export, URL sync)

### Rollback Plan
- Feature is additive (new endpoint + new UI page) — no existing functionality is modified
- Rollback: revert the PR, run `python manage.py migrate incidences zero` to remove the table
- Blast radius: limited to staff users only; no customer-facing impact
