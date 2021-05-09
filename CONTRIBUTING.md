# Contribute guide

## Pre-commit
We are using [`pre-commit`](https://pre-commit.com/) tool to perform checks on staged changes before committing. Such as black formatting.
Depending whether you prefer to work ouside or inside Poetry virtual environment, you should stick to one usage or use both to still have this usefull checks.
`pre-commit` can be used from the installation on your system or from inside Poetry virtual environment where it is installed.

To install the `git-hooks`, run:
```bash
pip3 install --user pre-commit
duniterpy> pre-commit install
```

```bash
duniterpy> poetry shell
(duniterpy-UyTOfZjU-py3.9) pre-commit install
```

### Black formatting
We are using [Black](https://github.com/psf/black) formatter tool.
Run Black on a Python file to format it:
```bash
poetry run black duniterpy/file.py
```
With `pre-commit`, Black is called on staged files, so the commit should fail in case black would make changes.
You will have to add Black changes in order to commit your changes.

## Release workflow
To handle a release, you have to respect this workflow:

* Verify all features and bug fixes are merged in the `dev` branch.
* Checkout on the `dev` branch
* Update the `CHANGELOG.md` file and commit
* Run the `release.sh` script with the version semantic number as argument:

```bash
./release.sh 0.50.0
```

* A new commit is added with the version number and a tag in git.
* Merge all new commits from `dev` to `master` on GitLab with a merge request.
* Release on PyPI from the GitLab pipeline manual job of the `master` branch.
