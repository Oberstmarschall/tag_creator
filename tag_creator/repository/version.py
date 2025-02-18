import re
import tag_creator.configuration as cfg
from tag_creator.logger import logger
from tag_creator.repository.git import Git
from typing import List, Tuple


class ProjectVersionUpdater(Git):

    MAJOR_VER = "major"
    MINOR_VER = "minor"
    PATCH_VER = "patch"

    def __init__(self, repo_dir: str, release_branch: str, dry_run: bool = False, prefix: str = "") -> None:
        super().__init__(repo_dir=repo_dir)
        self.release_branch = release_branch
        self.prefix = prefix
        self.dry_run = dry_run

    def current_tag(self) -> str:
        tags = self.__all_tags()
        if not tags:
            raise Exception("There is no initial tag!")
        return str(tags[-1])

    def create_new_version(self) -> None:
        """Create new tag for the release branch.
        Tag pattern: ${prefix}d.d.d .Initial tag must be created manually.
        """
        current_version = self.current_tag()
        self._exit_tag_exists_on_head(current_version)

        new_tag = self._formatted_new_tag(current_version, self.log("-n 1 --pretty=%B"))
        self._create_and_push_tag(new_tag)

    def _formatted_new_tag(self, current_version: str, commit_message: str) -> str:
        version_without_prefix = self.__version_witout_prefix(current_version)
        return self.__add_prefix(".".join(map(
            str,
            self.__increment_version(version_without_prefix, commit_message))
        ))

    def _exit_tag_exists_on_head(self, current_version: str) -> None:
        logger.info(f"Current version is: {current_version}")
        if self.__is_tag_on_current_head(current_version):
            logger.warning(
                f"There are no new changes starting from the latest tag: {current_version}. Skip tag creation."
            )
            raise Exception("There is a tag pointing to current HEAD")

    def _create_and_push_tag(self, tag: str) -> None:
        self.__create_tag(tag, "Automatically created tag")
        if self.dry_run:
            logger.info("Dry run! New tag will not be pushed.")
            return
        self.push(tag, "tag")

    def _patch_increment_based_on_title(self, title: str) -> Tuple[int, ...]:
        """Extract patch based on the change title.

        Args:
            title (_type_): merge request or commit.

        Raises:
            Exception: There are no allowed commit types in the configuration.

        Returns:
            tuple: major, minor and patch increment
        """
        logger.info(f"Determine increments for new tag based on commit (MR) msg: {title}")

        if self.__is_major_version(title):
            return (1, 0, 0)
        elif self.__is_starts_from_version(self.MINOR_VER, title):
            return (0, 1, 0)
        elif self.__is_starts_from_version(self.PATCH_VER, title):
            return (0, 0, 1)
        else:
            raise Exception("Can not determine commit majority based on it's message!")

    def __all_tags(self) -> list[str]:
        return list(
            self.tag(
                f"--merged '{self.release_branch}' --sort=creatordate --list "
                f"'{self.prefix}[0-9]*\\.[0-9]*\\.[0-9]*'"
            ).strip().splitlines()
        )

    def __commit_hash(self, ref: str) -> str:
        return str(self.rev_list(f"-n 1 {ref}"))

    def __is_tag_on_current_head(self, tag: str) -> bool:
        head_hash = self.__commit_hash("HEAD")
        tag_hash = self.__commit_hash(tag)

        return (head_hash == tag_hash)

    def __create_tag(self, tag: str, msg: str = "") -> None:
        logger.info(f"New tag will be created and pushed. Tag: {tag}, message {msg}")
        self.tag(f"-a '{tag}' -m '{msg}'")

    def __increment_version(self, version: str, change_title: str) -> Tuple[int, ...]:
        logger.info(f"Commit:\n{change_title}\nwill be used to update tag.")
        major, minor, patch = map(int, version.split('.'))
        new_major, new_minor, new_patch = self._patch_increment_based_on_title(change_title)

        if new_major > 0:
            major += new_major
            minor = 0
            patch = 0
        elif new_minor > 0:
            minor += new_minor
            patch = 0
        else:
            patch += new_patch

        return (major, minor, patch)

    def __version_witout_prefix(self, version: str) -> str:
        return version.lstrip(self.prefix)

    def __add_prefix(self, version: str) -> str:
        return f"{self.prefix}{version}"

    def __is_major_version(self, commit_msg: str) -> bool:
        return bool(
            re.match("^(" + ('|').join(self.__all_commit_types()) + ")[a-z()]*!:", commit_msg, re.MULTILINE) or
            re.search("^(" + ('|').join(self.__types_for_majority(self.MAJOR_VER)) + r"): \w", commit_msg, re.MULTILINE)
        )

    def __types_for_majority(self, majority: str) -> List[str]:
        types: list[str] = []
        types.extend(
            [entry["type"] for entry in cfg.allowed_commit_types() if entry["majority"] == majority]  # type: ignore
        )
        return [item for sublist in types for item in sublist]

    def __all_commit_types(self) -> List[str]:
        majority: list[str] = []
        for entry in cfg.allowed_commit_types():
            if isinstance(entry, dict) and "type" in entry:
                majority.extend(entry["type"])
            else:
                logger.warning(f"Skipping invalid entry: {entry}")

        return majority

    def __is_starts_from_version(self, version: str, commit_msg: str) -> bool:
        return bool(re.match(
            "^(" + "|".join(self.__types_for_majority(version)) + ")[a-z()]*:",
            commit_msg,
            re.MULTILINE
        ))
