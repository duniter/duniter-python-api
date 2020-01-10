import pytest

from duniterpy.helpers.ws2p import generate_ws2p_endpoint
from duniterpy.api.endpoint import WS2PEndpoint, SecuredBMAEndpoint, BMAEndpoint


async def peering_no_ws2p(self):
    return {
        "version": 10,
        "currency": "g1-test",
        "status": "UP",
        "first_down": None,
        "last_try": None,
        "pubkey": "238pNfpkNs4TdRgt6NnJ5Q72CDZbgNqm4cJo4nCP3BxC",
        "block": "500438-000122A8BCE2072958D18E1B76D0EA0308C072656926E144BA50119CDE0496F6",
        "signature": "98uQR2u0Nm2fJ9CRdE46oktotKYhNQhphQARhivUselUyYJldqoLRNOM6TANoolTuSmHubAtjT/YYKgMMBVRDg==",
        "endpoints": ["BASIC_MERKLED_API g1-test.duniter.org 91.121.157.13 10900"],
    }


async def peering_ws2p(self):
    return {
        "version": 10,
        "currency": "g1-test",
        "status": "UP",
        "first_down": None,
        "last_try": None,
        "pubkey": "82jMJtb8chXrpHMAMcreVdyPJK7LtWjEeRqkPw4eSEVP",
        "block": "500488-0001980F9AD959F86210BF872FE44A31ACF1596EB6D2D444CC9FD30EFE423541",
        "signature": "RbqCnXhPoq714z9gJFiJ7b8VE9sOQt1oWsDYIvAVoxhklDCYptFmGrrofR76dj9pThcaPDnwt93Is79nQ91ICg==",
        "endpoints": [
            "BASIC_MERKLED_API g1-test.duniter.org 443",
            "WS2P 96675302 g1-test.duniter.org 443 ws2p",
        ],
    }


@pytest.mark.parametrize(
    "bma_endpoint",
    [
        "BASIC_MERKLED_API g1-test.duniter.org 443",
        "BMAS g1-test.duniter.org 443",
        BMAEndpoint.from_inline("BASIC_MERKLED_API g1-test.duniter.org 443"),
        SecuredBMAEndpoint.from_inline("BMAS g1-test.duniter.org 443"),
    ],
)
@pytest.mark.asyncio
async def test_generate_ws2p_endpoint(bma_endpoint, monkeypatch):
    monkeypatch.setattr("duniterpy.api.bma.network.peering", peering_ws2p)
    reference_ep = WS2PEndpoint.from_inline(
        "WS2P 96675302 g1-test.duniter.org 443 ws2p"
    )
    generated_ep = await generate_ws2p_endpoint(bma_endpoint)
    assert reference_ep == generated_ep


@pytest.mark.parametrize("bma_endpoint", ["BMAS g1-test.duniter.org 443"])
@pytest.mark.asyncio
async def test_generate_ws2p_endpoint_no_ws2p(bma_endpoint, monkeypatch):
    monkeypatch.setattr("duniterpy.api.bma.network.peering", peering_no_ws2p)
    with pytest.raises(ValueError) as excinfo:
        await generate_ws2p_endpoint(bma_endpoint)
    assert "No WS2P endpoint found" in str(excinfo.value)
