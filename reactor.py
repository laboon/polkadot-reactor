import sys

from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

NODE_WSS = "wss://governance2-testnet.litentry.io"
# NODE_WSS = "wss://kusama-rpc.polkadot.io"

g_keypair = ""
g_substrate = ""

def vote():
    global g_keypair
    global g_substrate
    
    try:

        call = g_substrate.compose_call(
            call_module='System',
            call_function='remark',
            call_params={
                'remark': '0x1234'
            }
        )

        print("generating extrinsic...")
        extrinsic = g_substrate.create_signed_extrinsic(call=call, keypair=g_keypair, era={'period': 64})
        print("done!")
        
        print("submitting extrinsic...")
        receipt = g_substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        print("done!")
        
        print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))    

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

g_substrate = SubstrateInterface(
    url=NODE_WSS
)

# Generate keypair

print("Generating keypair...", end='')

g_keypair = Keypair.create_from_mnemonic(seed)

print(" done!")


result = g_substrate.query("System", "Events", [], subscription_handler=subscription_handler)
