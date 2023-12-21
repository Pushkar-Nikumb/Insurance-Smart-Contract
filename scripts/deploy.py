from brownie import network, accounts, config
from generated.InsuranceContract import InsuranceContract
from dotenv import load_dotenv
import os

NETWORK = "polygon-test"
insurance = InsuranceContract(contract_address=None)
deployed_insurance = InsuranceContract(contract_address="0xf0d1522e1b0D7C5024975C54eC76366c4D1f3A18")
IPFS_HASH = "QmfZ95SEMNiRsBTUjcPJAns55An7MDTUtGw57CLZn7kfJu"
def main(): #Conrtact deployment Code -> deployed on Polygon-test Network
    network.disconnect()
    network.connect(NETWORK)

    load_dotenv()
    private_key = os.getenv("CONTRACT_OWNER_PRIVATE_KEY")

    if private_key:
        print("Using private key from .env...")
        my_account = accounts.add(private_key)
        # Uncomment the next line if you want to print the account address
        # print("My Account:", my_account)
        print(my_account)
        # Deploy the contract using the specified account
        deployed_contract = insurance.deploy({'from': my_account})
        print("Contract Address:", deployed_contract.contract_address)

def submitDocument():       #IPFS_Hash,sender_address-> parameters to be pass to this function, IPFS HASh is generated first and then this transaction is initiated
    network.disconnect()
    network.connect(NETWORK)
    #tHIS IS Private key here, actually we have to do this transaction from Metamask side! But for Now we are testing this functionality
    private_key = "25ee647e7907670add6b8130f758adfc7b9a33bf2a9a0da6cdfde5c66e7c8abc"

    my_account = accounts.add(private_key)
        # Uncomment the next line if you want to print the account address
        # print("My Account:", my_account)
    print(my_account)
    document_Submitted = deployed_insurance.submit_document(document_hash = IPFS_HASH,transaction_config = {'from' : my_account})
    print(document_Submitted.events)

def grantAccess(): #parameters ->insurance_firm address, intended_client address
    network.disconnect()
    network.connect(NETWORK)
    #tHIS IS Private key here, actually we have to do this transaction from Metamask side! But for Now we are testing this functionality
    private_key = "25ee647e7907670add6b8130f758adfc7b9a33bf2a9a0da6cdfde5c66e7c8abc"

    my_account = accounts.add(private_key)
        # Uncomment the next line if you want to print the account address
        # print("My Account:", my_account)
    print(my_account)
    #This is the insurance company giving access to a particular client to access Claimed Insurance Policy Document
    insurance_firm = "0xB36D77D2d468D5af1972997D001AcDb7b140dF76"
    intended_client = "0x2076F5F77B6b502358A34E1fCfedE3C871C4d1f9"

    access_granted = deployed_insurance.grant_access(insurance_company = insurance_firm, client_address = intended_client,transaction_config = {'from' : my_account})

def setAccessControl(): # parameters -> address InsuranceFirm, uint256 index, address user, bool hasAccess
    network.disconnect()
    network.connect(NETWORK)

    load_dotenv()
    private_key = os.getenv("CONTRACT_OWNER_PRIVATE_KEY")
    insurance_firm = "0xB36D77D2d468D5af1972997D001AcDb7b140dF76"
    intended_client = "0x2076F5F77B6b502358A34E1fCfedE3C871C4d1f9"

    #Function called by Contract Owner, i.e. Insurance Broker oNLY!
    if private_key:
        print("Using private key from .env...")
        my_account = accounts.add(private_key)
        # Uncomment the next line if you want to print the account address
        # print("My Account:", my_account)
        print(my_account)
        # Deploy the contract using the specified account
        deployed_contract = deployed_insurance.set_access_control(
        insurance_firm = insurance_firm,
        index= 0,#this indexed is fetched using a simple call function, we will store index in our database!
        user= intended_client,
        has_access= True,
        transaction_config = {'from' : my_account})


def accessDocument(): #parameters to be given to function -> address InsuranceFirmAddress, uint256 index, string memory reason
    network.disconnect()
    network.connect(NETWORK)

    private_key = "66c20a86be43ad13fe0535da3a8d863e8fee9940e0aad92fa7670c3de2804904"
    my_account = accounts.add(private_key)

    print(my_account)
    insurance_firm = "0xB36D77D2d468D5af1972997D001AcDb7b140dF76"
    #THis docuement will be accessed only by the intended client whose claim is approved by the insurance Company/firm
    documentAccessed = deployed_insurance.access_document(
        insurance_firm_address =  insurance_firm,
        index= 0,
        reason= "View Claimed Insurance Policy",
        transaction_config = {'from' :my_account})
    #emitted Event
    print(documentAccessed.events[0])
