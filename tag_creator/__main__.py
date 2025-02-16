import yaml
from tag_creator.repository.version import ProjectVersionUpdater
from tag_creator.logger import logger
from tag_creator import configuration as cfg
from tag_creator.arguments import parse


if __name__ == "__main__":

    args = parse()

    if args.show_config:
        logger.info(yaml.dump(cfg.read_configuration(args.custom_config_path)))

    pvu = ProjectVersionUpdater(
        repo_dir=args.repo_dir,
        release_branch=args.release_branch,
        prefix=args.tag_prefix,
        dry_run=args.dry_run
    )

    if args.create_new_tag and args.start_from:
        pvu.new_versions_from_batch(args.start_from)

    if args.create_new_tag and not args.start_from:
        pvu.create_new_version()

    if args.current_version:
        logger.info(f"Current tag: {pvu.current_tag()} Branch: {args.release_branch}")
