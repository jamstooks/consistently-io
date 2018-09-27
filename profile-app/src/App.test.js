import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

// added mock fetch for Profile component's `componentDidMount` calls
import fetchMock from "fetch-mock";
import { mockProfileRepos } from "./mockData"


it('renders without crashing', () => {

  fetchMock.get("*", mockProfileRepos);


  const div = document.createElement('div');
  ReactDOM.render(<App />, div);
  ReactDOM.unmountComponentAtNode(div);

  fetchMock.reset();
  fetchMock.restore();
});
