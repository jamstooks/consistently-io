# Integrations

Consistently.io is designed to support a variety of integrations.

# Creating Integrations

Integrations have a set structure.

integrations/
    └── types/
    └── your_integration_app/
    ├── __init__.py
    ├── models.py
    ├── README.md
    ├── serializer.py
    └── tests.py

# Add a README to tell us about this integration


# Create the IntegrationConfig model

Your model should extend `integrations.models.Integration` and
define the following methods:

    - `description(self)` - markdown appears above the config form
    - `notes(self)` - markdown appears below the config form
    - `get_serializer_class(self)` - a custom serializer if necessary

Add this model to `integrations.models.INTEGRATION_TYPES`

# Build the worker method

Your model should also define `run(self, commit)`. This method will create
or update an `IntegrationStatus` object for the commit.

You may also need to override `get_task_kwargs` and `get_task_delay`,
if your integration requires retries or a custom delay.

`get_task_kwargs` should return the following:

        {'max_retries': 5, 'countdown:': 0.2}
        
`max_retries` defaults to 0
`countdown` defaults to 60 seconds

You can trigger the task to retry by raising the
`integrations.tasks.NeedsToRetry` exception.

# Add a Serializer

Your serializer will be used to validate a user's configuration for your
integration. You actually only need one if your integration has specific
properties, like a delay or URL.

# Style it up!

Add your logo to `static/img/integrations` and your
styles to `static/css/integrations.css`.

# Add tests

Test all your things! This includes integration tests for your `run` method.
