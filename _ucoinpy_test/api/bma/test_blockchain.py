import unittest
import jsonschema
from ucoinpy.api.bma.blockchain import Parameters, Block, Current, Hardship, Membership, Newcomers, \
    Certifications, Joiners, Actives, Leavers, UD, TX


class Test_BMA_Blockchain(unittest.TestCase):
    def test_parameters(self):
        json_sample = {
          "currency": "meta_brouzouf",
          "c": 0.1,
          "dt": 86400,
          "ud0": 100,
          "sigDelay": 604800,
          "sigValidity": 2629800,
          "sigQty": 3,
          "sigWoT": 3,
          "msValidity": 2629800,
          "stepMax": 3,
          "medianTimeBlocks": 11,
          "avgGenTime": 600,
          "dtDiffEval": 20,
          "blocksRot": 144,
          "percentRot": 0.67
        }
        jsonschema.validate(json_sample, Parameters.schema)

    def test_schema_block(self):
        json_sample = {
            "version": 1,
            "nonce": 162294,
            "number": 34435,
            "powMin": 5,
            "time": 1443895887,
            "medianTime": 1443881487,
            "membersCount": 19,
            "monetaryMass": 154381656062153,
            "currency": "meta_brouzouf",
            "issuer": "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
            "signature": "VVr2MHcIAxIwjc2skkHqNAOgXVYEVhw4YczZ/NL5fsNZLnu9qvs04q8OUA4dfrDnsYB9I+BhVOAYNYDwNa6KDw==",
            "hash": "000002B06C990DEBD5C1D947289C2CF4F4396FB2",
            "parameters": "",
            "previousHash": "00000D21F80687248A8C02F16BB19A975B4F983D",
            "previousIssuer": "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
            "dividend": None,
            "membersChanges": [],
            "identities": [
            "APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:Lld5KezKGDUgrvnNjKuEGZmWJZNYDYtsPJajuOdrEr7MKXIwJYBRTouWPlCoPP9OQBF7qi7dpX+qKeYcjVPPDA==:1443950660:Alcide"
            ],
            "joiners": [
            "APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:XpdVaX1TKnvjRfJRpFnpVDQOmxfDKKUp3YuSG/Ic8DHAT2SJKFSr+th3mK14JHiBtKMsNpVwFyV7TlKNHgnjAw==:34428:0000074D458E92EF09C2305BF0D191DD7CF1D452:1443950660:Alcide"
            ],
            "actives": [],
            "leavers": [],
            "excluded": [],
            "certifications": [
            "ATkjQPa4sn4LBF69jqEPzFtRdHYJs6MJQjvP8JdN7MtN:APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:34434:oGGiYVBAfhreOzWS1M7HQ0OHHUWAA3NdU29XAca3/3mbfD581QBxeADVR+Bj7kTBqrAxwpwyODtaHyZZNYI3AA==",
            "2sq8bBDQGK74f1eD3mAPQVgHCmFdijZr9nbv16FwbokX:APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:34432:KFKYioosI3FAvyfTKiWyQqRGUros03S/NITNxShB/3L1LI4P7XSLp2+hFbCK375ODm1g/fnwfzOoorOKPGIOAw==",
            "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:34431:nKDTapgYR/nMEEkLaT4ygLCHlxmiACzi4Zv+gzRJN8hGdirQAMN1FNpJ2RVli4V4z+7y3lklPidOX2Aln8ZNBA=="
            ],
            "transactions": [],
            "raw": "Version: 1\nType: Block\nCurrency: meta_brouzouf\nNonce: 162294\nNumber: 34435\nPoWMin: 5\nTime: 1443895887\nMedianTime: 1443881487\nIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk\nPreviousHash: 00000D21F80687248A8C02F16BB19A975B4F983D\nPreviousIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk\nMembersCount: 19\nIdentities:\nAPGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:Lld5KezKGDUgrvnNjKuEGZmWJZNYDYtsPJajuOdrEr7MKXIwJYBRTouWPlCoPP9OQBF7qi7dpX+qKeYcjVPPDA==:1443950660:Alcide\nJoiners:\nAPGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:XpdVaX1TKnvjRfJRpFnpVDQOmxfDKKUp3YuSG/Ic8DHAT2SJKFSr+th3mK14JHiBtKMsNpVwFyV7TlKNHgnjAw==:34428:0000074D458E92EF09C2305BF0D191DD7CF1D452:1443950660:Alcide\nActives:\nLeavers:\nExcluded:\nCertifications:\nATkjQPa4sn4LBF69jqEPzFtRdHYJs6MJQjvP8JdN7MtN:APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:34434:oGGiYVBAfhreOzWS1M7HQ0OHHUWAA3NdU29XAca3/3mbfD581QBxeADVR+Bj7kTBqrAxwpwyODtaHyZZNYI3AA==\n2sq8bBDQGK74f1eD3mAPQVgHCmFdijZr9nbv16FwbokX:APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:34432:KFKYioosI3FAvyfTKiWyQqRGUros03S/NITNxShB/3L1LI4P7XSLp2+hFbCK375ODm1g/fnwfzOoorOKPGIOAw==\n8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:34431:nKDTapgYR/nMEEkLaT4ygLCHlxmiACzi4Zv+gzRJN8hGdirQAMN1FNpJ2RVli4V4z+7y3lklPidOX2Aln8ZNBA==\nTransactions:\n"
            }
        jsonschema.validate(json_sample, Block.schema)
        jsonschema.validate(json_sample, Current.schema)

    def test_schema_hardship(self):
        json_sample = {
          "block": 40432,
          "level": 4
        }
        jsonschema.validate(json_sample, Hardship.schema)

    def test_schema_membership(self):
        json_sample = {
            "pubkey": "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU",
            "uid": "inso",
            "sigDate": 1421787800,
            "memberships": [
                {
                    "version": "1",
                    "currency": "meta_brouzouf",
                    "membership": "IN",
                    "blockNumber": 0,
                    "blockHash": "DA39A3EE5E6B4B0D3255BFEF95601890AFD80709"
                },
                {
                    "version": "1",
                    "currency": "meta_brouzouf",
                    "membership": "IN",
                    "blockNumber": 31658,
                    "blockHash": "0000C5336F0B64BFB87FF4BC858AE25726B88175"
                },
            ]
        }
        jsonschema.validate(json_sample, Membership.schema)

    def test_schema_newcomers(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, Newcomers.schema)

    def test_schema_certifications(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, Certifications.schema)

    def test_schema_joiners(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, Joiners.schema)

    def test_schema_actives(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, Actives.schema)

    def test_schema_leavers(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, Leavers.schema)

    def test_schema_ud(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, UD.schema)

    def test_schema_tx(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, TX.schema)
