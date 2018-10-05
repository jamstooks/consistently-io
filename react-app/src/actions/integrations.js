import { getEndpoint, updateEndpoint } from "../api";

const API_ROOT = process.env.REACT_APP_APIURL;
const BASE_URL = API_ROOT + "integrations/";

export const getList = () => {
  return getEndpoint(
    BASE_URL + window.repo.github_id + "/", ['LIST_REQUEST', 'LIST_SUCCESS', 'LIST_FAILURE']);
}

export const getDetail = (id) => {
  return getEndpoint(
    BASE_URL + window.repo.github_id + "/" + id + "/", ['DETAIL_REQUEST', 'DETAIL_SUCCESS', 'DETAIL_FAILURE'], { id: id });
}

export const updateIntegration = (id, data) => {
  return updateEndpoint(
    BASE_URL + window.repo.github_id + "/" + id + "/",
    data, ['UPDATE_REQUEST', 'UPDATE_SUCCESS', 'UPDATE_FAILURE'], { id: id });
}

export const deselectIntegration = () => ({
  type: "DESELECT_INTEGRATION"
});

export const updateFormValue = (key, value) => ({
  type: "UPDATE_FORM_VALUE",
  key,
  value
})
