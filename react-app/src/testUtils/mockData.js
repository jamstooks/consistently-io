export const mockProfileRepos = [{
    'prefix': 'prefix1',
    'name': 'repo1',
    'github_id': 123,
    'is_active': true,
    'settings_url': '#',
    'id': 1
  },
  {
    'prefix': 'prefix1',
    'name': 'repo2',
    'github_id': 124,
    'is_active': false,
    'settings_url': '#',
    'id': 2
  }
];

export const mockSettings = [
  { id: 1, is_active: false, type: 'html' },
  { id: 2, is_active: false, type: 'travis' }
];

export const mockIntegration = {
  is_active: false,
  url_to_validate: null,
  deployment_delay: null
};
