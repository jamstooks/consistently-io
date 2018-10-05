import React from 'react';
import ReactDOM from 'react-dom';
import registerServiceWorker from './registerServiceWorker';

import ProfileApp from './ProfileApp';
import SettingsApp from './SettingsApp';


let profile = document.getElementById('profileApp');
if (profile !== undefined && profile !== null) {
    ReactDOM.render(<ProfileApp />, document.getElementById('profileApp'));
}

let settings = document.getElementById('settingsApp');
if (settings !== undefined && settings !== null) {
    ReactDOM.render(<SettingsApp />, document.getElementById('settingsApp'));
}

registerServiceWorker();
