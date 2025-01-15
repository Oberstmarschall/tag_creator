import yaml
from tag_creator.repository.version import ProjectVersionUpdater
from tag_creator.logger import logger
from tag_creator import configuration as cfg
from tag_creator.arguments import args


if __name__ == "__main__":

    if args.show_config:
        logger.info(yaml.dump(cfg.read_configuration()))

    if args.create_new_tag:
        ProjectVersionUpdater(args.repo_dir, args.release_branch, args.dry_run).create_new_verion()
