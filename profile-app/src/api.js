import "cross-fetch/polyfill";

/**
 * @Note: If the number of actions evolves significantly, this could
 * evolve to middleware
 */

/**
 * A generic get request from the api.
 * 
 * Expects a `url` and a `actionTypes` array
 * with three action actionTypes... [request, success, failure]
 */
export const getEndpoint = (url, actionTypes, action_params) => {

  return dispatch => (
    runRequest(dispatch, url, { method: "GET" }, actionTypes, action_params)
  );
}

/**
 * A generic PATCH (or PUT or POST) request from the api.
 * 
 * Expects a `url` and a `actionTypes` array, like `getEndpoint`,
 * but also expects a `data` object to send to the API
 * 
 * `action_params` allows injection into the various action
 * properties
 */
export const updateEndpoint = (url, data, actionTypes, action_params, method = "PATCH") => {

  return dispatch => {

    let options = {
      method: method,
      headers: {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie('csrftoken')
      },
      body: JSON.stringify(data),
    }

    return runRequest(
      dispatch,
      url,
      options,
      actionTypes,
      action_params
    );
  }
}


/**
 * Generic fetch method to handle a variety of requests
 */
const runRequest = (dispatch, url, options, actionTypes, action_params = null) => {

  if (action_params === null) {
    action_params = {}
  }
  const [requestType, successType, failureType] = actionTypes

  dispatch({ ...action_params,
    ...{ type: requestType }
  });

  return fetch(url, options)
    .then(response =>
      response.json().then(json => ({
        status: response.status,
        json
      })))
    .then(
      ({ status, json }) => {
        if (status >= 400) {
          dispatch({ ...action_params,
            ...{ type: failureType, error: json }
          });
        }
        else {
          dispatch({ ...action_params,
            ...{ type: successType, json: json }
          });
        }
      },
      // Either fetching or parsing failed!
      err => {
        dispatch({ ...action_params,
          ...{ type: failureType, error: err.message }
        });
      }
    );
}

/**
 * simple cookie getter
 */
export const getCookie = name => {
  let match = "(?:(?:^|.*;\\s*)"
  match += name
  match += "\\s*\\=\\s*([^;]*).*$)|^.*$"
  return document.cookie.replace(RegExp(match), "$1")
}
