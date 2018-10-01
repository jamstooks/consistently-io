import React from "react";
import PropTypes from "prop-types";

import IntegrationGrid from "./IntegrationGrid";
import IntegrationConfig from "./IntegrationConfig";


class Settings extends React.Component {

  componentDidMount() {
    this.props.getIntegrations();
  }

  render() {

    if (this.props.error !== null && this.props.error !== undefined) {
      return (<p>Error! [{this.props.error}]</p>);
    }

    let classes = "repo-settings";
    if (this.props.current.id !== null && this.props.current.id !== undefined) {
      classes += " config-mode";
    }

    return (
      <div class={classes}>
        <IntegrationGrid
          isFetching={this.props.integrations.isFetching}
          integrationList={this.props.integrations.list}
          select={this.props.fetchIntegration} />
        <IntegrationConfig
          integration={this.props.current}
          unselect={this.props.unselect} />
      </div>
    );
  }
}

Settings.propTypes = {
  /**
   * The available integrations
   */
  integrations: PropTypes.object.isRequired,
  /**
   * The currently selected integration
   */
  current: PropTypes.object.isRequired,


  /**
   * Get the list of integrations for the repo
   */
  getIntegrations: PropTypes.func.isRequired,
  /**
   * Fetches a specific integration
   */
  fetchIntegration: PropTypes.func.isRequired,
  /**
   * Updates in integration
   */
  // updateIntegration: PropTypes.func.isRequired,
  /**
   * Deselects the current integration
   */
  unselect: PropTypes.func.isRequired,
};

export default Settings;
