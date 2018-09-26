import React from "react";
import PropTypes from "prop-types";


class StatusBox extends React.Component {

  render() {

    let is_active = this.props.repo.is_active;

    // Toggle Class
    let className = is_active ? "active" : "inactive";
    if(this.props.isFetching) {
      className = "fetching";
    }
    
    // Repo name and link
    let fullName = this.props.repo.prefix + "/" + this.props.repo.name;
    let repoName = !is_active ?
      fullName :
      (<a href="#test">{fullName}</a>);
    
    return (
      <div class="status-box">
        <div className="status-box-repo">{repoName}</div>
        <div
          className={'status-box-settings ' + className}
          onClick={this.goToSettings}>
        </div>
        <div
          className={'status-box-toggle ' + className}
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
   * Loading indicator
   */
  isFetching: PropTypes.bool,
  /**
   * The method to toggle the `is_active` property
   */
  toggle: PropTypes.func.isRequired
};

export default StatusBox;
