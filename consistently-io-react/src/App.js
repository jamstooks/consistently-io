import React, { Component } from 'react';
import { createStore, applyMiddleware } from "redux";
import thunkMiddleware from "redux-thunk";
import { createLogger } from "redux-logger";
import { Provider } from "react-redux";

import Profile from "./containers/Profile";
import rootReducer from "./reducers";


const loggerMiddleware = createLogger();

const store = createStore(
  rootReducer,
  applyMiddleware(
    thunkMiddleware, // lets us dispatch() functions
    loggerMiddleware,
  )
);

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <Profile/>
      </Provider>
    );
  }
}

export default App;
