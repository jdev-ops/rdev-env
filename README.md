# rdev-env tool

## Install

```
pip install --no-cache-dir -U https://github.com/jdev-ops/rdev-env/archive/dev.zip
```

![Alt text](docs/imgs/setup.cast.gif?raw=true "Title")

## Operation

You can see the default configurations on $HOME/.rdev/configs.json

```
cat $HOME/.rdev/configs.json
```

To set a pre-push hook in a git repository:

```
set-lppush
```

Now when you make a git push and the CHECK_COMMIT_FORMAT env var is set to `yes` you are enforcing that all the commits being pushed contains at least one section.

```
CHECK_COMMIT_FORMAT=yes git push
```

![Alt text](docs/imgs/check-commit-pre-push.cast.gif?raw=true "Title")

To set the k8s related configurations

```
set-lconfigs
```

This command uses the keys on "k8s-configs" from $HOME/.rdev/configs.json and generates a json file (.rdev-configs/configs.json) with entries for each directory of the folder in the "path" key that has as prefix the value of "dir-prefix" key.

## create-tag script

When the env var CREATE_TAG_ACTION = partial:

1. An entry in the CHANGELOG.md file is created, and the .yaml files from the k8s folder are updated.

```
CREATE_TAG_ACTION=partial create-tag
```

When the env var CREATE_TAG_ACTION = all (the default value):

1. and
2. the branch develop is merge to master and a tag is created

```
create-tag
```

![Alt text](docs/imgs/end.cast.gif?raw=true "Title")

## Elixir related scripts

There are scrits to support the Elixir development expirience:

```
cli/srv
```

To run via iex the current Elixir mix project.

```
r-iex
```

To lunch a new iex shell connected to the previous one.

and

```
r-exp <expression>
```

to run an Elixir expression over the one lunched via cli/srv

![Alt text](docs/imgs/extra.cast.gif?raw=true "Title")
