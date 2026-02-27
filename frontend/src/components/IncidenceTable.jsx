import React from 'react';

const STATUS_BADGE_CLASS = {
    unresolved: 'badge badge--unresolved',
    resolved: 'badge badge--resolved',
    ignored: 'badge badge--ignored',
};

/**
 * Format an ISO date string into a readable local format.
 */
function formatDate(isoString) {
    if (!isoString) return '—';
    const d = new Date(isoString);
    return d.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

/**
 * IncidenceTable — displays search results in a table.
 *
 * @param {{ incidences: Array, loading: boolean, ordering: string, onSort: (field) => void }} props
 */
export default function IncidenceTable({ incidences, loading, ordering, onSort }) {
    const columns = [
        { key: 'title', label: 'Title', sortable: true },
        { key: 'fingerprint', label: 'Fingerprint', sortable: false },
        { key: 'status', label: 'Status', sortable: true },
        { key: 'first_seen', label: 'First Seen', sortable: true },
        { key: 'last_seen', label: 'Last Seen', sortable: true },
    ];

    function getSortIndicator(key) {
        if (!ordering) return '';
        if (ordering === key) return ' ↑';
        if (ordering === `-${key}`) return ' ↓';
        return '';
    }

    if (loading) {
        return (
            <div className="table-container" id="incidence-table">
                <div className="table-loading">
                    <div className="spinner" />
                    <p>Loading incidences…</p>
                </div>
            </div>
        );
    }

    if (!incidences || incidences.length === 0) {
        return (
            <div className="table-container" id="incidence-table">
                <div className="table-empty">
                    <span className="table-empty__icon">📭</span>
                    <h3>No incidences found</h3>
                    <p>Try adjusting your filters or search terms.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="table-container" id="incidence-table">
            <table className="incidence-table">
                <thead>
                    <tr>
                        {columns.map((col) => (
                            <th
                                key={col.key}
                                className={col.sortable ? 'sortable' : ''}
                                onClick={() => col.sortable && onSort(col.key)}
                                role={col.sortable ? 'button' : undefined}
                                tabIndex={col.sortable ? 0 : undefined}
                                id={`col-${col.key}`}
                            >
                                {col.label}
                                {col.sortable && (
                                    <span className="sort-indicator">
                                        {getSortIndicator(col.key)}
                                    </span>
                                )}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {incidences.map((inc) => (
                        <tr key={inc.id} className="incidence-row" id={`row-${inc.id}`}>
                            <td className="cell-title" title={inc.title}>
                                {inc.title}
                            </td>
                            <td className="cell-fingerprint">
                                <code>{inc.fingerprint}</code>
                            </td>
                            <td className="cell-status">
                                <span className={STATUS_BADGE_CLASS[inc.status] || 'badge'}>
                                    {inc.status_display || inc.status}
                                </span>
                            </td>
                            <td className="cell-date">{formatDate(inc.first_seen)}</td>
                            <td className="cell-date">{formatDate(inc.last_seen)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
