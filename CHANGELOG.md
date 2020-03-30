## [v0.57.0](https://git.duniter.org/clients/python/duniterpy/-/milestones/11) (31st March 2020)
### Code
## Enhancements
- #122, !99 Implement `/wot/requirements-of-pending` command support in BMA api
- #120, !98 `HeadV2`, `HeadV1`, `HeadV0` and `Head` classes now each inherit from previous class **BREAK BACKWARD COMPATIBILITY**
## Fixes
- #119, !96 `software_version` field in WS2Pv1 messages now accept a string after patch number (`1.7.21-beta` accepted)
- #114, !100 Fix `bma.blockhain.revoked` command class calling `/blockchain/with/excluded` url
 
## CI/CD
- #66, !93  Migrate to [Poetry](https://python-poetry.org/) (build and development environment)

- Thanks @vtexier, @Moul

## [v0.56.0](https://git.duniter.org/clients/python/duniterpy/-/milestones/10) (20th January 2020)
### Code
- #58, !84: Introduce WS2P API support: **BREAK BACKWARD COMPATIBILITY**:
  - `bma.ws`: now websocket connections use the special `WSConnection` class and `async`, check examples.
  - Add two examples, a helper to retrieve the WS2P API from BMA.
- #113, !89: Blocks signature verification is correctly handled now, differently from other documents.
- #112, !88: fix `Unlock.from_inline()` error on a newly created Unlock
- !87: Typos in Block: `noonce` −> `nonce`, hash
- !82: Use `sys.exit()` instead of `exit()`
- !79:
  - Move tools out of the `helper` folder
  - Dedicate the `helper` folder to helpers
  - Introduce `output_available()` helper to check if an output is available

### Dependencies
- !91: fix the `attrs`/`attr` dependency

### Build
- #107, !81: Enhance version definition in `setup.py`

### CI/CD
- !78: Release on PyPI only on tags

### Documentation
- #101, !80: Publish auto-documentation on GitLab Pages
- #106, !83: Migrate the `README` back to markdown, reword and update it.
- !77: Improve v0.55.0 and add v0.55.1 changelog
- !92: Add v0.56.0 changelog
---

- Thanks @vtexier, @Moul

## v0.55.1 (19th July 2019)
- #102: wheel build does not longer include `duniterpy` sub-folders
- Trigger release only on `master` not on tag as protected environment variables are not shared with pipelines started on a tag
- Fix Makefile: rebuild not working

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

#### Others
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
