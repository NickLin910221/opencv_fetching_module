import io
import socket
import pickle
import cv2
from PIL import Image
from plate import Plate
import os
from IPCam import IPCam

class Client:
    __slots__ = ["SERVER_IP", "SERVER_PORT", "socket", "cache_source"]
    def __init__(self, ip, port):
        self.SERVER_IP = ip
        self.SERVER_PORT = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.SERVER_IP, self.SERVER_PORT))
        self.cache_source = IPCam("ipcam_ip", 30)
        self.cache_source.run()
        print(f"Client start!!!")

    def run(self):
        while True:
            img, _, status = self.cache_source.getimg()
            self.send(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))           
            print(f"Send!!!")         

    def send(self, img):
        # Load and convert the image into a byte stream
        byte_stream = io.BytesIO()
        img.save(byte_stream, format='JPEG')
        image_data = byte_stream.getvalue()
        # Send the image data
        data = Plate(image_data)
        self.socket.sendall(len(pickle.dumps(data)).to_bytes(8, 'big'))
        self.socket.sendall(pickle.dumps(data))
        # Close the socket

    def close(self):
        self.socket.close()
       
        
if __name__ == "__main__":
    client = Client("ipaddress", 3030)
    try:
        client.run()
    except KeyboardInterrupt:
        client.close()