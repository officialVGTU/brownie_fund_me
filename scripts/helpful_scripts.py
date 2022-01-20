from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3  # web3.py instance
from web3.middleware import geth_poa_middleware  # loads the middleware. This need for Geth --dev (POA)

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local']

DECIMALS = 8
STARTING_PRICE = 400000000000

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else: # for geth with testnet
        w3 = Web3(Web3.IPCProvider('/home/kali/geth/goerli/geth.ipc'))
        # inject the poa compatibility middleware to the innermost layer
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        # unlock account
        w3.geth.personal.unlock_account(w3.eth.accounts[0], config['pass']['unlock'])
        return w3.eth.accounts[0]

def deploy_mocks():
    if len(MockV3Aggregator) <= 0:
        print('> Deploying Mocks...')
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {'from': get_account()})
        print('+ Mocks Deployed!')
    else:
        print('> Mocks already Deployed...')

