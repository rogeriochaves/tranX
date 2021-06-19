import React, { useReducer } from "react";
import ReactDOM from "react-dom";
import Editor from "./Editor";
import { reducer, initialState } from "./state";

const App = () => {
  const [state, dispatch] = useReducer(reducer, initialState);

  return <Editor state={state} dispatch={dispatch} />;
};

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("main")
);
