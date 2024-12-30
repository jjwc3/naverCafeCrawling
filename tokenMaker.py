import hashlib, hmac, base64, requests

redirect_uri = 'http://localhost:8888'

client_id = 'YaBWiGQG10Pvch4jXzPj'
client_secret = 'WSIEIk07um'

state = "REWERWERTATE"

url = f'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}'
print(url)
code = input("Input Code: ")
# code = '2Xrg4oIp0k812RSR5T'

clientConnect = client_id + ":" + client_secret
clidst_base64 = base64.b64encode(bytes(clientConnect, "utf8")).decode()
url = f'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}&state={state}'
r = requests.get(url, headers={"Authorization": "Basic" + clidst_base64})
print(r.text)