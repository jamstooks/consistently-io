import React from "react";
import PropTypes from "prop-types";

import StatusBox from "./StatusBox";


class Profile extends React.Component {

  componentDidMount() {
    this.props.getProfile();
  }

  toggleRepo = (repo) => () => {
    this.props.toggleRepo(repo.github_id, !repo.is_active);
  }

  render() {

    if (this.props.isFetching) {
      return (<p className="loading-block">Loading...</p>);
    }

    if (this.props.error !== null && this.props.error !== undefined) {
      return (<p>Error! [{this.props.error}]</p>);
    }

    let rows = [];

    if (this.props.repoList !== null && this.props.repoList !== undefined) {
      this.props.repoList.forEach(r => {
        rows.push(
          <StatusBox
            repo={r}
            isFetching={false}
            toggle={this.toggleRepo(r)}>
          </StatusBox>
        );
      });
      return (
        <div>{rows}</div>
      );
    }
    else {
      return (<p>No Repos Found</p>);
    }
  }
}

Profile.propTypes = {
  /**
   * Get the profile for the authenticated user
   */
  getProfile: PropTypes.func.isRequired,
  /**
   * Toggles the active status on a repo
   */
  toggleRepo: PropTypes.func.isRequired,
  /**
   * The repository to show
   */
  repoList: PropTypes.array,
  /**
   * The repos currently being loaded
   */
  fetchingRepoList: PropTypes.array,
  /**
   * Loading indicator
   */
  isFetching: PropTypes.bool,
  /**
   * Error Code
   */
  error: PropTypes.string,
};

export default Profile;
