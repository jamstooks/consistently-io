import * as actions from "./profile";
import { mockProfileRepos } from "../testUtils/mockData";
import { testFetch } from "../testUtils/generics";


const expectedSuccessActions = [
  { type: "PROFILE_REQUEST" },
  { type: "PROFILE_SUCCESS", json: mockProfileRepos }
];

const expectedFailureActions = [
  { type: "PROFILE_REQUEST" },
  { type: "PROFILE_FAILURE", error: 500 }
];

testFetch(
  actions.getProfile, [],
  expectedSuccessActions,
  expectedFailureActions,
  mockProfileRepos);
