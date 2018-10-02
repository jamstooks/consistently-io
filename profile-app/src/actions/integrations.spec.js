import * as actions from "./integrations";
import { mockSettings, mockIntegration } from "../testUtils/mockData";
import { testFetch } from "../testUtils/generics";

// actions.getList

let expectedSuccessActions = [
  { type: "LIST_REQUEST" },
  { type: "LIST_SUCCESS", json: mockSettings }
];
let expectedFailureActions = [
  { type: "LIST_REQUEST" },
  { type: "LIST_FAILURE", error: 500 }
];

testFetch(
  actions.getList, [],
  expectedSuccessActions,
  expectedFailureActions,
  mockSettings,
  () => { window.repo = { github_id: "1" } },
  () => { window.repo = undefined }
);

// actions.getDetail

expectedSuccessActions = [
  { type: "DETAIL_REQUEST", id: 1 },
  { type: "DETAIL_SUCCESS", id: 1, json: mockIntegration }
];
expectedFailureActions = [
  { type: "DETAIL_REQUEST", id: 1 },
  { type: "DETAIL_FAILURE", error: 500 }
];

testFetch(
  actions.getDetail, [1],
  expectedSuccessActions,
  expectedFailureActions,
  mockIntegration,
  () => { window.repo = { github_id: "1" } },
  () => { window.repo = undefined }
);

// actions.updateIntegration

let updatedIntegration = {
  ...mockIntegration,
  ...{ url_to_validate: "http://www.example.com" }
};

expectedSuccessActions = [
  { type: "UPDATE_REQUEST", id: 1 },
  { type: "UPDATE_SUCCESS", id: 1, json: updatedIntegration }
];
expectedFailureActions = [
  { type: "UPDATE_REQUEST", id: 1 },
  { type: "UPDATE_FAILURE", id: 1, error: 500 }
];

testFetch(
  actions.updateIntegration, [1],
  expectedSuccessActions,
  expectedFailureActions,
  updatedIntegration,
  () => { window.repo = { github_id: "1" } },
  () => { window.repo = undefined }
);


it("deselectIntegration should create DESELECT_INTEGRATION action", () => {
  expect(actions.deselectIntegration()).toEqual({
    type: "DESELECT_INTEGRATION"
  });
});

it("updateFormValue should create UPDATE_FORM_VALUE action", () => {
  expect(actions.updateFormValue('key', 'value')).toEqual({
    type: "UPDATE_FORM_VALUE",
    key: 'key',
    value: 'value'
  });
});
