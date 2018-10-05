# SettingsApp

Handles integration configurations for a repository.

## Data

This connects to the `integration-list` and `integration-detail` api
endpoints to get the list of integrations for a repo and to edit
those integrations.

The repo itself is passed in using the `window.repo` variable, for now.

## State Shape

    {
      integrations: {
        isFetching: <bool>,
        list: [{
          id: <int:id>,
          integration_type: <string>,
          is_active: <string>,
          markdown: <string>,
          ...
        }
        ...],
        error: <string>
      },
      current: {
        id: <int:id>,
        isFetching: <bool>,
        error: <string>,
        obj: <obj>,
        form: {
          isUpdating: <bool>,
          values: <obj>,
          errors: <obj> or null,
        }
      }
    }

Note: Since integration props vary I have to have a separate
`current` even thought is is duplicated in `integrations`.

However, with something this simple, there doesn't appear to be a need
for further optimization at the moment.

## Actions and Reducers

 - `actions.integrations.*`
 - `reducers.integrations.*`