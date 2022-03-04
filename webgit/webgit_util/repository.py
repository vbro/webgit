import re
import subprocess
from dataclasses import dataclass

from .constants import (
    REGEX_BRANCH,
    REGEX_REMOTE_REPO,
    SUPPORTED_WEB_HOSTS,
    REGEX_URL,
)
from enum import IntEnum
from typing import List


class GitRemoteRepoActionType(IntEnum):
    FETCH = 1
    PUSH = 2


class GitRemoteRepoConnectionType(IntEnum):
    SSH = 1
    HTTPS = 2


class GitException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


@dataclass
class BranchInfo:
    from_branch: str
    to_repo: str
    to_branch: str


class GitRemoteRepo:

    def __init__(
            self,
            name: str or None,
            url: str or None,
            git_repo_action_type: GitRemoteRepoActionType or None,
            git_repo_connection_type: GitRemoteRepoConnectionType or None,
            command_line_str: str):

        self.name: str = name
        self.url: str = url
        self.repo_action_type: GitRemoteRepoActionType = git_repo_action_type
        self.repo_connection_type: GitRemoteRepoConnectionType = git_repo_connection_type
        self.repo: str = ""
        self.org_or_user: str = ""
        self.web_host: str = ""

        if command_line_str is not None:
            remote_repo_regex_match: re.Match = re.search(REGEX_REMOTE_REPO, command_line_str.lower())

            self.name = remote_repo_regex_match.group(1)

            type_str: str = remote_repo_regex_match.group(2)
            if type_str.startswith("http"):
                self.repo_connection_type = GitRemoteRepoConnectionType.HTTPS
            elif type_str.startswith("git"):
                self.repo_connection_type = GitRemoteRepoConnectionType.SSH

            self.url = sanitize_url(remote_repo_regex_match.group(3))

            self.repo_action_type = GitRemoteRepoActionType.__members__.get(remote_repo_regex_match.group(4).upper())
            for s in SUPPORTED_WEB_HOSTS:
                if self.url.__contains__(s):
                    self.web_host = s
                    break

            url_regex_match: re.Match = re.search(REGEX_URL, self.url)
            self.org_or_user = url_regex_match.group(2)
            self.repo = url_regex_match.group(3)


def get_remote_output(git_dir: str) -> str:
    p_open = subprocess.Popen(["git", "-C", git_dir, "remote", "-v"], stdout=subprocess.PIPE, encoding="utf-8")
    return p_open.stdout.read()


def get_repos_from_git_remote_output(remote_output: str) -> List[GitRemoteRepo]:
    if not remote_output:
        raise GitException("Git repository not available")

    fatal_outputs: List[str] = ["fatal: cannot change to", "fatal: not a git repository"]
    if any(remote_output.startswith(fatal_output) for fatal_output in fatal_outputs):
        raise GitException(remote_output)

    remote_repos = []
    for remote_line in remote_output.strip().split("\n"):
        remote_repos.append(GitRemoteRepo(
            name=None,
            url=None,
            git_repo_action_type=None,
            git_repo_connection_type=None,
            command_line_str=remote_line, ))
    return remote_repos


def get_remote_repos(git_dir: str) -> List[GitRemoteRepo]:
    return get_repos_from_git_remote_output(get_remote_output(git_dir))


def get_branch_output(git_dir: str) -> str:
    p_open = subprocess.Popen(["git", "-C", git_dir, "branch", "-vv"], stdout=subprocess.PIPE, encoding="utf-8")
    return p_open.stdout.read()


def get_branch_info_from_line(branch_output_line: str) -> BranchInfo:
    branch_regex_match: re.Match = re.search(REGEX_BRANCH, branch_output_line)
    from_branch: str = branch_regex_match.group(1)

    to_repo_branch: str = branch_regex_match.group(3)
    if to_repo_branch:
        to_repo_branch = to_repo_branch[1:-1]  # remove first and last characters, i.e. "[" and "]"
        to_repo, to_branch = to_repo_branch.split("/", 1)  # split around first "/"
    else:
        to_repo, to_branch = "upstream", from_branch

    if to_branch.__contains__(":"):
        to_branch = to_branch[0:to_branch.index(":", 0)]

    return BranchInfo(from_branch=from_branch, to_repo=to_repo, to_branch=to_branch)


def get_branch_info_from_output(branch_output: str) -> BranchInfo:
    for remote_line in branch_output.split("\n"):
        remote_line = remote_line.strip()
        if remote_line.startswith("*"):
            return get_branch_info_from_line(remote_line)


def get_branch_info(git_dir: str) -> BranchInfo:
    return get_branch_info_from_output(get_branch_output(git_dir))


def sanitize_url(git_url: str) -> str:
    sanitized_url: str = git_url.replace(":", "/")
    if sanitized_url.endswith("/"):
        sanitized_url = sanitized_url[:-1]
    if sanitized_url.endswith(".git"):
        sanitized_url = sanitized_url[:-4]
    return sanitized_url
