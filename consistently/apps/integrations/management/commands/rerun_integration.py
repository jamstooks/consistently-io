from django.core.management.base import BaseCommand, CommandError

from consistently.apps.repos.models import Commit


class Command(BaseCommand):
    help = """
Runs the integration of a specific type for a commit

Accepts the commit's `sha` and the `type` of the integration to run
    """

    def add_arguments(self, parser):
        parser.add_argument('sha')
        parser.add_argument('type')

    def handle(self, *args, **options):

        sha = options['sha']
        commit = Commit.objects.get(sha=sha)
        _type = options['type']
        status = commit.integrationstatus_set.get(
            integration__integration_type=_type)

        integration = status.integration.type_instance

        if integration.is_active:
            print("running %s on %s" % (integration, commit))
            integration.run(status)
        else:
            print("integration isn't active")
