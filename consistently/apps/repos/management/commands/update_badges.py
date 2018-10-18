from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from pybadges import badge
import os

from consistently.apps.integrations.models import INTEGRATION_TYPES
from consistently.apps.repos.utils import get_badge_name


LEFT_TEXT = "deployment goals"
# LOGO = 'https://consistently.io/static/img/menu_icon.svg'


class Command(BaseCommand):
    help = "Creates any necessary badges and adds them to `static`"

    def handle(self, *args, **options):
        """
        Given the number integrations we need badges for each possible outcome

        For example, if there are 3 integrations, then we need:
        pending
        0/0
        0/1, 1/1
        0/2, 1/2, 2/2
        0/3, 1/3, 2/3, 3/3
        """

        grey = 'lightgrey'
        green = '#93c47d'
        orange = '#f6b26b'

        # the "pending" badge
        filename = get_badge_name(None, None, 1)
        self.write_badge(filename, 'pending', grey)

        for i in range(len(INTEGRATION_TYPES)+1):
            for j in range(i+1):

                color = green if j == i else orange

                self.write_badge(
                    get_badge_name(j, i-j, 0),
                    "%d / %d" % (j, i),
                    color if i != 0 else grey)

    def write_badge(self, filename, right, color):
        """
        writes a badge to the given `filename`
        with `right` content and `color` background
        """

        print("making badge: %s - %s - %s" % (filename, right, color))

        outfile = os.path.join(
            settings.PROJECT_DIR, 'static', 'img', 'badges', filename)
        f = open(outfile, 'w')

        b = badge(
            left_text=LEFT_TEXT,
            right_text=right,
            right_color=color)
        # logo = LOGO)

        f.write(b)
        f.close()
