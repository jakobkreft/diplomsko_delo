from hashlib import shake_256
import socket

s1 = socket.socket()
s2 = socket.socket()

host1 = "169.254.204.4"
host2 = "169.254.41.236"

port = 12345
s1.connect((host1, port))
s2.connect((host2, port))

message = "foo"
s1.send(message.encode())
s2.send(message.encode())

s1.close()
s2.close()
