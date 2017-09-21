#!/usr/bin/env python
""" Python socketIO client code to fetch emos Sentimentv2 API """

import logging
import threading
from socketIO_client import SocketIO

# For debug purpose
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()


class Sentiment():

    HOST = 'https://emosapi.com'
    PORT = 443
    APPKEY = '<APP KEY>'
    APPSECRET = '<APP SECRET>'
    
    socket_io = None
    s_thread_login = None
    s_thread_post = None
    
    def connect(self):
        self.socket_io = SocketIO(self.HOST, self.PORT, verify=False)
        self.socket_io.on('success', self.on_success)
        self.socket_io.on('response', self.on_response)
        self.socket_io.emit(
            'login',
            {'appkey': self.APPKEY, 'appsecret': self.APPSECRET}
        )

        self.s_thread_login = threading.Thread(target=self.socket_io.wait)
        self.s_thread_login.start()

    def on_success(self, res):
        print("SUCCESS:", res)
        if res.get('action') == 'login' and res.get('code') == 100:
            self.socket_io.emit(
                'post',
                {
                    'api': 'Sentimentv2',
                    'version': 'emotion',
                    'params': {
                        'text': 'required parameter', # Hard coded test text.
                        'lang':'en-us'
                    }
                }
            )
            self.s_thread_post = threading.Thread(target=self.socket_io.wait)
            self.s_thread_post.start()
        else:
            raise Exception("Login failed")
    
    def on_response(self, res):
        print("RESPONSE", res)
        # Disconnect when get API response. 
        self.disconnect()
        
    def disconnect(self):
        if not self.socket_io:
            raise Exception("Please connect first.")

        print("disconnect before:", self.socket_io.connected)
        self.socket_io.disconnect()        
        print("disconnect after:", self.socket_io.connected)

        self.socket_io = None
        self.s_thread_login = None
        self.s_thread_post = None


if __name__=='__main__':
    s = Sentiment()
    s.connect()
