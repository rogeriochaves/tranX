import * as React from "react";
import { render } from "@testing-library/react";
import { expect } from "chai";
import Editor from "./Editor";

describe("<Editor>", () => {
  it("renders learn react link", async () => {
    const wrapper = render(<Editor />);
    const canvas = await wrapper.findByPlaceholderText(/type some code/i);
    expect(document.body.contains(canvas));
  });
});
