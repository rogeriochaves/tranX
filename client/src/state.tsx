import type { RemoteData } from "./utils/remoteData";

export interface State {
  text: string;
  results: Array<RemoteData<string> | undefined>;
}

export const initialState: State = {
  text: "",
  results: [],
};

export type Action =
  | { type: "SET_TEXT"; value: string }
  | { type: "UPDATE_RESULTS"; index: number; result: RemoteData<string> };

export function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "SET_TEXT":
      return { ...state, text: action.value };
    case "UPDATE_RESULTS":
      const results = [...state.results];
      results[action.index] = action.result;
      return { ...state, results };
  }
}
