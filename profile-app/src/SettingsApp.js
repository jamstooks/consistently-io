import React, { Component } from 'react';
import { createStore, applyMiddleware } from "redux";
import thunkMiddleware from "redux-thunk";
import { createLogger } from "redux-logger";
import { Provider } from "react-redux";

import Settings from "./containers/Settings";
import rootReducer from "./reducers/integrations";


const loggerMiddleware = createLogger();

const store = createStore(
  rootReducer,
  applyMiddleware(thunkMiddleware, loggerMiddleware)
);

class SettingsApp extends Component {
  render() {
    return (
      <Provider store={store}>
        <Settings/>
      </Provider>
    );
  }
}

export default SettingsApp;
