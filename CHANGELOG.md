## v0.55.0 (18 July 2019)
- Refactor request api.ws2p.heads in api.bma.network.ws2p_heads (BMA command to get ws2p heads)
- Add support for PEP 561 for duniterpy type hints to be recognized by mypy when imported
- Add Pylint as dev dependency to check code validity and in MakeFile (check and pylint command)
- Add Black as dev dependency to format code (not PEP8 compliant) and in MakeFile (check and format commands)
- Add pylint, format and check-format commands to Makefile
- Apply Mypy, Pylint and Black on tests and examples folders
- Add build command in Makefile
- Install build tools separately via a requirements_deploy.txt file
- Add deploy and deploy_test commands in Makefile
- Fix setup.py to not include tests folder in wheel package
- Fix bug in pubsec v1 secret key length check while loading
- Fix pipeline not run when Makefile is changed
- Trigger PyPi release job only on tag
- Use extends instead of Yaml anchors in gitlab-ci (require gitlab v12+)
- Rename gitlab_ci job "mypy" to "check" which run "make check" (Mypy + Pylint)
- Add check format stage as first stage in gitlab-ci
- Move github-sync stage in release stage as after-script step
- Remove coveralls dependency

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
