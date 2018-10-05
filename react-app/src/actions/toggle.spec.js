// import configureMockStore from "redux-mock-store";
// import thunk from "redux-thunk";
// import fetchMock from "fetch-mock";

import * as actions from "./toggle";
import { mockProfileRepos } from "../testUtils/mockData"

import { testFetch } from "../testUtils/generics";

const expectedSuccessActions = [
  { type: "TOGGLE_REQUEST", github_id: mockProfileRepos[0].github_id }, {
    type: "TOGGLE_SUCCESS",
    github_id: mockProfileRepos[0].github_id,
    json: { is_active: !mockProfileRepos[0].is_active }
  }
];

const expectedFailureActions = [
  { type: "TOGGLE_REQUEST", github_id: mockProfileRepos[0].github_id },
  { type: "TOGGLE_FAILURE", error: 500 }
];

testFetch(
  actions.toggleRepo, [mockProfileRepos[0].github_id, ],
  expectedSuccessActions,
  expectedFailureActions, { is_active: !mockProfileRepos[0].is_active });
