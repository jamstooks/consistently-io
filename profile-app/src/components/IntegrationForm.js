import React from 'react';
import PropTypes from "prop-types";
import debounce from "lodash/debounce";

class IntegrationForm extends React.Component {

  getType = (key) => {
    // @todo - would be nice to get this from the api
    let type = "text";
    if (key.includes("url")) {
      type = "url";
    }
    else if (key.includes("is_active")) {
      type = "checkbox";
    }
    else if (key === "deployment_delay") {
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

  // @todo - look at a better way to link these dispatches,
  // but retain the debounce... see `src/utils.js`
  handleChange = e => {
    this.props.handleFieldChange(e);
    setTimeout(() => { this.handleSubmit() }, 100);
  }

  handleSubmit = debounce(e => {
    console.log("submitting");
    console.log(this.props.values);
    this.props.handleSubmit(this.props.values);
  }, 400);

  render() {

    let fields = [];
    Object.keys(this.props.values).forEach((k, i) => {

      let type = this.getType(k);

      let val = this.props.values[k];
      if (val === null) {
        val = "";
      }

      let error = [];
      if (this.props.errors !== null && this.props.errors !== undefined) {
        if (k in this.props.errors) {
          this.props.errors[k].forEach((e, i) => {
            let key = "e-" + k + "-" + i;
            error.push((<p key={key} className="warning">{e}</p>));
          });
        }
      }

      let input = (<input
            value={val}
            type={this.getType(k)}
            name={k}
            id={k}
            onChange={this.handleChange}/>)

      if (type === "checkbox") {
        input = (<input
              checked={val}
              type={this.getType(k)}
              name={k}
              id={k}
              onChange={this.handleChange}/>)
      }

      fields.push((
        <div key={k}>
          <label htmlFor={k}>
            {this.keyToLabel(k)}:
            {error}
          </label>
          {input}
        </div>
      ));
    });

    return (
      <form onSubmit={this.handleSubmit} className="integration-form">
        {fields}
      </form>
    )
  }
}

IntegrationForm.propTypes = {
  /**
   * the fields and values
   * 
   * [{name: ..., label: ..., value: ...}, ...]
   */
  values: PropTypes.object.isRequired,
  /**
   * any errors
   */
  errors: PropTypes.object,
  /**
   * Submit the form
   */
  handleSubmit: PropTypes.func.isRequired,
  handleFieldChange: PropTypes.func.isRequired
};

export default IntegrationForm
