from operator import itemgetter


def merge_commits(commit_lists):
    """
    Expects an iterable of lists of the "commits" node from the GitHub API
    
    $ curl http://github.com/api/v2/json/commits/list/mojombo/grit/master
    {
          "commits": [
            {
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
    one_list = []
    for l in commit_lists:
        one_list.extend(l)
    
    return sorted(
        one_list,
        key=itemgetter("committed_date"),
        reverse=True
    )
