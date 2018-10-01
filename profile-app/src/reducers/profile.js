const profile = (
  state = {
    isFetching: false,
    repoList: null,
    error: null
  },
  action
) => {

  switch (action.type) {
  case "PROFILE_REQUEST":
    return {
      ...state,
      ...{
        isFetching: true,
        repoList: null,
        error: null
      }
    };
  case "PROFILE_SUCCESS":
    return {
      ...state,
      ...{
        isFetching: false,
        repoList: action.json,
        error: null
      }
    };
  case "PROFILE_FAILURE":
    return {
      ...state,
      ...{
        isFetching: false,
        repoList: null,
        error: action.error
      }
    };
  case "TOGGLE_REQUEST":

    // add the loading indicator to the repo
    let rl = [...state.repoList];
    // find the repo and update it
    let repo = rl.find(r => r.github_id === action.github_id);
    repo.isFetching = true;

    let newState = {
      ...state,
      ...{ repoList: rl }
    };

    return newState;
  case "TOGGLE_SUCCESS":

    let rl2 = [...state.repoList];
    // find the repo and update the `is_active` status
    let repo2 = rl2.find(r => r.github_id === action.github_id);
    repo2.is_active = action.json.is_active;
    repo2.isFetching = false;

    return {
      ...state,
      ...{ repoList: rl2 }
    };
  default:
    return state;
  }
};

export default profile;
