import re
import tag_creator.configuration as cfg
from tag_creator.logger import logger
from tag_creator.repository.git import Git


class ProjectVersionUpdater(Git):

    MAJOR_VER = "major"
    MINOR_VER = "minor"
    PATCH_VER = "patch"

    def __init__(self, repo_dir: str, dry_run: bool) -> None:
        super().__init__(repo_dir=repo_dir)
        self.release_branch = cfg.read_configuration()["repo"]["release_branch"]
        self.dry_run = dry_run

    def create_new_verion(self) -> None:
        current_version = self.__current_tag()
        logger.info(f"Current version is {current_version}")
        new_patch = ".".join(map(
            str,
            self.__increment_version(current_version, self.log("-n 1 --pretty=%B").stdout))
        )

        if self.__is_tag_on_current_head(current_version):
            logger.warning(
                f"There are no new changes starting from the latest tag: {current_version}. Skip tag creation."
            )
            return

        self.__create_tag(new_patch, "Automatically created tag")
        if self.dry_run:
            logger.info("Dry run! New tag will not be pushed.")
            return
        self.push(new_patch)

    def __all_tags(self):
        return self.tag(f"--merged {self.release_branch} --list '[0-9]*\\.[0-9]*\\.[0-9]*'").stdout.strip().splitlines()

    def __current_tag(self):
        tags = self.__all_tags()
        if not tags:
            raise Exception("There is no initial tag!")
        return tags[-1]

    def __commit_hash(self, ref: str) -> str:
        return self.rev_list(f"-n 1 {ref}").stdout

    def __is_tag_on_current_head(self, tag: str) -> bool:
        head_hash = self.__commit_hash("HEAD")
        tag_hash = self.__commit_hash(tag)

        return (head_hash == tag_hash)

    def __create_tag(self, tag: str, msg: str =""):
        logger.info(f"New tag will be created and pushed. Tag: {tag}, message {msg}")
        self.tag(f"-a '{tag}' -m '{msg}'")

    def __increment_version(self, version: str, change_title: str) -> tuple:
        major, minor, patch = map(int, version.split('.'))
        new_major, new_minor, new_patch = self.__patch_increment_based_on_title(change_title)

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

    def __patch_increment_based_on_title(self, title: str) -> tuple:
        """Extract patch based on the change title.

        Args:
            title (_type_): merge request or commit.

        Raises:
            Exception: There are no allowed commit types in the configuration.

        Returns:
            tuple: major, minor and patch increment
        """
        logger.info(f"Commit (MR) msg: {title}")

        if self.__is_major_version(title):
            return 1, 0, 0
        elif self.__is_starts_from_version(self.MINOR_VER, title):
            return 0, 1, 0
        elif self.__is_starts_from_version(self.PATCH_VER, title):
            return 0, 0, 1
        else:
            raise Exception("Can not determine commit majority based on it's message!")

    def __is_major_version(self, commit_msg: str) -> bool:
        return (
            re.match(f"^(" + ('|').join(self.__all_commit_types()) + ")[a-z()]*!:", commit_msg, re.MULTILINE) or
            re.search(f"^(" + ('|').join(self.__types_for_majority(self.MAJOR_VER)) + r"): \w", commit_msg, re.MULTILINE)
        )

    def __types_for_majority(self, majority: str) -> list:
        types = []
        types.extend([entry["type"] for entry in cfg.allowed_commit_types() if entry["majority"] == majority])
        return [item for sublist in types for item in sublist]

    def __all_commit_types(self) -> list:
        majority = []
        for entry in cfg.allowed_commit_types():
            majority.extend(entry["type"])

        return majority

    def __is_starts_from_version(self, version: str, commit_msg: str) -> bool:
        return re.match(f"^(" + "|".join(self.__types_for_majority(version)) + ")[a-z()]*:", commit_msg, re.MULTILINE)


