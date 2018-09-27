import "cross-fetch/polyfill";

const API_ROOT = process.env.REACT_APP_APIURL;

function getCookie(name) {
  let match = "(?:(?:^|.*;\\s*)"
  match += name;
  match += "\\s*\\=\\s*([^;]*).*$)|^.*$";
  return document.cookie.replace(RegExp(match), "$1");
}

export const toggleRequest = (github_id) => ({
  type: 'TOGGLE_REQUEST',
  github_id
});
export const toggleSuccess = (github_id, json) => ({
  type: 'TOGGLE_SUCCESS',
  github_id,
  json
});
export const toggleFailure = error => ({
  type: 'TOGGLE_FAILURE',
  error
});

export const toggleRepo = (github_id, active) => {

  return dispatch => {

    let url = API_ROOT + "toggle-repo/" + github_id + "/";

    dispatch(toggleRequest(github_id));

    return fetch(url, {
        method: "PATCH",
        headers: {
          "Accept": "application/json, text/plain, */*",
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify({ 'is_active': active })
      })
      .then(response =>
        response.json().then(json => ({
          status: response.status,
          json
        })))
      .then(
        ({ status, json }) => {
          if (status >= 400) {
            dispatch(toggleFailure(status));
          }
          else {
            dispatch(toggleSuccess(github_id, json))
          }
        },
        // Either fetching or parsing failed!
        err => {
          dispatch(toggleFailure(err.message))
        }
      );
  }
}
