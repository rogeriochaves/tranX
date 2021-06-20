import { stub } from "sinon";

export default {
  get: stub().callsFake((url) =>
    Promise.reject(`GET request for ${url} not mocked`)
  ),
  post: stub().callsFake((url) =>
    Promise.reject(`POST request for ${url} not mocked`)
  ),
};
