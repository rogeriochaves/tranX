import React, { useState, useEffect, useRef, Dispatch, Props } from "react";
import Row from "./components/Row";
import useWindowDimensions from "./utils/useWindowDimensions";
import axios from "axios";
import type { State, Action } from "./state";
import { Failure, Loading, RemoteData, Success } from "./utils/remoteData";

function Canvas(props: {
  state: State;
  parentHeight: string;
  textAreaRef: React.Ref<HTMLTextAreaElement>;
  textAreaHeight: string;
  fontSize: number;
  lineHeight: number;
  onChangeHandler: React.ChangeEventHandler<HTMLTextAreaElement>;
}) {
  const [output, setOutput] = useState("");

  const runCodeButtonDisabled = Object.values(props.state.parsedLines).some(
    (x) => x.state != "SUCCESS"
  );

  const runCode = () => {
    const parsedCode = Object.values(props.state.parsedLines)
      .map((parsedLine) => {
        if (parsedLine.state == "SUCCESS") {
          return parsedLine.data;
        }
        return "";
      })
      .join("\n");

    axios.post("/api/execute", { parsedCode }).then((response) => {
      setOutput(response.data);
    });
  };

  return (
    <div
      className="canvas"
      style={{
        minHeight: props.parentHeight,
        width: "100%",
        minWidth: 300,
        maxWidth: 800,
        position: "relative",
      }}
    >
      <textarea
        className="canvas-textarea"
        data-testid="canvas-textarea"
        ref={props.textAreaRef}
        rows={1}
        style={{
          width: "100%",
          height: props.textAreaHeight,
          padding: 30,
          fontSize: props.fontSize,
          lineHeight: props.lineHeight,
        }}
        onChange={props.onChangeHandler}
        placeholder="type some code..."
        value={props.state.input}
      />
      <div
        style={{
          position: "absolute",
          left: "30px",
          top: 50 + props.state.input.split("\n").length * 60 + "px",
        }}
      >
        <button
          data-testid="run-code"
          onClick={runCode}
          disabled={runCodeButtonDisabled}
        >
          Run Code
        </button>
        <div data-testid="output">{output}</div>
      </div>
    </div>
  );
}

function parsedLineAsText(parsedLine: RemoteData<string>): string {
  switch (parsedLine.state) {
    case "NOT_ASKED":
      return "";
    case "LOADING":
      return "*";
    case "FAILURE":
      return parsedLine.error;
    case "SUCCESS":
      return parsedLine.data;
  }
}

function ParsedCode(props: {
  state: State;
  parentHeight: string;
  fontSize: number;
  lineHeight: number;
}) {
  return (
    <div
      className="parsed-code"
      data-testid="parsed-code"
      style={{
        width: "100%",
        maxWidth: 400,
        minHeight: props.parentHeight,
        paddingTop: 30 + props.fontSize / 2,
        paddingLeft: 30,
      }}
    >
      {Object.values(props.state.parsedLines).map(
        (parsedLine: RemoteData<string>, index) => (
          <div
            key={index}
            className="parsed-line"
            style={{
              height: props.fontSize * props.lineHeight,
              lineHeight: `${props.fontSize}px`,
            }}
          >
            {parsedLineAsText(parsedLine)}
          </div>
        )
      )}
    </div>
  );
}

interface ParseCall {
  line: string;
  timeout: number;
}

let parseCalls: Array<ParseCall> = [];
function callParse(
  inputLine: string,
  lineNumber: number,
  dispatch: Dispatch<Action>
) {
  dispatch({
    type: "UPDATE_PARSED_LINE",
    index: lineNumber,
    parsedLine: Loading(),
  });

  axios
    .get("/api/parse", { params: { inputLine: inputLine } })
    .then((response) => {
      if (inputLine != parseCalls[lineNumber]?.line) return;

      dispatch({
        type: "UPDATE_PARSED_LINE",
        index: lineNumber,
        parsedLine: Success(response.data),
      });
    })
    .catch((_error) => {
      dispatch({
        type: "UPDATE_PARSED_LINE",
        index: lineNumber,
        parsedLine: Failure("parsing error"),
      });
    });
}

function runDebouncedParse(input: string, dispatch: Dispatch<Action>) {
  const inputLines = input.split("\n");
  for (let lineNumber in inputLines) {
    const inputLine = inputLines[lineNumber];
    if (inputLine.trim().length == 0) continue; // TODO: set line to empty
    if (parseCalls[lineNumber]?.line == inputLine) continue;

    clearTimeout(parseCalls[lineNumber]?.timeout);
    const timeout = setTimeout(
      () => callParse(inputLine, parseInt(lineNumber), dispatch),
      500
    );

    parseCalls[lineNumber] = { line: inputLine, timeout };
  }
}

export default function Editor(props: {
  state: State;
  dispatch: Dispatch<Action>;
}) {
  const windowDimensions = useWindowDimensions();
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  const [textAreaHeight, setTextAreaHeight] = useState("auto");
  const [parentHeight, setParentHeight] = useState("auto");

  const topbarHeight = 10;
  const fontSize = 30;
  const lineHeight = 2;

  const getTextAreaHeight = () =>
    Math.max(
      textAreaRef.current!.scrollHeight,
      windowDimensions.height - topbarHeight - 2
    );

  const setCanvasHeight = () => {
    setParentHeight(`${getTextAreaHeight()}px`);
    setTextAreaHeight(`${getTextAreaHeight()}px`);
  };

  useEffect(setCanvasHeight, [props.state.input]);

  useEffect(() => {
    setTextAreaHeight("auto");
    setTimeout(setCanvasHeight, 0);
  }, [windowDimensions]);

  const onChangeHandler = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    const input = event.target.value;

    setTextAreaHeight("auto");
    props.dispatch({ type: "SET_INPUT", value: input });

    runDebouncedParse(input, props.dispatch);
  };

  return (
    <>
      <div
        className="topbar"
        style={{ width: "100%", height: topbarHeight }}
      ></div>
      <Row style={{ maxWidth: 1200, margin: "0 auto" }}>
        <Canvas
          state={props.state}
          textAreaRef={textAreaRef}
          textAreaHeight={textAreaHeight}
          parentHeight={parentHeight}
          onChangeHandler={onChangeHandler}
          fontSize={fontSize}
          lineHeight={lineHeight}
        />
        <ParsedCode
          state={props.state}
          parentHeight={parentHeight}
          fontSize={fontSize}
          lineHeight={lineHeight}
        />
      </Row>
    </>
  );
}
