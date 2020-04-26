# Contribute guide

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
