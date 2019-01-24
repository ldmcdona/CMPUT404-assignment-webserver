#  coding: utf-8 
import socketserver
import mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).decode().split()
        '''
        print("---------")
        print(self.data)
        print("---------")
        '''
        if self.data[0] != "GET":
            self.request.sendall(bytearray('HTTP/1.1 405 Method Not Allowed', 'utf-8'))
        else:
            f = self.data[1]
            f2 = f.split("/")
            f3 = []
            for piece in f2:
                if piece != "" and piece != "..":
                    f3.append(piece)
                    #print("len:", len(f3))
            if len(f3) > 1:
                #print("Flag 1 -------------")
                pass
            elif len(f3) == 1:
                fname = f3[0]
                #print("Flag 2 -------------")
                try:
                    a = "www/" + fname
                    b = ""
                    x = open(a, "r")
                    mimetypes.init()
                    b = mimetypes.guess_type(a)
                    print(a, b[0])
                    self.request.send(bytearray('HTTP/1.1 200 OK\n', 'utf-8'))
                    self.request.sendall(bytearray(b[0], 'utf-8'))
                    print("Worked -----------")
                except Exception as e:
                    print(e)
                    self.request.sendall(bytearray('HTTP/1.1 404 Not Found', 'utf-8'))
                    print("Broke -----------")
            else:
                #print("Flag 3 -------------")
            
                self.request.sendall(bytearray('HTTP/1.1 404 Not Found', 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
