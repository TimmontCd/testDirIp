from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Lista simulada de clientes con todos los campos
clientes = [
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
    },
    {
        "clientId": 5887241,
        "branchId": 881,
        "branchName": "BANCO DIGITAL BILLU",
        "statusCode": "1",
        "personType": "PF",
        "companyName": "ABRAHAM MARTINEZ LOPEZ",
        "lastNameFather": "MARTINEZ",
        "lastNameMother": "LOPEZ",
        "birthDate": "12/05/1985",
        "nationalityCode": "MEX",
        "nationalityName": "MEXICO",
        "gender": "M",
        "civilStatus": "2",
        "curp": "MALA850512HNLY2033",
        "countryName": "MEXICO",
        "countryCode": "MEX",
        "stateCode": "NL",
        "stateId": 19,
        "cityName": "MONTERREY",
        "cityId": 19001,
        "street": "AV. UNIVERSIDAD 123",
        "zipcode": "64000",
        "email": "abraham.martinez@afirme.com",
        "name": "ABRAHAM",
        "registrationDate": "20/04/2025",
        "companyNumber": "000000001"
    },
    {
        "clientId": 5887242,
        "branchId": 882,
        "branchName": "BANCO DIGITAL BILLU",
        "statusCode": "1",
        "personType": "PF",
        "companyName": "MARIA GONZALEZ PEREZ",
        "lastNameFather": "GONZALEZ",
        "lastNameMother": "PEREZ",
        "birthDate": "03/09/1990",
        "nationalityCode": "MEX",
        "nationalityName": "MEXICO",
        "gender": "F",
        "civilStatus": "1",
        "curp": "GOPM900903MNLY2033",
        "countryName": "MEXICO",
        "countryCode": "MEX",
        "stateCode": "NL",
        "stateId": 19,
        "cityName": "SAN NICOLÁS",
        "cityId": 19002,
        "street": "CALLE JUÁREZ 456",
        "zipcode": "66400",
        "email": "maria.gonzalez@afirme.com",
        "name": "MARIA",
        "registrationDate": "01/05/2025",
        "companyNumber": "000000002"
    }
]

@app.get("/afirme/dev/customers_api/v3/customers")
async def get_customers(searchType: str = "", informationSearch: str = ""):
    resultados = []

    for cliente in clientes:
        nombre_completo = f"{cliente['name']} {cliente['lastNameFather']} {cliente['lastNameMother']}".lower()
        if informationSearch.lower() in nombre_completo or cliente['name'].lower() in informationSearch.lower():
            resultados.append(cliente)

    dummy_response = {
        "customersList": resultados,
        "responseList": [
            {
                "codeResponse": "0000",
                "replyMessage": "OK"
            }
        ]
    }

    return JSONResponse(content=dummy_response)