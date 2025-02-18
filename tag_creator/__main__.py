import yaml
from tag_creator.repository.version import ProjectVersionUpdater
from tag_creator.repository.batch_version import BatchProjectVersionUpdater
from tag_creator.logger import logger
from tag_creator import configuration as cfg
from tag_creator.arguments import parse
from argparse import Namespace


def create_updater(args: Namespace) -> ProjectVersionUpdater:
    if args.start_from:
        return BatchProjectVersionUpdater(
            repo_dir=args.repo_dir,
            release_branch=args.release_branch,
            initial_commit=args.start_from,
            dry_run=args.dry_run,
            prefix=args.tag_prefix
        )
    return ProjectVersionUpdater(
        repo_dir=args.repo_dir,
        release_branch=args.release_branch,
        dry_run=args.dry_run,
        prefix=args.tag_prefix
    )


if __name__ == "__main__":

    args = parse()

    if args.show_config:
        logger.info(yaml.dump(cfg.read_configuration(args.custom_config_path)))

    pvu = create_updater(args)

    if args.create_new_tag:
        pvu.create_new_version()

    if args.current_version:
        logger.info(f"Current tag: {pvu.current_tag()} Branch: {args.release_branch}")
