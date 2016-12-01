import asyncio
import logging
from duniterpy.documents import BlockUID
from duniter_mock_server import Node, User

async def example(lp):
    node = await Node.start(4444, "testnet", "12356", "123456", lp)
    alice = User.create("testnet", "alice", "alicesalt", "alicepassword", BlockUID.empty())
    bob = User.create("testnet", "bob", "bobsalt", "bobpassword", BlockUID.empty())

    node.forge.push(alice.identity())
    node.forge.push(bob.identity())
    node.forge.push(alice.join(BlockUID.empty()))
    node.forge.push(bob.join(BlockUID.empty()))
    node.forge.push(alice.certify(bob, BlockUID.empty()))
    node.forge.push(bob.certify(alice, BlockUID.empty()))
    await node.forge.forge_block()
    node.forge.set_member(alice.key.pubkey, True)
    node.forge.set_member(bob.key.pubkey, True)
    await node.forge.forge_block()
    await node.forge.forge_block()
    node.forge.generate_dividend()
    await node.forge.forge_block()
    await asyncio.sleep(60)


logging.getLogger('duniter_mock_server').setLevel(logging.DEBUG)
lp = asyncio.get_event_loop()
lp.run_until_complete(example(lp))