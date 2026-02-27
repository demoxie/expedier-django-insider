/**
 * API service for incidence search.
 * Handles request building, error handling, and response parsing.
 */
import axios from 'axios';

const api = axios.create({
    baseURL: '/api',
    timeout: 15000,
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true,
});

/**
 * Build query params object from filter state, omitting empty values.
 */
function buildParams(filters) {
    const params = {};
    if (filters.q?.trim()) params.q = filters.q.trim();
    if (filters.fingerprint?.trim()) params.fingerprint = filters.fingerprint.trim();
    if (filters.status) params.status = filters.status;
    if (filters.first_seen_from) params.first_seen_from = filters.first_seen_from;
    if (filters.first_seen_to) params.first_seen_to = filters.first_seen_to;
    if (filters.last_seen_from) params.last_seen_from = filters.last_seen_from;
    if (filters.last_seen_to) params.last_seen_to = filters.last_seen_to;
    if (filters.page && filters.page > 1) params.page = filters.page;
    if (filters.ordering) params.ordering = filters.ordering;
    return params;
}

/**
 * Fetch incidences with the given filters.
 * @param {Object} filters - Filter state from the search page.
 * @returns {{ count, next, previous, results }}
 */
export async function fetchIncidences(filters = {}) {
    const params = buildParams(filters);
    const response = await api.get('/incidences/', { params });
    return response.data;
}

export default api;
