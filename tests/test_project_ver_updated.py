import pytest
from unittest.mock import patch, MagicMock, call
from tag_creator.repository.version import ProjectVersionUpdater


@pytest.fixture(autouse=True)
def mock_git():
    with patch('tag_creator.repository.git.Git') as MockGit:
        yield MockGit

@pytest.fixture()
def mock_shell():
    def mock_exec(command, *args, **kwargs):
        if "tag --merged" in command:
            return "1.0.0"
        elif "log" in command:
            return "fix: some fix"
        elif "-n 1 HEAD" in command:
            return "1"
        else:
            return "foo-bar"

    with patch('tag_creator.utils.shell.exec', MagicMock()) as mock:
        mock.side_effect = mock_exec
        yield mock

def test_version_updated(mock_shell):
    ProjectVersionUpdater(repo_dir="fake_repo", release_branch="main", dry_run=False).create_new_version()

    mock_shell.assert_has_calls([
        call("git -C fake_repo tag --merged 'main' --sort=creatordate --list '[0-9]*\\.[0-9]*\\.[0-9]*'"),
        call("git -C fake_repo rev-list -n 1 HEAD"),
        call("git -C fake_repo rev-list -n 1 1.0.0"),
        call("git -C fake_repo log -n 1 --pretty=%B"),
        call("git -C fake_repo tag -a '1.0.1' -m 'Automatically created tag'"),
        call("git -C fake_repo push origin tag 1.0.1"),
    ])

def test_dry_run_mode(mock_shell):
    ProjectVersionUpdater(repo_dir="fake_repo", release_branch="main", dry_run=True).create_new_version()

    assert call("git -C fake_repo push origin tag 1.0.1") not in mock_shell.call_args_list

def test_tag_creation_with_prefix(mock_shell):
    ProjectVersionUpdater(repo_dir="fake_repo", release_branch="main", prefix="v").create_new_version()

    mock_shell.assert_has_calls([
        call("git -C fake_repo tag --merged 'main' --sort=creatordate --list 'v[0-9]*\\.[0-9]*\\.[0-9]*'"),
        call("git -C fake_repo tag -a 'v1.0.1' -m 'Automatically created tag'"),
    ], any_order=True)

def test_not_allowed_type_raise():
    with pytest.raises(Exception, match="Can not determine commit majority based on it's message!"):
        with patch("tag_creator.utils.shell.exec", MagicMock()) as shell_mock:
            def mock_exec(command, *args, **kwargs):
                if "log" in command:
                    return "foo: bar"
                elif "tag --merged" in command:
                    return "1.0.0"
                elif "-n 1 HEAD" in command:
                    return "1"
                else:
                    return "foo-bar"
            shell_mock.side_effect = mock_exec
            ProjectVersionUpdater(repo_dir="fake_repo", release_branch="main", prefix="v").create_new_version()

@pytest.mark.parametrize(
    "commit_msg, increments",
    [
        ("fix: foo", (0, 0, 1)),
        ("perf: docs", (0, 0, 1)),
        ("test: refactor", (0, 0, 1)),
        ("feat: new feature", (0, 1, 0)),
        ("style: new feature", (0, 0, 1)),
        ("chore: new feature", (0, 0, 1)),
        ("ci: new feature", (0, 1, 0)),
        ("build: new feature", (0, 1, 0)),
        ("revert: new feature", (0, 1, 0)),
        ("feat!: test", (1, 0, 0)),
        ("BREAKING_CHANGE: foo", (1, 0, 0)),
        ("fix: some fix\nBREAKING_CHANGE: foo", (1, 0 , 0))
    ],
)
def test_increments_based_on_commit_msg(commit_msg, increments):
    with patch("tag_creator.utils.shell.exec", MagicMock()) as shell_mock:
        def mock_exec(command, *args, **kwargs):
            if "log" in command:
                return commit_msg
            elif "tag --merged" in command:
                return "1.0.0"
            elif "-n 1 HEAD" in command:
                return "1"
            else:
                return "foo-bar"

        shell_mock.side_effect = mock_exec

        ProjectVersionUpdater(repo_dir="fake_repo", release_branch="main", prefix="v").create_new_version()
        expected_tag = f"v{1 + increments[0]}.{0 + increments[1]}.{0 + increments[2]}"

        shell_mock.assert_any_call(f"git -C fake_repo tag -a '{expected_tag}' -m 'Automatically created tag'")
