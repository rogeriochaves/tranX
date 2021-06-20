import { stub } from "sinon";

export default {
  // TODO: tell which url we forgot to mock
  post: stub().returns(Promise.reject("Not mocked")),
};
