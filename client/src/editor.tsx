import React, { useState, useEffect, useRef, Dispatch } from "react";
import Row from "./components/Row";
import useWindowDimensions from "./utils/useWindowDimensions";
import axios from "axios";
import type { State, Action, Line } from "./state";
import {
  Failure,
  Loading,
  NotAsked,
  RemoteData,
  Success,
} from "./utils/remoteData";

export default function Editor(props: {
  state: State;
  dispatch: Dispatch<Action>;
}) {
  const topbarHeight = 10;
  const fontSize = 30;
  const lineHeight = 2;

  const runCodeButtonDisabled = Object.values(props.state.lines).some(
    (x) => x.parsed.state != "SUCCESS"
  );

  const runCode = () => {
    const parsedCode = Object.values(props.state.lines)
      .map((line) => {
        if (line.parsed.state == "SUCCESS") {
          return line.parsed.data;
        }
        return "";
      })
      .join("\n");

    axios.post("/api/execute", { parsedCode }).then((response) => {
      props.dispatch({ type: "SET_OUTPUT", value: response.data });
    });
  };

  return (
    <>
      <div
        className="topbar"
        style={{ width: "100%", height: topbarHeight }}
      ></div>
      <Row style={{ maxWidth: 1200, margin: "0 auto" }}>
        <div
          className="canvas"
          style={{
            minHeight: `calc(100vh - ${topbarHeight}px)`,
            width: "100%",
            minWidth: 300,
            maxWidth: 800,
          }}
        >
          <Canvas
            state={props.state}
            dispatch={props.dispatch}
            fontSize={fontSize}
            lineHeight={lineHeight}
          />
          <div style={{ padding: "0 30px" }}>
            <button
              data-testid="run-code"
              onClick={runCode}
              disabled={runCodeButtonDisabled}
            >
              Run Code
            </button>
            <Output state={props.state} />
          </div>
        </div>
        <ParsedCode
          state={props.state}
          fontSize={fontSize}
          lineHeight={lineHeight}
        />
      </Row>
    </>
  );
}

function Canvas(props: {
  state: State;
  dispatch: Dispatch<Action>;
  fontSize: number;
  lineHeight: number;
}) {
  const windowDimensions = useWindowDimensions();
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  const [textAreaHeight, setTextAreaHeight] = useState("auto");
  const [parentHeight, setParentHeight] = useState("auto");

  const getTextAreaHeight = () => textAreaRef.current!.scrollHeight;

  const setCanvasHeight = () => {
    setParentHeight(`${getTextAreaHeight()}px`);
    setTextAreaHeight(`${getTextAreaHeight()}px`);
  };

  const input = props.state.lines.map((line) => line.input).join("\n");
  useEffect(setCanvasHeight, [input]);

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
    <div
      style={{
        minHeight: parentHeight,
        position: "relative",
      }}
    >
      <textarea
        className="canvas-textarea"
        data-testid="canvas-textarea"
        ref={textAreaRef}
        rows={1}
        style={{
          width: "100%",
          height: textAreaHeight,
          padding: 30,
          fontSize: props.fontSize,
          lineHeight: props.lineHeight,
        }}
        onChange={onChangeHandler}
        placeholder="type some code..."
        value={input}
      />
    </div>
  );
}

function ParsedCode(props: {
  state: State;
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
        paddingTop: 30 + props.fontSize / 2,
        paddingLeft: 30,
      }}
    >
      {Object.values(props.state.lines).map((line: Line, index) => (
        <div
          key={index}
          className="parsed-line"
          style={{
            height: props.fontSize * props.lineHeight,
            lineHeight: `${props.fontSize}px`,
          }}
        >
          {parsedLineAsText(line.parsed)}
        </div>
      ))}
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

function Output(props: { state: State }) {
  return (
    <div style={{ paddingTop: "30px" }}>
      {props.state.output && (
        <>
          <div
            className="output-title"
            style={{
              position: "absolute",
              margin: "-1px 0 0 10px",
              padding: "0 5px",
            }}
          >
            output:
          </div>
          <hr />
        </>
      )}
      <div
        className="output"
        data-testid="output"
        style={{ paddingTop: "20px" }}
      >
        {(props.state.output.toString() || "").split("\n").map((line, i) => (
          <React.Fragment key={i}>
            {line}
            <br />
          </React.Fragment>
        ))}
      </div>
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
    parsed: Loading(),
  });

  axios
    .get("/api/parse", { params: { inputLine: inputLine } })
    .then((response) => {
      if (inputLine != parseCalls[lineNumber]?.line) return;

      dispatch({
        type: "UPDATE_PARSED_LINE",
        index: lineNumber,
        parsed: Success(response.data),
      });
    })
    .catch((_error) => {
      dispatch({
        type: "UPDATE_PARSED_LINE",
        index: lineNumber,
        parsed: Failure("parsing error"),
      });
    });
}

function runDebouncedParse(input: string, dispatch: Dispatch<Action>) {
  const inputLines = input.split("\n");
  for (let lineNumber in inputLines) {
    const inputLine = inputLines[lineNumber];
    if (parseCalls[lineNumber]?.line == inputLine) continue;

    clearTimeout(parseCalls[lineNumber]?.timeout);

    parseCalls[lineNumber] = { line: inputLine, timeout: 0 };
    if (inputLine.trim().length == 0) {
      dispatch({
        type: "UPDATE_PARSED_LINE",
        index: parseInt(lineNumber),
        parsed: NotAsked(),
      });
      continue;
    }

    const timeout = setTimeout(
      () => callParse(inputLine, parseInt(lineNumber), dispatch),
      500
    );

    parseCalls[lineNumber] = { line: inputLine, timeout };
  }
}
