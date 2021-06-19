import React from "react";

export default function Row(props: React.PropsWithChildren<Object>) {
  return (
    <div {...props} style={{ ...props.style, display: "flex" }}>
      {props.children}
    </div>
  );
}
