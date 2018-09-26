import React from "react";
import PropTypes from "prop-types";

import StatusBox from "./StatusBox";


class Profile extends React.Component {

  componentDidMount() {
    this.props.getProfile();
  }

  toggleRepo = (repoId) => () => {
    console.log("toggling repo! " + repoId);
  }

  render() {

    if (this.props.error !== null && this.props.error !== undefined) {
      return (<p>Error! [{this.props.error}]</p>)
    }

    let rows = [];

    if (this.props.repoList !== null && this.props.repoList !== undefined) {
      this.props.repoList.forEach(r => {
        rows.push(
          <StatusBox
            repo={r}
            isFetching={false}
            toggle={this.toggleRepo(r.id)}>
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
