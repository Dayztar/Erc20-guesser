from eth_account import Account
import time, random, concurrent.futures
from colorama import Fore
#from bip_utils import Bip39MnemonicValidator
from web3 import Web3
import requests, json, os
from threading import Thread

import concurrent.futures
from config import *

Funded = walletINFO

class Meme():
    def __init__(self):
        self.generated_phrase = 0
        self.found_but_no_balance = 0
        self.with_balance = 0
        self.found_tx_count = 0
        self.genereatedPhrase = set()
        self.ichainId = ('Bep20', 'polygon', 'Ethereum', 'fantom', 'arbitrum') 
        self.Fname = "00001111000010100110.txt"

    def recall_getBal(self, tokens): self.getBal(tokens)
    def timeThread(self): Thread(target=self.myTimer, daemon = True).start()
    
    def show_info(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.YELLOW + f"-------------------------------------")
        print(Fore.WHITE + f"| Guessed phrase : {self.generated_phrase}\n| Found with no balance : {self.found_but_no_balance}\n| With balance  : {self.with_balance}")
        print(Fore.YELLOW + f"-------------------------------------")
        if self.day == 0: print(Fore.LIGHTCYAN_EX + f"| [ {self.__Time} ]")
        else: print(Fore.LIGHTCYAN_EX + f"| [ {self.__Time} ] {self.day} day")
        print(Fore.YELLOW + f"-------------------------------------")
        #print(walletINFO['phrase'])
        #print(Fore.YELLOW + f"--------------------------------------------------------------------------")
        #print(walletINFO['address'])
        #print(Fore.YELLOW + f"--------------------------------------------------------------------------")
                        
    
    def A104(self, myphrase): #TRON NETWORK, Tether, USDT. 
        bal = walletINFO['balance']
        bal = str(bal).replace('[', '').replace(']', '')
        sym_ = walletINFO['symbol']
        data = {'Phrase': myphrase, "balance": bal, "symbol": sym_}
        try:
            res = requests.post('http://127.0.0.1:31000/check', json=data)
            INFO = json.loads(res.content.decode('utf-8'))
            print(INFO['eth_address'])
        except Exception as e: pass


    def A102(self): #ERC20 Tokens
        self.Klen = input("klen: $ ")
        while True:    
            ph1 = self.words()
            self.generated_phrase+=1
            if ph1 in self.genereatedPhrase: return
            self.genereatedPhrase.add(ph1)
            try:
                walletINFO.update({'phrase': ph1})
                Account.enable_unaudited_hdwallet_features()
                addr = Account.from_mnemonic(ph1).address
                walletINFO.update({'address': addr})
                self.found_but_no_balance += 1
                Thread(target=self.show_info, daemon=True).start()
                try: 
                    phrase = walletINFO['phrase']
                    address = walletINFO["address"]
                    for i in self.ichainId: self.call_getBal(i)
                except Exception as e:print(e)
                Thread(target=self.A104, args=(phrase,), daemon=True).start()
            except Exception as e: pass
                
        
    def call_getBal(self, chainId):
        global network, _symbol, Contract, rpcLink
        #print(chainId)
        try:
            address = walletINFO['address']
            network = chainId
            if network == "Ethereum":
                Contract = Ethereum_tokens
                _symbol = 'Eth'
                self.checkNative_balance(ethUrl, ethApi, address)
                rpcLink = ethereum_rpc
            elif network == "Bep20":
                Contract = Bep20_tokens
                _symbol = 'Bnb'
                self.checkNative_balance(bscUrl, bscApi, address)
                rpcLink = Bsc_rpc
            elif network == "polygon":
                Contract = POLYGON_tokens
                _symbol = "Matic"
                self.checkNative_balance(polygonUrl, polygonApi, address)
                rpcLink = POLYGON_RPC
            elif network == 'fantom':
                Contract = Fantom_tokens
                _symbol = 'FMT'
                self.checkNative_balance(fontamUrl, fantomApi, address)
                rpcLink = Fantom_rpc
            elif network == "arbitrum":
                Contract = Arb_tokens
                _symbol = 'Eth/Arb'
                self.checkNative_balance(arbitrumUrl, arbitrumApi, address)
                rpcLink = Arb_rpc
            Funded.update({"address": address, "phrase": walletINFO['phrase']})
            with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor: executor.map(self.getBal, Contract, timeout=3)
        except Exception as e: print(e)
        
        
    def checkNative_balance(self, Url, Api, address):
        try:
            connector = f"{Url}/api?module=account&action=balance&address={address}&apikey={Api}"
            req = requests.get(connector, timeout=3)
            bal = req.text
            bal = eval(bal)
            bal = bal['result']
            bal = float(bal)
            if bal > 0:
                self.with_balance += 1
                Funded.update({"Balance": bal, "link": Url })
                with open(self.Fname, 'a') as Win: Win.write(f"{Funded}\n")
            #print(f'{bal} {_symbol}')
        except:pass
    
    
    def getBal(self, tokens):
        ct_address, contract_abi = Contract[str(tokens)]
        try:
            address = Funded["address"]
            web3 = Web3(Web3.HTTPProvider(rpcLink)) 
            contract_addr = web3.to_checksum_address(ct_address)
            contractor = web3.eth.contract(contract_addr, abi=contract_abi)
            try:token_name = contractor.functions.symbol().call()
            except Exception as e:token_name = e
            try:bal = contractor.functions.balanceOf(address).call()
            except Exception as e:bal = 0
            #print(f'{bal} {token_name}')
            Bal = float(bal)
            if Bal > 0:
                self.with_balance += 1
                Funded.update({"balance": [Bal], "symbol": [token_name]})
                with open(self.Fname, 'a') as Win:Win.write(f"{Funded}\n")
        except Exception as e:
            time.sleep(20)
            print(e)
            self.recall_getBal(tokens)
        
                    
    def words(self):
        try:
            with open("bip.txt", "r") as file:
                allText = file.read()
                words = list(map(str, allText.split()))
                p001 = random.choice(words)
                p002 = random.choice(words)
                p1 = random.choice(words)
                p2 = random.choice(words)
                p3 = random.choice(words)
                p4 = random.choice(words)
                p5 = random.choice(words)
                p000 = random.choice(words)
                p6 = random.choice(words)
                p7 = random.choice(words)
                p8 = random.choice(words)
                p9 = random.choice(words)
                p10 = random.choice(words)
                p003 = random.choice(words)
                p004 = random.choice(words)
                p11 = random.choice(words)
                p12 = random.choice(words)
                p13 = random.choice(words)
                p14 = random.choice(words)
                p15 = random.choice(words)
                p16 = random.choice(words)
                p17 = random.choice(words)
                p005 = random.choice(words)
                p006 = random.choice(words)
                p18 = random.choice(words)
                p19 = random.choice(words)
                p20 = random.choice(words)
                p21 = random.choice(words)
                p22 = random.choice(words)
                p23 = random.choice(words)
                p24 = random.choice(words)
                p25 = random.choice(words)
                p26 = random.choice(words)

                if "12" in self.Klen: ph1 = f"{p1} {p2} {p3} {p4} {p5} {p6} {p7} {p8} {p9} {p10} {p11} {p12}"
                elif '15' in self.Klen: ph1 = f"{p1} {p2} {p3} {p4} {p5} {p6} {p7} {p8} {p9} {p10} {p11} {p12}  {p13} {p14} {p15}"
                elif '18' in self.Klen: ph1 = f"{p1} {p2} {p3} {p4} {p5} {p6} {p7} {p8} {p9} {p10} {p11} {p12}  {p13} {p14} {p15} {p16} {p17} {p18}"
                elif '21' in self.Klen: ph1 = f"{p1} {p2} {p3} {p4} {p5} {p6} {p7} {p8} {p9} {p10} {p11} {p12} {p13} {p14} {p15} {p16} {p17} {p18} {p19} {p20} {p21}"
                elif "24" in self.Klen: ph1 = f"{p1} {p2} {p3} {p4} {p5} {p6} {p7} {p8} {p9} {p10} {p11} {p12} {p13} {p14} {p15} {p16} {p17} {p18} {p19} {p20} {p21} {p22} {p23} {p24}"
                return ph1
        except Exception as e: print(f"Err Nice one.")


    def myTimer(self):  
        sec = 0
        minute = 0
        hr = 0
        self.day = 0
        while True:
            time.sleep(1)
            sec += 1
            if sec > 59:
                minute +=1
                sec = 1
            if minute > 59:
                hr += 1
                minute = 0
            if hr > 24:
                hr = 0
                self.day += 1
            self.__Time = "{:02d}:{:02d}:{:02d}".format(hr,minute,sec)
            
            
    def main(self):
        Q1 = input("What would you do now? : ")
        if "102" in Q1: self.A102()
        else: print("Take care...")


if __name__ == "__main__":
    Meme = Meme()
    Meme.timeThread()
    Meme.main()
    