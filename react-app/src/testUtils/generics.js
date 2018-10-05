import configureMockStore from "redux-mock-store";
import thunk from "redux-thunk";
import fetchMock from "fetch-mock";

const middleware = [thunk];
const mockStore = configureMockStore(middleware);

/**
 * Generic method to run a test for a standard getEndpoint method
 * 
 * `params` is an array that will be passed as paremeters ot the method
 * `mockData` is the data that should be returned after a good request
 */
export const testFetch = (
  method,
  params,
  expectedSuccessActions,
  expectedFailureActions,
  mockData,
  beforeMethod = null,
  afterMethod = null) => {

  describe("get action", () => {
    afterEach(() => {
      fetchMock.reset();
      fetchMock.restore();
      if (afterMethod !== null) {
        afterMethod();
      }
    });

    beforeEach(() => {
      if (beforeMethod !== null) {
        beforeMethod();
      }
    })

    it(method.name + " success creates the right actions", () => {
      fetchMock.mock("*", mockData);

      const store = mockStore({});
      return store.dispatch(method(...params)).then(() => {
        expect(store.getActions()[0]).toEqual(expectedSuccessActions[0]);
        expect(store.getActions()[1]).toEqual(expectedSuccessActions[1]);
      });
    });

    it(method.name + " failure creates the right actions", () => {
      fetchMock.mock('*', {
        status: 500,
        body: JSON.stringify({
          someJson: "someval"
        })
      });

      const store = mockStore({});
      return store.dispatch(method(...params)).then(() => {
        expect(store.getActions()[0]).toEqual(expectedFailureActions[0]);
        expect(store.getActions()[1].type).toEqual(expectedFailureActions[1].type);
      });
    });

    it(method.name + " failure creates the right actions", () => {
      fetchMock.mock('*', {
        status: 400,
        body: JSON.stringify({
          someJson: "someval"
        })
      });

      const store = mockStore({});
      return store.dispatch(method(...params)).then(() => {
        expect(store.getActions()[0]).toEqual(expectedFailureActions[0]);
        expect(store.getActions()[1].type).toEqual(expectedFailureActions[1].type);
      });
    });

  });
}
