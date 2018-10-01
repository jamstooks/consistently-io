import { getCookie } from "./utils";

/**
 * A generic get request from the api.
 * 
 * Expects a `url` and a `types` array
 * with three action types... [request, success, failure]
 */
export const getEndpoint = (url, types) => {

  const [requestType, successType, failureType] = types

  return dispatch => (
    runRequest(dispatch, url, "GET", null, null, types)
  );
}

/**
 * A generic PATCH (or PUT or POST) request from the api.
 * 
 * Expects a `url` and a `types` array, like `getEndpoint`,
 * but also expects a `data` object to send to the API
 */
export const updateEndpoint = (url, data, types, method = "PATCH") => {

  const [requestType, successType, failureType] = types

  return dispatch => {

    return runRequest(
      dispatch,
      url,
      "PATCH", {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie('csrftoken')
      },
      JSON.stringify(data),
      types
    );
  }
}


/**
 * Generic fetch method to handle a variety of requests
 */
const runRequest = (dispatch, url, method, headers, body, types) => {

  const [requestType, successType, failureType] = types

  dispatch({ type: requestType });

  return fetch(url, {
      method: method,
      headers: headers,
      body: body
    })
    .then(response =>
      response.json().then(json => ({
        status: response.status,
        json
      })))
    .then(
      ({ status, json }) => {
        if (status >= 400) {
          dispatch({ type: failureType, status: status });
        }
        else {
          dispatch({ type: successType, json: json })
        }
      },
      // Either fetching or parsing failed!
      err => {
        dispatch({ type: failureType, status: err.message });
      }
    );
}
