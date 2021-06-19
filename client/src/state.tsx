export interface State {
  text: string;
}

export const initialState: State = {
  text: "",
};

export type Action = { type: "SET_TEXT"; value: string };

export function reducer(_state: State, action: Action): State {
  switch (action.type) {
    case "SET_TEXT":
      return { text: action.value };
  }
}
