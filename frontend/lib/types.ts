export type BoundaryMode = "toroidal" | "bounded";

export interface PresetPattern {
  id: string;
  name: string;
  category: string;
  description: string;
  cell_count: number;
}

export interface GameState {
  generation: number;
  grid: number[][];
  live_count: number;
  is_running: boolean;
  speed: number;
  width: number;
  height: number;
  boundary_mode: BoundaryMode;
}

// WebSocket Client Command Payloads
export interface WSInitMessage {
  type: "init";
  width?: number;
  height?: number;
  boundary_mode?: BoundaryMode;
  initial_grid?: number[][];
}

export interface WSStartMessage {
  type: "start";
}

export interface WSPauseMessage {
  type: "pause";
}

export interface WSStepMessage {
  type: "step";
}

export interface WSResetMessage {
  type: "reset";
}

export interface WSSetSpeedMessage {
  type: "set_speed";
  speed: number;
}

export interface WSSetCellMessage {
  type: "set_cell";
  x: number;
  y: number;
  alive: boolean;
}

export interface WSLoadPresetMessage {
  type: "load_preset";
  pattern_id: string;
}

export type WSClientMessage =
  | WSInitMessage
  | WSStartMessage
  | WSPauseMessage
  | WSStepMessage
  | WSResetMessage
  | WSSetSpeedMessage
  | WSSetCellMessage
  | WSLoadPresetMessage;

// WebSocket Server Event Payloads
export interface WSServerStateUpdateMessage {
  type: "state_update";
  generation: number;
  grid: number[][];
  live_count: number;
  is_running: boolean;
  speed: number;
}

export interface WSServerErrorMessage {
  type: "error";
  message: string;
}

export type WSServerMessage = WSServerStateUpdateMessage | WSServerErrorMessage;
