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
      classes = "integration-logo "
      classes += i.integration_type + "-integration-background";;
      if (i.is_active) {
        classes += " active";
      }
      integrations.push(
        (<div
          key={i.id}
          className={classes}
          onClick={() => this.props.select(i.id)}>
          <span class="screen-reader">{classes}</span>
        </div>)
      );
    });

    return (
      <div className="grid-container">
        <div className="integration-grid">
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
