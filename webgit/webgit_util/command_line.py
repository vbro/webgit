import getpass
import os
import re
import subprocess
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from typing import List

from .constants import (
    ENV_DEFAULT_ORIGIN_REPO_NAME,
    ENV_DEFAULT_UPSTREAM_REPO_NAME,
    ENV_DEFAULT_USER,
    REGEX_COMMIT_HASH,
    REGEX_PULL_REQUEST_HASH,
    WEB_ADDRESS_TEMPLATES,
)

from .repository import (
    GitException,
    GitRemoteRepo,
    get_remote_repos,
)


def _create_argument_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(
        prog="webgit",
        description="Open Github and Gitlab web pages",
        formatter_class=RawTextHelpFormatter,
    )

    command_help: str = "\n".join([
        "commits - open webpage for commits",
        "repo    - open webpage for repo (default behavior)",
        "org     - open webpage for organization",
        "user    - open webpage for user",
        "pr      - open webpage to create a pull request page",
        "prs     - open webpage for all pull requests",
        "myprs [username]    - open webpage for pull requests for specified user",
        "issue [number]      - open webpage for specified issue",
        "issues   - open webpage for all issue",
        "tree [commit | branch | tag] - open webpage for commit, branch or tag tree",
        "[commit_hash] (e.g 76ac43b)  - open webpage for commit",
        "[pull_request_number] (e.g. 7, 3034, #1234567) - open webpage for pull request",
    ])

    parser.add_argument(
        "command",
        type=str,
        help=command_help,
        default="repo",
        nargs="*",
    )

    parser.add_argument("-a", "--print-address", help="print the web address", default=False, action="store_true")
    parser.add_argument("-C", "--path", help="git repository directory")
    parser.add_argument("-f", "--file", help="full repository path for file or directory")
    parser.add_argument("-o", "--org", help="git web org or project name")
    parser.add_argument("-u", "--git-user", help="git web username, e.g. username for github")
    parser.add_argument("-r", "--remote", help="the git remote to use, e.g. main, upstream")

    return parser


def run_program(parameters: List[str]):
    parser: ArgumentParser = _create_argument_parser()
    args_namespace: Namespace = parser.parse_args(parameters)

    if isinstance(args_namespace.command, list):
        webgit_command: str = args_namespace.command[0]
        webgit_commands: List[str] = args_namespace.command
    else:
        webgit_command = args_namespace.command
        webgit_commands = [webgit_command]

    web_address: str = ""
    git_dir: str = args_namespace.path or os.getcwd()
    git_repos: List[GitRemoteRepo] = get_remote_repos(git_dir)
    relevant_remote: GitRemoteRepo = _get_relevant_remote(git_repos, args_namespace.remote)
    web_host: str = relevant_remote.web_host
    remote_url: str = relevant_remote.url

    if webgit_command == "repo":
        web_address = "https://{}".format(remote_url)

    elif webgit_command == "org" or webgit_command == "user":
        org_or_user: str = args_namespace.org or args_namespace.user
        web_address = WEB_ADDRESS_TEMPLATES["org_or_user"][web_host].format(org_or_user)

    elif webgit_command == "commits":
        web_address = WEB_ADDRESS_TEMPLATES["commits"][web_host].format(remote_url)

    elif webgit_command == "prs":
        web_address = WEB_ADDRESS_TEMPLATES["prs"][web_host].format(remote_url)

    elif webgit_command == "myprs":
        git_user: str = (
                args_namespace.git_user or
                (webgit_commands[1] if len(webgit_commands) > 1 else None) or
                os.environ.get(ENV_DEFAULT_USER) or
                getpass.getuser() or
                _get_origin_repo_user(git_repos)
        )
        web_address = WEB_ADDRESS_TEMPLATES["myprs"][web_host].format(remote_url, git_user)

    elif webgit_command in ["issue", "issues"]:
        issue_number: str = webgit_commands[1] if len(webgit_commands) > 1 else None
        if issue_number:
            web_address = WEB_ADDRESS_TEMPLATES["issue"][web_host].format(remote_url, issue_number)
        else:
            web_address = WEB_ADDRESS_TEMPLATES["issues"][web_host].format(remote_url)

    elif webgit_command == "tree":
        git_object: str = webgit_commands[1] if len(webgit_commands) > 1 else None
        if not git_object:
            print("Git commit, branch or tag required after \"tree\"")
            return
        git_file_path: str = (
            args_namespace.file or
            (webgit_commands[2] if len(webgit_commands) > 2 else None)
        )
        if git_file_path:
            web_address = WEB_ADDRESS_TEMPLATES["tree_file"][web_host].format(
                remote_url, git_object, git_file_path)
        else:
            web_address = WEB_ADDRESS_TEMPLATES["tree"][web_host].format(remote_url, git_object)

    elif re.match(REGEX_COMMIT_HASH, webgit_command):
        git_file_path: str = (
            args_namespace.file or
            (webgit_commands[1] if len(webgit_commands) > 1 else None)
        )
        if git_file_path:
            web_address = WEB_ADDRESS_TEMPLATES["tree_file"][web_host].format(
                remote_url, webgit_command, git_file_path)
        else:
            web_address = WEB_ADDRESS_TEMPLATES["commit"][web_host].format(remote_url, webgit_command)

    elif re.match(REGEX_PULL_REQUEST_HASH, webgit_command):
        web_address = WEB_ADDRESS_TEMPLATES["pr"][web_host].format(
            remote_url,
            webgit_command.replace("#", "")
        )

    else:
        print("Unrecognized command")
        parser.print_help()
        exit(1)

    if args_namespace.print_address:
        print(web_address)
    else:
        subprocess.Popen(["open", web_address], stdout=subprocess.PIPE, encoding="utf-8")


def _get_relevant_remote(git_repos: List[GitRemoteRepo], remote_name: str) -> GitRemoteRepo:

    if len(git_repos) == 0:
        raise GitException("")

    remote_repo_name: str = (
            remote_name or
            os.getenv(ENV_DEFAULT_UPSTREAM_REPO_NAME) or
            "upstream"
    )

    git_repo: GitRemoteRepo
    if remote_repo_name:
        matching_git_repos = [r for r in git_repos if r.name == remote_repo_name]
        if len(matching_git_repos) > 0:
            return matching_git_repos[0]

    return git_repos[0]


def _get_origin_repo(git_repos: List[GitRemoteRepo]) -> (GitRemoteRepo or None):
    origin_repo_name = os.environ.get(ENV_DEFAULT_ORIGIN_REPO_NAME) or "origin"
    origin_repos: List[GitRemoteRepo] = [r for r in git_repos if r.name == origin_repo_name]
    if len(origin_repos) > 0:
        return origin_repos[0]
    else:
        return None


def _get_origin_repo_user(git_repos: List[GitRemoteRepo]) -> (GitRemoteRepo or None):
    origin_repo: GitRemoteRepo = _get_origin_repo(git_repos)
    if origin_repo is not None:
        return origin_repo.org_or_user
    else:
        return None
