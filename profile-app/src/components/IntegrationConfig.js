import React from "react";
import PropTypes from "prop-types";


class IntegrationConfig extends React.Component {

  getType = (key) => {
    // @todo - would be nice to get this from the api
    let type = "text";
    if(key.includes("url")) {
      type = "url";
    }
    else if(key === "deployment_delay") {
      type = "number"
    }
    return type;
  }
  
  keyToLabel = (key) => {
    var re = new RegExp("_", 'g');
    let label = key.replace(re, " ");
    label = label.replace("url", "URL");
    return label.charAt(0).toUpperCase() + label.slice(1);
  }

  render() {
    
    let current = this.props.integration.obj;

    if (this.props.isFetching) {
      return (<p className="loading-block">Loading...</p>);
    }

    if (this.props.error !== null && this.props.error !== undefined) {
      return (<p>Error! [{this.props.error}]</p>);
    }
    
    let toggleClass = 'inactive';
    
    let fields = [];
    if(current !== null && current !== null) {
      
      toggleClass = 'active';
      
      Object.keys(current).forEach((key, index) => {
        
        if(key !== "is_active") {
          fields.push(<div>
            <label for={key}>
              {this.keyToLabel(key)}:
              <p class="warning">Invalid URL.</p>
            </label>
            <input
              value={current[key]}
              type={this.getType(key)}
              name={key}
              id={key} required />
          </div>);
        }
      });
    }
    
    return (
      <div class="config">
        <div className="back-button" onClick={() => this.props.unselect()}>
          &lt;&lt;
        </div>
        <div className={"toggle-switch " + toggleClass}></div>
  
        <p className="details">
          <strong>HTML Validation</strong> - service provided by
          <a href="#">W3C.org</a>
        </p>
  
        <p className="warning">URL is required to activate.</p>
        <form action="" method="get" className="integration-form">
          {fields}
        </form>
        <p className="notes">
          Currently we only support one URL per repo.
        </p>
      </div>
    );
  }
}
/*
        <div>
          <label for="name">
                    URL to Validate:
                    <p class="warning">Invalid URL.</p>
                  </label>
          <input type="url" name="name" id="name" required />
        </div>
        <div>
          <label for="delay">Delay (seconds): </label>
          <input type="number" name="delay" id="delay" />
        </div>
*/

IntegrationConfig.propTypes = {
  /**
   * The current integration
   */
  integration: PropTypes.object.isRequired,
  /**
   * Deselects the current integration
   */
  unselect: PropTypes.func.isRequired,
  /**
   * Sends update request for integration
   */
  update: PropTypes.func.isRequired,
};

export default IntegrationConfig;
