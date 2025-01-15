import argparse


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="Repository tool.")
    parser.add_argument("--repo_dir", help="Repository root directory", default=".")
    parser.add_argument("--release_branch", help="Release branch", required=False, default="main")
    parser.add_argument("--create_new_tag", help="Update tag", action="store_true")
    parser.add_argument("--dry_run", help="Do not update remote", action="store_true", default=False)
    parser.add_argument("--show_config", help="Show default config", action="store_true", default=False)
    parser.add_argument("--config", help="Config file", default="", required=False)

    return parser.parse_args()


args = parse()
