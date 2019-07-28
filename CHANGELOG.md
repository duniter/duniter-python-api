## [v0.55.0](https://git.duniter.org/clients/python/duniterpy/-/milestones/9) (18th July 2019)
### Code
- Refactor request `api.ws2p.heads` in `api.bma.network.ws2p_heads` (BMA command to get ws2p heads)
- Fix bug in PubSec v1 secret key length check while loading

### Checks
#### Pylint
- Add Pylint as a dev dependency to check code validity
- Add `pylint` command to the `Makefile`
- #91, !65: Apply Pylint on the code

#### Black
- #54: Add Black as dev dependency to format the code (not PEP8 compliant)
- Add `format` and `check-format` commands to the `MakeFile`
- !63: Format the code with Black

#### Other
- `Makefile`: `check` command for `mypy`, `pylint`, and `check-format` checks
- #94: Apply Mypy, Pylint and Black on `tests` and `examples` folders

### CI
- Add MyPy, Black, and Pylint jobs
- Rename `mypy` job to `check` which run `make check`: `mypy`, `pylint`, `check-format`
- Add `check-format` job at the first stage

### Build
- Add `build` command to the Makefile
- Install build dependencies separately via a `requirements_deploy.txt` file
- #98, !72: Do not include `tests` folder in the wheel package for PyPi distribution

### CD
- Add `deploy` and `deploy_test` commands to the Makefile
- #99, !74: Add job for PyPi test deployment
- !73: Trigger PyPi release job only on tag
- Move `github-sync` stage in release stage as an `after-script` step
- #100, !75: Use extends instead of Yaml anchors in `.gitlab-ci.yml` (requires GitLab v12+)
- Also trigger the pipeline when the `Makefile` changes

### Project
- #96, !70: Add support for PEP 561 for DuniterPy type hints to be recognized by mypy when imported
- Remove not used `coveralls` dependency

## v0.54.3 (29th May 2019)
- Upload again to PyPi as previous release haven’t been uploaded thanks to the tag
- Transaction: fix `time` type

## v0.54.2 (27th May 2019)
- fix Transaction document generation
- lock transaction document generation with a test

## v0.54.1 (9th May 2019)
- `Transaction`: add __eq__() and __hash__() methods
- Transaction Unlock parameters: add __eq__() and __hash__() methods
- Transaction: add 'time' variable for read and write but not for doc generation
- output conditions: add __eq__() and __hash__() methods
- test transaction equality at all levels

---

- Thanks @Moul, @vtexier

## v0.54.0 (5th May 2019)

### Code/tests
- Fix OutputSource and InputSource from_inline() regex matching
- Transaction document: tests and code: drop versions 2 and 3 management
- Block document: code: drop vensions 2 and 3 management
- Block document: Upgrade blocks to v11 and TX to v10
- Add OutputSource.inline_condition() method
- output conditions: fix 'parser' variables default definition
- output conditions: add token() and compose() tests

### Other
- CI: Do not trigger build, tests, type check on modification of non-relevant files
- Makefile: use python3 module to run tests and type check
- Add coveralls as dev dependency
- setup.py: add classifiers: Python versions, Intended Audience
- Add CHANGELOG.md from v0.53.1

---

- Thanks @Moul, @vtexier

## v0.53.1 (18 April 2019)

- Implement equality `__eq__()` and `__hash__()` methods for InputSource and OutputSource classes

Thanks @Moul, @vtexier

## v0.53.0 (30 March 2019)

- To be completed…
