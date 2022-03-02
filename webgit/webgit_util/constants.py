from typing import List

ENV_DEFAULT_REMOTE: str = "WEBGIT_DEFAULT_REMOTE"

ENV_DEFAULT_USER: str = "WEBGIT_DEFAULT_USER"

ENV_DEFAULT_UPSTREAM_REPO_NAME: str = "WEBGIT_DEFAULT_UPSTREAM_REPO_NAME"

ENV_DEFAULT_ORIGIN_REPO_NAME: str = "WEBGIT_DEFAULT_ORIGIN_REPO_NAME"

REGEX_BRANCH = r'\*\s+(\S+)\s+([0-9a-f]{7,40})\s+(\[(\S+)\/(\S+)?.*\])?.*'

REGEX_REMOTE_REPO: str = r'(\w+)\s+(https\:\/\/|git@)(\S+)\s+\((\w+)\)'

REGEX_URL: str = r'(.*)\/(.*)\/(.*)'

REGEX_COMMIT_HASH: str = r'^[0-9a-f]{7,40}$'

REGEX_PULL_REQUEST_HASH: str = r'^(#?)(\d+)$'

SUPPORTED_WEB_HOSTS: List[str] = ["github", "gitlab"]

WEB_ADDRESS_TEMPLATES: dict = {
    "org_or_user": {
        "github": "https://github.com/{}",
        "gitlab": "https://gitlab.com/{}",
    },

    "commit": {
        "github": "https://{}/commit/{}",
        "gitlab": "https://{}/-/commit/{}",
    },

    "commits": {
        "github": "https://{}/commits",
        "gitlab": "https://{}/-/commits",
    },

    "issue": {
        "github": "https://{}/issues/{}",
        "gitlab": "https://{}/-/issues/{}",
    },

    "issues": {
        "github": "https://{}/issues",
        "gitlab": "https://{}/-/issues",
    },

    "pr": {
        "github": "https://{}/compare/{}...{}:{}?expand=1",
        "gitlab": "https://{}/-/compare?from={}&to={}",
    },

    "prs": {
        "github": "https://{}/pulls",
        "gitlab": "https://{}/-/merge_requests",
    },

    "myprs": {
        "github": "https://{}/pulls?q=is%3Apr+author%3A{}",
        "gitlab": "https://{}/-/merge_requests?scope=all&state=all&author_username={}",
    },

    "tree": {
        "github": "https://{}/tree/{}",
        "gitlab": "https://{}/-/tree/{}",
    },

    "tree_file": {
        "github": "https://{}/blob/{}/{}",
        "gitlab": "https://{}/-/blob/{}/{}",
    },

}
