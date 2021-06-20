import type { queries } from "@testing-library/dom";
import { render, RenderResult } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect } from "./utils/testing";
import React, { useReducer } from "react";
import Editor from "./Editor";
import { initialState, reducer } from "./state";
import type { SinonStub } from "sinon";
import axios from "axios";

function TestWrapper() {
  const [state, dispatch] = useReducer(reducer, initialState);
  return <Editor state={state} dispatch={dispatch} />;
}

describe("<Editor>", () => {
  const axiosGET = axios.get as SinonStub;
  let wrapper: RenderResult<typeof queries, HTMLElement>;
  let canvas: HTMLInputElement;

  beforeEach(async () => {
    wrapper = render(<TestWrapper />);

    canvas = (await wrapper.findByTestId(
      "canvas-textarea"
    )) as HTMLInputElement;
  });

  it("displays the text typed on the canvas", async () => {
    axiosGET.returns(Promise.resolve({ data: "" }));

    userEvent.type(canvas, "set x to 1{enter}x + 1");
    expect(canvas.value).contains("set x to 1\nx + 1");
  });

  it("renders the result from the backend for each line", async () => {
    axiosGET.returns(Promise.resolve({ data: "1 + 1" }));

    userEvent.type(canvas, "one plus one{enter}");

    const results = await wrapper.findByTestId("results");

    expect(axiosGET).calledWith("/api/parse", { params: { code: "one plus one" } });
    expect(results.textContent).contains("1 + 1");
  });
});
