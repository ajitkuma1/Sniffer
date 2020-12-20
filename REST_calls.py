import requests
import certifi
from requests.auth import HTTPBasicAuth
import ssl
print(ssl.get_default_verify_paths())
openssl_cafile='/Users/ajitkuma/Downloads/DNAC_211.crt'

#req = requests.post("https://10.78.20.211/dna/system/api/v1/auth/token", auth=HTTPBasicAuth('admin', 'Maglev123'))
#token = resp.json()['Token']
#print("Token Retrieved: {}".format(token))


def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    s = requests.Session()
    s.verify = '/Users/ajitkuma/Downloads/DNAC_certificate/kong.pem'
    print(s.verify)
    openssl_cafile = '/Users/ajitkuma/Downloads/DNAC_211.crt'
    certPath='/Users/ajitkuma/Downloads/DNAC_211.crt'
    #url = 'https://sandboxdnac.cisco.com/dna/system/api/v1/auth/token'
    url = 'https://10.78.20.211/dna/system/api/v1/auth/token'       # Endpoint URL
    #resp = requests.post(url, auth=HTTPBasicAuth('devnetuser', 'Cisco123!'))  # Make the POST Request
    resp = requests.post(url, auth=HTTPBasicAuth(username='admin', password='Maglev123'), verify=False)   # Make the POST Request
    print(resp)
    token = resp.json()['Token']    # Retrieve the Token from the returned JSON
    print("Token Retrieved: {}".format(token))  # Print out the Token
    return token    #


def get_device_from_dnac(device_ip):
    response = requests.get(
        'https://10.78.20.211/dna/intent/api/v1/network-device/ip-address/{}'.format(device_ip),
        headers={
            ‘X-Auth-Token’: ‘{}’.format(token),
            ‘Content-type’: ‘application/json’,
        },
        verify=False
    )
    print(response.json())
    return response.json()

if __name__ == "__main__":
    get_auth_token()
    get_device_from_dnac('5.0.5.11')
