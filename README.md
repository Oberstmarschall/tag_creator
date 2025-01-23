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

## Configuration

Use --help option to see available scripts options.
You can provide a custom configuration file to change the default majority-to-type match to change the script behaviour.
Default configuration file is located [here](tag_creator/configuration.yml)
Be aware that configs will not be joined when you provide new config file.
