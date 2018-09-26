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
            ...{ isFetching: true, repoList: null, error: null }
        };
    case "PROFILE_SUCCESS":
        return {
            ...state,
            ...{ isFetching: false, repoList: action.repoList, error: null }
        };
    case "PROFILE_FAILURE":
        return {
            ...state,
            ...{ isFetching: false, repoList: null, error: action.error }
        };
    default:
        return state;
    }
};

export default profile;
