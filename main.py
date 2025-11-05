from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/afirme/dev/customers_api/v3/customers")
async def get_customers(searchType: str = "", informationSearch: str = ""):
    dummy_response = {
        "customersList": [
            {
                "clientId": 5887240,
                "branchId": 880,
                "branchName": "BANCO DIGITAL BILLU",
                "statusCode": "2",
                "personType": "PF",
                "companyName": "ABRAHAM REIS RODRI",
                "lastNameFather": "REIS",
                "lastNameMother": "RODRI",
                "birthDate": "06/10/1982",
                "nationalityCode": "MEX",
                "nationalityName": "MEXICO",
                "gender": "M",
                "civilStatus": "1",
                "curp": "LORP821006HNLY2033",
                "countryName": "MEXICO",
                "countryCode": "MEX",
                "stateCode": "NL",
                "stateId": 19,
                "cityName": "APODACA",
                "cityId": 19006,
                "street": "GALICIA 729 7777",
                "zipcode": "66612",
                "email": "0BILLUYO2001@AFIRME.COM",
                "name": "ABRAHAM",
                "registrationDate": "18/03/2025",
                "companyNumber": "000000000"
            }
        ],
        "responseList": [
            {
                "codeResponse": "0000",
                "replyMessage": "OK"
            }
        ]
    }

    return JSONResponse(content=dummy_response)
