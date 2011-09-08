from django.core.management.base import NoArgsCommand

from dateutil import parser

from packages.models import Commit, Person, Package, PullRequest


def parse(date_str):
    if date_str:
        return parser.parse(date_str)


class Command(NoArgsCommand):
    help = "Populate local cache of recent commits for Projects"
    
    def handle_noargs(self, **options):
        for package in Package.objects.all():
            print "%s:" % package.name
            
            package.update_stats()
            
            print " Getting Pull Requests..."
            count = 0
            for pull in package.fetch_pull_requests():
                user, _ = Person.objects.get_or_create(
                    github_id = pull["user"]["id"],
                    url = pull["user"]["url"],
                    login = pull["user"]["login"],
                    avatar_url = pull["user"]["avatar_url"]
                )
                
                if pull["state"] == "closed":
                    state = PullRequest.STATE_CLOSED
                else:
                    state = PullRequest.STATE_OPEN
                
                pull_request, created = PullRequest.objects.get_or_create(
                    package=package,
                    number=pull["number"]
                )
                if created:
                    pull_request.number = pull["number"]
                    pull_request.state = state
                    pull_request.package = package
                    pull_request.user = user
                    pull_request.created_at = parse(pull["created_at"])
                    pull_request.html_url = pull["html_url"]
                    pull_request.diff_url = pull["diff_url"]
                    pull_request.url = pull["url"]
                    pull_request.patch_url = pull["patch_url"]
                    pull_request.issue_url = pull["issue_url"]
                
                pull_request.title = pull["title"]
                pull_request.body = pull["body"]
                pull_request.closed_at = parse(pull["closed_at"])
                pull_request.merged_at = parse(pull["merged_at"])
                pull_request.updated_at = parse(pull["updated_at"])
                pull_request.save()
                count += 1
            print " Total Pull Requests: %s" % count
            
            for branch in package.active_branches():
                print " (%s)" % branch.branch_name
                print "     Getting Commits..."
                count = 0
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
                    _, created = Commit.objects.get_or_create(
                        branch=branch,
                        author=author,
                        committer=committer,
                        url=commit["url"],
                        sha=commit["id"],
                        committed_date=parse(commit["committed_date"]),
                        authored_date=parse(commit["authored_date"]),
                        message=commit["message"]
                    )
                    if not created:
                        break
                    count += 1
                print "     Total Commits: %s" % count

