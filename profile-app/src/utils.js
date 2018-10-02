import * as actions from "../actions/integrations";
import debounce from "lodash/debounce";


/**
 * This isn't working yet, but with a few changes to api.js
 * I should be able to use this solution instead handling
 * this in the component
 * 
 * [reference](https://github.com/reduxjs/redux/issues/1676)
 */

const debouncedUpdate = debounce((id, obj) => {
    console.log("DEBOUNCED!");
    console.log(id, obj);
    actions.updateIntegration(id, obj)
}, 500);

export const updateValue = (id, value) => {

    return (dispatch, getState) => {
        return dispatch(actions.updateFormValue(id, value)).then(() => {
            let _state = getState();
            return dispatch(debouncedUpdate(_state.current.id, _state.current.form.values));
        });
    };

    // return (dispatch, getState) => {
    //   new Promise(function (resolve) {
    //       console.log("updating form " + id);
    //       console.log(value);
    //       dispatch(actions.updateFormValue(id, value));
    //       return resolve();
    //     }).then(() => {
    //       let _state = getState();
    //       dispatch(debouncedUpdate(_state.current.id, _state.current.form.values));
    //     })
    //     .catch((e) => {
    //       console.log(e);
    //     });
    // };
}
