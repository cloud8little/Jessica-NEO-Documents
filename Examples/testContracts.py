import requests
import json
import base64
import urllib
import time

headers={'content-type': 'application/json'}
endpoint = "http://localhost:10332"

policy_contract = "0xcc5e4edd9f5f8dba8bb65734541df7a1c081c67b"
contractmangement_contract = "0xfffdc93764dbaddd97c48f252a53ea4643faa3fd"
committee_address = "0x411b6a1c4771c3e906425331388fc981401dc4a1"   # 7 CN   4 CN NYjarRnRtMDy1SQqd4k5pGpkjdwjQT4sbH

def setExecFee(execFeeFactor):
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [policy_contract,"setExecFeeFactor",[{"type":"Integer","value":execFeeFactor} ],[
                {	"account":committee_address,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
            }
    responseData=sendRequest(data)
    return responseData["result"]

def sendRawTx(rawtx):
    data = {
        "jsonrpc": "2.0",
        "method": "sendrawtransaction",
        "params": [rawtx],
        "id": 1
        }
    responseData = sendRequest(data)
    return responseData["result"]

def getapplicationlog(txid):
    data = {
        "jsonrpc": "2.0",
        "method": "getapplicationlog",
        "params": [txid],
        "id": 1
        }
    responseData = sendRequest(data)
    return responseData["result"]    

def openwallet(walletname, password):
    data = {
        "jsonrpc": "2.0",
        "method": "openwallet",
        "params": [walletname,password],
        "id": 1
    }
    response = requests.post(endpoint, data = json.dumps(data), headers = headers, timeout=10)
    responseData=response.json()
    return responseData["result"]

def sendonegas():
    data = {
        "jsonrpc": "2.0",
        "method": "sendtoaddress",
        "params": ["0xd2a4cff31913016155e38e474a2c06d08be276cf", "NXV7ZhHiyM1aHXwpVsRZC6BwNFP2jghXAq", 100000000],
        "id": 1
    } 
    response = requests.post(endpoint, data = json.dumps(data), headers = headers, timeout=10)
    responseData=response.json()
    return responseData["result"]

def testsetExecFee():
    assert(openwallet("1.json","1") == True)
    rawtx = setExecFee(1)["tx"]
    print(rawtx)
    print("txid: " + sendRawTx(rawtx)["hash"])

flm_contract = "0xb110e944d4b86c30bf932a9d69c8ac6b9e4eaee9"   #"0x04d35b3511864375eb0127c850637dd4e11f8ed0"
normal1_address = "NXV7ZhHiyM1aHXwpVsRZC6BwNFP2jghXAq"
author = minter = "0x71a87191aef3fcf5e4441d791ded67ebab1aee7e"
receiver = "0xd6c3faaa54321494e550ae3ed7bfb8a0fe728e97"
weth_manager_address = "NfqRaYgdFrR4gwxyiTZR56YyAv6ULPACyq"
flm_nefpath = r"D:\Github\personal\yinwei\flamingo-contract-staking-n3\FLM\bin\sc\FLM.nef"
flm_manifestpath = r"D:\Github\personal\yinwei\flamingo-contract-staking-n3\FLM\bin\sc\FLM.manifest.json"

weth_nefpath = r"D:\SmartContract\WETH\bin\sc\WETH.nef"
weth_manifestpath = r"D:\SmartContract\WETH\bin\sc\WETH.manifest.json"

stake_nefpath = r"D:\Github\personal\yinwei\flamingo-contract-staking-n3\Staking\bin\sc\Staking.nef"
stake_manifestpath = r"D:\Github\personal\yinwei\flamingo-contract-staking-n3\Staking\bin\sc\Staking.manifest.json"

# mint 1 flm
def mintFLM():
    data ={
            "jsonrpc": "2.0",
            "method": "invokefunction",
            "params": [flm_contract,"mint",[{"type":"Hash160","value":minter},
                {"type":"Hash160","value":receiver},
                            {"type":"ByteArray","value":"AAAAQOrtdEbQnCyfDA=="}],[
                    {	"account":normal1_address,
                        "scopes":"Global"
                    }
                ]
            ],
            "id": 1
        }
    response = requests.post(endpoint, data = json.dumps(data), headers = headers, timeout=10)
    responseData=response.json()
    return responseData["result"]

def updateFLMcontract():
    with open(r'D:\Github\personal\yinwei\flamingo-contract-staking-n3\FLM\bin\sc\FLM.nef','rb') as file_byte:
        file_hex = file_byte.read()
        nefbytearray = base64.b64encode(file_hex).decode()

    with open(r'D:\Github\personal\yinwei\flamingo-contract-staking-n3\FLM\bin\sc\FLM.manifest.json','rb') as file_byte:
        file_hex = file_byte.read()
        manifestbytearray = base64.b64encode(file_hex).decode()
    print(nefbytearray)
    print(manifestbytearray)
    data ={
            "jsonrpc": "2.0",
            "method": "invokefunction",
            "params": [flm_contract,"update",[{"type":"ByteArray","value":nefbytearray},
                {"type":"ByteArray","value":manifestbytearray}, {"type":"String","value":"update"}],[
                    {	
                        "account":normal1_address,
                        "scopes":"Global"
                    }
                ]
            ],
            "id": 1
        }
    responseData=sendRequest(data)
    return responseData["result"]

def updateStakecontract():
    with open(stake_nefpath,'rb') as file_byte:
        file_hex = file_byte.read()
        nefbytearray = base64.b64encode(file_hex).decode()

    with open(stake_manifestpath,'rb') as file_byte:
        file_hex = file_byte.read()
        manifestbytearray = base64.b64encode(file_hex).decode()
    data ={
            "jsonrpc": "2.0",
            "method": "invokefunction",
            "params": [stake_contract,"update",[{"type":"ByteArray","value":nefbytearray},
                {"type":"ByteArray","value":manifestbytearray}, {"type":"String","value":"update"}],[
                    {	
                        "account":normal1_address,
                        "scopes":"Global"
                    }
                ]
            ],
            "id": 1
        }
    responseData=sendRequest(data)
    return responseData["result"]
    

def deployContract(nef=weth_nefpath, manifest = weth_manifestpath, deployer=normal1_address):
    with open(nef,'rb') as file_byte:
        file_hex = file_byte.read()
        nefbytearray = base64.b64encode(file_hex).decode()

    with open(manifest,'rb') as file_byte:
        file_hex = file_byte.read()
        manifestbytearray = base64.b64encode(file_hex).decode()
    print(nefbytearray)
    print(manifestbytearray)
    data ={
            "jsonrpc": "2.0",
            "method": "invokefunction",
            "params": [contractmangement_contract,"deploy",[{"type":"ByteArray","value":nefbytearray},
                {"type":"ByteArray","value":manifestbytearray}],[
                    {	
                        "account":deployer,
                        "scopes":"Global"
                    }
                ]
            ],
            "id": 1
        }
    responseData=sendRequest(data)
    return responseData["result"]

stake_contract = "0xb86c0ac1ff5df58a10251af46e64b57944bd7cb9" #"0xf8ffef6af5eccbb9526c3baf8ee702e69c036465"
#weth_contract = "0x3af100c91d8626d16b75f80b7c218d979551bf73"
weth_contract = "0xe80294d573527905962637763af9adeee7e31aa8"
gas_contract = "0xd2a4cff31913016155e38e474a2c06d08be276cf"
jessica1_account = "0x935ce5f249ac2771a3e9ec4b89934d6ecba171f7"
zero_account = "0x9e4fbbaa7e9cf5d997327e63ef1359da263c7b73"

def setFlmAddress():
    data = {
            "jsonrpc": "2.0",
            "method": "invokefunction",
            "params": [stake_contract,"setFLMAddress",[{"type":"Hash160","value":flm_contract},
                {"type":"Hash160","value":author} ],[
                    {	"account":normal1_address,
                        "scopes":"Global"
                    }
                ]
            ],
            "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]   

def addStakeAuthor(_author = author):
    data = {
            "jsonrpc": "2.0",
            "method": "invokefunction",
            "params": [stake_contract,"addAuthor",[ {"type":"Hash160","value":_author} ],[
                    {	"account":normal1_address,
                        "scopes":"Global"
                    }
                ]
            ],
            "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]   

def addFLMAuthor(_author = author):
    data = {
            "jsonrpc": "2.0",
            "method": "invokefunction",
            "params": [flm_contract,"addAuthor",[ {"type":"Hash160","value":_author} ],[
                    {	"account":normal1_address,
                        "scopes":"Global"
                    }
                ]
            ],
            "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]      

def addAsset(_asset = weth_contract):
    data = {
            "jsonrpc": "2.0",
            "method": "invokefunction",
            "params": [stake_contract,"addAsset",[{"type":"Hash160","value":_asset}, {"type":"Hash160","value":author} ],[
                    {	"account":normal1_address,
                        "scopes":"Global"
                    }
                ]
            ],
            "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]   

wethmanager = "0x88af1c96df69f155a3f2facf751cba1eb47786da"

def transfer100weth(_receiver=author):
    data = {
         "jsonrpc": "2.0",
            "method": "invokefunction",
            "params": [weth_contract,"transfer",[{"type":"Hash160","value":wethmanager}, {"type":"Hash160","value":_receiver}, {"type":"Integer","value":1}, {"type":"String","value":"test"} ],[
                    {	"account":wethmanager,
                        "scopes":"Global"
                    }
                ]
            ],
            "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]     

def getCurrentShareAmount():
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [stake_contract,"getCurrentShareAmount",[{"type":"Hash160","value":weth_contract}],[
                {	"account":normal1_address,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]

def setCurrentShareAmount():
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [stake_contract,"setCurrentShareAmount",[{"type":"Hash160","value":weth_contract},{"type":"Integer","value":1000000},{"type":"Hash160","value":author}],[
                {	"account":normal1_address,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]

def transferwethforstake():
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [weth_contract,"transfer",[{"type":"Hash160","value":author},{"type":"Hash160","value":stake_contract},{"type":"Integer","value":1000000},{"type":"String","value":"test"}],[
                {	"account":normal1_address,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]


def transferwethfromstake():
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [weth_contract,"transfer",[{"type":"Hash160","value":stake_contract},{"type":"Hash160","value":jessica1_account},{"type":"Integer","value":1000000},{"type":"String","value":"test"}],[
                {	"account":jessica1_account,
                    "scopes":"Global"
                },
                 {	"account":stake_contract,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]

def transferflm():
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [flm_contract,"transfer",[{"type":"Hash160","value":author},{"type":"Hash160","value":jessica1_account},{"type":"Integer","value":799735830008},{"type":"String","value":"test"}],[
                {	"account":author,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]
    

# assetId
def getuintProfit():
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [stake_contract,"getUintProfit",[{"type":"Hash160","value":weth_contract}],[
                {	"account":normal1_address,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]

# UInt160 fromAddress, BigInteger amount, UInt160 asset
# TODO 
def refund(amount):
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [stake_contract,"refund",[{"type":"Hash160","value":author},{"type":"Integer","value":amount},{"type":"Hash160","value":weth_contract}],[
                {	"account":normal1_address,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]

# UInt160 fromAddress, UInt160 asset
def claimFLM():
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [stake_contract,"claimFLM",[{"type":"Hash160","value":author},{"type":"Hash160","value":weth_contract}],[
                {	"account":normal1_address,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]  

# UInt160 fromAddress, UInt160 asset
def checkFLM():
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [stake_contract,"checkFLM",[{"type":"Hash160","value":author},{"type":"Hash160","value":weth_contract}],[
                {	"account":normal1_address,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]    

# UInt160 fromAddress, UInt160 asset
# 查看某个账户质押的资产是多少
def getStakingAmount():
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [stake_contract,"getStakingAmount",[{"type":"Hash160","value":author},{"type":"Hash160","value":weth_contract}],[
                {	"account":normal1_address,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]

# assetId  资产总共质押的数目
def getCurrentTotalAmount():
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [stake_contract,"getCurrentTotalAmount", [{"type":"Hash160","value":weth_contract}],[
                {	"account":normal1_address,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }
    responseData=sendRequest(data)
    return responseData["result"]

def upgradestart():
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [stake_contract,"upgradeStart", [],[
                {	"account":normal1_address,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }   
    responseData=sendRequest(data)
    return responseData["result"]

def getcurrenttimestamp():
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [stake_contract,"getCurrentTimestamp", [],[
                {	"account":normal1_address,
                    "scopes":"Global"
                }
            ]
        ],
        "id": 1
    }   
    responseData=sendRequest(data)
    return responseData["result"]    

def sendRequest(data):
    response = requests.post(endpoint, data = json.dumps(data), headers = headers, timeout=10)
    responseData=response.json()
    print(json.dumps(responseData,indent=4))
    return responseData

def send1kgas(receiver):
    data = {
        "jsonrpc": "2.0",
        "method": "sendfrom",
        "params": [gas_contract,"NYjarRnRtMDy1SQqd4k5pGpkjdwjQT4sbH", receiver, 1000 * 1e8],
        "id": 1
    }   
    responseData=sendRequest(data)
    return responseData["result"]

def s1_sendgas2normalandwethmanager():
    openwallet("1.json","1")
    send1kgas(author)
    time.sleep(1)
    send1kgas(wethmanager)
    time.sleep(1)

def s2_deploycontract():
    testdeployflmcontract()
    testdeploystakecontract()
    testdeploywethcontract()

def testFLM():
    openwallet("normal1.json","1")
    rawtx = mintFLM()["tx"]
    print("txid: " + sendRawTx(rawtx)["hash"])

def testupdateFLM():
    openwallet("normal1.json","1")
    rawtx = updateFLMcontract()["tx"]
    print("txid: " + sendRawTx(rawtx)["hash"])

def testupdateStake():
    openwallet("normal1.json","1")
    rawtx = updateStakecontract()["tx"]
    print("txid: " + sendRawTx(rawtx)["hash"])       

def testAddStakeAuthor():
    openwallet("normal1.json","1")
    rawtx = addStakeAuthor()["tx"]
    print("add author")
    print("txid: " + sendRawTx(rawtx)["hash"])

def testAddStakeAsStakeAuthor():
    openwallet("normal1.json","1")
    rawtx = addStakeAuthor(stake_contract)["tx"] 
    print("txid: " + sendRawTx(rawtx)["hash"])

def testAddFLMAuthor():
    openwallet("normal1.json","1")
    rawtx = addFLMAuthor()["tx"]
    print("add author")
    print("txid: " + sendRawTx(rawtx)["hash"])

def testAddStakeAsFLMAuthor():
    openwallet("normal1.json","1")
    rawtx = addFLMAuthor(stake_contract)["tx"] 
    print("txid: " + sendRawTx(rawtx)["hash"])    

def testsetFLMAddress():
    openwallet("normal1.json","1")
    rawtx = setFlmAddress()["tx"]
    print("set flm address")
    print("txid: " + sendRawTx(rawtx)["hash"])

def testaddAsset():
    rawtx = addAsset()["tx"]
    print("add Asset")
    print("txid: " + sendRawTx(rawtx)["hash"])      

def testtransferweth(_receiver=author):
    openwallet("wethmanager.json","1")
    rawtx = transfer100weth(_receiver)["tx"]
    print("transfer 100 weth to normal1")
    print("txid: " + sendRawTx(rawtx)["hash"])

def testgetCurrentShare():
    openwallet("normal1.json","1")
    getCurrentShareAmount()

def testsetCurrentShare():
    openwallet("normal1.json","1")
    rawtx = setCurrentShareAmount()["tx"]
    sendRawTx(rawtx)

def teststakeweth():
    openwallet("normal1.json","1")
    rawtx = transferwethforstake()["tx"]
    sendRawTx(rawtx)   

def testgetuintprofit():
    getuintProfit()

def testrefund():
    openwallet("normal1.json","1")
    rawtx = refund(1000000)["tx"]
    sendRawTx(rawtx)

def testclaimflm():
    openwallet("normal1.json","1")
    rawtx = claimFLM()["tx"]
    sendRawTx(rawtx)

def testcheckflm():
    checkFLM()

def testgetStakingAmount():
    getStakingAmount()     

def testgetCurrentTotalAmount():
    getCurrentTotalAmount()

def testupgradestart():
    openwallet("normal1.json","1")
    rawtx = upgradestart()["tx"]
    sendRawTx(rawtx)

def testgetcurrenttimestamp():
    getcurrenttimestamp()

def testwithdrawfromstakecontract():
    openwallet("jessica1.json","1")
    rawtx = transferwethfromstake()["tx"]
    sendRawTx(rawtx)

def testaddgasasset():
    openwallet("normal1.json","1")
    rawtx = addAsset(gas_contract)["tx"]
    sendRawTx(rawtx)

def testsetmaxfee():
    openwallet("1.json","1")
    rawtx = setExecFee(100)["tx"]
    sendRawTx(rawtx)

def testdeploywethcontract():
    openwallet("wethmanager.json","1")
    rawtx = deployContract(weth_nefpath, weth_manifestpath, weth_manager_address)["tx"]
    result = sendRawTx(rawtx)
    global weth_contract
    weth_contract = getcontracthash(result["hash"])
    print(weth_contract)

def testdeploystakecontract():
    openwallet("normal1.json","1")
    rawtx = deployContract(stake_nefpath, stake_manifestpath, author)["tx"]
    result = sendRawTx(rawtx)
    global stake_contract
    stake_contract = getcontracthash(result["hash"])
    print(stake_contract)

def testdeployflmcontract():
    openwallet("normal1.json","1")
    rawtx = deployContract(flm_nefpath, flm_manifestpath, author)["tx"]
    result = sendRawTx(rawtx)
    global flm_contract
    flm_contract = getcontracthash(result["hash"])
    print(flm_contract)

def getcontracthash(txid):
    result = getapplicationlog(txid)
    base64data = result["executions"][0]["notifications"][-1]["state"]["value"][0]["value"]
    return toBigEndian(base64.b64decode(base64data).hex())

def testtransferflm():
    openwallet("normal1.json","1")
    rawtx = transferflm()["tx"]
    sendRawTx(rawtx) 

def toBigEndian(str):
    loop = len(str) - 2
    result = ""
    while(loop >=0):
        result += str[loop] + (str[loop+1])
        loop -= 2
    return "0x" + result                   

while(1):
    print("input command to start")
    a = input()
    if(a == "addflmauthor"):
        testAddFLMAuthor()
    elif(a == "addstakeauthor"):
        testAddStakeAuthor()    
    elif(a == "setflmaddress"):
        testsetFLMAddress()  
    elif(a == "addweth"):
        testaddAsset()
    elif(a == "transferweth"):
        testtransferweth() 
    elif(a == "getcurrentshare"):
        testgetCurrentShare()
    elif(a == "setcurrentshare"):
        testsetCurrentShare()
    elif(a == "stakeweth"):
        teststakeweth()
    elif(a == "getassetprofit"):
        testgetuintprofit()
    elif(a == "refund"):
        testrefund()
    elif(a == "claimflm"):
        testclaimflm()
    elif(a == "checkflm"):
        testcheckflm()
    elif(a == "getstakingamount"):
        testgetStakingAmount() 
    elif(a == "gettotalamount"):
        testgetCurrentTotalAmount()
    # update contract function
    elif(a == "upgradestart"):
        testupgradestart()
    elif(a == "updateflm"):
        testupdateFLM()
    elif(a == "updatestake"):
        testupdateStake()    
    elif(a == "addstaketoauthor"):
        testAddStakeAsFLMAuthor()
    elif(a == "gettime"):
        testgetcurrenttimestamp()
    elif(a == "withdrawfromstake"):
        testwithdrawfromstakecontract() 
    elif(a == "addgastowhitelist"):
        testaddgasasset()
    elif(a == "setmaxfeefactor"):
        testsetmaxfee()
    # deploy function
    elif(a == "deployweth"):
        print("you are going to deploy weth contract, press yes to continue")
        bb = input()
        if(bb == "yes"):
            testdeploywethcontract()
    elif(a == "deployflm"):
        print("you are going to deploy flm contract, press yes to continue")
        bb = input()
        if(bb == "yes"):
            testdeployflmcontract()
    elif(a == "deploystake"):
        print("you are going to deploy stake contract, press yes to continue")
        bb = input()
        if(bb == "yes"):
            testdeploystakecontract()
    elif(a == "transferflm"):
        testtransferflm()
    elif(a == "init"):
        s1_sendgas2normalandwethmanager()
        s2_deploycontract()
    elif(a == "getcontracthash"):
        print("stake: " + stake_contract)
        print("flm: " + flm_contract)
        print("weth: " + weth_contract)               


