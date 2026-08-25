import { PresetPattern } from "./types";

const API_BASE = "http://127.0.0.1:8000/api";

export async function fetchPresetPatterns(): Promise<PresetPattern[]> {
  const response = await fetch(`${API_BASE}/patterns`);
  if (!response.ok) {
    throw new Error(`Failed to fetch patterns: ${response.statusText}`);
  }
  return response.json();
}
