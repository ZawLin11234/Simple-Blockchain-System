from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import time
import json
import hashlib

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-2a472627-10b0-45a4-86f8-37217787a200'
pnconfig.publish_key = 'pub-c-79d3cfa2-7414-40ab-8c1e-bb6313684616'
pnconfig.user_id = "Bob"

pubnub = PubNub(pnconfig)

transactions = [
    [3, 4, 5, 6], [4, 5, 6, 7], [6, 6, 7, 8], [6, 7, 8, 9], [7, 8, 9, 10],
    [8, 9, 10, 11], [9, 10, 11, 12], [10, 11, 12, 13], [11, 12, 13, 14],
    [12, 13, 14, 15], [13, 14, 15, 16]
]

def my_publish_callback(envelope, status):
    if not status.is_error():
        pass
    else:
        pass

class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass
        elif status.category == PNStatusCategory.PNConnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
    
    def message(self, pubnub, message):
        print(message.message)
        time.sleep(1)
        blkfile = open("memory.txt", "r")
        info = blkfile.read()
        counter = int(info) + 1
        blkfile.close()
        if counter == 1:
            nonce = 1000000000
            fr = open(str(counter - 1) + ".txt", "r")
            preblk = fr.read()
            fr.close()
            prehash = hashlib.sha256(preblk.encode()).hexdigest()
            condition = True
            while condition:
                blk = json.dumps({'Block number': counter, 'Creator': "Bob", 'Hash': prehash, 'Trasnsaction': transactions[counter - 1], 'Nonce': nonce}, sort_keys=True, indent=4, separators=(',', ': '))
                hashout = hashlib.sha256(blk.encode()).hexdigest()
                if int(hashout, 16) < 2**236:  # Check against the condition 2^236
                    condition = False
                else:
                    nonce += 1
            fw = open(str(counter) + ".txt", "w+")
            fw.write(blk)
            fw.close()
            fw = open("memory.txt", "w+")
            fw.write(str(counter))
            fw.close()
            print("Bob write file " + str(counter))
            pubnub.publish().channel('Channel-Alice').message(blk).sync()
        else:
            nonce = 1000000000
            fr2 = open(str(counter - 1) + ".txt", "r")
            data = fr2.read()
            fr2.close()
            hashval = json.loads(data)['Hash']
            fr2 = open(str(counter - 2) + ".txt", "r")
            blk = fr2.read()
            fr2.close()
            prehash = hashlib.sha256(blk.encode()).hexdigest()
            if int(hashval, 16) == int(prehash, 16):
                print(str(counter - 1) + ".txt" + " is correct")
                if counter < len(transactions) or counter == len(transactions):
                    fr = open(str(counter - 1) + ".txt", "r")
                    preblk = fr.read()
                    fr.close()
                    prehash = hashlib.sha256(preblk.encode()).hexdigest()
                    condition = True
                    while condition:
                        blk = json.dumps({'Block number': counter, 'Creator': "Bob", 'Hash': prehash, 'Trasnsaction': transactions[counter - 1], 'Nonce': nonce}, sort_keys=True, indent=4, separators=(',', ': '))
                        hashout = hashlib.sha256(blk.encode()).hexdigest()
                        if int(hashout, 16) < 2**236:  # Check against the condition 2^236
                            condition = False
                        else:
                            nonce += 1
                    fw = open(str(counter) + ".txt", "w+")
                    fw.write(blk)
                    fw.close()
                    fw = open("memory.txt", "w+")
                    fw.write(str(counter))
                    fw.close()
                    print("Bob write file " + str(counter))
                    pubnub.publish().channel('Channel-Alice').message(blk).sync()
                else:
                    print("Done!")
            else:
                print(str(counter - 1) + ".txt" + " is Not correct")

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('Channel-Bob').execute()

blk0 = json.dumps({'Block number': 0, 'Hash': "Genesis", 'Transaction': ""}, sort_keys=True, indent=4, separators=(',', ': '))

fw = open("0.txt", "w+")
fw.write(blk0)
fw.close()

fw = open("memory.txt", "w+")
fw.write("0")
fw.close()

#print("Bob should start first")
