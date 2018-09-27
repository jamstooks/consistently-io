import { connect } from "react-redux";

import Profile from "../components/Profile";
import { getProfile } from "../actions/profile";
import { toggleRepo } from "../actions/toggle";

const mapStateToProps = state => ({
  isFetching: state.isFetching,
  repoList: state.repoList,
  error: state.error,
  fetchingRepoList: []
});

const mapDispatchToProps = dispatch => ({
  getProfile: () => dispatch(getProfile()),
  toggleRepo: (github_id, active) => dispatch(toggleRepo(github_id, active))
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Profile);
