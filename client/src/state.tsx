import type { RemoteData } from "./utils/remoteData";

export interface State {
  input: string;
  parsedLines: Record<number, RemoteData<string>>;
}

export const initialState: State = {
  input: "",
  parsedLines: {},
};

export type Action =
  | { type: "SET_INPUT"; value: string }
  | {
      type: "UPDATE_PARSED_LINE";
      index: number;
      parsedLine: RemoteData<string>;
    };

export function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "SET_INPUT":
      return { ...state, input: action.value };
    case "UPDATE_PARSED_LINE":
      const parsedLines = {
        ...state.parsedLines,
        [action.index]: action.parsedLine,
      };
      return { ...state, parsedLines };
  }
}
