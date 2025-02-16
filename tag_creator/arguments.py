import argparse


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="Tag creator")
    parser.add_argument("--repo_dir", help="Repository root directory. (default: %(default)s)", default=".")
    parser.add_argument("--release_branch",
                        help="Release branch. (default: %(default)s)", required=False, default="main")
    parser.add_argument("--create_new_tag", help="Update tag", action="store_true", default=False)
    parser.add_argument(
        "--start_from",
        help=(
            "Find the new value starting from the given commit."
            "The highest increment present in the commits will be selected."
        ),
        required=False,
        default=""
    )
    parser.add_argument("--dry_run", help="Do not update remote", action="store_true", default=False)
    parser.add_argument("--show_config", help="Show default config", action="store_true", default=False)
    parser.add_argument("--config", help="Config file", required=False, default="")
    parser.add_argument("--current_version", help="Show current version", action="store_true", default=False)
    parser.add_argument("--tag_prefix", help="Prefix of version number. (default: %(default)s)",
                        required=False, default="")

    return parser.parse_args()
