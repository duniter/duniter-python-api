import unittest
import jsonschema
import aiohttp
from tests.api.webserver import WebFunctionalSetupMixin, web, asyncio
from duniterpy.documents import BMAEndpoint
from duniterpy.api.bma.blockchain import API, parameters, block, current, hardship, memberships, newcomers, \
    certifications, joiners, actives, leavers, ud, tx, blocks, \
    BLOCK_NUMBERS_SCHEMA, BLOCK_SCHEMA, BLOCKS_SCHEMA, HARDSHIP_SCHEMA, MEMBERSHIPS_SCHEMA, PARAMETERS_SCHEMA


class Test_BMA_blockchain(WebFunctionalSetupMixin, unittest.TestCase):
    def test_parameters(self):
        json_sample = {
                          "currency": "g1",
                          "c": 0.0488,
                          "dt": 86400,
                          "ud0": 1000,
                          "sigPeriod": 432000,
                          "sigStock": 100,
                          "sigWindow": 5259600,
                          "sigValidity": 63115200,
                          "sigQty": 5,
                          "idtyWindow": 5259600,
                          "msWindow": 5259600,
                          "xpercent": 0.8,
                          "msValidity": 31557600,
                          "stepMax": 5,
                          "medianTimeBlocks": 24,
                          "avgGenTime": 300,
                          "dtDiffEval": 12,
                          "percentRot": 0.67,
                          "udTime0": 1488970800,
                          "udReevalTime0": 1490094000,
                          "dtReeval": 15778800
        }
        jsonschema.validate(json_sample, PARAMETERS_SCHEMA)

    def test_parameters_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/blockchain/parameters', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await parameters(connection)

        self.loop.run_until_complete(go())

    def test_schema_block_0(self):
        json_sample = {
  "version": 2,
  "nonce": 10144,
  "number": 0,
  "powMin": 3,
  "time": 1421838980,
  "medianTime": 1421838980,
  "membersCount": 4,
  "monetaryMass": 0,
  "currency": "meta_brouzouf",
  "issuer": "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
  "signature": "+78w7251vvRdhoIJ6IWHEiEOLxNrmfQf45Y5sYvPdnAdXkVpO1unMV5YA/G5Vhphyz1dICrbeKCPM5qbFsoWAQ==",
  "hash": "00063EB6E83F8717CEF1D25B3E2EE308374A14B1",
  "inner_hash": "00063EB6E83F8717CEF1D25B3E2EE308374A14B1",
  "parameters": "0.1:86400:100:604800:2629800:3:3:2629800:3:11:600:20:144:0.67",
  "previousHash": None,
  "previousIssuer": None,
  "dividend": None,
  "membersChanges": [],
  "identities": [
    "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:Ot3zIp/nsHT3zgJy+2YcXPL6vaM5WFsD+F8w3qnJoBRuBG6lv761zoaExp2iyUnm8fDAyKPpMxRK2kf437QSCw==:1421787800:inso",
    "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:GZKLgaxJKL+GqxVLePMt8OVLJ6qTLrib5Mr/j2gjiNRY2k485YLB2OlzhBzZVnD3xLs0xi69JUfmLnM54j3aCA==:1421786393:cgeek",
    "BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:th576H89dfymkG7/sH+DAIzjlmIqNEW6zY3ONrGeAml+k3f1ver399kYnEgG5YCaKXnnVM7P0oJHah80BV3mDw==:1421790376:moul",
    "37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:XRmbTYFkPeGVEU2mJzzN4h1oVNDsZ4yyNZlDAfBm9CWhBsZ82QqX9GPHye2hBxxiu4Nz1BHgQiME6B4JcAC8BA==:1421787461:galuel"
  ],
  "joiners": [
    "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:ccJm3F44eLMhQtnQY/7+14SWCDqVTL3Miw65hBVpV+YiUSUknIGhBNN0C0Cf+Pf0/pa1tjucW8Us3z5IklFSDg==:0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1421787800:inso",
    "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:1lFIiaR0QX0jibr5zQpXVGzBvMGqcsTRlmHiwGz5HOAZT8PTdVUb5q6YGZ6qAUZjdMjPmhLaiMIpYc47wUnzBA==:0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1421786393:cgeek",
    "BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:ctyAhpTRrAAOhFJukWI8RBr//nqYYdQibVzjOfaCdcWLb3TNFKrNBBothNsq/YrYHr7gKrpoftucf/oxLF8zAg==:0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1421790376:moul",
    "37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:uoiGaC5b7kWqtqdPxwatPk9QajZHCNT9rf8/8ud9Rli24z/igcOf0Zr4A6RTAIKWUq9foW39VqJe+Y9R3rhACw==:0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1421787461:galuel"
  ],
  "actives": [],
  "leavers": [],
  "excluded": [],
  "revoked": [],
  "certifications": [
    "37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:3wmCVW8AbVxRFm2PuLXD9UTCIg93MhUblZJvlYrDldSV4xuA7mZCd8TV4vb/6Bkc0FMQgBdHtpXrQ7dpo20uBA==",
    "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:7UMQsUjLvuiZKIzOH5rrZDdDi5rXUo69EuQulY1Zm42xpRx/Gt5CkoTcJ/Mu83oElQbcZZTz/lVJ6IS0jzMiCQ==",
    "BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:twWSY9etI82FLEHzhdqIoHsC9ehWCA7DCPiGxDLCWGPO4TG77hwtn3RcC68qoKHCib577JCp+fcKyp2vyI6FDA==",
    "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:0:7K5MHkO8ibf5SchmPkRrmsg9owEZZ23uEMJJSQYG7L3PUmAKmmV/0VSjivxXH8gJGQBGsXQoK79x1jsYnj2nAg==",
    "BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:0:Jua4FcEJFptSE5OoG1/Mgzx4e9jgGnYu7t8g1sqqPujI9hRhLFNXbQXedPS1q1OD5vWivA045gKOq/gnj8opDg==",
    "37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:0:R/DV4/wYjvBG09QSOGtnxd3bfPFhVjEE5Uy3BsBMVUvjLsgxjf8NgLhYVozcHTRWS43ArxlXKfS5m3+KIPhhAQ==",
    "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:0:4hP+ahJK021akL4UxB6c5QLaGJXa9eapd3nfdFQe+Xy87f/XLhj8BCa22XbbOlyGdaZRT3AYzbCL2UD5tI8mCw==",
    "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:0:sZTQJr0d/xQnxrIIdSePUJpSTOa8v6IYGXMF2fVDZxQU8vwfzPm2dUKTaF0nU6E9wOYszzkBHaXL85nir+WtCQ==",
    "37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:0:hDuBkoFhWhR/FgOU1+9SbQGBMIr47xqUzw1ZMERaPQo4aWm0WFbZurG4lvuJZzTyG6RF/gSw4VPvYZFPxWmADg==",
    "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:0:79ZVrBehElVZh82fJdR18IJx06GkEVZTbwdHH4zb0S6VaGwdtLh1rvomm4ukBvUc8r/suTweG/SScsJairXNAg==",
    "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:0:e/ai9E4G5CFB9Qi329e0ffYpZMgxj8mM4rviqIr2+UESA0UG86OuAAyHO11hYeyolZRiU8I7WdtNE98B1uZuBg==",
    "BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:0:q4PCneYkcPH8AHEqEvqTtYQWslhlYO2B87aReuOl1uPczn5Q3VkZFAsU48ZTYryeyWp2nxdQojdFYhlAUNchAw=="
  ],
  "transactions": [],
  "raw": "Version: 1\nType: block\nCurrency: meta_brouzouf\nNonce: 10144\nNumber: 0\nPoWMin: 3\nTime: 1421838980\nMedianTime: 1421838980\nIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk\nparameters: 0.1:86400:100:604800:2629800:3:3:2629800:3:11:600:20:144:0.67\nMembersCount: 4\nIdentities:\n8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:Ot3zIp/nsHT3zgJy+2YcXPL6vaM5WFsD+F8w3qnJoBRuBG6lv761zoaExp2iyUnm8fDAyKPpMxRK2kf437QSCw==:1421787800:inso\nHnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:GZKLgaxJKL+GqxVLePMt8OVLJ6qTLrib5Mr/j2gjiNRY2k485YLB2OlzhBzZVnD3xLs0xi69JUfmLnM54j3aCA==:1421786393:cgeek\nBMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:th576H89dfymkG7/sH+DAIzjlmIqNEW6zY3ONrGeAml+k3f1ver399kYnEgG5YCaKXnnVM7P0oJHah80BV3mDw==:1421790376:moul\n37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:XRmbTYFkPeGVEU2mJzzN4h1oVNDsZ4yyNZlDAfBm9CWhBsZ82QqX9GPHye2hBxxiu4Nz1BHgQiME6B4JcAC8BA==:1421787461:galuel\nJoiners:\n8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:ccJm3F44eLMhQtnQY/7+14SWCDqVTL3Miw65hBVpV+YiUSUknIGhBNN0C0Cf+Pf0/pa1tjucW8Us3z5IklFSDg==:0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1421787800:inso\nHnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:1lFIiaR0QX0jibr5zQpXVGzBvMGqcsTRlmHiwGz5HOAZT8PTdVUb5q6YGZ6qAUZjdMjPmhLaiMIpYc47wUnzBA==:0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1421786393:cgeek\nBMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:ctyAhpTRrAAOhFJukWI8RBr//nqYYdQibVzjOfaCdcWLb3TNFKrNBBothNsq/YrYHr7gKrpoftucf/oxLF8zAg==:0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1421790376:moul\n37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:uoiGaC5b7kWqtqdPxwatPk9QajZHCNT9rf8/8ud9Rli24z/igcOf0Zr4A6RTAIKWUq9foW39VqJe+Y9R3rhACw==:0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1421787461:galuel\nActives:\nLeavers:\nExcluded:\nCertifications:\n37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:3wmCVW8AbVxRFm2PuLXD9UTCIg93MhUblZJvlYrDldSV4xuA7mZCd8TV4vb/6Bkc0FMQgBdHtpXrQ7dpo20uBA==\nHnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:7UMQsUjLvuiZKIzOH5rrZDdDi5rXUo69EuQulY1Zm42xpRx/Gt5CkoTcJ/Mu83oElQbcZZTz/lVJ6IS0jzMiCQ==\nBMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:twWSY9etI82FLEHzhdqIoHsC9ehWCA7DCPiGxDLCWGPO4TG77hwtn3RcC68qoKHCib577JCp+fcKyp2vyI6FDA==\n8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:0:7K5MHkO8ibf5SchmPkRrmsg9owEZZ23uEMJJSQYG7L3PUmAKmmV/0VSjivxXH8gJGQBGsXQoK79x1jsYnj2nAg==\nBMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:0:Jua4FcEJFptSE5OoG1/Mgzx4e9jgGnYu7t8g1sqqPujI9hRhLFNXbQXedPS1q1OD5vWivA045gKOq/gnj8opDg==\n37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:0:R/DV4/wYjvBG09QSOGtnxd3bfPFhVjEE5Uy3BsBMVUvjLsgxjf8NgLhYVozcHTRWS43ArxlXKfS5m3+KIPhhAQ==\n8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:0:4hP+ahJK021akL4UxB6c5QLaGJXa9eapd3nfdFQe+Xy87f/XLhj8BCa22XbbOlyGdaZRT3AYzbCL2UD5tI8mCw==\nHnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:0:sZTQJr0d/xQnxrIIdSePUJpSTOa8v6IYGXMF2fVDZxQU8vwfzPm2dUKTaF0nU6E9wOYszzkBHaXL85nir+WtCQ==\n37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:0:hDuBkoFhWhR/FgOU1+9SbQGBMIr47xqUzw1ZMERaPQo4aWm0WFbZurG4lvuJZzTyG6RF/gSw4VPvYZFPxWmADg==\n8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:0:79ZVrBehElVZh82fJdR18IJx06GkEVZTbwdHH4zb0S6VaGwdtLh1rvomm4ukBvUc8r/suTweG/SScsJairXNAg==\nHnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:0:e/ai9E4G5CFB9Qi329e0ffYpZMgxj8mM4rviqIr2+UESA0UG86OuAAyHO11hYeyolZRiU8I7WdtNE98B1uZuBg==\nBMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:0:q4PCneYkcPH8AHEqEvqTtYQWslhlYO2B87aReuOl1uPczn5Q3VkZFAsU48ZTYryeyWp2nxdQojdFYhlAUNchAw==\nTransactions:\n"
}
        jsonschema.validate(json_sample, BLOCK_SCHEMA)

    def test_block_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/blockchain/block/100', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await block(connection, 100)

        self.loop.run_until_complete(go())

    def test_current_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/blockchain/current', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await current(connection)

        self.loop.run_until_complete(go())

    def test_schema_block(self):
        json_sample = {
            "version": 2,
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
            "revoked": [],
            "inner_hash": "00063EB6E83F8717CEF1D25B3E2EE308374A14B1",
            "certifications": [
            "ATkjQPa4sn4LBF69jqEPzFtRdHYJs6MJQjvP8JdN7MtN:APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:34434:oGGiYVBAfhreOzWS1M7HQ0OHHUWAA3NdU29XAca3/3mbfD581QBxeADVR+Bj7kTBqrAxwpwyODtaHyZZNYI3AA==",
            "2sq8bBDQGK74f1eD3mAPQVgHCmFdijZr9nbv16FwbokX:APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:34432:KFKYioosI3FAvyfTKiWyQqRGUros03S/NITNxShB/3L1LI4P7XSLp2+hFbCK375ODm1g/fnwfzOoorOKPGIOAw==",
            "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:34431:nKDTapgYR/nMEEkLaT4ygLCHlxmiACzi4Zv+gzRJN8hGdirQAMN1FNpJ2RVli4V4z+7y3lklPidOX2Aln8ZNBA=="
            ],
            "transactions": [],
            "raw": "Version: 1\nType: block\nCurrency: meta_brouzouf\nNonce: 162294\nNumber: 34435\nPoWMin: 5\nTime: 1443895887\nMedianTime: 1443881487\nIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk\nPreviousHash: 00000D21F80687248A8C02F16BB19A975B4F983D\nPreviousIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk\nMembersCount: 19\nIdentities:\nAPGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:Lld5KezKGDUgrvnNjKuEGZmWJZNYDYtsPJajuOdrEr7MKXIwJYBRTouWPlCoPP9OQBF7qi7dpX+qKeYcjVPPDA==:1443950660:Alcide\nJoiners:\nAPGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:XpdVaX1TKnvjRfJRpFnpVDQOmxfDKKUp3YuSG/Ic8DHAT2SJKFSr+th3mK14JHiBtKMsNpVwFyV7TlKNHgnjAw==:34428:0000074D458E92EF09C2305BF0D191DD7CF1D452:1443950660:Alcide\nActives:\nLeavers:\nExcluded:\nCertifications:\nATkjQPa4sn4LBF69jqEPzFtRdHYJs6MJQjvP8JdN7MtN:APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:34434:oGGiYVBAfhreOzWS1M7HQ0OHHUWAA3NdU29XAca3/3mbfD581QBxeADVR+Bj7kTBqrAxwpwyODtaHyZZNYI3AA==\n2sq8bBDQGK74f1eD3mAPQVgHCmFdijZr9nbv16FwbokX:APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:34432:KFKYioosI3FAvyfTKiWyQqRGUros03S/NITNxShB/3L1LI4P7XSLp2+hFbCK375ODm1g/fnwfzOoorOKPGIOAw==\n8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:APGtJqMq91jKxgGX9KEoCKqqD6UTsnPmALGNyaLbTknA:34431:nKDTapgYR/nMEEkLaT4ygLCHlxmiACzi4Zv+gzRJN8hGdirQAMN1FNpJ2RVli4V4z+7y3lklPidOX2Aln8ZNBA==\nTransactions:\n"
            }
        jsonschema.validate(json_sample, BLOCK_SCHEMA)

    def test_schema_hardship(self):
        json_sample = {
          "block": 40432,
          "level": 4
        }
        jsonschema.validate(json_sample, HARDSHIP_SCHEMA)

    def test_hardship_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/blockchain/hardship/8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await hardship(connection, "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU")

        self.loop.run_until_complete(go())

    def test_schema_membership(self):
        json_sample = {
            "pubkey": "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU",
            "uid": "inso",
            "sigDate": "0-E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
            "memberships": [
                {
                    "version": 1,
                    "currency": "meta_brouzouf",
                    "membership": "IN",
                    "blockNumber": 0,
                    "blockHash": "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
                    "written": 10005
                },
                {
                    "version": 1,
                    "currency": "meta_brouzouf",
                    "membership": "IN",
                    "blockNumber": 31658,
                    "blockHash": "0000C5336F0B64BFB87FF4BC858AE25726B88175",
                    "written": 43222
                },
            ]
        }
        jsonschema.validate(json_sample, MEMBERSHIPS_SCHEMA)

    def test_membership_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/blockchain/memberships/8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await memberships(connection, "8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU")

        self.loop.run_until_complete(go())

    def test_schema_newcomers(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, BLOCK_NUMBERS_SCHEMA)

    def test_newcomers_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/blockchain/with/newcomers', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await newcomers(connection)

        self.loop.run_until_complete(go())

    def test_schema_certifications(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, BLOCK_NUMBERS_SCHEMA)

    def test_certifications_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/blockchain/with/certs', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await certifications(connection)

        self.loop.run_until_complete(go())

    def test_schema_joiners(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, BLOCK_NUMBERS_SCHEMA)

    def test_joiners_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/blockchain/with/joiners', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await joiners(connection)

        self.loop.run_until_complete(go())

    def test_schema_actives(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, BLOCK_NUMBERS_SCHEMA)

    def test_actives_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/blockchain/with/actives', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await actives(connection)

        self.loop.run_until_complete(go())

    def test_schema_leavers(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, BLOCK_NUMBERS_SCHEMA)

    def test_leavers_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/blockchain/with/leavers', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await leavers(connection)

        self.loop.run_until_complete(go())

    def test_schema_ud(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, BLOCK_NUMBERS_SCHEMA)

    def test_schema_blocks(self):
        json_sample = [
          {
            "version": 2,
            "nonce": 1,
            "number": 100,
            "powMin": 4,
            "time": 1461847414,
            "medianTime": 1461847412,
            "membersCount": 2,
            "monetaryMass": 0,
            "unitbase": 0,
            "issuersCount": 0,
            "issuersFrame": 0,
            "issuersFrameVar": 0,
            "currency": "test_net",
            "issuer": "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
            "signature": "R6XzQ7DDTam+koGCoEeygxFAuy9Uh/by6GS8mMx5rFWqusxaUYRJW4QkeGmqT9yHTpXCbHwZZbpIgm3SbrrVDg==",
            "hash": "2C49A15983AEA3EBFD6B430876933A72C11D8D20E49ED94C4066557C1B528973",
            "parameters": "",
            "previousHash": "12DD8737F97BD3AC0B7E4B10F770F101A0D3EB3EEC858023CBCA06BB4AA9EBE6",
            "previousIssuer": "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
            "inner_hash": "0C9002C192ADB5D913C78D813216E56677CCF53A4DE0764C30E46E858D4854A5",
            "dividend": None,
            "identities": [],
            "joiners": [],
            "actives": [],
            "leavers": [],
            "revoked": [],
            "excluded": [],
            "certifications": [],
            "transactions": [],
            "raw": "Version: 2\nType: block\nCurrency: test_net\nNumber: 100\nPoWMin: 4\nTime: 1461847414\nMedianTime: 1461847412\nIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk\nPreviousHash: 12DD8737F97BD3AC0B7E4B10F770F101A0D3EB3EEC858023CBCA06BB4AA9EBE6\nPreviousIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk\nMembersCount: 2\nIdentities:\nJoiners:\nActives:\nLeavers:\nRevoked:\nExcluded:\nCertifications:\nTransactions:\nInnerHash: 0C9002C192ADB5D913C78D813216E56677CCF53A4DE0764C30E46E858D4854A5\nNonce: 1\n"
          },
          {
            "version": 2,
            "nonce": 1,
            "number": 101,
            "powMin": 4,
            "time": 1461847414,
            "medianTime": 1461847412,
            "membersCount": 2,
            "monetaryMass": 0,
            "unitbase": 0,
            "issuersCount": 0,
            "issuersFrame": 0,
            "issuersFrameVar": 0,
            "currency": "test_net",
            "issuer": "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
            "signature": "IDWQCVtI8XxRVqakKc822ayZ8qNzm0kYK3ew1heqMf8aqsMhiS/1IKBi4gBFBXMpO49bX8GkZW/R/TDxiYsUAg==",
            "hash": "9A29E79EC06444EEC4ADC9F7C9B720A91A9FC1B66219F641EF71661BD2F28F8F",
            "parameters": "",
            "previousHash": "2C49A15983AEA3EBFD6B430876933A72C11D8D20E49ED94C4066557C1B528973",
            "previousIssuer": "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
            "inner_hash": "A91B10BA4EEB7CF712DC92CAE7F6FF761571929B8BF1A13E1FF5CC402442A10A",
            "dividend": None,
            "identities": [],
            "joiners": [],
            "actives": [],
            "leavers": [],
            "revoked": [],
            "excluded": [],
            "certifications": [],
            "transactions": [],
            "raw": "Version: 2\nType: block\nCurrency: test_net\nNumber: 101\nPoWMin: 4\nTime: 1461847414\nMedianTime: 1461847412\nIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk\nPreviousHash: 2C49A15983AEA3EBFD6B430876933A72C11D8D20E49ED94C4066557C1B528973\nPreviousIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk\nMembersCount: 2\nIdentities:\nJoiners:\nActives:\nLeavers:\nRevoked:\nExcluded:\nCertifications:\nTransactions:\nInnerHash: A91B10BA4EEB7CF712DC92CAE7F6FF761571929B8BF1A13E1FF5CC402442A10A\nNonce: 1\n"
          },
          {
            "version": 2,
            "nonce": 1,
            "number": 102,
            "powMin": 4,
            "time": 1461847414,
            "medianTime": 1461847413,
            "membersCount": 2,
            "monetaryMass": 0,
            "unitbase": 0,
            "issuersCount": 0,
            "issuersFrame": 0,
            "issuersFrameVar": 0,
            "currency": "test_net",
            "issuer": "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
            "signature": "jUfBfFwzsXyPGi/seEonWHOfq5/lAudASpnpiHhfr7OQhOTYL3RRECy2RVlZAoqJ9FqlcdTSaj+I+FFPBomoBA==",
            "hash": "8B6F0E8EA4B9D5A078D679E6004F891CAB5BDE827B51B1090E6B71B1FFB3E727",
            "parameters": "",
            "previousHash": "9A29E79EC06444EEC4ADC9F7C9B720A91A9FC1B66219F641EF71661BD2F28F8F",
            "previousIssuer": "HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk",
            "inner_hash": "301236A7771CBDE30F253E2A42E34BF758450DADDDB37A832328701B04213A59",
            "dividend": None,
            "identities": [],
            "joiners": [],
            "actives": [],
            "leavers": [],
            "revoked": [],
            "excluded": [],
            "certifications": [],
            "transactions": [],
            "raw": "Version: 2\nType: block\nCurrency: test_net\nNumber: 102\nPoWMin: 4\nTime: 1461847414\nMedianTime: 1461847413\nIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk\nPreviousHash: 9A29E79EC06444EEC4ADC9F7C9B720A91A9FC1B66219F641EF71661BD2F28F8F\nPreviousIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk\nMembersCount: 2\nIdentities:\nJoiners:\nActives:\nLeavers:\nRevoked:\nExcluded:\nCertifications:\nTransactions:\nInnerHash: 301236A7771CBDE30F253E2A42E34BF758450DADDDB37A832328701B04213A59\nNonce: 1\n"
          }
        ]
        jsonschema.validate(json_sample, BLOCKS_SCHEMA)

    def test_ud_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/blockchain/with/ud', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await ud(connection)

        self.loop.run_until_complete(go())

    def test_schema_tx(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, BLOCK_NUMBERS_SCHEMA)

    def test_tx_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, port, url = await self.create_server('GET', '/blockchain/with/tx', handler)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    connection = next(BMAEndpoint("127.0.0.1", None, None, port).conn_handler(session))
                    await tx(connection)

        self.loop.run_until_complete(go())
