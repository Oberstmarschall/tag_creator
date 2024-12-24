import pytest
from unittest.mock import patch, MagicMock, call
from tag_creator.repository.version import ProjectVersionUpdater


@pytest.fixture(autouse=True)
def mock_git():
    with patch('tag_creator.repository.git.Git') as MockGit:
        yield MockGit

@pytest.fixture(autouse=True)
def mock_shell():
    def mock_exec(command, *args, **kwargs):
        if "tag --merged" in command:
            return MagicMock(stdout="1.0.0")
        elif "log" in command:
            return MagicMock(stdout="fix: some fix")
        elif "-n 1 HEAD" in command:
            return MagicMock(stdout="1")
        else:
            return MagicMock(stdout="foo-bar")

    with patch('tag_creator.utils.shell.exec', MagicMock()) as mock:
        mock.side_effect = mock_exec
        yield mock

def test_version_updated(mock_shell):
    ProjectVersionUpdater(repo_dir="fake_repo", dry_run=False).create_new_verion()

    mock_shell.assert_has_calls([
        call("git -C fake_repo tag --merged master --list '[0-9]*\\.[0-9]*\\.[0-9]*'"),
        call("git -C fake_repo log -n 1 --pretty=%B"),
        call("git -C fake_repo rev-list -n 1 HEAD"),
        call("git -C fake_repo rev-list -n 1 1.0.0"),
        call("git -C fake_repo tag -a '1.0.1' -m 'Automatically created tag'"),
        call("git -C fake_repo push origin 1.0.1"),
    ])

def test_dry_run_mode(mock_shell):
    ProjectVersionUpdater(repo_dir="fake_repo", dry_run=True).create_new_verion()

    assert call("git -C fake_repo push origin 1.0.1") not in mock_shell.call_args_list

