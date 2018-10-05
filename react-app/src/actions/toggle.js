import { updateEndpoint } from "../api";

const API_ROOT = process.env.REACT_APP_APIURL;
const ACTION_TYPES = ['TOGGLE_REQUEST', 'TOGGLE_SUCCESS', 'TOGGLE_FAILURE']

export const toggleRepo = (github_id, active) => {
  let url = API_ROOT + "toggle-repo/" + github_id + "/";
  let data = { 'is_active': active };
  return updateEndpoint(url, data, ACTION_TYPES, { 'github_id': github_id });
}
