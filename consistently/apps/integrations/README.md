# Integrations

Consistently.io is designed to support a variety of integrations.

# Creating Integrations

Integrations have a set structure.

    integrations/
    └── types/
        └── your_integration_app/
            ├── __init__.py
            ├── models.py
            ├── serializer.py
            ├── tests.py

# Create the IntegrationConfig model

Your model should extend `integrations.models.Integration` and
define the following methods:

 - `description(self)`
 - `link(self)`
 - `get_serializer_class(self)`

Add this model to `integrations.models.INTEGRATION_TYPES`

# Build the worker method

Your model should also define `run(self, commit)`. This method will create
or update an `IntegrationStatus` object for the commit.

# Add a Serializer

Your serializer will be used to validate a user's configuration for your
integration. You actually only need one if your integration has specific
properties, like a delay or URL.

# Style it up!

Add your logo to `static/img/integrations` and your
styles to `static/css/integrations.css`.

# Add tests

Test all your things! This includes integration tests for your `run` method.
