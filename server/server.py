import ast
import os
import socketserver
import yaml
import zlib

from influxdb import InfluxDBClient


config_yaml = '/config/config.yml'
yaml_path = os.path.dirname(__file__) + config_yaml
with open(yaml_path, 'r') as yml:
    config = yaml.safe_load(yml)
    db_host = config['Influx']['host']
    db_port = config['Influx']['port']
    username = config['Influx']['username']
    password = config['Influx']['password']
    database = config['Influx']['database']


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(4096).strip()
        print("{} wrote:".format(self.client_address[0]))
        data = zlib.decompress(self.data).decode('unicode-escape')
        write_data = [ast.literal_eval(data)]
        # print(write_data)
        # just send back the same data, but upper-cased
        client = InfluxDBClient(
            host=db_host, port=db_port, username=username, password=password, database=database
        )
        client.write_points(write_data)
        self.request.sendall(b'Got your back!!!')


if __name__ == "__main__":
    HOST, PORT = "localhost", 30001
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()
