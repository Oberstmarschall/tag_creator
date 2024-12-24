import argparse
from tag_creator.repository.version import ProjectVersionUpdater



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Repository tool.")
    parser.add_argument("--repo_dir", help="Repository root directory", default=".")
    parser.add_argument("--create_new_tag", help="Update tag", action="store_true")
    parser.add_argument("--dry_run", help="Do not update remote", action="store_true", default=False)

    args = parser.parse_args()

    if args.create_new_tag:
        ProjectVersionUpdater(args.repo_dir, args.dry_run).create_new_verion()
