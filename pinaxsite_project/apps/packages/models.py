import datetime
import json

from django.db import models
from django.db.models import Count

import requests

from biblion.models import Post


class DateAuditModel(models.Model):
    
    date_created = models.DateTimeField(default=datetime.datetime.utcnow, editable=False)
    date_modified = models.DateTimeField(null=True, editable=False)
    
    def save(self, *args, **kwargs):
        if self.pk:
            self.date_modified = datetime.datetime.utcnow()
        super(DateAuditModel, self).save(*args, **kwargs)
    
    class Meta:
        abstract = True


class Package(DateAuditModel):
    
    MATURITY_NEW = 1           # repo created, not in use anywhere, may not have fully working code
    MATURITY_EXPERIMENTAL = 2  # used in unreleased site or project
    MATURITY_WORKING = 3       # used in a live site
    MATURITY_STABLE = 4        # used in multiple sites, api isn't changing much
    MATURITY_MATURE = 5        # 1.0, docs, tests
    
    MATURITY_CHOICES = [
        (MATURITY_NEW, "New"),
        (MATURITY_EXPERIMENTAL, "Experimental"),
        (MATURITY_WORKING, "Working"),
        (MATURITY_STABLE, "Stable"),
        (MATURITY_MATURE, "Mature"),
    ]
    
    STATUS_ACTIVE = 1      # multiple commits in the last month
    STATUS_STALE = 2       # hasn't been worked on for a while 
    STATUS_ABANDONED = 3   # no work for a very very long time
    STATUS_DEPRECATED = 4  # we plan to replace this moving forward
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_STALE, "Stale"),
        (STATUS_ABANDONED, "Abandoned"),
        (STATUS_DEPRECATED, "Deprecated")
    ]
    
    PACKAGE_APP = 1
    PACKAGE_STARTER = 2
    PACKAGE_THEME = 3
    
    PACKAGE_CHOICES = [
        (PACKAGE_APP, "App"),
        (PACKAGE_STARTER, "Starter Project"),
        (PACKAGE_THEME, "Theme")
    ]
    
    name = models.CharField(max_length=96)
    package_type = models.IntegerField(choices=PACKAGE_CHOICES)
    repo_url = models.URLField()
    description = models.TextField(null=True, blank=True)
    pinax_external = models.BooleanField(default=False)
    
    maturity_level = models.IntegerField(choices=MATURITY_CHOICES, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    
    docs_url = models.URLField(null=True, blank=True)
    blog_post = models.ForeignKey(Post, null=True, blank=True)
    cpc_tag = models.CharField(max_length=64, null=True, blank=True)
    package_name = models.CharField(max_length=96, null=True, blank=True)
    package_uses = models.ManyToManyField("Package", blank=True) # make sure that this is nullable/blankable
    
    forks = models.IntegerField(null=True, blank=True)
    watchers = models.IntegerField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    
    def last_commit(self):
        return Commit.objects.filter(
            branch__package=self
        ).latest("committed_date")
    
    def repo(self):
        if "://github.com" in self.repo_url:
            return self.repo_url.replace(
                "http://github.com/", ""
            ).replace(
                "https://github.com/", ""
            ).strip("/")
        return None
    
    def update_stats(self):
        url = "https://api.github.com/repos/%s" % self.repo()
        data = json.loads(requests.get(url).content)
        if data.get("forks"):
            self.forks = data.get("forks")
        if data.get("watchers"):
            self.watchers = data.get("watchers")
        if data.get("size"):
            self.size = data.get("size")
        self.save()
    
    def open_pull_requests(self):
        return self.pull_requests.filter(
            state=PullRequest.STATE_OPEN
        ).order_by("number")
    
    def fetch_pull_requests(self):
        pull_requests = []
        if self.repo():
            page = 1
            url = "https://api.github.com/repos/%s/pulls" % self.repo()
            data = json.loads(requests.get(url).content)
            while len(data) > 0:
                pull_requests.extend(data)
                page += 1
                next_url = url + "?page=%s" % page
                data = json.loads(requests.get(next_url).content)
            
            page = 1
            url = "https://api.github.com/repos/%s/pulls?state=closed" % self.repo()
            data = json.loads(requests.get(url).content)
            while len(data) > 0:
                pull_requests.extend(data)
                page += 1
                next_url = url + "&page=%s" % page
                data = json.loads(requests.get(next_url).content)
        return pull_requests
    
    def save(self, *args, **kwargs):
        if not self.description:
            if self.repo():
                info = json.loads(
                    requests.get("http://github.com/api/v2/json/repos/show/%s" % self.repo()
                ).content)
                if info.get("repository"):
                    self.description = info["repository"]["description"]
                else:
                    self.description = info["error"]
        super(Package, self).save(*args, **kwargs)
        if self.branches.count() == 0:
            self.branches.create(branch_name="master")
    
    @classmethod
    def apps(cls):
        return cls.objects.filter(package_type=cls.PACKAGE_APP)
    
    @classmethod
    def starter_projects(cls):
        return cls.objects.filter(package_type=cls.PACKAGE_STARTER)
    
    @classmethod
    def themes(cls):
        return cls.objects.filter(package_type=cls.PACKAGE_THEME)
    
    def __unicode__(self):
        return unicode(self.name)
    
    def active_branches(self):
        return self.branches.filter(active=True)


class PackageBranch(DateAuditModel):
    
    package = models.ForeignKey(Package, related_name="branches")
    branch_name = models.CharField(max_length=96)
    active = models.BooleanField(default=True)
    
    def fetch_commits(self):
        if self.package.repo(): # @@@ ?page=N until no more results to fetch all commits
            page = 1
            url = "https://github.com/api/v2/json/commits/list/%s/%s" % (self.package.repo(), self.branch_name)
            data = json.loads(requests.get(url).content)
            while data.get("error") != "Not Found":
                for commit in data["commits"]:
                    yield commit
                page += 1
                next_url = url + "?page=%s" % page
                data = json.loads(requests.get(next_url).content)
    
    @classmethod
    def active_branches(cls):
        return cls.objects.filter(active=True)
    
    def commit_counts_by_month(self):
        if not hasattr(self, "_commit_counts_by_month"):
            self._commit_counts_by_month = self.commits.extra(
                select={
                    "month": "DATE_TRUNC('month', \"packages_commit\".\"committed_date\")"
                }
            ).values("month").annotate(total=Count("id")).order_by("-month")[:6]
            x = list(self._commit_counts_by_month)
            x.reverse()
            self._commit_counts_by_month = x
        return self._commit_counts_by_month


class Person(DateAuditModel):
    
    github_id = models.IntegerField(null=True, blank=True)
    url = models.CharField(max_length=96, null=True, blank=True)
    avatar_url = models.CharField(max_length=255, null=True, blank=True)
    
    name = models.CharField(max_length=128, null=True, blank=True)
    login = models.CharField(max_length=64)
    email = models.CharField(max_length=128)


class PullRequest(DateAuditModel):
    
    STATE_OPEN = 1
    STATE_CLOSED = 2
    
    STATE_CHOICES = [
        (STATE_OPEN, "Open"),
        (STATE_CLOSED, "Closed")
    ]
    
    package = models.ForeignKey(Package, related_name="pull_requests")
    user = models.ForeignKey(Person, related_name="pull_requests")
    number = models.IntegerField()
    state = models.IntegerField(choices=STATE_CHOICES)
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=96)
    html_url = models.CharField(max_length=96)
    diff_url = models.CharField(max_length=96)
    patch_url = models.CharField(max_length=96, null=True, blank=True)
    issue_url = models.CharField(max_length=96, null=True, blank=True)
    created_at = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)
    merged_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    
    @property
    def how_long_open(self):
        if not self.merged_at or not self.closed_at:
            return datetime.datetime.now() - self.created_at
    
    @property
    def how_long_to_merge(self):
        if self.merged_at:
            return self.merged_at - self.created_at
    
    @property
    def how_long_to_close(self):
        if self.closed_at:
            return self.closed_at - self.created_at


class Commit(DateAuditModel):
    
    branch = models.ForeignKey(PackageBranch, related_name="commits")
    author = models.ForeignKey(Person, related_name="authored_commits")
    committer = models.ForeignKey(Person, related_name="committed_commits")
    url = models.CharField(max_length=128)
    sha = models.CharField(max_length=64)
    committed_date = models.DateTimeField()
    authored_date = models.DateTimeField()
    message = models.TextField()
    
    @classmethod
    def active_commits(cls):
        return Commit.objects.filter(branch__active=True).order_by("-committed_date")
