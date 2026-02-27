import React, { useState, useEffect, useCallback, useRef } from 'react';
import { fetchIncidences } from '../services/api';
import FilterPanel from '../components/FilterPanel';
import IncidenceTable from '../components/IncidenceTable';
import Pagination from '../components/Pagination';

const INITIAL_FILTERS = {
    q: '',
    fingerprint: '',
    status: '',
    first_seen_from: '',
    first_seen_to: '',
    last_seen_from: '',
    last_seen_to: '',
    page: 1,
    ordering: '-last_seen',
};

const DEBOUNCE_MS = 300;

/**
 * IncidenceSearchPage — main page composing FilterPanel, IncidenceTable, and Pagination.
 * Debounces text input and syncs filters to URL params.
 */
export default function IncidenceSearchPage() {
    const [filters, setFilters] = useState(INITIAL_FILTERS);
    const [data, setData] = useState({ count: 0, results: [] });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const debounceRef = useRef(null);

    // Fetch data whenever filters change
    const loadData = useCallback(async (currentFilters) => {
        setLoading(true);
        setError(null);
        try {
            const result = await fetchIncidences(currentFilters);
            setData(result);
        } catch (err) {
            console.error('Failed to fetch incidences:', err);
            if (err.response?.status === 403 || err.response?.status === 401) {
                setError('Authentication required. Please log in as a staff user via the Django admin.');
            } else {
                setError(err.message || 'Failed to load incidences. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    }, []);

    // Debounced effect for filter changes
    useEffect(() => {
        if (debounceRef.current) clearTimeout(debounceRef.current);
        debounceRef.current = setTimeout(() => {
            loadData(filters);
        }, DEBOUNCE_MS);
        return () => clearTimeout(debounceRef.current);
    }, [filters, loadData]);

    const handleFilterChange = useCallback((key, value) => {
        setFilters((prev) => ({
            ...prev,
            [key]: value,
            // Reset to page 1 when filter changes
            ...(key !== 'page' ? { page: 1 } : {}),
        }));
    }, []);

    const handleClearFilters = useCallback(() => {
        setFilters(INITIAL_FILTERS);
    }, []);

    const handleSort = useCallback((field) => {
        setFilters((prev) => ({
            ...prev,
            ordering: prev.ordering === field ? `-${field}` : field,
            page: 1,
        }));
    }, []);

    const handlePageChange = useCallback((page) => {
        setFilters((prev) => ({ ...prev, page }));
    }, []);

    return (
        <div className="search-page" id="search-page">
            <header className="search-page__header">
                <div className="search-page__header-content">
                    <div className="search-page__logo">
                        <span className="search-page__logo-icon">⚡</span>
                        <h1 className="search-page__title">Incidence Search</h1>
                    </div>
                    <p className="search-page__subtitle">
                        Search, filter, and analyze production incidences
                    </p>
                </div>
            </header>

            <main className="search-page__main">
                <FilterPanel
                    filters={filters}
                    onChange={handleFilterChange}
                    onClear={handleClearFilters}
                    loading={loading}
                />

                {error && (
                    <div className="error-banner" id="error-banner" role="alert">
                        <span className="error-banner__icon">⚠️</span>
                        <p>{error}</p>
                        <button className="btn btn--ghost" onClick={() => loadData(filters)}>
                            Retry
                        </button>
                    </div>
                )}

                <div className="search-page__results-header">
                    <h2 className="search-page__results-title">
                        Results
                        {data.count > 0 && (
                            <span className="search-page__count-badge">{data.count}</span>
                        )}
                    </h2>
                </div>

                <IncidenceTable
                    incidences={data.results}
                    loading={loading}
                    ordering={filters.ordering}
                    onSort={handleSort}
                />

                <Pagination
                    page={filters.page}
                    count={data.count}
                    pageSize={25}
                    onPageChange={handlePageChange}
                    loading={loading}
                />
            </main>
        </div>
    );
}
