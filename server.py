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
        #self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        self.data = self.request.recv(1024).decode().split()
        '''
        print("---------")
        print(self.data)
        print("---------")
        '''
        f = self.data[1]
        f2 = f.split("/")
        f3 = []
        for piece in f2:
            if piece != "" and piece != "..":
                f3.append(piece)
        print("len:", len(f3))
        if len(f3) > 1:
            print("Flag 1 -------------\n")
            pass
        elif len(f3) == 1:
            fname = f2[0]
            print("Flag 2 -------------\n")
            try:
                x = open("www/" + fname, r)
                self.request.send(bytearray('HTTP/1.0 200 OK\n', 'utf-8'))
                answer = ""
                for line in x:
                    answer += line
                self.request.sendall(bytearray(answer, 'utf-8'))
                print("Worked -----------\n")
            except:
                self.request.sendall(bytearray('HTTP/1.0 404 Not Found', 'utf-8'))
                print("Broke -----------\n")
        else:
            print("Flag 3 -------------\n")
        
        #self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
