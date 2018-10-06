import React from "react";
import PropTypes from "prop-types";
import ReactMarkdown from "react-markdown";

import IntegrationForm from "./IntegrationForm";


class IntegrationConfig extends React.Component {

  handleSubmit = values => {
    this.props.updateIntegration(this.props.integration.id, values);
  }

  handleFieldChange = event => {
    let val = (event.target.type === "checkbox") ?
      event.target.checked :
      event.target.value;
    this.props.changeFormValue(event.target.id, val);
  }

  render() {

    let obj = this.props.integration.obj;
    let form = this.props.integration.form;

    if (this.props.error !== null && this.props.error !== undefined) {
      return (<p>Error! [{this.props.error}]</p>);
    }

    let toggleClass = 'inactive';
    let configClass = 'config ';
    let description = null;
    let notes = null;
    let loadingIndicator = null;

    if (this.props.integration.isFetching) {
      return (<p className="loading-block">Loading...</p>);
    }
    else {

      if (obj !== null && obj !== null) {

        if (obj.is_active) { toggleClass = 'active'; }
        if (form.isUpdating) {
          loadingIndicator = (
            <div className="loading-block form-loading-indicator"></div>);
        }

        let fullIntegration = this.props.allIntegrations.find(
          (i) => i.id === this.props.integration.id);

        description = (
          <ReactMarkdown source={fullIntegration.description} />);
        notes = (
          <ReactMarkdown source={fullIntegration.notes} />);
        configClass += 
          fullIntegration.integration_type + "-integration-background";

        if (form !== null && form !== undefined) {
          form = (<IntegrationForm
            values={form.values}
            errors={form.errors}
            handleSubmit={this.handleSubmit}
            handleFieldChange={this.handleFieldChange} />);
        }
      }
    }

    let warning = "";
    if (form !== null && form.errors !== null && form.errors !== undefined) {
      warning = (<p className="warning">Please fix the errors below.</p>);
    }

    return (
      <div className={configClass}>
        <div className="back-button" onClick={() => this.props.unselect()}>
          &lt;&lt;
        </div>
        <div className={"toggle-switch " + toggleClass}></div>
        {loadingIndicator}
  
        <div className="details">
          {description}
        </div>

        {warning}        
        {form}
        <p className="notes">{notes}</p>
      </div>
    );
  }
}


IntegrationConfig.propTypes = {
  /**
   * The obj integration
   */
  integration: PropTypes.object.isRequired,
  /**
   * All the integrations (to access additional fields)
   */
  allIntegrations: PropTypes.array.isRequired,
  /**
   * Deselects the obj integration
   */
  unselect: PropTypes.func.isRequired,
  /**
   * Sends update request for integration
   */
  updateIntegration: PropTypes.func.isRequired,
  /**
   * 
   */
  changeFormValue: PropTypes.func.isRequired
};

export default IntegrationConfig;
