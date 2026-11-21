import axios from "axios";
import type { Investigation } from "../types";
import { investigations } from "../data/demo";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "",
  timeout: 8000
});

// Demo-first adapter: without VITE_API_BASE_URL, the app remains fully usable.
// Backend contract: GET /api/investigations/:alertId -> Investigation JSON.
export async function getInvestigation(alertId: string): Promise<Investigation> {
  const baseURL = import.meta.env.VITE_API_BASE_URL;
  if (baseURL) {
    const response = await api.get<Investigation>(`/api/investigations/${alertId}`);
    return response.data;
  }
  const result = investigations.find((item) => item.alertId === alertId);
  if (!result) throw new Error(`No demo investigation found for ${alertId}`);
  return result;
}