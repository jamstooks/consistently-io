import configureMockStore from "redux-mock-store";
import thunk from "redux-thunk";
import fetchMock from "fetch-mock";

import * as actions from "./list";
import { mockList } from "../mockData";

const middleware = [thunk];
const mockStore = configureMockStore(middleware);


describe("async actions", () => {
  afterEach(() => {
    fetchMock.reset();
    fetchMock.restore();
    window.repo = undefined;
  });

  beforeEach(() => {
    window.repo = { github_id: "1" }
  })

  it("getList success creates the right actions", () => {
    fetchMock.get("*", mockList);

    const expectedActions = [
      { type: "LIST_REQUEST" },
      { type: "LIST_SUCCESS", json: mockList }
    ];
    const store = mockStore({});

    return store.dispatch(actions.getList()).then(() => {
      expect(store.getActions()[0]).toEqual(expectedActions[0]);
      expect(store.getActions()[1]).toEqual(expectedActions[1]);
    });
  });

  it("getList failure creates the right actions", () => {
    fetchMock.mock('*', 500);

    const expectedActions = [
      { type: "LIST_REQUEST" },
      { type: "LIST_FAILURE", error: 500 }
    ];
    const store = mockStore({});

    return store.dispatch(actions.getList()).then(() => {
      expect(store.getActions()[0]).toEqual(expectedActions[0]);
      expect(store.getActions()[1].type).toEqual(expectedActions[1].type);
    });
  });

});
