import unittest
from typing import List
from webgit.webgit_util.repository import (
    get_repos_from_git_remote_output,
    GitRemoteRepo,
    GitRemoteRepoConnectionType,
    GitRemoteRepoActionType,
    GitException,
)


class RepositoryTests(unittest.TestCase):

    def test_parse_remote_text_origin_only(self):
        remote_text: str = "\n".join([
            "origin	https://github.com/apache/kafka.git (fetch)",
            "origin	https://github.com/apache/kafka.git (push)",
        ])
        remote_repos: List[GitRemoteRepo] = get_repos_from_git_remote_output(remote_text)
        self.assertEqual(2, len(remote_repos))

        repo_0: GitRemoteRepo = remote_repos[0]
        self.assertEqual("origin", repo_0.name)
        self.assertEqual("github.com/apache/kafka", repo_0.url)
        self.assertEqual("github", repo_0.web_host)
        self.assertEqual("apache", repo_0.org_or_user)
        self.assertEqual("kafka", repo_0.repo)
        self.assertEqual(GitRemoteRepoConnectionType.HTTPS, repo_0.repo_connection_type)
        self.assertEqual(GitRemoteRepoActionType.FETCH, repo_0.repo_action_type)

        repo_1: GitRemoteRepo = remote_repos[1]
        self.assertEqual("origin", repo_1.name)
        self.assertEqual("github.com/apache/kafka", repo_1.url)
        self.assertEqual("github", repo_1.web_host)
        self.assertEqual("apache", repo_1.org_or_user)
        self.assertEqual("kafka", repo_1.repo)
        self.assertEqual(GitRemoteRepoConnectionType.HTTPS, repo_1.repo_connection_type)
        self.assertEqual(GitRemoteRepoActionType.PUSH, repo_1.repo_action_type)

    def test_parse_remote_text_origin_upstream(self):
        remote_text: str = "\n".join([
            "origin	git@gitlab.com:user/project.git (fetch)",
            "origin	git@gitlab.com:user/project.git (push)",
            "upstream	git@gitlab.com:org/project.git (fetch)",
            "upstream	git@gitlab.com:org/project.git (push)",
        ])
        remote_repos: List[GitRemoteRepo] = get_repos_from_git_remote_output(remote_text)
        self.assertEqual(4, len(remote_repos))

        repo_0: GitRemoteRepo = remote_repos[0]
        self.assertEqual("origin", repo_0.name)
        self.assertEqual("gitlab.com/user/project", repo_0.url)
        self.assertEqual("gitlab", repo_0.web_host)
        self.assertEqual("user", repo_0.org_or_user)
        self.assertEqual("project", repo_0.repo)
        self.assertEqual(GitRemoteRepoConnectionType.SSH, repo_0.repo_connection_type)
        self.assertEqual(GitRemoteRepoActionType.FETCH, repo_0.repo_action_type)

        repo_1: GitRemoteRepo = remote_repos[1]
        self.assertEqual("origin", repo_1.name)
        self.assertEqual("gitlab.com/user/project", repo_1.url)
        self.assertEqual("gitlab", repo_1.web_host)
        self.assertEqual("user", repo_1.org_or_user)
        self.assertEqual("project", repo_1.repo)
        self.assertEqual(GitRemoteRepoConnectionType.SSH, repo_1.repo_connection_type)
        self.assertEqual(GitRemoteRepoActionType.PUSH, repo_1.repo_action_type)

        repo_2: GitRemoteRepo = remote_repos[2]
        self.assertEqual("upstream", repo_2.name)
        self.assertEqual("gitlab.com/org/project", repo_2.url)
        self.assertEqual("gitlab", repo_2.web_host)
        self.assertEqual("org", repo_2.org_or_user)
        self.assertEqual("project", repo_2.repo)
        self.assertEqual(GitRemoteRepoConnectionType.SSH, repo_2.repo_connection_type)
        self.assertEqual(GitRemoteRepoActionType.FETCH, repo_2.repo_action_type)

        repo_3: GitRemoteRepo = remote_repos[3]
        self.assertEqual("upstream", repo_3.name)
        self.assertEqual("gitlab.com/org/project", repo_3.url)
        self.assertEqual("gitlab", repo_3.web_host)
        self.assertEqual("org", repo_3.org_or_user)
        self.assertEqual("project", repo_3.repo)
        self.assertEqual(GitRemoteRepoConnectionType.SSH, repo_3.repo_connection_type)
        self.assertEqual(GitRemoteRepoActionType.PUSH, repo_3.repo_action_type)

    def test_fatal(self):
        cannot_change_dir: str = "fatal: cannot change to 'hello_world': No such file or directory"
        with self.assertRaises(GitException):
            get_repos_from_git_remote_output(cannot_change_dir)

        not_git_repo: str = "fatal: not a git repository (or any of the parent directories): .git"
        with self.assertRaises(GitException):
            get_repos_from_git_remote_output(not_git_repo)


if __name__ == '__main__':
    unittest.main()
