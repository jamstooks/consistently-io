# repo-config-app

Handles integration configurations for a repository.

## Data

This connects to the `integration-list` and `integration-detail` api
endpoints to get the list of integrations for a repo and to edit
those integrations.

The repo itself is passed in using the `window.repo` variable, for
lack of a better option.

## State Shape

    {
      fetchingList: <bool>,
      integrations: {
        <int:id>: {
          integration_type: <string>,
          is_active: <string>
        },
        ...
      },
      currentIntegration: {
        isFetching: <bool>,
        id: <int>,
        is_active: <bool>,
        ...<unique props>
      }
    }

Note: Since integration props vary I have to have a separate
`currentIntegration` that is actually one in `integrations`.

With something this simple, there doesn't appear to be a need
for further normalization at the moment.

