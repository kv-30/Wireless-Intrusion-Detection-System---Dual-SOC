import axios from "axios";
import {
  buildRangeParams,
  getSecondsFromRange,
  resolveApiBase,
} from "../utils/endpoints";

const API_BASE = resolveApiBase();

export const fetchHistoricalData = async (layer, start, end, macFilter) => {
  try {
    const seconds = getSecondsFromRange(start, end, 600);
    const resp = await axios.get(`${API_BASE}/${layer}`, {
      params: {
        ...buildRangeParams(seconds, start, end),
        mac: macFilter || ""
      }
    });
    return resp.data;
  } catch (err) {
    console.error("API fetch error:", err);
    return [];
  }
};