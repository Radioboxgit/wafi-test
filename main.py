from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import List
import random

fixed_digits = 10


app = FastAPI()

@app.get("/", tags=["WAFI GREETING"])
def root():
    return {"message": "welcome to my world"}


class UserIn(BaseModel):
    firstname: str
    lastname: str
    gender: str
    balance: float
    email: EmailStr


class UserDB(BaseModel):
    firstname: str
    lastname: str
    gender:str
    balance:float
    email: EmailStr
    account_no:str

users_db=[]  #users database

@app.get("/user/balance", tags=['Users'])
async def get_blance(user_account_no: str):
    message={}
    # check if the account exist
    beneficiary= [a for a in users_db if a['account_no']==user_account_no]
    if beneficiary:
        message['Balance'] =beneficiary[0]['balance'] 
        message['Account_no']=user_account_no
        return message
    else:
        return 'User not Found'


@app.get("/users",response_model=list[UserDB], tags=['Users'])
async def get_users():
    return users_db

@app.post("/users/onboard",status_code=201,response_model=UserDB, tags=['Users'])
async def onboard_user(user: UserIn):
    user_details= user.dict()
    user_details['account_no']= str(random.randrange(1111111111, 9999999999, fixed_digits))
    users_db.append(user_details)
    return user_details

@app.post("/deposit", status_code=201 ,tags=['Transactions'])
async def deposit_money(user_account_no: str, amount:float):
    message={'message':"Credit Alert"}
    # check if the account exist
    beneficiary= [a for a in users_db if a['account_no']==user_account_no]
    if beneficiary:
        try:
            index_db= users_db.index(beneficiary[0])
            beneficiary[0]['balance'] +=amount
            users_db[index_db]=beneficiary[0]
            message['Amount']=amount
            message['Balance']=beneficiary[0]['balance']
            message['Account No']=user_account_no
            return message
        except Exception as err:
            return "error occcured, Transaction was unsuccessful"
    else:
        return 'User not Found'



@app.post("/intra/transfer",status_code=201 ,tags=['Transactions'])
async def transfer(account_no_from:str, beneficiary_account:str, amount:float):
    # check if the balance of the initiator 
    initiator_account_details= [a for a in users_db if a['account_no'] == account_no_from]
    if initiator_account_details:
        initiator_index= users_db.index(initiator_account_details[0])
        if initiator_account_details[0]['balance'] >= amount:
            # get the beneficiary details and update 
            beneficiary_account_details=[a for a in users_db if a['account_no'] == beneficiary_account]
            if beneficiary_account_details:
                benefiary_index=users_db.index(beneficiary_account_details[0])
                #  deduct from the initiator
                initiator_account_details[0]['balance'] -=amount
                #  update the transaction in the database
                users_db[initiator_index]=initiator_account_details[0]
                # add to the beneficiary
                beneficiary_account_details[0]['balance'] +=amount
                users_db[benefiary_index]=beneficiary_account_details[0]
                return {'message':'Transaction Successful'}
            else:
                return "Beneficiary account number is incorrect"
        else:
            return " insufficient balance, can't complete the transaction"
    else:
        return "User Does Not Exist"




@app.post("/inter/transfer",status_code=201 ,tags=['Transactions'])
async def inter_transfer(account_no_from:str, amount:float):
    # check if the balance of the initiator 
    initiator_account_details= [a for a in users_db if a['account_no'] == account_no_from]
    if initiator_account_details:
        initiator_index= users_db.index(initiator_account_details[0])
        if initiator_account_details[0]['balance'] >= amount:
            #  deduct from the initiator
            initiator_account_details[0]['balance'] -=amount
            #  update the transaction in the database
            users_db[initiator_index]=initiator_account_details[0]
            # send to the beneficiary
            return {'message':'Transaction Successful'}
        else:
            return " insufficient balance, can't complete the transaction"
    else:
        return "User Does Not Exist"

