import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import IncidenceTable from '../components/IncidenceTable';

const mockIncidences = [
    {
        id: '1',
        title: 'TypeError in payment module',
        fingerprint: 'fp-001',
        status: 'unresolved',
        status_display: 'Unresolved',
        first_seen: '2025-02-10T10:00:00Z',
        last_seen: '2025-02-26T12:00:00Z',
    },
    {
        id: '2',
        title: 'Connection timeout on dashboard',
        fingerprint: 'fp-002',
        status: 'resolved',
        status_display: 'Resolved',
        first_seen: '2025-02-15T08:00:00Z',
        last_seen: '2025-02-27T09:00:00Z',
    },
];

describe('IncidenceTable', () => {
    it('renders table rows for each incidence', () => {
        render(
            <IncidenceTable
                incidences={mockIncidences}
                loading={false}
                ordering="-last_seen"
                onSort={vi.fn()}
            />
        );

        expect(screen.getByText('TypeError in payment module')).toBeInTheDocument();
        expect(screen.getByText('Connection timeout on dashboard')).toBeInTheDocument();
    });

    it('renders column headers', () => {
        render(
            <IncidenceTable
                incidences={mockIncidences}
                loading={false}
                ordering="-last_seen"
                onSort={vi.fn()}
            />
        );

        expect(screen.getByText('Title')).toBeInTheDocument();
        expect(screen.getByText('Fingerprint')).toBeInTheDocument();
        expect(screen.getByText('Status')).toBeInTheDocument();
        expect(screen.getByText('First Seen')).toBeInTheDocument();
        expect(screen.getByText('Last Seen')).toBeInTheDocument();
    });

    it('renders status badges', () => {
        render(
            <IncidenceTable
                incidences={mockIncidences}
                loading={false}
                ordering="-last_seen"
                onSort={vi.fn()}
            />
        );

        expect(screen.getByText('Unresolved')).toHaveClass('badge--unresolved');
        expect(screen.getByText('Resolved')).toHaveClass('badge--resolved');
    });

    it('shows loading state', () => {
        render(
            <IncidenceTable incidences={[]} loading={true} ordering="-last_seen" onSort={vi.fn()} />
        );

        expect(screen.getByText(/loading incidences/i)).toBeInTheDocument();
    });

    it('shows empty state when no results', () => {
        render(
            <IncidenceTable incidences={[]} loading={false} ordering="-last_seen" onSort={vi.fn()} />
        );

        expect(screen.getByText(/no incidences found/i)).toBeInTheDocument();
    });

    it('calls onSort when sortable column header is clicked', () => {
        const onSort = vi.fn();
        render(
            <IncidenceTable
                incidences={mockIncidences}
                loading={false}
                ordering="-last_seen"
                onSort={onSort}
            />
        );

        fireEvent.click(screen.getByText('Title'));
        expect(onSort).toHaveBeenCalledWith('title');
    });

    it('renders fingerprint as code element', () => {
        render(
            <IncidenceTable
                incidences={mockIncidences}
                loading={false}
                ordering="-last_seen"
                onSort={vi.fn()}
            />
        );

        const fpElements = screen.getAllByText(/fp-00/);
        fpElements.forEach((el) => {
            expect(el.tagName).toBe('CODE');
        });
    });
});
