import React from 'react';

/**
 * Pagination — page navigation controls.
 *
 * @param {{ page: number, count: number, pageSize: number, onPageChange: (page) => void, loading: boolean }} props
 */
export default function Pagination({ page, count, pageSize = 25, onPageChange, loading }) {
    const totalPages = Math.ceil(count / pageSize);

    if (totalPages <= 1) return null;

    const pages = [];
    const maxVisible = 5;
    let startPage = Math.max(1, page - Math.floor(maxVisible / 2));
    let endPage = Math.min(totalPages, startPage + maxVisible - 1);

    if (endPage - startPage + 1 < maxVisible) {
        startPage = Math.max(1, endPage - maxVisible + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
    }

    return (
        <div className="pagination" id="pagination">
            <div className="pagination__info">
                Showing {Math.min((page - 1) * pageSize + 1, count)}–{Math.min(page * pageSize, count)} of{' '}
                <strong>{count}</strong> results
            </div>
            <div className="pagination__controls">
                <button
                    className="pagination__btn"
                    onClick={() => onPageChange(1)}
                    disabled={page <= 1 || loading}
                    id="page-first"
                    title="First page"
                >
                    ««
                </button>
                <button
                    className="pagination__btn"
                    onClick={() => onPageChange(page - 1)}
                    disabled={page <= 1 || loading}
                    id="page-prev"
                    title="Previous page"
                >
                    «
                </button>

                {startPage > 1 && <span className="pagination__ellipsis">…</span>}

                {pages.map((p) => (
                    <button
                        key={p}
                        className={`pagination__btn ${p === page ? 'pagination__btn--active' : ''}`}
                        onClick={() => onPageChange(p)}
                        disabled={loading}
                        id={`page-${p}`}
                    >
                        {p}
                    </button>
                ))}

                {endPage < totalPages && <span className="pagination__ellipsis">…</span>}

                <button
                    className="pagination__btn"
                    onClick={() => onPageChange(page + 1)}
                    disabled={page >= totalPages || loading}
                    id="page-next"
                    title="Next page"
                >
                    »
                </button>
                <button
                    className="pagination__btn"
                    onClick={() => onPageChange(totalPages)}
                    disabled={page >= totalPages || loading}
                    id="page-last"
                    title="Last page"
                >
                    »»
                </button>
            </div>
        </div>
    );
}
