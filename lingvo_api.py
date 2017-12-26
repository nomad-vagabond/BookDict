import json, requests

BASEURL = 'https://developers.lingvolive.com/'

LANGCODE = {
    'En': 1033,
    'Es': 1034,
    'Fr': 1036,
    'De': 1031,
    'It': 1040,
    'Kk': 1087,
    'Uk': 1058,
    'Ch': 1028,
    'El': 1032,
    'Pl': 1045,
    'Da': 1030,
    'Ru': 1049,
    'Tt': 1092,
    'La': 1142
}

LANGCODE.update({k.lower(): v for k, v in LANGCODE.items()})
LANGCODE.update({k.upper(): v for k, v in LANGCODE.items()})

# KEY = 'ZDQwYWRkMzMtNTQwMy00YzQzLTlmYjktZDA0M2YyOWMxN2M2OmEyMzZkZmQ2NmM1MjRlMTlhMzJiN2I4Nzc5N2Q0ZmZk'

def get_token():

    with open('lingvoapi_key') as keyfile:
        key = keyfile.readline().strip('\n')

    headers = {'Content-Type': 'application/json',
              'Content-length': '0',
              'Authorization': 'Basic {0}'.format(key)}

    api_url = '{0}api/v1/authenticate'.format(BASEURL)
    
    response = requests.post(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return response.status_code


def get_translation(word, srclang='En', dstlang='Uk'):

    with open('lingvoapi_token') as tokenfile:
        token = tokenfile.readline().strip('\n')

    headers = {'Content-Type': 'application/json',
              'Authorization': 'Bearer {0}'.format(token)}

    api_url = '{0}api/v1/'.format(BASEURL)
    tu = 'Minicard?text={0}&srcLang={1}&dstLang={2}'
    translate_url = tu.format(word, LANGCODE[srclang], LANGCODE[dstlang])

    # response = requests.post(api_url, headers=headers_auth)
    response = requests.get(api_url+translate_url, headers=headers)

    # print(response.headers)

    if response.status_code == 200:
        content = json.loads(response.content.decode('utf-8'))
        translation = content['Translation']
        return translation
        # return content
    else:
        content = response.status_code
        # print(type(content))
        return content

    
# t = get_translation('filter')
# print(t)


if __name__ == '__main__': 
    token = get_token()
    print(token)
    if type(token) is not int:
        with open('lingvoapi_token', 'w') as tokenfile:
            tokenfile.write(token)
    



