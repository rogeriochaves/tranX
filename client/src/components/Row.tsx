import React from "react";

interface MaybeStyle {
  style: Object;
}

export default function Row(props: React.PropsWithChildren<MaybeStyle>) {
  return (
    <div {...props} style={{ ...props.style, display: "flex" }}>
      {props.children}
    </div>
  );
}
