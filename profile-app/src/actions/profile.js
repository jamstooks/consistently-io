// import { CALL_API, Schemas } from '../middleware/api'
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

    // dispatch(profileRequest());

    let url = API_ROOT + "profile-repos/";

    dispatch(profileRequest())
    // return fetch(url)
    //   .then(response => response.json().then(json => {
    //     if (response.ok) {
    //       return dispatch(profileSuccess(json));
    //     }
    //     else {
    //       return dispatch(profileFailure(response.status));
    //     }
    //   }))

    // return fetch(url)
    //   .then(response =>
    //     response.json().then(json => {
    //       if (!response.ok) {
    //         return Promise.reject(json)
    //       }
    //       return response;
    //     }))
    //   .then(
    //     response => dispatch(profileSuccess(response.json()),
    //       error => dispatch(profileFailure(error.message))
    //     )
    //   )

    // return fetch(url)
    //   .then(
    //     response => {
    //       return (response.ok) ?
    //         dispatch(profileSuccess(response.json())) :
    //         dispatch(profileFailure(response.status));
    //     },
    //     error => dispatch(profileFailure(error))
    //   )
    // .then(json => dispatch(profileSuccess(json)))
    // }

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
