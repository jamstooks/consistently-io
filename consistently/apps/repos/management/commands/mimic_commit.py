from django.core.management.base import BaseCommand, CommandError
from django.http import HttpRequest
from datetime import datetime

from consistently.apps.repos.models import Repository, Commit
from consistently.apps.integrations.tasks import queue_integration_tasks


class Command(BaseCommand):
    help = """
Mimics the sending of a commit to GithubWebhookView.

If the commit already exists, it will be deleted and recreated.

Will trigger worker, so you should have celery running.
    """

    def add_arguments(self, parser):
        parser.add_argument('repo_github_id')
        parser.add_argument('sha')

    def handle(self, *args, **options):

        github_id = options['repo_github_id']
        sha = options['sha']

        repo = Repository.objects.get(github_id=github_id)

        try:
            commit = Commit.objects.get(sha=sha)
            print("deleting existing commit")
            commit.delete()
        except:
            print("creating commit")

        commit = Commit.objects.create(
            repo=repo,
            sha=sha,
            message="mimicked commit",
            github_timestamp=datetime.now().isoformat()
        )
        repo.latest_commit = commit
        repo.save()

        print("queuing up tasks for commit: %s" % commit)
        queue_integration_tasks(commit)
