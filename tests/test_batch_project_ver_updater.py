import pytest
from unittest.mock import patch, MagicMock, call
from tag_creator.repository.batch_version import BatchProjectVersionUpdater


@pytest.mark.parametrize(
    "commits, expected_result",
    [
        (
            {
                "123rty": "fix: some fix",
                "321cbd": "feat: some feat",
                "098rcm": "fix: some fix",
                "123abc": "chore: some change",
            },
            "1.1.0"
        ),
        (
            {
                "123tyy": "fix: some fix",
                "321cbd": "feat: some feat",
                "123abc": "fix!: some major fix",
            },
            "2.0.0"
        ),
        (
            {
                "123qer": "fix: some fix",
                "123abc": "fix: another fix",
            },
            "1.0.1"
        )
    ]
)
def test_version_update_from_batch(commits, expected_result):
    commit_msg_from_hash = lambda commits, text: next((msg for hash, msg in commits.items() if hash in text), None)
    def mock_exec(command, *args, **kwargs):
        if "tag --merged" in command:
            return "1.0.0"
        elif "log --oneline --boundary --pretty=%H" in command:
            return "\n".join(commits.keys())
        elif "--pretty=%B" in command:
            return commit_msg_from_hash(commits, command)
        elif "-n 1 HEAD" in command:
            return "1"
        else:
            return "foo-bar"

    with patch('tag_creator.utils.shell.exec', MagicMock()) as mock:
        mock.side_effect = mock_exec
        BatchProjectVersionUpdater(
            repo_dir="fake_repo", release_branch="main", initial_commit="abc123", dry_run=False
        ).create_new_version()

        mock.assert_has_calls([
            call(f"git -C fake_repo tag -a '{expected_result}' -m 'Automatically created tag'"),
            call(f"git -C fake_repo push origin tag {expected_result}")
        ])
