import requests as req

headers = {
    "User-Agent":"Server-Checker/1.0",
}

try:
    res = req.get("http://localhost:5000", headers=headers)
    if res.status_code == 500:
        print(res.status_code)
    else:
        print(res.status_code)

except:
    print("err")
