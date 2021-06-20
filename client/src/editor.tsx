import React, { useState, useEffect, useRef, Dispatch, Props } from "react";
import Row from "./components/Row";
import useWindowDimensions from "./utils/useWindowDimensions";
import axios from "axios";
import type { State, Action } from "./state";

function Canvas(props: {
  state: State;
  parentHeight: string;
  textAreaRef: React.Ref<HTMLTextAreaElement>;
  textAreaHeight: string;
  fontSize: number;
  lineHeight: number;
  onChangeHandler: React.ChangeEventHandler<HTMLTextAreaElement>;
}) {
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
        value={props.state.text}
      />
    </div>
  );
}

function Results(props: {
  state: State;
  parentHeight: string;
  fontSize: number;
  lineHeight: number;
}) {
  return (
    <div
      className="results"
      data-testid="results"
      style={{
        width: "100%",
        maxWidth: 400,
        minHeight: props.parentHeight,
        paddingTop: 30 + props.fontSize / 2,
        paddingLeft: 30,
      }}
    >
      {props.state.results.map((result: string, index) => (
        <div
          key={index}
          className="results-item"
          style={{
            height: props.fontSize * props.lineHeight,
            lineHeight: `${props.fontSize}px`,
          }}
        >
          {result}
        </div>
      ))}
    </div>
  );
}

interface ParseCall {
  line: string;
  timeout: number;
}

let parseCalls: Array<ParseCall> = [];
function runDebouncedParse(text: string, dispatch: Dispatch<Action>) {
  const lines = text.split("\n");
  for (const lineNumber in lines) {
    const line = lines[lineNumber];
    if (line.trim().length == 0) continue; // TODO: set line to empty
    if (parseCalls[lineNumber]?.line == line) continue;

    clearTimeout(parseCalls[lineNumber]?.timeout);
    const timeout = setTimeout(() => {
      axios.get("/api/parse", { params: { code: line } }).then((response) => {
        if (line != parseCalls[lineNumber]?.line) return;

        dispatch({
          type: "UPDATE_RESULTS",
          index: parseInt(lineNumber),
          result: response.data,
        });
      });
    }, 500);

    parseCalls[lineNumber] = { line, timeout };
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

  useEffect(setCanvasHeight, [props.state.text]);

  useEffect(() => {
    setTextAreaHeight("auto");
    setTimeout(setCanvasHeight, 0);
  }, [windowDimensions]);

  const onChangeHandler = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    const text = event.target.value;

    setTextAreaHeight("auto");
    props.dispatch({ type: "SET_TEXT", value: text });

    runDebouncedParse(text, props.dispatch);
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
        <Results
          state={props.state}
          parentHeight={parentHeight}
          fontSize={fontSize}
          lineHeight={lineHeight}
        />
      </Row>
    </>
  );
}
