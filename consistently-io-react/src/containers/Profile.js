import { connect } from "react-redux";

import Profile from "../components/Profile";
import { getProfile } from "../actions";

const mapStateToProps = state => ({
  isFetching: state.profile.isFetching,
  repoList: state.profile.repoList,
  error: state.profile.error,
  fetchingRepoList: []
});

const mapDispatchToProps = dispatch => ({
  getProfile: () => dispatch(getProfile())
//   saveNewBenchmark: data => dispatch(saveNewBenchmark(data)),
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Profile);