import "cross-fetch/polyfill";
import { getCookie } from "./utils";

const API_ROOT = process.env.REACT_APP_APIURL;

export const detailRequest = () => ({
  type: 'DETAIL_REQUEST'
});
export const detailSuccess = (integration_id, json) => ({
  type: 'DETAIL_SUCCESS',
  integration_id,
  json
});
export const detailFailure = error => ({
  type: 'DETAIL_FAILURE',
  error
});

export const updateIntegration = (integration_id, props) => {

  return dispatch => {

    let url = API_ROOT + "integrations/" + window.repo.github_id + "/";
    url += integration_id + "/";

    dispatch(detailRequest());

    return fetch(url, {
        method: "PATCH",
        headers: {
          "Accept": "application/json, text/plain, */*",
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify(props)
      })
      .then(response =>
        response.json().then(json => ({
          status: response.status,
          json
        })))
      .then(
        ({ status, json }) => {
          if (status >= 400) {
            dispatch(detailFailure(status));
          }
          else {
            dispatch(detailSuccess(github_id, json))
          }
        },
        // Either fetching or parsing failed!
        err => {
          dispatch(detailFailure(err.message))
        }
      );
  }
}
