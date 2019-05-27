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
