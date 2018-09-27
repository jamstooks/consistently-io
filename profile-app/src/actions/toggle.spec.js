import configureMockStore from "redux-mock-store";
import thunk from "redux-thunk";
import fetchMock from "fetch-mock";

import * as actions from "./toggle";
import { mockProfileRepos } from "../mockData"

const middleware = [thunk];
const mockStore = configureMockStore(middleware);

describe("async actions", () => {
  afterEach(() => {
    fetchMock.reset();
    fetchMock.restore();
  });

  it("toggleRepo success creates the right actions", () => {
    fetchMock.patch("*", { is_active: !mockProfileRepos[0].is_active });

    const expectedActions = [
      { type: "TOGGLE_REQUEST", github_id: mockProfileRepos[0].github_id },
      {
        type: "TOGGLE_SUCCESS",
        github_id: mockProfileRepos[0].github_id,
        json: { is_active: !mockProfileRepos[0].is_active }
      }
    ];
    const store = mockStore({});

    return store.dispatch(actions.toggleRepo(mockProfileRepos[0].github_id))
      .then(() => {
        expect(store.getActions()[0]).toEqual(expectedActions[0]);
        expect(store.getActions()[1]).toEqual(expectedActions[1]);
      });
  });

  it("toggleRepo failure creates the right actions", () => {
    fetchMock.mock('*', 500);

    const expectedActions = [
      { type: "TOGGLE_REQUEST" },
      { type: "TOGGLE_FAILURE", error: 500 }
    ];
    const store = mockStore({});

    return store.dispatch(actions.toggleRepo()).then(() => {
      expect(store.getActions()[0]).toEqual(expectedActions[0]);
      expect(store.getActions()[1].type).toEqual(expectedActions[1].type);
    });
  });

});
