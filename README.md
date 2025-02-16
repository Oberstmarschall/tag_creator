## Tag creator

Tag Creator is a Python tool that automatically generates release tags follow [SemVer](https://semver.org/) conventions.
It's designed to streamline the process of creating version tags for software projects, ensuring consistency and saving time.
Each new release tag will be created based on the latest tag version for the provided git branch. Increments for new version
will be parsed from the commit message. Commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format.

Each commit must start from the allowed [type](tag_creator/configuration.yml) to find increments for next tag based on it.
Be avare that the `MAJOR` verion rule is differnt. Commits still can start from the allowed types in the `MAJOR` section, however there are several
additional rules:

- script will interpret commits with the `!` character after the allowed type as a major verion
- allowed type can be declared in a description. E.g.:

```
fix: some fix

BREAKING CHANGE: this is a breaking change!
```

Initial list of types in the configuration provided by [conventional-changelog](https://github.com/conventional-changelog/commitlint/tree/master/@commitlint/config-conventional#type-enum).

## Features

- Automatically generates release tags
- Easy integration into existing workflows
- Lightweight and configurable

## Examples

Use --help option to see available scripts arguments.

### Show the latest tag for branch

Since project tags have the `v` prefix before versions, `--tag_prefix="v"` argument passed.

```python
python -m tag_creator --current_version --release_branch="main" --tag_prefix="v"
__main__ INFO: Current tag: v0.0.3 Branch: main
```

Internal command to search a tag will be: `git -C . tag --merged 'main' --sort=creatordate --list 'v[0-9]*\.[0-9]*\.[0-9]*'`.

### Create new release tag

To create new tag with push to remote use `--create_new_tag ` argument. Add `--dry_run` argument if you do not need to update your remote.
```python
python -m tag_creator --create_new_tag --tag_prefix="v" --release_branch="main"

version INFO: Current version is: v0.0.4
14:36:01 version INFO: Determine increments for new tag based on commit (MR) msg: docs: foo-bar

version INFO: New tag will be created and pushed. Tag: v0.0.5, message Automatically created tag
```

To create new tag from the bunch of commits, e.g. in case of merge not squashed merge request, use `--start_from` option.
It allows to parse all commits from the specified version to current HEAD and select the highest increment, based on
commit messages. Be aware, that only current HEAD are not allowed to contain a tag!

See your CI preferences to obtain a commit before your merge.

### See or change the configuration


You can provide a custom configuration file to change the default majority-to-type match to change the script behaviour.
Default configuration file is located [here](tag_creator/configuration.yml)
Be aware that configs will not be joined when you provide new config file.

See default config:

```python
python -m tag_creator --show_config

__main__ INFO: commit_types:
- majority: major
  type:
  - BREAKING_CHANGE
  - BREAKING CHANGE
- majority: minor
  type:
  - feat
  - build
  - ci
  - revert
- majority: patch
  type:
  - fix
  - docs
  - refactor
  - perf
  - test
  - chore
  - style
```

Update config (follow the same structure as in the default configuration file):

```python
python -m tag_creator --config="$HOME/custom_cfg.yml" --show_config
configuration INFO: Custom config read!
__main__ INFO: commit_types:
- majority: major
  type:
  - major
- majority: minor
  type:
  - minor
- majority: patch
  type:
  - patch
```
