import type { queries } from "@testing-library/dom";
import { render, RenderResult } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect } from "./utils/testing";
import React, { useReducer } from "react";
import Editor from "./Editor";
import { initialState, reducer } from "./state";
import { SinonFakeTimers, SinonStub, useFakeTimers } from "sinon";
import axios from "axios";
import sleep from "./utils/sleep";

function TestWrapper() {
  const [state, dispatch] = useReducer(reducer, initialState);
  return <Editor state={state} dispatch={dispatch} />;
}

describe("<Editor>", () => {
  const axiosGET = axios.get as SinonStub;
  let wrapper: RenderResult<typeof queries, HTMLElement>;
  let canvas: HTMLInputElement;
  let clock: SinonFakeTimers;

  beforeEach(async () => {
    clock = useFakeTimers();

    wrapper = render(<TestWrapper />);

    canvas = (await wrapper.findByTestId(
      "canvas-textarea"
    )) as HTMLInputElement;
  });

  afterEach(() => {
    axiosGET.reset();
    clock.restore();
  });

  it("displays the text typed on the canvas", async () => {
    axiosGET.returns(Promise.resolve({ data: "" }));

    userEvent.type(canvas, "set x to 1{enter}x + 1");
    expect(canvas.value).contains("set x to 1\nx + 1");
  });

  it("renders the result from the backend for each line", async () => {
    axiosGET.returns(Promise.resolve({ data: "1 + 1" }));

    userEvent.type(canvas, "one plus one{enter}");

    clock.tick(500); // input debounce time

    const results = await wrapper.findByTestId("results");

    expect(axiosGET).calledWith("/api/parse", {
      params: { code: "one plus one" },
    });
    expect(results.textContent).contains("1 + 1");
  });

  it("has a debounce when typing", async () => {
    axiosGET.returns(Promise.resolve({ data: "1 +" }));
    userEvent.type(canvas, "one plus");

    expect(axiosGET).callCount(0);
    clock.tick(500);
    expect(axiosGET).callCount(1);
    userEvent.type(canvas, " one");
    clock.tick(500);
    expect(axiosGET).callCount(2);
  });

  it("does not make a call to parse empty lines", async () => {
    axiosGET.returns(Promise.resolve({ data: "1 +" }));
    userEvent.type(canvas, "one plus one{enter} {enter}two plus two");

    clock.tick(500);

    expect(axiosGET).callCount(2);
    expect(axiosGET).calledWith("/api/parse", {
      params: { code: "one plus one" },
    });
    expect(axiosGET).calledWith("/api/parse", {
      params: { code: "two plus two" },
    });
  });

  it("uses only the last requested parsing if there is a race condition", async () => {
    axiosGET.onFirstCall().callsFake(async () => {
      await sleep(800);
      return { data: "first result" };
    });
    axiosGET.onSecondCall().callsFake(async () => {
      await sleep(100);
      return { data: "second result" };
    });

    userEvent.type(canvas, "one plus");
    clock.tick(500);
    userEvent.type(canvas, " one");
    clock.tick(600);

    let results = await wrapper.findByTestId("results");
    expect(results.textContent).contains("second result");

    clock.tick(200); // first result loads after the second

    results = await wrapper.findByTestId("results");
    expect(results.textContent).contains("second result");
    expect(results.textContent).not.contains("first result");
  });

  it("shows the results for each line typed", async () => {
    axiosGET.onFirstCall().returns(Promise.resolve({ data: "1 + 1" }));
    axiosGET.onSecondCall().returns(Promise.resolve({ data: "2 + 2" }));

    userEvent.type(canvas, "one plus one{enter}two plus two");

    clock.tick(500); // input debounce time

    const results = await wrapper.findByTestId("results");
    expect(results.textContent).contains("1 + 1");
    expect(results.textContent).contains("2 + 2");
  });
});
