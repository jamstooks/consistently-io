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
      obj: null,
      form: null
    }
  },
  action
) => {

  let newCurrent, newForm, newValues = null;

  switch (action.type) {
  case "LIST_REQUEST":
    return {
      ...state,
      ...{
        integrations: { isFetching: true, list: [], error: null },
        current: {
          id: null,
          isFetching: false,
          error: null,
          obj: null,
          form: null
        },
      }
    };
  case "LIST_SUCCESS":

    // @todo - we should probably do some normalization here
    // (or in `src/api.js`) like { '1': {id: 1, ...} }

    return {
      ...state,
      ...{
        integrations: { isFetching: false, list: action.json, error: null },
        current: {
          id: null,
          isFetching: false,
          error: null,
          obj: null,
          form: null
        },
      }
    };
  case "LIST_FAILURE":
    return {
      ...state,
      ...{
        integrations: { isFetching: false, list: [], error: action.error },
        current: {
          id: null,
          isFetching: false,
          error: null,
          obj: null,
          form: null
        },
      }
    };
  case "DETAIL_REQUEST":
    return {
      ...state,
      ...{
        current: {
          id: action.id,
          isFetching: true,
          error: null,
          obj: null,
          form: null
        },
      }
    };
  case "DETAIL_SUCCESS":
    return {
      ...state,
      ...{
        current: {
          id: action.id,
          isFetching: false,
          error: null,
          obj: action.json,
          form: {
            isUpdating: false,
            values: action.json,
            errors: null
          }
        },
      }
    };
  case "DETAIL_FAILURE":
    return {
      ...state,
      ...{
        current: {
          id: action.id,
          isFetching: false,
          error: action.error,
          obj: null,
          form: null
        },
      }
    };
  case "UPDATE_REQUEST":

    newForm = {
      ...state['current']['form'],
      ...{
        isUpdating: true
      }
    };
    newCurrent = {
      ...state['current'],
      ...{ form: newForm, id: action.id }
    };
    return {
      ...state,
      ...{ current: newCurrent }
    };
  case "UPDATE_SUCCESS":

    newCurrent = {
      ...state['current'],
      ...{
        id: action.id,
        isFetching: false,
        error: null,
        obj: action.json,
        form: {
          isUpdating: false,
          values: action.json,
          errors: null
        }
      }
    };

    // update the status of the integration in `integrations`
    let i = state.integrations.list.find(i => i.id === action.id);
    i.is_active = action.json.is_active;

    return {
      ...state,
      ...{ current: newCurrent }
    };
  case "UPDATE_FAILURE":

    newForm = {
      ...state['current']['form'],
      ...{
        isUpdating: false,
        errors: action.error,
      }
    };

    newCurrent = {
      ...state['current'],
      ...{
        id: action.id,
        form: newForm
      }
    };
    return { ...state, ...{ current: newCurrent } };

  case "DESELECT_INTEGRATION":
    return {
      ...state,
      ...{
        current: {
          id: null,
          isFetching: false,
          error: null,
          obj: null,
          form: null
        }
      }
    };
  case "UPDATE_FORM_VALUE":

    newValues = { ...state['current']['form']['values'] };
    newValues[action.key] = action.value;

    newForm = { ...state['current']['form'], ...{ values: newValues } };
    newCurrent = { ...state['current'], ...{ form: newForm } };

    return { ...state, ...{ current: newCurrent } };

  default:
    return state;
  }
};

export default integrations;
