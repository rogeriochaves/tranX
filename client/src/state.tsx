export interface State {
  text: string;
  results: Array<string>;
}

export const initialState: State = {
  text: "",
  results: [],
};

export type Action =
  | { type: "SET_TEXT"; value: string }
  | { type: "UPDATE_RESULTS"; results: Array<string> };

export function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "SET_TEXT":
      return { ...state, text: action.value };
    case "UPDATE_RESULTS":
      return { ...state, results: action.results };
  }
}
