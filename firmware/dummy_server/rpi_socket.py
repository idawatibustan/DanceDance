from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import socket
import os
import sys

secret_key = b'this is dance12!'
target_ipaddr = sys.argv[1]
target_port = int(sys.argv[2])


def main():
    # print("Creating socket")
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((target_ipaddr, target_port))
    # print("Connected to " + str(target_ipaddr) + " at port " + str(target_port))

    text = b"this is for next milestone"
    cipher = AES.new(secret_key, AES.MODE_CBC)  # CypherBlockChaining
    encrypted_text = cipher.encrypt(text)


if __name__ == '__main__':
    main()
