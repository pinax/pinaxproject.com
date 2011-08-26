from django.core.management.base import NoArgsCommand

from dateutil import parser

from packages.models import Commit, Person, Package


class Command(NoArgsCommand):
    help = "Populate local cache of recent commits for Projects"

    def handle_noargs(self, **options):
        for package in Package.objects.all():
            for branch in package.active_branches():
                print "%s (%s)" % (package.name, branch.branch_name)
                
                for commit in branch.fetch_commits():
                    author, _ = Person.objects.get_or_create(
                        name=commit["author"]["name"],
                        login=commit["author"]["login"],
                        email=commit["author"]["email"]
                    )
                    committer, _ = Person.objects.get_or_create(
                        name=commit["committer"]["name"],
                        login=commit["committer"]["login"],
                        email=commit["committer"]["email"]
                    )
                    Commit.objects.get_or_create(
                        branch=branch,
                        author=author,
                        committer=committer,
                        url=commit["url"],
                        sha=commit["id"],
                        committed_date=parser.parse(commit["committed_date"]),
                        authored_date=parser.parse(commit["authored_date"]),
                        message=commit["message"]
                    )
