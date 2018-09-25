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
            └── static/
                └── logo.png

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
integration...

# Add tests

Test all your things! This includes integration tests for your `run` method.

# Validation

Since integration objects exist before they have values, we'll need to
perform some additional validation when they are set to active.
Django Rest Framework doesn't support the clean method by default, but
[we can still use it](http: // www.django-rest-framework.org/topics/3.0-announcement /  # differences-between-modelserializer-validation-and-modelform)
for validation in the api.
