import json
import requests

from ...models import IntegrationStatus


VALIDATOR_URL_PATTERN = "https://validator.nu/?doc=%s&out=json"


def get_validation_status(status):
    """
    Receives an Integration and an IntegrationStatus

    Validates a Integration's URL with the W3 Markup Validation Service
    and updates and saves the IntegrationStatus
    """

    integration = status.integration.htmlvalidation
    with_settings = json.loads(status.with_settings)

    print("checking integration: %s" % integration)

    url = VALIDATOR_URL_PATTERN % with_settings[0]['fields']['url_to_validate']

    response = requests.get(url)

    if response.status_code != 200:
        status.status = IntegrationStatus.STATUS_CHOICES.failed
        status.value = "Connection Failed"
        status.details = "Status Code: %d for %s" % (response.status_code, url)
        status.save()
        print(status.value)
        return status.status

    warning_count = 0
    error_count = 0
    error_details = None
    r_json = response.json()
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
        print(status.value)
        return status.status

    else:
        status.status = IntegrationStatus.STATUS_CHOICES.failed
        status.value = "Failed"
        if error_details:
            status.details = error_details
        else:
            status.details = "%d Errors, %d Warnings" % (
                error_count, warning_count)
        status.save()
        print(status.value)
        return status.status
