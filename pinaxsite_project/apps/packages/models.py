import datetime
import json

from django.db import models

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
    
    def repo(self):
        if "://github.com" in self.repo_url:
            return self.repo_url.replace(
                "http://github.com/", ""
            ).replace(
                "https://github.com/", ""
            ).strip("/")
        return None
    
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
            url = "http://github.com/api/v2/json/commits/list/%s/%s" % (self.package.repo(), self.branch_name)
            print "\tGetting commits for page %s" % page
            data = json.loads(requests.get(url).content)
            commits = []
            while data.get("error") != "Not Found":
                commits.extend(data.get("commits", []))
                page += 1
                next_url = url + "?page=%s" % page
                print "\tGetting commits for page %s" % page
                data = json.loads(requests.get(next_url).content)
            print "\t%s Total Commits" % len(commits)
        return commits
    
    @classmethod
    def active_branches(cls):
        return cls.objects.filter(active=True)


class Person(DateAuditModel):
    
    name = models.CharField(max_length=128)
    login = models.CharField(max_length=64)
    email = models.CharField(max_length=128)


class Commit(DateAuditModel):
    """
    $ curl http://github.com/api/v2/json/commits/list/mojombo/grit/master
    {
          "commits": [
            {
              "package_branch": <obj>,   # modified to include reference to PackageBranch
              "parents": [
                {
                  "id": "e3be659a93ce0de359dd3e5c3b3b42ab53029065"
                }
              ],
              "author": {
                "name": "Ryan Tomayko",
                "login": "rtomayko",
                "email": "rtomayko@gmail.com"
              },
              "url": "/mojombo/grit/commit/6b7dff52aad33df4bfc0c0eaa88922fe1d1cd43b",
              "id": "6b7dff52aad33df4bfc0c0eaa88922fe1d1cd43b",
              "committed_date": "2010-12-09T13:50:17-08:00",
              "authored_date": "2010-12-09T13:50:17-08:00",
              "message": "update History.txt with bug fix merges",
              "tree": "a6a09ebb4ca4b1461a0ce9ee1a5b2aefe0045d5f",
              "committer": {
                "name": "Ryan Tomayko",
                "login": "rtomayko",
                "email": "rtomayko@gmail.com"
              }
            }
        ]
    }
    """
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
