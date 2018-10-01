import React from "react";
import PropTypes from "prop-types";


class IntegrationGrid extends React.Component {

  render() {

    if (this.props.isFetching) {
      return (<p className="loading-block">Loading...</p>);
    }

    if (this.props.error !== null && this.props.error !== undefined) {
      return (<p>Error! [{this.props.error}]</p>);
    }

    let integrations = [];
    let classes = null;
    this.props.integrationList.forEach((i) => {
      classes = "integration-logo " + i.integration_type;
      if (i.is_active) {
        classes += " active";
      }
      integrations.push(
        (<div className={classes} onClick={() => this.props.select(i.id)}></div>)
      )
    });

    return (
      <div class="grid-container">
        <div class="integration-grid">
          {integrations}
        </div>
      </div>
    );
  }
}

IntegrationGrid.propTypes = {

  isFetching: PropTypes.bool.isRequired,
  /**
   * Available integrations
   */
  integrationList: PropTypes.array.isRequired,
  /**
   * Selects an integration
   */
  select: PropTypes.func.isRequired,
};

export default IntegrationGrid;
