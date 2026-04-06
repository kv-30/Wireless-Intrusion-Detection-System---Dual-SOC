import { useState, useEffect } from "react";
import axios from "axios";
import {
  buildRangeParams,
  getSecondsFromRange,
  resolveApiBase,
} from "../utils/endpoints";

const API_BASE = resolveApiBase();

export const useHistoricalData = (layer, start, end) => {
  const [data, setData] = useState([]);
  useEffect(() => {
    if (!start || !end) return;
    const seconds = getSecondsFromRange(start, end, 600);
    const params = new URLSearchParams(buildRangeParams(seconds, start, end));
    axios.get(`${API_BASE}/${layer}?${params.toString()}`)
      .then(res => setData(res.data))
      .catch(console.error);
  }, [layer, start, end]);
  return data;
};