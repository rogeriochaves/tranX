import React, { useState, useEffect, useRef } from "react";
import Row from "./components/Row";
import useWindowDimensions from "./utils/useWindowDimensions";

function Canvas(props: {
  parentHeight: string;
  textAreaRef: React.LegacyRef<HTMLTextAreaElement>;
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
      />
    </div>
  );
}

function Results(props: {
  parentHeight: string;
  fontSize: number;
  text: string;
  lineHeight: number;
}) {
  return (
    <div
      className="results"
      style={{
        width: "100%",
        maxWidth: 400,
        minHeight: props.parentHeight,
        paddingTop: 30 + props.fontSize / 2,
        paddingLeft: 30,
      }}
    >
      {props.text.split("\n").map((line: string) => (
        <div
          className="results-item"
          style={{
            height: props.fontSize * props.lineHeight,
            lineHeight: `${props.fontSize}px`,
          }}
        >
          {line}
        </div>
      ))}
    </div>
  );
}

export default function Editor() {
  const windowDimensions = useWindowDimensions();
  const textAreaRef = useRef<HTMLTextAreaElement>(null);
  const [text, setText] = useState("");
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

  useEffect(setCanvasHeight, [text]);

  useEffect(() => {
    setTextAreaHeight("auto");
    setTimeout(setCanvasHeight, 0);
  }, [windowDimensions]);

  const onChangeHandler = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setTextAreaHeight("auto");
    setText(event.target.value);
  };

  return (
    <>
      <div
        className="topbar"
        style={{ width: "100%", height: topbarHeight }}
      ></div>
      <Row style={{ maxWidth: 1200, margin: "0 auto" }}>
        <Canvas
          textAreaRef={textAreaRef}
          textAreaHeight={textAreaHeight}
          parentHeight={parentHeight}
          onChangeHandler={onChangeHandler}
          fontSize={fontSize}
          lineHeight={lineHeight}
        />
        <Results
          text={text}
          parentHeight={parentHeight}
          fontSize={fontSize}
          lineHeight={lineHeight}
        />
      </Row>
    </>
  );
}
