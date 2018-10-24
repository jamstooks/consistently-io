import json
import requests

from django.conf import settings
from ...models import IntegrationStatus

import logging
logger = logging.getLogger(__name__)

BASE_URL = "https://www.googleapis.com/pagespeedonline/v4/runPagespeed"


def get_pagespeed_score(status):
    """
    Gets a pagespeed score from the pagespeed insights API

    Updates the IntegrationStatus accordingly.

    @todo - might consider allowing retrying for some errors
    """

    with_settings = json.loads(status.with_settings)

    strategy = 'desktop'
    if ('use_mobile_strategy' in with_settings[0]['fields'] and
            with_settings[0]['fields']['use_mobile_strategy']):
        strategy = 'mobile'

    params = {
        'url': with_settings[0]['fields']['url'],
        'key': settings.GOOGLE_API_KEY,
        'strategy': strategy
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != requests.codes.ok:
        logger.error(
            'Pagespeed error response',
            exc_info=True,
            extra={'response': response, 'params': params})
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
    status.value = "%s: %d%%" % (strategy.capitalize(), score)
    status.details = result['pageStats']
    status.save()
