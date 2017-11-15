from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Padding
import base64
import socket
import os
import sys
import time
import random
import uart_serial_v3 as uart
import threading

secret_key = 'this is dance12!'
target_ipaddr = sys.argv[1]
target_port = int(sys.argv[2])
dance_moves = [
'idle',
'wavehands', 'busdriver', 'frontback', 'sidestep', 'jumping',
'jumpingjack', 'turnclap', 'squatturnclap', 'windowcleaning', 'windowcleaner360',
'logout', 'prediction error', 'not ready yet'
]
us = uart.Uart_Serial(print_sensor=False)

def main():
    num_moves = 0
    counter = 0
    temp = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ipaddr, target_port))
    print("Connecting to " + str(target_ipaddr) + " at port " + str(target_port))
    time.sleep(30)
    '''
    Data required: action, voltage, current, power, cumpower (in this order)
    (only action is returned from the ML script, everything else is sent direct from Mega)
    '''
    try:
        while True:
            res, conf = us.get_pred_prob()
            voltage, current, power, cumpower = us.get_info()
            if ( res != 0 ) and ( res < 12 ):
                if res == temp:
                    counter += conf
                else:
                    temp = res
                    counter = conf
                print "detected = ", dance_moves[res], "| count = ", counter
                if num_moves < 40 and dance_moves[res] == 'logout':
                    counter = 0
                if counter >= 2 :
                    data_list = [dance_moves[res], voltage, current, power, cumpower]
                    print("Sending:\n%s" % data_list)
                    send_data(s, data_list)
                    num_moves = num_moves + 1
                    counter = 0
                    temp = ""
            time.sleep(1)

    except KeyboardInterrupt:
        send_data(s, ['logout  ', 'END', 'END', 'END', 'END'])
        print("\nEnded connection with %s" % target_ipaddr)
        us.shutdown()
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
    # encoded_data = encrypt_text(bytes(data, 'utf-8'), secret_key)
    encoded_data = encrypt_text(bytes(data), secret_key)

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
