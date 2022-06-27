import sys

from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

NODE_WSS = "wss://kusama-rpc.polkadot.io"

g_keypair = ""

def vote():
    global g_keypair
    print("voting no!")

def subscription_handler(events_obj, update_nr, subscription_id):

    for event in events_obj:
        if event.value["module_id"] == "System" and event.value["event_id"] == "Remarked":
            print('System.Remarked event found with attributes:', event.value['attributes'])
            vote()


##########################################
# EXECUTION STARTS HERE
##########################################


# Check that a seed phrase is entered

if len(sys.argv) != 2:
    print("Arguments: seed_phrase_in_quotes")
    sys.exit("Could not read arguments")

print(sys.argv)
seed = sys.argv[1]

# Connect to node. 

print("Connecting to node...", end='')

substrate = SubstrateInterface(
    url=NODE_WSS,
    ss58_format=2,
    type_registry_preset='kusama'
)

# Generate keypair

print("Generating keypair...", end='')

g_keypair = Keypair.create_from_mnemonic(seed)

print(" done!")


result = substrate.query("System", "Events", [], subscription_handler=subscription_handler)
