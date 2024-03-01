import random
from bit import Key
from colorama import Fore
c = 0
import concurrent.futures

def check(self):
    global c
    c +=1
    try:
        key1 = Key.from_hex(self) #length is 64
        k_wif = key1.to_wif()       #get private key
        #key1 = Key(self) #length is 52, check if private key is valid
        bal = float(key1.balance)
        if bal != 0:
            with open('btc_privatekey.txt', 'a') as BKs:
                BKs.write(Fore.GREEN + f"[{c}] Valid key : {self} : {key1.address} :{key1.balance}\n")
            #hx = key1.to_hex()
            #print(f"Valid private key : {self} : {key1.address} :{key1.balance}\n{hx}")
        elif bal == 0:
            print(Fore.BLACK + f"[{c}] Address: {key1.address}\nBalance: {key1.balance}\nPrivate Key: {k_wif}")
        
    except Exception as e:
        #print(e)
        print(Fore.MAGENTA+ f'[{c}] {e} invalid private key : {self}')


def words():
    numbs = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','1','2','3','4','5','6','7','8','9','0', 'a','b','c','d','e','f']
    case1 = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
    INT = ['4','6','6','7','8','8','9','9','3','2','2','2','2','5','4','4','1','1','1','5','8','9','1','5','0','6','1','7','2','0','3','6','6','4','2','9','8','3','4','0','4','2','9','2','6','4','4','4','7','0','2','6','6','3','9','9','4','3','6','4','9','8','7','5','0','7','1','5','7','8','4','4','6','9','1','8','7']
    random.shuffle(numbs)
    F = str(numbs).strip()
    F = F.replace("'", '', 150).replace(',', '', 99).replace('[','').replace(']','').replace(' ',"",150)
    check(F)


while True:
    #with concurrent.futures.ThreadPoolExecutor(max_workers=61) as executor:
    #    future = executor.submit(words)
    words()   
   