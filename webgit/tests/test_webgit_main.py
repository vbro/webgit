import io
import unittest

from unittest.mock import Mock, patch
from webgit.webgit_util import command_line
from webgit.webgit_util import repository

GITLAB_REMOTE_OUTPUT_TEXT: str = "\n".join([
    "origin	git@gitlab.com:user/project.git (fetch)",
    "origin	git@gitlab.com:user/project.git (push)",
    "upstream	git@gitlab.com:org/project.git (fetch)",
    "upstream	git@gitlab.com:org/project.git (push)",
])

GITHUB_REMOTE_OUTPUT_TEXT: str = "\n".join([
    "origin	git@github.company.io:user/project.git (fetch)",
    "origin	git@github.company.io:user/project.git (push)",
    "upstream	git@github.company.io:org/project.git (fetch)",
    "upstream	git@github.company.io:org/project.git (push)",
])

BRANCH_VERBOSE_OUTPUT_TEXT: str = "\n".join([
    "local_branch01 5bac452 [upstream01/main01] commit message",
    "* local_branch02 a11bce2 [upstream/main02] commit message",
    "local_branch03 424def7 [upstream03/main03] commit message",
])

GIT_DIR = "/Users/user/org/project"


def mock_getcwd_function():
    return lambda: GIT_DIR


def mock_branch_output_function():
    return lambda x: BRANCH_VERBOSE_OUTPUT_TEXT


class WebGitMainTests(unittest.TestCase):

    def setUp(self) -> None:
        repository.get_remote_output = Mock(return_value=GITHUB_REMOTE_OUTPUT_TEXT)

    @patch("os.getcwd", new_callable=mock_getcwd_function)
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_commit_local_dir(self, mock_stdout: io.StringIO, mock_getcwd):
        command_line.run_program("12ab45c -a".split())
        repository.get_remote_output.assert_called_once_with(GIT_DIR)
        std_out: str = mock_stdout.getvalue()
        self.assertEqual("https://github.company.io/org/project/commit/12ab45c\n", std_out)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_commit_c_dir(self, mock_stdout: io.StringIO):
        project_2_dir: str = "/Users/user/org2/project2"
        command_line.run_program(f"12abc34 -a -C {project_2_dir}".split())
        repository.get_remote_output.assert_called_once_with(project_2_dir)
        std_out: str = mock_stdout.getvalue()
        self.assertEqual("https://github.company.io/org/project/commit/12abc34\n", std_out)

    @patch("os.getcwd", new_callable=mock_getcwd_function)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_issues(self, mock_stdout: io.StringIO, mock_getcwd):
        command_line.run_program("issues -a".split())
        repository.get_remote_output.assert_called_once_with(GIT_DIR)
        std_out: str = mock_stdout.getvalue()
        self.assertEqual("https://github.company.io/org/project/issues\n", std_out)

    @patch("os.getcwd", new_callable=mock_getcwd_function)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_issues_specific(self, mock_stdout: io.StringIO, mock_getcwd):
        command_line.run_program("issues 123 -a".split())
        repository.get_remote_output.assert_called_once_with(GIT_DIR)
        std_out: str = mock_stdout.getvalue()
        self.assertEqual("https://github.company.io/org/project/issues/123\n", std_out)

    @patch("webgit.webgit_util.repository.get_branch_output", new_callable=mock_branch_output_function)
    @patch("os.getcwd", new_callable=mock_getcwd_function)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pr(self, mock_stdout: io.StringIO, mock_getcwd, mock_branch_output):
        command_line.run_program("pr -a".split())
        repository.get_remote_output.assert_called_once_with(GIT_DIR)
        std_out: str = mock_stdout.getvalue()
        self.assertEqual(
            "https://github.company.io/org/project/compare/main02...user:local_branch02?expand=1\n",
            std_out
        )

    @patch("webgit.webgit_util.repository.get_branch_output", new_callable=mock_branch_output_function)
    @patch("os.getcwd", new_callable=mock_getcwd_function)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pr_with_all_cli_inputs(self, mock_stdout: io.StringIO, mock_getcwd, mock_branch_output):
        command_line.run_program("pr origin/feature_branch upstream/dev -a".split())
        repository.get_remote_output.assert_called_once_with(GIT_DIR)
        std_out: str = mock_stdout.getvalue()
        self.assertEqual("https://github.company.io/org/project/compare/dev...user:feature_branch?expand=1\n", std_out)

    @patch("webgit.webgit_util.repository.get_branch_output", new_callable=mock_branch_output_function)
    @patch("os.getcwd", new_callable=mock_getcwd_function)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pr_with_branch_cli_inputs(self, mock_stdout: io.StringIO, mock_getcwd, mock_branch_output):
        command_line.run_program("pr feature_branch dev -a".split())
        repository.get_remote_output.assert_called_once_with(GIT_DIR)
        std_out: str = mock_stdout.getvalue()
        self.assertEqual("https://github.company.io/org/project/compare/dev...user:feature_branch?expand=1\n", std_out)

    @patch("webgit.webgit_util.repository.get_branch_output", new_callable=mock_branch_output_function)
    @patch("os.getcwd", new_callable=mock_getcwd_function)
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pr_to_origin(self, mock_stdout: io.StringIO, mock_getcwd, mock_branch_output):
        command_line.run_program("pr origin/feature_branch origin/dev -a".split())
        repository.get_remote_output.assert_called_once_with(GIT_DIR)
        std_out: str = mock_stdout.getvalue()
        self.assertEqual("https://github.company.io/user/project/compare/dev...user:feature_branch?expand=1\n", std_out)
