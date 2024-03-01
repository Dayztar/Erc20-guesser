from web3 import Web3
import time,concurrent.futures, requests, json
import random, time, concurrent.futures
from config import *


Funded = walletINFO

    
def recall_getBal(tokens):
    getBal(tokens)


def getBal(tokens):
    ct_address, contract_abi = Contract[str(tokens)]
   
    try:
        #contract_abi = abi
        address = Funded["address"]
        web3 = Web3(Web3.HTTPProvider(rpcLink)) 
        contract_addr = web3.to_checksum_address(ct_address)
        contractor = web3.eth.contract(contract_addr, abi=contract_abi)
        try:
            token_name = contractor.functions.symbol().call()
        except Exception as e:
            token_name = e
        try:
            bal = contractor.functions.balanceOf(address).call()
        except Exception as e:
            bal = 0

        print(f'{bal} {token_name}')
        
        Bal = str(bal)
        
        if Bal != '0':
            
            Funded.update({"balance": [Bal], "symbol": [token_name]})
            return True
    except Exception as e:
        time.sleep(20)
        print(e)
        recall_getBal(tokens)
    return False


def checkNative_balance(Url, Api, address):
    global with_balance
    try:
        connector = f"{Url}/api?module=account&action=balance&address={address}&apikey={Api}"
        req = requests.get(connector, timeout=3)
        bal = req.text
        bal = eval(bal)
        bal = bal['result']
        bal = int(bal)
        if bal > 0:
            walletINFO['balance': bal, 'symbol': _symbol]
            with_balance += 1
        print(f'{bal} {_symbol}')
    except:
        pass


def call_getBal(chainId):
    global network, _symbol, Contract, rpcLink
    print(chainId)
    
    try:
        address = walletINFO['address']
        network = chainId
        
        if network == "Ethereum":
            Contract = Ethereum_tokens
            _symbol = 'Eth'
            checkNative_balance(ethUrl, ethApi, address)
            rpcLink = ethereum_rpc
        
        elif network == "Bep20":
            Contract = Bep20_tokens
            _symbol = 'Bnb'
            checkNative_balance(bscUrl, bscApi, address)
            rpcLink = Bsc_rpc
            
        elif network == "polygon":
            Contract = POLYGON_tokens
            _symbol = "Matic"
            checkNative_balance(polygonUrl, polygonApi, address)
            rpcLink = POLYGON_RPC
            
        elif network == 'fantom':
            Contract = Fantom_tokens
            _symbol = 'FMT'
            checkNative_balance(fontamUrl, fantomApi, address)
            rpcLink = Fantom_rpc
            
        elif network == "arbitrum":
            Contract = Arb_tokens
            _symbol = 'Eth/Arb'
            checkNative_balance(arbitrumUrl, arbitrumApi, address)
            rpcLink = Arb_rpc
        
        Funded.update({"address": address})
        with concurrent.futures.ThreadPoolExecutor(max_workers=55) as executor:
            result = executor.map(getBal, Contract, timeout=3)
            for x in result:
                if x:
                    return True
    except Exception as e:
        print(e)
        