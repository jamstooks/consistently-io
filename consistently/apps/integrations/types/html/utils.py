import json
import requests

from ...models import IntegrationStatus


VALIDATOR_URL_PATTERN = "https://validator.w3.org/nu/?doc=%s&out=json"


def get_validation_status(status):
    """
    Receives an Integration and an IntegrationStatus

    Validates a Integration's URL with the W3 Markup Validation Service
    and updates and saves the IntegrationStatus
    """
    integration = status.integration.htmlvalidation
    with_settings = {
        'url_to_validate': integration.url_to_validate,
        'deployment_delay': integration.deployment_delay
    }
    status.with_settings = json.dumps(with_settings)

    url = VALIDATOR_URL_PATTERN % integration.url_to_validate
    r = requests.get(url)
    if r.status_code != 200:
        status.status = IntegrationStatus.STATUS_CHOICES.failed
        status.value = "Connection Failed"
        status.details = "Status Code: %d for %s" % (r.status_code, url)
        status.save()
        return

    warning_count = 0
    error_count = 0
    error_details = None
    r_json = r.json()
    for m in r_json['messages']:
        if m['type'] == 'info' and m['subType'] == "warning":
            warning_count += 1
        if m['type'] == 'error':
            error_count += 1
        if m['type'] == 'non-document-error':
            error_count += 1
            error_details = m['message']

    if not error_count and not warning_count:
        status.status = IntegrationStatus.STATUS_CHOICES.passed
        status.value = "Valid HTML"
        status.details = "Validated using %s" % url
        status.save()

    else:
        status.status = IntegrationStatus.STATUS_CHOICES.failed
        status.value = "Failed"
        if error_details:
            status.details = error_details
        else:
            status.details = "%d Errors, %d Warnings" % (
                error_count, warning_count)
        status.save()
