#!/usr/bin/python3
class MinecraftQuery(object):
    def __init__(self, host = "localhost", port = 25565, timeout = 5):
        self.host = host
        self.port = port
        self.timeout = timeout
    
    def __getData(self):
        from socket import socket, AF_INET, SOCK_STREAM
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(self.timeout)
        s.connect((self.host, self.port))
        s.sendall(b'\xfe\x01')
        data = s.recv(1024)
        s.close()
        return data
        
    def getResult(self):
        try:
            from re import split, sub
            status = {"Version": "", "MOTD": "", "OnlinePlayers": 0, "MaxPlayers": 0}
            data = self.__getData()[9:].decode("UTF-8", "replace")
            data = split("\x00\x00", data)
            status["Version"] = sub("\x00", "", data[1])
            status["MOTD"] = sub("�\w", "", sub("\x00", "", data[2]))
            status["OnlinePlayers"] = sub("\x00", "", data[3])
            status["MaxPlayers"] = sub("\x00", "", data[4])
        except Exception as e:
            status["Error"] = repr(e)
        finally:
            return status