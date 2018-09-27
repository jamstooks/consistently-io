import configureMockStore from "redux-mock-store";
import thunk from "redux-thunk";
import fetchMock from "fetch-mock";

import * as actions from "./profile";
import { mockProfileRepos } from "../mockData"


const middleware = [thunk];
const mockStore = configureMockStore(middleware);

describe("async actions", () => {
  afterEach(() => {
    fetchMock.reset();
    fetchMock.restore();
  });

  it("getProfile success creates the right actions", () => {
    fetchMock.get("*", mockProfileRepos);

    const expectedActions = [
      { type: "PROFILE_REQUEST" },
      { type: "PROFILE_SUCCESS", repoList: mockProfileRepos }
    ];
    const store = mockStore({});

    return store.dispatch(actions.getProfile()).then(() => {
      expect(store.getActions()[0]).toEqual(expectedActions[0]);
      expect(store.getActions()[1]).toEqual(expectedActions[1]);
    });
  });

  it("getProfile failure creates the right actions", () => {
    fetchMock.mock('*', 500);

    const expectedActions = [
      { type: "PROFILE_REQUEST" },
      { type: "PROFILE_FAILURE", error: 500 }
    ];
    const store = mockStore({});

    return store.dispatch(actions.getProfile()).then(() => {
      expect(store.getActions()[0]).toEqual(expectedActions[0]);
      expect(store.getActions()[1].type).toEqual(expectedActions[1].type);
    });
  });

});
