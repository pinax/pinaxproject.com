import slumber


class GitHubApi(slumber.API):
    
    class Meta:
        base_url = "https://api.github.com/"
        format = "json"
        append_slash = False


class GitHubV2Api(slumber.API):
    
    class Meta:
        base_url = "https://github.com/api/v2/json/"
        format = "json"
        append_slash = False
