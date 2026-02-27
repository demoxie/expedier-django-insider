import React from 'react';

const STATUS_OPTIONS = [
    { value: '', label: 'All Statuses' },
    { value: 'unresolved', label: 'Unresolved' },
    { value: 'resolved', label: 'Resolved' },
    { value: 'ignored', label: 'Ignored' },
];

/**
 * FilterPanel — search and filter controls for incidences.
 *
 * @param {{ filters: Object, onChange: (key, value) => void, onClear: () => void, loading: boolean }} props
 */
export default function FilterPanel({ filters, onChange, onClear, loading }) {
    return (
        <div className="filter-panel" id="filter-panel">
            <div className="filter-panel__header">
                <h2 className="filter-panel__title">
                    <span className="filter-panel__icon">🔍</span>
                    Filters
                </h2>
                <button
                    className="btn btn--ghost"
                    onClick={onClear}
                    disabled={loading}
                    id="clear-filters-btn"
                    type="button"
                >
                    Clear All
                </button>
            </div>

            <div className="filter-panel__grid">
                {/* Text search */}
                <div className="filter-group filter-group--wide">
                    <label className="filter-group__label" htmlFor="filter-q">
                        Search Title
                    </label>
                    <input
                        id="filter-q"
                        type="text"
                        className="filter-group__input"
                        placeholder="e.g. TypeError, connection timeout…"
                        value={filters.q || ''}
                        onChange={(e) => onChange('q', e.target.value)}
                        disabled={loading}
                    />
                </div>

                {/* Fingerprint */}
                <div className="filter-group">
                    <label className="filter-group__label" htmlFor="filter-fingerprint">
                        Fingerprint
                    </label>
                    <input
                        id="filter-fingerprint"
                        type="text"
                        className="filter-group__input"
                        placeholder="Exact match…"
                        value={filters.fingerprint || ''}
                        onChange={(e) => onChange('fingerprint', e.target.value)}
                        disabled={loading}
                    />
                </div>

                {/* Status */}
                <div className="filter-group">
                    <label className="filter-group__label" htmlFor="filter-status">
                        Status
                    </label>
                    <select
                        id="filter-status"
                        className="filter-group__select"
                        value={filters.status || ''}
                        onChange={(e) => onChange('status', e.target.value)}
                        disabled={loading}
                    >
                        {STATUS_OPTIONS.map((opt) => (
                            <option key={opt.value} value={opt.value}>
                                {opt.label}
                            </option>
                        ))}
                    </select>
                </div>

                {/* First Seen From */}
                <div className="filter-group">
                    <label className="filter-group__label" htmlFor="filter-first-seen-from">
                        First Seen From
                    </label>
                    <input
                        id="filter-first-seen-from"
                        type="date"
                        className="filter-group__input"
                        value={filters.first_seen_from || ''}
                        onChange={(e) => onChange('first_seen_from', e.target.value)}
                        disabled={loading}
                    />
                </div>

                {/* First Seen To */}
                <div className="filter-group">
                    <label className="filter-group__label" htmlFor="filter-first-seen-to">
                        First Seen To
                    </label>
                    <input
                        id="filter-first-seen-to"
                        type="date"
                        className="filter-group__input"
                        value={filters.first_seen_to || ''}
                        onChange={(e) => onChange('first_seen_to', e.target.value)}
                        disabled={loading}
                    />
                </div>

                {/* Last Seen From */}
                <div className="filter-group">
                    <label className="filter-group__label" htmlFor="filter-last-seen-from">
                        Last Seen From
                    </label>
                    <input
                        id="filter-last-seen-from"
                        type="date"
                        className="filter-group__input"
                        value={filters.last_seen_from || ''}
                        onChange={(e) => onChange('last_seen_from', e.target.value)}
                        disabled={loading}
                    />
                </div>

                {/* Last Seen To */}
                <div className="filter-group">
                    <label className="filter-group__label" htmlFor="filter-last-seen-to">
                        Last Seen To
                    </label>
                    <input
                        id="filter-last-seen-to"
                        type="date"
                        className="filter-group__input"
                        value={filters.last_seen_to || ''}
                        onChange={(e) => onChange('last_seen_to', e.target.value)}
                        disabled={loading}
                    />
                </div>
            </div>
        </div>
    );
}
