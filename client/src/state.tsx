import { NotAsked, RemoteData } from "./utils/remoteData";

export interface Line {
  input: string;
  parsed: RemoteData<string>;
}

export interface State {
  lines: Array<Line>;
  output: string;
}

export const initialState: State = {
  lines: [],
  output: "",
};

export type Action =
  | { type: "SET_INPUT"; value: string }
  | {
      type: "UPDATE_PARSED_LINE";
      index: number;
      parsed: RemoteData<string>;
    }
  | { type: "SET_OUTPUT"; value: string };

export function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "SET_INPUT":
      const inputLines = action.value.split("\n");
      return {
        ...state,
        lines: inputLines.map((input, index) => ({
          ...(state.lines[index] || { parsed: NotAsked() }),
          input,
        })),
      };
    case "UPDATE_PARSED_LINE":
      return {
        ...state,
        lines: state.lines.map((line, index) =>
          index == action.index ? { ...line, parsed: action.parsed } : line
        ),
      };
    case "SET_OUTPUT":
      return { ...state, output: action.value };
  }
}
