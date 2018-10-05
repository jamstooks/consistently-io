"""
    [Travis API V3](https://developer.travis-ci.org/explore/)
    
    Looks like we can do this pretty easily with requests
    and without TravisPy for now.
    
    If I could switch the sort oder on
    [this query](https://developer.travis-ci.org/explore/repo/19982802/builds?branch.name=master&limit=2&sort_by=started_at),
    then I could find a specific commit among the most recent builds,
    but I haven't been able to change the sort order and don't
    want to search a massive dictionary, so...
    
    For now, if a the latest master build isn't for this commit, then
    we'll skip it.

    [Rate Limits](https://stackoverflow.com/a/45746284/295789)
    looks we'll have to go authenticated very soon
"""

import requests
from ...models import IntegrationStatus

# States
CANCELED = 'canceled'
CREATED = 'created'
ERRORED = 'errored'
FAILED = 'failed'
PASSED = 'passed'
QUEUED = 'queued'
READY = 'ready'
STARTED = 'started'


def get_travis_state(commit):
    """
    Connect to travis to get build status
    """

    base_url = "https://api.travis-ci.org"
    headers = {
        'User-Agent': 'API Explorer',
        'Travis-API-Version': '3'
    }
    slug = "%s%%2F%s" % (commit.repo.prefix, commit.repo.name)
    url = "%s/repo/%s/builds" % (base_url, slug)

    # get the 5 most recent master builds
    # first we have to get the total builds and then get the last 5
    # `offset=-5` and `sort_by=-started_at` didn't work

    params = {'branch.name': 'master'}
    response = requests.get(url, headers=headers, params=params)
    if not response.status_code == requests.codes.ok:
        return None
    count = response.json()['@pagination']['count']
    offset = count - 5 if count > 5 else 0

    params.update({'sort_by': 'started_at', 'offset': offset})
    response = requests.get(url, headers=headers, params=params)
    if not response.status_code == requests.codes.ok:
        return None

    # see if the build was in the last 5
    state = None
    for b in response.json()["builds"]:
        if b["commit"]["sha"] == commit.sha:
            state = b['state']
            break

    return state


def get_status(status):
    """
    Receives an Integration and an IntegrationStatus

    Finds the corresponding build on Travis and checks the
    build status.

    Note: consistently.io is a realtime tool, so if the current
    master build isn't for this commit, we'll skip it.
    """

    state = get_travis_state(status.commit)

    # if the build isn't complete, raise `NeedsToRetry`
    if state in [CREATED, QUEUED, READY, STARTED, None]:
        status.value = state
        status.save()
        from ...tasks import NeedsToRetry
        raise NeedsToRetry()

    if state == PASSED:
        status.value = state
        status.status = IntegrationStatus.STATUS_CHOICES.passed
        status.save()

    if state in [CANCELED, ERRORED, FAILED]:
        status.value = state
        status.status = IntegrationStatus.STATUS_CHOICES.failed
        status.save()
