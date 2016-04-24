import unittest
import jsonschema
import aiohttp
from tests.api.webserver import WebFunctionalSetupMixin, web, asyncio
from duniterpy.api.bma.blockchain import Parameters, Block, Current, Hardship, Membership, Newcomers, \
    Certifications, Joiners, Actives, Leavers, UD, TX


class Test_BMA_Blockchain(WebFunctionalSetupMixin, unittest.TestCase):
    def test_parameters(self):
        json_sample = {
              "currency": "super_currency",
              "c": 0.007376575,
              "dt": 36000,
              "ud0": 100,
              "sigPeriod": 0,
              "sigStock": 0,
              "sigWindow": 1209600,
              "sigValidity": 31536000,
              "sigQty": 0,
              "xpercent": 0.9,
              "msValidity": 31536000,
              "stepMax": 3,
              "medianTimeBlocks": 20,
              "avgGenTime": 960,
              "dtDiffEval": 10,
              "blocksRot": 20,
              "percentRot": 0.66
            }
        jsonschema.validate(json_sample, Parameters.schema)

    def test_parameters_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/', handler)
            params = Parameters(None)
            params.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await params.get(session)

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
  "raw": "Version: 1\nType: Block\nCurrency: meta_brouzouf\nNonce: 10144\nNumber: 0\nPoWMin: 3\nTime: 1421838980\nMedianTime: 1421838980\nIssuer: HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk\nParameters: 0.1:86400:100:604800:2629800:3:3:2629800:3:11:600:20:144:0.67\nMembersCount: 4\nIdentities:\n8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:Ot3zIp/nsHT3zgJy+2YcXPL6vaM5WFsD+F8w3qnJoBRuBG6lv761zoaExp2iyUnm8fDAyKPpMxRK2kf437QSCw==:1421787800:inso\nHnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:GZKLgaxJKL+GqxVLePMt8OVLJ6qTLrib5Mr/j2gjiNRY2k485YLB2OlzhBzZVnD3xLs0xi69JUfmLnM54j3aCA==:1421786393:cgeek\nBMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:th576H89dfymkG7/sH+DAIzjlmIqNEW6zY3ONrGeAml+k3f1ver399kYnEgG5YCaKXnnVM7P0oJHah80BV3mDw==:1421790376:moul\n37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:XRmbTYFkPeGVEU2mJzzN4h1oVNDsZ4yyNZlDAfBm9CWhBsZ82QqX9GPHye2hBxxiu4Nz1BHgQiME6B4JcAC8BA==:1421787461:galuel\nJoiners:\n8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:ccJm3F44eLMhQtnQY/7+14SWCDqVTL3Miw65hBVpV+YiUSUknIGhBNN0C0Cf+Pf0/pa1tjucW8Us3z5IklFSDg==:0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1421787800:inso\nHnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:1lFIiaR0QX0jibr5zQpXVGzBvMGqcsTRlmHiwGz5HOAZT8PTdVUb5q6YGZ6qAUZjdMjPmhLaiMIpYc47wUnzBA==:0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1421786393:cgeek\nBMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:ctyAhpTRrAAOhFJukWI8RBr//nqYYdQibVzjOfaCdcWLb3TNFKrNBBothNsq/YrYHr7gKrpoftucf/oxLF8zAg==:0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1421790376:moul\n37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:uoiGaC5b7kWqtqdPxwatPk9QajZHCNT9rf8/8ud9Rli24z/igcOf0Zr4A6RTAIKWUq9foW39VqJe+Y9R3rhACw==:0:DA39A3EE5E6B4B0D3255BFEF95601890AFD80709:1421787461:galuel\nActives:\nLeavers:\nExcluded:\nCertifications:\n37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:3wmCVW8AbVxRFm2PuLXD9UTCIg93MhUblZJvlYrDldSV4xuA7mZCd8TV4vb/6Bkc0FMQgBdHtpXrQ7dpo20uBA==\nHnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:7UMQsUjLvuiZKIzOH5rrZDdDi5rXUo69EuQulY1Zm42xpRx/Gt5CkoTcJ/Mu83oElQbcZZTz/lVJ6IS0jzMiCQ==\nBMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:0:twWSY9etI82FLEHzhdqIoHsC9ehWCA7DCPiGxDLCWGPO4TG77hwtn3RcC68qoKHCib577JCp+fcKyp2vyI6FDA==\n8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:0:7K5MHkO8ibf5SchmPkRrmsg9owEZZ23uEMJJSQYG7L3PUmAKmmV/0VSjivxXH8gJGQBGsXQoK79x1jsYnj2nAg==\nBMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:0:Jua4FcEJFptSE5OoG1/Mgzx4e9jgGnYu7t8g1sqqPujI9hRhLFNXbQXedPS1q1OD5vWivA045gKOq/gnj8opDg==\n37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:HnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:0:R/DV4/wYjvBG09QSOGtnxd3bfPFhVjEE5Uy3BsBMVUvjLsgxjf8NgLhYVozcHTRWS43ArxlXKfS5m3+KIPhhAQ==\n8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:0:4hP+ahJK021akL4UxB6c5QLaGJXa9eapd3nfdFQe+Xy87f/XLhj8BCa22XbbOlyGdaZRT3AYzbCL2UD5tI8mCw==\nHnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:0:sZTQJr0d/xQnxrIIdSePUJpSTOa8v6IYGXMF2fVDZxQU8vwfzPm2dUKTaF0nU6E9wOYszzkBHaXL85nir+WtCQ==\n37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:BMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:0:hDuBkoFhWhR/FgOU1+9SbQGBMIr47xqUzw1ZMERaPQo4aWm0WFbZurG4lvuJZzTyG6RF/gSw4VPvYZFPxWmADg==\n8Fi1VSTbjkXguwThF4v2ZxC5whK7pwG2vcGTkPUPjPGU:37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:0:79ZVrBehElVZh82fJdR18IJx06GkEVZTbwdHH4zb0S6VaGwdtLh1rvomm4ukBvUc8r/suTweG/SScsJairXNAg==\nHnFcSms8jzwngtVomTTnzudZx7SHUQY8sVE1y8yBmULk:37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:0:e/ai9E4G5CFB9Qi329e0ffYpZMgxj8mM4rviqIr2+UESA0UG86OuAAyHO11hYeyolZRiU8I7WdtNE98B1uZuBg==\nBMAVuMDcGhYAV4wA27DL1VXX2ZARZGJYaMwpf7DJFMYH:37qBxM4hLV2jfyYo2bNzAjkeLngLr2r7G2HpdpKieVxw:0:q4PCneYkcPH8AHEqEvqTtYQWslhlYO2B87aReuOl1uPczn5Q3VkZFAsU48ZTYryeyWp2nxdQojdFYhlAUNchAw==\nTransactions:\n"
}
        jsonschema.validate(json_sample, Block.schema)
        jsonschema.validate(json_sample, Current.schema)

    def test_block_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/100', handler)
            block = Block(None, 100)
            block.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await block.get(session)

        self.loop.run_until_complete(go())

    def test_current_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/', handler)
            current = Current(None)
            current.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await current.get(session)

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

    def test_hardship_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/fingerprint', handler)
            hardship = Hardship(None, "fingerprint")
            hardship.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await hardship.get(session)

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
        jsonschema.validate(json_sample, Membership.schema)

    def test_membership_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/pubkey', handler)
            membership = Membership(None, "pubkey")
            membership.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await membership.get(session)

        self.loop.run_until_complete(go())

    def test_schema_newcomers(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, Newcomers.schema)

    def test_newcomers_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/', handler)
            newcomers = Newcomers(None)
            newcomers.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await newcomers.get(session)

        self.loop.run_until_complete(go())

    def test_schema_certifications(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, Certifications.schema)

    def test_certifications_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/', handler)
            certs = Certifications(None)
            certs.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await certs.get(session)

        self.loop.run_until_complete(go())

    def test_schema_joiners(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, Joiners.schema)

    def test_joiners_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/', handler)
            joiners = Joiners(None)
            joiners.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await joiners.get(session)

        self.loop.run_until_complete(go())

    def test_schema_actives(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, Actives.schema)

    def test_actives_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/', handler)
            actives = Actives(None)
            actives.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await actives.get(session)

        self.loop.run_until_complete(go())

    def test_schema_leavers(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, Leavers.schema)

    def test_leavers_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/', handler)
            leavers = Leavers(None)
            leavers.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await leavers.get(session)

        self.loop.run_until_complete(go())

    def test_schema_ud(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, UD.schema)

    def test_ud_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/', handler)
            ud = UD(None)
            ud.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await ud.get(session)

        self.loop.run_until_complete(go())

    def test_schema_tx(self):
        json_sample = {
            "result": {
                "blocks": [223, 813]
            }
        }
        jsonschema.validate(json_sample, TX.schema)

    def test_tx_bad(self):
        async def handler(request):
            await request.read()
            return web.Response(body=b'{}', content_type='application/json')

        async def go():
            _, srv, url = await self.create_server('GET', '/', handler)
            tx = TX(None)
            tx.reverse_url = lambda scheme, path: url
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                with aiohttp.ClientSession() as session:
                    await tx.get(session)

        self.loop.run_until_complete(go())