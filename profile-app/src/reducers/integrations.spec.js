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
    obj: null,
    form: null
  }
};

let FORM_STATE = {
  integrations: {
    isFetching: false,
    list: [{ id: 1 }],
    error: null
  },
  current: {
    id: null,
    isFetching: false,
    error: null,
    obj: null,
    form: {
      isUpdating: false,
      values: { one: 1 },
      errors: null
    }
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
      obj: null,
      form: null
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
      obj: mockIntegration,
      form: {
        isUpdating: false,
        values: mockIntegration,
        errors: null
      }
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
      obj: null,
      form: null
    });
  });

  it("should handle UPDATE_REQUEST", () => {
    expect(
      integrations(FORM_STATE, {
        type: "UPDATE_REQUEST",
        id: 1
      }).current
    ).toEqual({
      id: 1,
      isFetching: false,
      error: null,
      obj: null,
      form: {
        isUpdating: true,
        values: { one: 1 },
        errors: null
      }
    });
  });

  it("should handle UPDATE_SUCCESS", () => {

    // test current
    expect(
      integrations(FORM_STATE, {
        type: "UPDATE_SUCCESS",
        id: 1,
        json: mockIntegration
      }).current
    ).toEqual({
      id: 1,
      isFetching: false,
      error: null,
      obj: mockIntegration,
      form: {
        isUpdating: false,
        values: mockIntegration,
        errors: null
      }
    });

    // test actual
    expect(
      integrations(FORM_STATE, {
        type: "UPDATE_SUCCESS",
        id: 1,
        json: mockIntegration
      }).integrations.list[0].is_active
    ).toEqual(mockIntegration.is_active);
  });

  it("should handle UPDATE_FAILURE", () => {
    expect(
      integrations(FORM_STATE, {
        type: "UPDATE_FAILURE",
        id: 1,
        error: "ERR!"
      }).current
    ).toEqual({
      id: 1,
      isFetching: false,
      error: null,
      obj: null,
      form: {
        isUpdating: false,
        values: { one: 1 },
        errors: "ERR!"
      }
    });
  });

  it("should handle UPDATE_FORM_VALUE", () => {
    expect(
      integrations(FORM_STATE, {
        type: "UPDATE_FORM_VALUE",
        key: 'one',
        value: 2
      }).current.form.values
    ).toEqual({ one: 2 });
  });

});
