from requests import Session
from time import sleep
from random import random
from datetime import datetime



class ChangePassword:
    def __init__(self, login, password, new_password, proxies=False, user_agent=False):
        self.login = login
        self.password = password
        self.new_password = new_password
        self.data_change = {
            "enc_old_password": '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), self.password),
            "enc_new_password1": '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), self.new_password),
            "enc_new_password2": '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), self.new_password)
            }
        self.user_agent = (
            user_agent if user_agent else 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            )
        self.proxies = (proxies if proxies else {})
        self.login_and_change()


    def login_and_change(self):
        
        session = Session()
        session.proxies = self.proxies
        session.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                                'ig_vw': '1920', 'ig_cb': '1', 'csrftoken': '',
                                's_network': '', 'ds_user_id': ''})

        session.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': self.user_agent,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
            })

        session.get('https://www.instagram.com/web/__mid/')
        csrf_token = session.cookies.get_dict()['csrftoken']
        session.headers.update({'X-CSRFToken': csrf_token})
        sleep(random() * random())
        enc_password = '#PWD_INSTAGRAM_BROWSER:0:{}:{}'.format(int(datetime.now().timestamp()), self.password)
        login = session.post('https://www.instagram.com/accounts/login/ajax/',
                             data={'enc_password': enc_password, 'username': self.login}, allow_redirects=True)
        
        login_json = login.json()
        session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})

        if 'userId' in login.text:
            print(f'[ + ] Logado: {self.login}:{self.password}')

            session.headers.update({
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'no-cache',
                'content-length': '658',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.instagram.com',
                'pragma': 'no-cache',
                'referer': 'https://www.instagram.com/accounts/password/change/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': self.user_agent,
                'x-ig-app-id': '936619743392459',
                'x-ig-www-claim': 'hmac.AR1TN4gla-aM3DKrODT9HYvDnxFKjeiB-rKi8I1kO9fYvAxs',
                'x-instagram-ajax': '35b547292413',
                'x-requested-with': 'XMLHttpRequest'
                })
            
            sleep(random() * random())
            change_response = session.post(
                'https://www.instagram.com/accounts/password/change/',
                data=self.data_change
                )
            if '{"status": "ok"}' in change_response.text:
                print(f'[ + ] Senha alterada com sucesso, Nova senha: {self.new_password}')
            else:
                print(f'[ - ] Erro ao alterar senha => ', change_response.text)
        else:
            print('[ - ] Login error: => ', login.text)

            


# ChangePassword(
#     login='E-mail/Username',
#     password='Password',
#     new_password='New_password'
#     )

import os
ChangePassword(
    login=os.environ['login'],
    password=os.environ['password'],
    new_password=os.environ['new_password']
    )
