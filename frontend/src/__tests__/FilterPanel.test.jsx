import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import FilterPanel from '../components/FilterPanel';

const defaultFilters = {
    q: '',
    fingerprint: '',
    status: '',
    first_seen_from: '',
    first_seen_to: '',
    last_seen_from: '',
    last_seen_to: '',
};

describe('FilterPanel', () => {
    it('renders all filter controls', () => {
        render(
            <FilterPanel filters={defaultFilters} onChange={vi.fn()} onClear={vi.fn()} loading={false} />
        );

        expect(screen.getByLabelText(/search title/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/fingerprint/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/status/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/first seen from/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/first seen to/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/last seen from/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/last seen to/i)).toBeInTheDocument();
    });

    it('calls onChange when text search input changes', () => {
        const onChange = vi.fn();
        render(
            <FilterPanel filters={defaultFilters} onChange={onChange} onClear={vi.fn()} loading={false} />
        );

        fireEvent.change(screen.getByLabelText(/search title/i), {
            target: { value: 'TypeError' },
        });

        expect(onChange).toHaveBeenCalledWith('q', 'TypeError');
    });

    it('calls onChange when status select changes', () => {
        const onChange = vi.fn();
        render(
            <FilterPanel filters={defaultFilters} onChange={onChange} onClear={vi.fn()} loading={false} />
        );

        fireEvent.change(screen.getByLabelText(/status/i), {
            target: { value: 'resolved' },
        });

        expect(onChange).toHaveBeenCalledWith('status', 'resolved');
    });

    it('calls onClear when Clear All button is clicked', () => {
        const onClear = vi.fn();
        render(
            <FilterPanel filters={defaultFilters} onChange={vi.fn()} onClear={onClear} loading={false} />
        );

        fireEvent.click(screen.getByText(/clear all/i));
        expect(onClear).toHaveBeenCalledOnce();
    });

    it('disables inputs when loading', () => {
        render(
            <FilterPanel filters={defaultFilters} onChange={vi.fn()} onClear={vi.fn()} loading={true} />
        );

        expect(screen.getByLabelText(/search title/i)).toBeDisabled();
        expect(screen.getByLabelText(/fingerprint/i)).toBeDisabled();
        expect(screen.getByLabelText(/status/i)).toBeDisabled();
    });

    it('renders status options', () => {
        render(
            <FilterPanel filters={defaultFilters} onChange={vi.fn()} onClear={vi.fn()} loading={false} />
        );

        const select = screen.getByLabelText(/status/i);
        expect(select.options).toHaveLength(4); // All + 3 statuses
    });
});
