"""
    [Coveralls API](https://docs.coveralls.io/api-introduction)

    
    https://coveralls.io/builds/<sha>.json
"""


import requests
from ...models import IntegrationStatus


def get_status(status):
    """
    Receives an Integration and an IntegrationStatus

    Find the build on Coveralls. Retry if not found or not done.
    """
    from ...tasks import NeedsToRetry

    BASE_URL = "https://coveralls.io/builds/%s.json"
    url = BASE_URL % status.commit.sha

    try:
        response = requests.get(url)
    except:
        raise NeedsToRetry()

    if response.status_code == requests.codes.ok and response.json():

        if 'covered_percent' in response.json():

            percent = response.json()['covered_percent']
            status.value = "%d%% Coverage" % round(percent)
            if percent >= 90:
                status.status = IntegrationStatus.STATUS_CHOICES.passed
            else:
                status.status = IntegrationStatus.STATUS_CHOICES.failed
            status.save()
            return

    raise NeedsToRetry()
