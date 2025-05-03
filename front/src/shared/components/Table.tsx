'use client';

import { Calendar } from 'primereact/calendar';
import React, { useState, useMemo } from 'react';

export type Column<T> = {
  key: keyof T;
  header: string;
  filter?: {
    type: string;
    mask?: string;
    validation?: {
      minLength?: { value: number; message: string };
      maxLength?: { value: number; message: string };
      pattern?: { value: RegExp; message: string };
      custom?: (value: unknown) => string | true;
    };
  };
  render?: (value: T[keyof T], row: T) => React.ReactNode;
};

type TableProps<T> = {
  columns: Column<T>[];
  data: T[] | null;
  filter?: boolean;
  onClickRow?: (row: T) => void;
};

export function Table<T extends object>({
  columns,
  data,
  filter = false,
  onClickRow
}: TableProps<T>) {
  const [filters, setFilters] = useState<Record<string, string | number | Date>>({});

  const handleFilterChange = (key: keyof T, value: string | number | Date) => {
    setFilters((prev) => ({
      ...prev,
      [key as string]: value
    }));
  };

  const filteredData = useMemo(() => {
    if (!filter || !data) return data;
    return data.filter((row) =>
      columns.every((col) => {
        const filterValue = filters[col.key as string];
        if (!filterValue) return true;

        const cellValue = row[col.key];
        if (col.filter?.type === 'calendar' && filterValue instanceof Date) {
          const rowDate = new Date(cellValue as string);
          return (
            rowDate.toDateString() === (filterValue as Date).toDateString()
          );
        }

        const cellString = String(cellValue ?? '').toLowerCase();
        const filterString = String(filterValue ?? '').toLowerCase();
        return cellString.includes(filterString);
      })
    );
  }, [filters, data, columns, filter]);

  const hasData = Array.isArray(filteredData) && filteredData.length > 0;

  return (
    <div className="overflow-x-auto w-full">
      <table className="min-w-full border-collapse border border-gray-400 shadow-sm">
        <thead className="bg-gray-100">
          <tr>
            {columns.map((col) => (
              <th
                key={col.key.toString()}
                className="px-4 py-2 text-left text-xs font-semibold text-gray-700 border border-gray-300"
              >
                {col.header}
                {filter && ['text', 'number', 'email', 'password'].includes(col.filter?.type || '') && (
                  <input
                    type={col.filter?.type}
                    className="mt-1 w-full text-xs bg-white border-stone-500 rounded-md p-1"
                    value={filters[col.key as string] || ''}
                    onChange={(e) => handleFilterChange(col.key, e.target.value)}
                  />
                )}
                {filter && col.filter?.type === 'calendar' && (
                  <Calendar
                    value={
                      filters[col.key as string]
                        ? new Date(filters[col.key as string])
                        : null
                    }
                    onChange={(e) =>
                      handleFilterChange(col.key, e.value as Date)
                    }
                    className="mt-1 w-full text-xs"
                    dateFormat="dd/mm/yy"
                  />
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {!hasData ? (
            <tr>
              <td
                colSpan={columns.length}
                className="px-4 py-4 text-center text-gray-500"
              >
                Нет Данных.
              </td>
            </tr>
          ) : (
            filteredData.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className="hover:bg-gray-50 transition-colors cursor-pointer"
                onClick={() => onClickRow?.(row)}
              >
                {columns.map((col) => (
                  <td
                    key={col.key.toString()}
                    className="px-4 py-2 text-xs border border-gray-300"
                  >
                    {col.render
                      ? col.render(row[col.key], row)
                      : String(row[col.key])}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
