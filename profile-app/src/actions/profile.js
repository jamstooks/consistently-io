import "cross-fetch/polyfill";

const API_ROOT = process.env.REACT_APP_APIURL;


export const profileRequest = () => ({
  type: 'PROFILE_REQUEST'
});
export const profileSuccess = repoList => ({
  type: 'PROFILE_SUCCESS',
  repoList
});
export const profileFailure = error => ({
  type: 'PROFILE_FAILURE',
  error
});

export const getProfile = () => {

  return dispatch => {

    let url = API_ROOT + "profile-repos/";

    dispatch(profileRequest())

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
            dispatch(profileFailure(status));
          }
          else {
            // Status looks good
            dispatch(profileSuccess(json))
          }
        },
        // Either fetching or parsing failed!
        err => {
          dispatch(profileFailure(err.message))
        }
      );

  }
}
