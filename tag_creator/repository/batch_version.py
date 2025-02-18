from tag_creator.repository.version import ProjectVersionUpdater
from typing import Dict, Tuple


class BatchProjectVersionUpdater(ProjectVersionUpdater):
    "Create new version from a chain of commits"

    def __init__(
        self,
        repo_dir: str,
        release_branch: str,
        initial_commit: str,
        dry_run: bool = False,
        prefix: str = ""
    ) -> None:
        super().__init__(repo_dir, release_branch, dry_run, prefix)
        self.initial_commit = initial_commit

    def create_new_version(self) -> None:
        """Create new version from batch of commits. Select the highest increment from commits.
        Commits collected from initial_commit to current HEAD
        """
        current_version = self.current_tag()
        self._exit_tag_exists_on_head(current_version)

        most_major_commit_hash = self.__select_increment_version_from_batch()
        new_tag = self._formatted_new_tag(current_version, self.log(f" -n 1 --pretty=%B {most_major_commit_hash}"))
        self._create_and_push_tag(new_tag)

    def __increments_from_commits(self) -> Dict[str, Tuple[int, ...]]:
        increments = {}
        for commit_hash in self.__refs_from_batch():
            commit_message = self.log(f"-n 1 --pretty=%B {commit_hash}")
            increments[commit_hash] = self._patch_increment_based_on_title(commit_message)

        return increments

    def __refs_from_batch(self) -> list[str]:
        refs = self.log(f"--oneline --boundary --pretty=%H {self.initial_commit}..HEAD").strip().splitlines()

        if not refs:
            raise Exception(f"Can not find list of commits between {self.initial_commit} and HEAD")

        return refs

    def __select_increment_version_from_batch(self) -> str:
        increments = self.__increments_from_commits()
        tuple_to_increment_index = {}

        for commit_hash, tuple in increments.items():
            tuple_to_increment_index[commit_hash] = tuple.index(1)

        return str(
            [
                key for key in tuple_to_increment_index
                if tuple_to_increment_index[key] == min(tuple_to_increment_index.values())
            ][0]
        )
