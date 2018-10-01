import { getEndpoint } from "../api";

const API_ROOT = process.env.REACT_APP_APIURL;
const TYPES = ['LIST_REQUEST', 'LIST_SUCCESS', 'LIST_FAILURE']

export const getList = () => {
  let url = API_ROOT + "integrations/" + window.repo.github_id + "/";
  return getEndpoint(url, TYPES);
}
