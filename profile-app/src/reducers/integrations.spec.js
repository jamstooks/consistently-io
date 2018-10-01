import integrations from "./integrations";
import { mockSettings, mockIntegration } from "../testUtils/mockData"

let BASE_STATE = {
  integrations: {
    isFetching: false,
    list: [],
    error: null
  },
  current: {
    id: null,
    isFetching: false,
    error: null,
    obj: null
  }
};

describe("integrations reducer", () => {
  it("should handle initial state", () => {
    expect(integrations(undefined, [])).toEqual(BASE_STATE);
  });

  it("should handle LIST_REQUEST", () => {
    expect(
      integrations(BASE_STATE, {
        type: "LIST_REQUEST"
      }).integrations.isFetching
    ).toEqual(true);
  });

  it("should handle LIST_SUCCESS", () => {
    expect(
      integrations(BASE_STATE, {
        type: "LIST_SUCCESS",
        json: mockSettings
      }).integrations
    ).toEqual({
      isFetching: false,
      error: null,
      list: mockSettings
    });
  });

  it("should handle LIST_FAILURE", () => {
    expect(
      integrations(BASE_STATE, {
        type: "LIST_FAILURE",
        error: "is human"
      }).integrations
    ).toEqual({
      isFetching: false,
      error: "is human",
      list: []
    });
  });

  it("should handle DETAIL_REQUEST", () => {
    expect(
      integrations(BASE_STATE, {
        type: "DETAIL_REQUEST",
        id: 1
      }).current
    ).toEqual({
      id: 1,
      isFetching: true,
      error: null,
      obj: null
    });
  });

  it("should handle DETAIL_SUCCESS", () => {
    expect(
      integrations(BASE_STATE, {
        type: "DETAIL_SUCCESS",
        id: 1,
        json: mockIntegration
      }).current
    ).toEqual({
      id: 1,
      isFetching: false,
      error: null,
      obj: mockIntegration
    });
  });

  it("should handle DETAIL_FAILURE", () => {
    expect(
      integrations(BASE_STATE, {
        type: "DETAIL_FAILURE",
        id: 1,
        error: "ERR!"
      }).current
    ).toEqual({
      id: 1,
      isFetching: false,
      error: "ERR!",
      obj: null
    });
  });

  it("should handle UPDATE_REQUEST", () => {
    expect(
      integrations(BASE_STATE, {
        type: "UPDATE_REQUEST",
        id: 1
      }).current
    ).toEqual({
      id: 1,
      isFetching: true,
      error: null,
      obj: null
    });
  });

  it("should handle UPDATE_SUCCESS", () => {
    expect(
      integrations(BASE_STATE, {
        type: "UPDATE_SUCCESS",
        id: 1,
        json: mockIntegration
      }).current
    ).toEqual({
      id: 1,
      isFetching: false,
      error: null,
      obj: mockIntegration
    });
  });

  it("should handle UPDATE_FAILURE", () => {
    expect(
      integrations(BASE_STATE, {
        type: "UPDATE_FAILURE",
        id: 1,
        error: "ERR!"
      }).current
    ).toEqual({
      id: 1,
      isFetching: false,
      error: "ERR!",
      obj: null
    });
  });


  it("should handle UPDATE_FAILURE", () => {
    expect(
      integrations(BASE_STATE, {
        type: "UPDATE_FAILURE",
        id: 1,
        error: "ERR!"
      }).current
    ).toEqual({
      id: 1,
      isFetching: false,
      error: "ERR!",
      obj: null
    });
  });

});
