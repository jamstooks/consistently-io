const integrations = (
  state = {
    integrations: {
      isFetching: false,
      list: [],
      error: null
    },
    current: {
      id: null,
      isFetching: false,
      error: null,
      obj: null
    }
  },
  action
) => {

  let newCurrent = null;

  switch (action.type) {
  case "LIST_REQUEST":
    return {
      ...state,
      ...{
        integrations: { isFetching: true, list: [], error: null },
        current: { id: null, isFetching: false, error: null, obj: null },
      }
    };
  case "LIST_SUCCESS":
    return {
      ...state,
      ...{
        integrations: { isFetching: false, list: action.json, error: null },
        current: { id: null, isFetching: false, error: null, obj: null },
      }
    };
  case "LIST_FAILURE":
    return {
      ...state,
      ...{
        integrations: { isFetching: false, list: [], error: action.error },
        current: { id: null, isFetching: false, error: null, obj: null },
      }
    };
  case "DETAIL_REQUEST":
    return {
      ...state,
      ...{
        current: { id: action.id, isFetching: true, error: null, obj: null },
      }
    };
  case "DETAIL_SUCCESS":
    return {
      ...state,
      ...{
        current: { id: action.id, isFetching: false, error: null, obj: action.json },
      }
    };
  case "DETAIL_FAILURE":
    return {
      ...state,
      ...{
        current: { id: action.id, isFetching: false, error: action.error, obj: null },
      }
    };
  case "UPDATE_REQUEST":
    newCurrent = {
      ...state['current'],
      ...{ id: action.id, isFetching: true, error: null }
    };
    return {
      ...state,
      ...{ current: newCurrent }
    };
  case "UPDATE_SUCCESS":
    newCurrent = {
      ...state['current'],
      ...{ id: action.id, isFetching: false, error: null, obj: action.json }
    };
    return {
      ...state,
      ...{ current: newCurrent }
    };
  case "UPDATE_FAILURE":
    newCurrent = {
      ...state['current'],
      ...{ id: action.id, isFetching: false, error: action.error }
    };
    return {
      ...state,
      ...{ current: newCurrent }
    };
  case "DESELECT_INTEGRATION":
    return {
      ...state,
      ...{ current: { id: null, isFetching: false, error: null, obj: null } }
    };
  default:
    return state;
  }
};

export default integrations;
