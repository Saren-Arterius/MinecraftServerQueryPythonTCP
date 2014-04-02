#!/usr/bin/python3
from socket import socket, AF_INET, SOCK_STREAM, timeout
from re import findall, sub, split

class MinecraftQuery(object):
    def __init__(self, host = "localhost", port = 25565, timeout = 5):
        self.host = host
        self.port = port
        self.timeout = timeout
    
    def __getData(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(self.timeout)
        s.connect((self.host, self.port))
        s.sendall(b'\xfe\x01')
        data = s.recv(1024)
        s.close()
        return data
        
    def __getDataNew(self):
        from struct import pack
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(self.timeout)
        s.connect((self.host, self.port))
        
        handShake = b"\x00"
        handShake += b"\x04"
        handShake += bytes(encode_varint(len(self.host)), "UTF-8")
        handShake += bytes(self.host, "UTF-8")
        handShake += pack("H", self.port)
        handShake += b"\x01"
        handShake = bytes(encode_varint(len(handShake)), "UTF-8") + handShake
        s.sendall(handShake)
        s.sendall(b'\x01\x00')
        
        data = s.recv(1024)
        dataLength = decode_varint(data[:2].decode("latin-1")) + 2
        while 1:
            recv = s.recv(1024)
            data += recv
            if len(data) == dataLength:
                break
        s.close()
        assert data[2:3] == b"\x00"
        assert decode_varint(data[3:5].decode("latin-1")) == len(data[5:])
        return data[5:].decode("UTF-8")
        
    def getResultNew(self):
        try:
            status = {"Version": "", "MOTD": "", "OnlinePlayers": 0, "MaxPlayers": 0}
            from json import loads
            jsonData = loads(self.__getDataNew())
            status["Version"] = findall("(\d.\d.\d)", jsonData["version"]["name"])[0]
            status["MOTD"] = sub("§\w", "", jsonData["description"])
            status["OnlinePlayers"] = int(jsonData["players"]["online"])
            status["MaxPlayers"] = int(jsonData["players"]["max"])
            status["ServerIcon"]= sub("\n", "", jsonData["favicon"])
        except Exception as e:
            status["Error"] = repr(e)
        finally:
            return status
            
    def getResult(self):
        try:
            status = {"Version": "", "MOTD": "", "OnlinePlayers": 0, "MaxPlayers": 0}
            data = self.__getData()[9:].decode("UTF-8", "replace")
            data = split("\x00\x00", data)
            status["Version"] = sub("\x00", "", data[1])
            status["MOTD"] = sub("�\w", "", sub("\x00", "", data[2]))
            status["OnlinePlayers"] = int(sub("\x00", "", data[3]))
            status["MaxPlayers"] = int(sub("\x00", "", data[4]))
            return status
        except Exception as e:
            status["Error"] = repr(e)
            return status
            
def encode_varint(value):
    return "".join(encode_varint_stream([value]))
    
def decode_varint(value):
    return decode_varint_stream(value).__next__()
    
def encode_varint_stream(values):
    for value in values:
        while True:
            if value > 127:
                yield chr((1 << 7) | (value & 0x7f))
                value >>=  7
            else:
                yield chr(value)
                break
                
def decode_varint_stream(stream):
    value = 0
    base = 1
    for raw_byte in stream:
        val_byte = ord(raw_byte)
        value += (val_byte & 0x7f) * base
        if (val_byte & 0x80):
            base *= 128
        else:
            yield value
            value = 0
            base = 1