import { render } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect } from "chai";
import Editor from "./Editor";
import React, { useReducer } from "react";
import { reducer, initialState } from "./state";

function TestWrapper() {
  const [state, dispatch] = useReducer(reducer, initialState);
  return <Editor state={state} dispatch={dispatch} />;
}

describe("<Editor>", () => {
  it("displays the text typed on the canvas", async () => {
    const wrapper = render(<TestWrapper />);

    const canvas = (await wrapper.findByTestId(
      "canvas-textarea"
    )) as HTMLInputElement;

    userEvent.type(canvas, "set x to 1{enter}x + 1");
    expect(canvas.value).contains("set x to 1\nx + 1");
  });
});
