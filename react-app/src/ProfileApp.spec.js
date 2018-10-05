import React from 'react';
import ReactDOM from 'react-dom';
import ProfileApp from './ProfileApp';

// added mock fetch for Profile component's `componentDidMount` calls
import fetchMock from "fetch-mock";
import { mockProfileRepos } from "./testUtils/mockData"


it('renders without crashing', () => {

  fetchMock.get("*", mockProfileRepos);


  const div = document.createElement('div');
  ReactDOM.render(<ProfileApp />, div);
  ReactDOM.unmountComponentAtNode(div);

  fetchMock.reset();
  fetchMock.restore();
});
