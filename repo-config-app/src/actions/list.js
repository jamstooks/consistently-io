import "cross-fetch/polyfill";

const API_ROOT = process.env.REACT_APP_APIURL;


export const listRequest = () => ({
  type: 'LIST_REQUEST'
});
export const listSuccess = list => ({
  type: 'LIST_SUCCESS',
  list
});
export const listFailure = error => ({
  type: 'LIST_FAILURE',
  error
});

export const getList = () => {

  return dispatch => {

    let url = API_ROOT + "integrations/" + window.repo.github_id + "/";

    dispatch(listRequest())

    return fetch(url)
      // Try to parse the response
      .then(response =>
        response.json().then(json => ({
          status: response.status,
          json
        })))
      .then(
        // Both fetching and parsing succeeded!
        ({ status, json }) => {
          if (status >= 400) {
            // Status looks bad
            dispatch(listFailure(status));
          }
          else {
            // Status looks good
            dispatch(listSuccess(json))
          }
        },
        // Either fetching or parsing failed!
        err => {
          dispatch(listFailure(err.message))
        }
      );
  }
}