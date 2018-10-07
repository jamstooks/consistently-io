import React from "react";
import PropTypes from "prop-types";


class StatusBox extends React.Component {

  render() {

    let is_active = this.props.repo.is_active;

    // Toggle Class
    let className = is_active ? "active" : "inactive";
    if (this.props.repo.isFetching) {
      className = "fetching";
    }

    // Repo name and link
    let fullName = this.props.repo.prefix + " / " + this.props.repo.name;
    let repoName = !is_active ?
      fullName :
      (<a href={this.props.repo.url}>{fullName}</a>);

    let settings = !is_active ?
      null :
      (<div
          className={'repo-box-settings ' + className}>
          <a href={this.props.repo.settings_url}
            className="settings-link">
            <span class="screen-reader">settings</span>
          </a>
        </div>);

    return (
      <div class="repo-box">
        <div className="repo-box-repo">{repoName}</div>
        { settings }
        <div
          className={'toggle-switch ' + className}
          onClick={this.props.toggle}
          ></div>
      </div>
    );
  }
}

StatusBox.propTypes = {
  /**
   * The repository to show
   */
  repo: PropTypes.object.isRequired,
  /**
   * The method to toggle the `is_active` property
   */
  toggle: PropTypes.func.isRequired
};

export default StatusBox;
