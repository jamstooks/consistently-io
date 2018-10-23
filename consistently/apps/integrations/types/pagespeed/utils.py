import json
import requests
from django.conf import settings

from ...models import IntegrationStatus

BASE_URL = "https://www.googleapis.com/pagespeedonline/v4/runPagespeed"


def get_pagespeed_score(status):
    """
    Gets a pagespeed score from the pagespeed insights API

    Updates the IntegrationStatus accordingly.

    @todo - might consider allowing retrying for some errors
    """

    with_settings = json.loads(status.with_settings)

    response = requests.get(
        BASE_URL,
        params={
            'url': with_settings[0]['fields']['url'],
            'key': settings.GOOGLE_API_KEY,
            # 'strategy': 'mobile',
        })

    if response.status_code != requests.codes.ok:
        status.status = IntegrationStatus.STATUS_CHOICES.failed
        status.value = "Failed (%s)" % response.status_code
        status.details = response.status_code  # @todo - maybe something else here?
        status.save()
        return

    result = response.json()

    if 'error' in result:
        status.status = IntegrationStatus.STATUS_CHOICES.failed
        status.value = "Failed"
        status.details = "\n".join(result['error']['errors'])
        status.save()
        return

    score = result['ruleGroups']['SPEED']['score']
    if score >= 90:
        status.status = IntegrationStatus.STATUS_CHOICES.passed
    else:
        status.status = IntegrationStatus.STATUS_CHOICES.failed
    status.value = "%d / 100" % score
    status.details = result['pageStats']
    status.save()
