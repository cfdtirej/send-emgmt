import ast
import socketserver
import zlib


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(4096).strip()
        print("{} wrote:".format(self.client_address[0]))
        data = zlib.decompress(self.data).decode('unicode-escape')
        write_data = [ast.literal_eval(data)]
        print(write_data)
        # just send back the same data, but upper-cased
        self.request.sendall(b'Got your back!!!')


if __name__ == "__main__":
    HOST, PORT = "localhost", 30001

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
