import { getEndpoint } from "../api";

const API_ROOT = process.env.REACT_APP_APIURL;
const ACTION_TYPES = ['PROFILE_REQUEST', 'PROFILE_SUCCESS', 'PROFILE_FAILURE']

export const getProfile = () => {
  let url = API_ROOT + "profile-repos/";
  return getEndpoint(url, ACTION_TYPES);
}
