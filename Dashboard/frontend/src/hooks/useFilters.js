import { useState } from "react";

export const useFilters = () => {
  const [filters, setFilters] = useState({ mac: "", start: null, end: null });

  const updateFilter = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  return { filters, updateFilter };
};