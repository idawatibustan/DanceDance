from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding
import base64
import socket
import os
import sys
import time
import random

secret_key = b'this is dance12!'
target_ipaddr = sys.argv[1]
target_port = int(sys.argv[2])

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ipaddr, target_port))
    print("Connecting to " + str(target_ipaddr) + " at port " + str(target_port))
    time.sleep(1)
    '''
    Data required: action, voltage, current, power, cumpower (in this order)
    (only action is returned from the ML script, everything else is sent direct from Mega)
    '''
    try:
        while True:
            data_list = ['random action', random.random(), random.random(), random.random(), random.random()]
            print("Sending:\n%s" % data_list)
            send_data(s, data_list)
    except KeyboardInterrupt:
        send_data(s, ['logout  ', 'END', 'END', 'END', 'END'])
        print("\nEnded connection with %s" % target_ipaddr)
        s.close()

    # # test encryption/decryption
    # data_list = ['random action', 1, 2, 3, 4]
    # data = "#"
    # for element in data_list:
    #     data += str(element) + "|"

    # print(data)
    # encrypted_data = encrypt_text(bytes(data, 'utf8'), secret_key)
    # print(encrypted_data)
    # decrypted_data = decryptText(encrypted_data, secret_key)
    # print(decrypted_data)

def encrypt_text(data, Key):
    '''
    iv = initialization vector
    CBC = CypherBlockChaining
    '''
    iv = get_random_bytes(16)
    cipher = AES.new(Key, AES.MODE_CBC, iv)
    padded_data = Padding.pad(data, 16)
    encrypted_data = iv + cipher.encrypt(padded_data)
    encoded_data = base64.b64encode(encrypted_data)
    return encoded_data

def send_data(s, data_list):
    data = '#'
    for element in data_list:
        data += str(element) + '|'
    encoded_data = encrypt_text(bytes(data, 'utf-8'), secret_key)
    
    total_sent = 0
    while total_sent < len(encoded_data): # improve on logic here
        sent = s.send(encoded_data[total_sent:])
        if sent == 0:
            pass
            # print("NOTHING TO SEND")
        total_sent += sent
        time.sleep(1)

# PROVIDED EXAMPLE - REVERSE ENGINEER THIS
def decryptText(cipherText, Key):
    decodedMSG = base64.b64decode(cipherText)
    iv = decodedMSG[:16]
    secret_key = Key
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    decryptedText = cipher.decrypt(decodedMSG[16:]).strip()
    decryptedTextStr = decryptedText.decode('utf8')
    decryptedTextStr1 = decryptedTextStr[decryptedTextStr.find('#'):]
    decryptedTextFinal = bytes(decryptedTextStr1[1:]).decode('utf8')
    action = decryptedTextFinal.split('|')[0]
    voltage = decryptedTextFinal.split('|')[1]
    current = decryptedTextFinal.split('|')[2]
    power = decryptedTextFinal.split('|')[3]
    cumpower = decryptedTextFinal.split('|')[4]
    return {'action': action, 'voltage': voltage, 'current': current, 'power': power, 'cumpower': cumpower}


if __name__ == '__main__':
    main()
