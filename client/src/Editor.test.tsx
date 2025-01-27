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
  const axiosPOST = axios.post as SinonStub;

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
    axiosGET.resetHistory();
    axiosPOST.resetHistory();
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

    const parsedCode = await wrapper.findByTestId("parsed-code");

    expect(axiosGET).calledWith("/api/parse", {
      params: { inputLine: "one plus one" },
    });
    expect(parsedCode.textContent).contains("1 + 1");
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

  it("displays loading feedback waiting for backend result", async () => {
    axiosGET.callsFake(async () => {
      await sleep(1000);
      return { data: "1 + 1" };
    });

    userEvent.type(canvas, "one plus one{enter}");

    clock.tick(500); // input debounce time

    let parsedCode = await wrapper.findByTestId("parsed-code");
    expect(parsedCode.textContent).contains("*");

    clock.tick(1000);

    parsedCode = await wrapper.findByTestId("parsed-code");
    expect(parsedCode.textContent).not.contains("*");
    expect(parsedCode.textContent).contains("1 + 1");
  });

  it("displays error when there is one", async () => {
    axiosGET.returns(Promise.reject({ response: { data: "weird input man" } }));

    userEvent.type(canvas, "hasiuehsuiahuisahe{enter}");

    clock.tick(500); // input debounce time

    let parsedCode = await wrapper.findByTestId("parsed-code");
    expect(parsedCode.textContent).contains("parsing error");
  });

  it("does not make a call to parse empty lines", async () => {
    axiosGET.returns(Promise.resolve({ data: "1 +" }));
    userEvent.type(canvas, "one plus one{enter} {enter}two plus two");

    clock.tick(500);

    expect(axiosGET).callCount(2);
    expect(axiosGET).calledWith("/api/parse", {
      params: { inputLine: "one plus one" },
    });
    expect(axiosGET).calledWith("/api/parse", {
      params: { inputLine: "two plus two" },
    });
  });

  it("hides deleted lines", async () => {
    axiosGET.onFirstCall().returns(Promise.resolve({ data: "1 + 1" }));
    axiosGET.onSecondCall().returns(Promise.resolve({ data: "2 + 2" }));
    userEvent.type(canvas, "one plus one{enter}two plus two");

    clock.tick(500);

    let parsedCode = await wrapper.findByTestId("parsed-code");
    expect(parsedCode.textContent).contains("1 + 1");
    expect(parsedCode.textContent).contains("2 + 2");

    canvas.setSelectionRange(12, 25); // selects "\ntwo plus two"
    userEvent.type(canvas, "{backspace}");

    parsedCode = await wrapper.findByTestId("parsed-code");
    expect(parsedCode.textContent).contains("1 + 1");
    expect(parsedCode.textContent).not.contains("2 + 2");
  });

  it("clears emptied lines", async () => {
    axiosGET.onFirstCall().returns(Promise.resolve({ data: "1 + 1" }));
    axiosGET.onSecondCall().returns(Promise.resolve({ data: "2 + 2" }));
    userEvent.type(canvas, "one plus one{enter}two plus two");

    clock.tick(500);

    let parsedCode = await wrapper.findByTestId("parsed-code");
    expect(parsedCode.textContent).contains("1 + 1");
    expect(parsedCode.textContent).contains("2 + 2");

    canvas.setSelectionRange(13, 25); // selects "two plus two" after \n
    userEvent.type(canvas, "{backspace}");

    parsedCode = await wrapper.findByTestId("parsed-code");
    expect(parsedCode.textContent).contains("1 + 1");
    expect(parsedCode.textContent).not.contains("2 + 2");
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

    let parsedCode = await wrapper.findByTestId("parsed-code");
    expect(parsedCode.textContent).contains("second result");

    clock.tick(200); // first result loads after the second

    parsedCode = await wrapper.findByTestId("parsed-code");
    expect(parsedCode.textContent).contains("second result");
    expect(parsedCode.textContent).not.contains("first result");
  });

  it("shows the parsedCode for each line typed", async () => {
    axiosGET.onFirstCall().returns(Promise.resolve({ data: "1 + 1" }));
    axiosGET.onSecondCall().returns(Promise.resolve({ data: "2 + 2" }));

    userEvent.type(canvas, "one plus one{enter}two plus two");

    clock.tick(500); // input debounce time

    const parsedCode = await wrapper.findByTestId("parsed-code");
    expect(parsedCode.textContent).contains("1 + 1");
    expect(parsedCode.textContent).contains("2 + 2");
  });

  it("executes the code when clicking the run button", async () => {
    axiosGET.onFirstCall().returns(Promise.resolve({ data: "foo = 1 + 1" }));
    axiosGET.onSecondCall().returns(Promise.resolve({ data: "print(foo)" }));

    userEvent.type(canvas, "set foo to one plus one{enter}print foo");

    clock.tick(500); // input debounce time

    axiosPOST.returns(Promise.resolve({ data: "2\n" }));

    const runButton = await wrapper.findByTestId("run-code");
    userEvent.click(runButton);

    const output = await wrapper.findByTestId("output");
    expect(output.textContent).contains("2");
    expect(axiosPOST).calledWith("/api/execute", {
      parsedCode: "foo = 1 + 1\nprint(foo)",
    });
  });

  it("disables the run button while there is some line parsing", async () => {
    axiosGET.onFirstCall().callsFake(async () => {
      return { data: "first result" };
    });
    axiosGET.onSecondCall().callsFake(async () => {
      await sleep(1000);
      return { data: "parsing result" };
    });

    userEvent.type(canvas, "set foo to one plus one{enter}print foo");

    clock.tick(500); // input debounce time

    const runButton = await wrapper.findByTestId("run-code");
    userEvent.click(runButton);
    expect(axiosPOST).not.called;
  });
});
