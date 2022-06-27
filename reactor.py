import sys

from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

NODE_WSS = "wss://kusama-rpc.polkadot.io"

def subscription_handler(events_obj, update_nr, subscription_id):

    for event in events_obj:
        if event.value["module_id"] == "System" and event.value["event_id"] == "Remarked":
            print('System.Remarked event found with attributes:', event.value['attributes'])


##########################################
# EXECUTION STARTS HERE
##########################################


# Check that a seed phrase is entered

# if len(sys.argv) != 5:
#     print("Arguments:  amount_in_plancks filename seed_phrase_in_quotes")
#     sys.exit("Could not read arguments")

# print(sys.argv)
# asset_id = sys.argv[1]
# amount = sys.argv[2]
# filename = sys.argv[3]
# seed = sys.argv[4]

# Connect to node. By default this goes to Statemine, just change RPC endpoint to
# Statemint to use that instead.

print("Connecting to node...", end='')

substrate = SubstrateInterface(
    url=NODE_WSS,
    ss58_format=2,
    type_registry_preset='kusama'
)


result = substrate.query("System", "Events", [], subscription_handler=subscription_handler)
