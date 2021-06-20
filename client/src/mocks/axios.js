import { stub } from "sinon";

export default {
  // TODO: tell which url we forgot to mock
  post: stub().callsFake((url) =>
    Promise.reject(`POST request for ${url} not mocked`)
  ),
};
