import io
import socket
import pickle
import argparse
import cv2
import numpy as np
from plate import Plate
from PIL import Image
import os

class Server:
    __slots__ = ["SERVER_IP", "SERVER_PORT", "socket", "_socket_"]
    def __init__(self, ip, port):
        self.SERVER_IP = ip
        self.SERVER_PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.SERVER_IP, self.SERVER_PORT))
        self.socket.listen(1)
        print(f"Server start!!!")

    def run(self):
        while True:
            connection, client_address = self.socket.accept()
            try:
                # Receive the image data
                while True:
                    packet_size = int.from_bytes(connection.recv(8), 'big')
                    data = bytearray()
                    while packet_size:
                        packet = connection.recv(4096 if packet_size > 4096 else packet_size)
                        if not packet:
                            break
                        packet_size -= len(packet)
                        data.extend(packet)

                    try:
                        received_obj = pickle.loads(data)
                        byte_stream = io.BytesIO(received_obj.img)
                        image = Image.open(byte_stream)
                        # image.save(OUTPUT_IMAGE_PATH)
                        img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
                    except Exception as e:
                        continue
                    print(f"Received!!!")
                    cv2.imwrite('output.jpg', img)

            finally:
                # Clean up the connection
                connection.close()

    def close(self):
        self._socket_.close()

if __name__ == "__main__":
    server = Server("0.0.0.0", 3030)
    server.run()