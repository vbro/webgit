import io
import os
import unittest

from unittest.mock import Mock, patch
from webgit.webgit_util import command_line
from webgit.webgit_util import repository

GITLAB_REMOTE_TEXT: str = "\n".join([
    "origin	git@gitlab.com:user/project.git (fetch)",
    "origin	git@gitlab.com:user/project.git (push)",
    "upstream	git@gitlab.com:org/project.git (fetch)",
    "upstream	git@gitlab.com:org/project.git (push)",
])

GITHUB_REMOTE_TEXT: str = "\n".join([
    "origin	git@github.company.io:user/project.git (fetch)",
    "origin	git@github.company.io:user/project.git (push)",
    "upstream	git@github.company.io:org/project.git (fetch)",
    "upstream	git@github.company.io:org/project.git (push)",
])


class WebGitMainTests(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_git_dir: str = "/Users/user/org/project"
        repository.get_remote_output = Mock(return_value=GITHUB_REMOTE_TEXT)
        os.getcwd = Mock(return_value=self.mock_git_dir)
        os.getcwd.assert_not_called()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_commit_local_dir(self, mock_stdout: io.StringIO):
        command_line.run_program("12ab45c -a".split())
        os.getcwd.assert_called_once()
        repository.get_remote_output.assert_called_once_with(self.mock_git_dir)
        std_out: str = mock_stdout.getvalue()
        assert "https://github.company.io/org/project/commit/12ab45c\n" == std_out

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_commit_local_dir(self, mock_stdout: io.StringIO):
        project_2_dir: str = "/Users/user/org2/project2"
        command_line.run_program(f"12abc34 -a -C {project_2_dir}".split())
        os.getcwd.assert_not_called()
        repository.get_remote_output.assert_called_once_with(project_2_dir)
        std_out: str = mock_stdout.getvalue()
        assert "https://github.company.io/org/project/commit/12abc34\n" == std_out

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_issues(self, mock_stdout: io.StringIO):
        command_line.run_program("issues -a".split())
        os.getcwd.assert_called_once()
        repository.get_remote_output.assert_called_once_with(self.mock_git_dir)
        std_out: str = mock_stdout.getvalue()
        assert "https://github.company.io/org/project/issues\n" == std_out

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_issues_specific(self, mock_stdout: io.StringIO):
        command_line.run_program("issues 123 -a".split())
        os.getcwd.assert_called_once()
        repository.get_remote_output.assert_called_once_with(self.mock_git_dir)
        std_out: str = mock_stdout.getvalue()
        assert "https://github.company.io/org/project/issues/123\n" == std_out
