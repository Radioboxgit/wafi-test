from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

user_a={
  "firstname": "User",
  "lastname": "A",
  "gender": "male",
  "balance": 0,
  "email": "usera@example.com",
}

user_b={
  "firstname": "User",
  "lastname": "B",
  "gender": "female",
  "balance": 0,
  "email": "userb@example.com",
}

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "welcome to my world"}


def test_user_a_onboard():
    "onboard User A"
    response = client.post("/users/onboard",json=user_a)
    assert response.status_code == 201
    assert response.json()['email'] == "usera@example.com"

def test_user_a_deposit():
    "User A deposits 10 Dollars"
    users=client.get("/users").json()[0]
    account_no=users["account_no"]
    response = client.post(f"/deposit?user_account_no={account_no}&amount=10" )
    assert response.status_code == 201
    assert response.json()['Balance'] == 10

def test_user_b_onboard():
    "onboard User B"
    response = client.post("/users/onboard",json=user_b)
    assert response.status_code == 201
    assert response.json()['email'] == "userb@example.com"

def test_user_b_deposit():
    "User B deposits 20 Dollars"
    userb= [a for a in client.get("/users").json() if a['email']=="userb@example.com"][0]
    account_no=userb["account_no"]
    response = client.post(f"/deposit?user_account_no={account_no}&amount=20" )
    assert response.status_code == 201
    assert response.json()['Balance'] == 20

def test_user_b_transfer():
    "User B transfers 15 Dollars to user A"
    usera= [a for a in client.get("/users").json() if a['email']=="usera@example.com"][0]
    userb= [a for a in client.get("/users").json() if a['email']=="userb@example.com"][0]
    account_no_user_a=usera["account_no"]
    account_no_user_b=userb["account_no"]
    response = client.post(f"/intra/transfer?account_no_from={account_no_user_b}&beneficiary_account={account_no_user_a}&amount=15" )
    assert response.status_code == 201
    assert response.json()['message'] == 'Transaction Successful'



def test_user_a_checks_balance():
    "User A checks his/her balance, the balance should be 25 dollars"
    usera= [a for a in client.get("/users").json() if a['email']=="usera@example.com"][0]
    user_a_account_no= usera['account_no']
    response=client.get(f"/user/balance?user_account_no={user_a_account_no}")
    assert response.status_code == 200
    assert response.json()['Balance'] == 25

def test_user_b_checks_balance():
    "User B checks his/her balance, the balance should be 5 dollars"
    userb= [a for a in client.get("/users").json() if a['email']=="userb@example.com"][0]
    user_b_account_no= userb['account_no']
    response=client.get(f"/user/balance?user_account_no={user_b_account_no}")
    assert response.status_code == 200
    assert response.json()['Balance'] == 5



def test_user_a_interbank_transfer():
    "User A transfers  25 Dollars to another banking institution"
    usera= [a for a in client.get("/users").json() if a['email']=="usera@example.com"][0]
    user_a_account_no=usera['account_no']
    response=client.post(f"/inter/transfer?account_no_from={user_a_account_no}&amount=25")
    assert response.status_code == 201
    assert response.json()['message'] == 'Transaction Successful'



def test_user_a_checks_balance_again():
    "User A finally checks his/her balance, the balance should now be 0 dollars"
    usera= [a for a in client.get("/users").json() if a['email']=="usera@example.com"][0]
    user_a_account_no= usera['account_no']
    response=client.get(f"/user/balance?user_account_no={user_a_account_no}")
    assert response.status_code == 200
    assert response.json()['Balance'] == 0

    