import zmq
import time

context = zmq.Context()

print("Connecting to data storage microservice")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

socket.send(b"append!new_file!This is the data I want to write")
message = socket.recv()
print("Expected: Success")
print("Received reply %s" % message)

time.sleep(1)

socket.send(b"asdojckhasoihsoi")
message2 = socket.recv()
print("Expected: some error message")
print("Received reply: %s" % message2)

time.sleep(1)

socket.send(b"askjdhsiu!new_file!This should never appear")
message3 = socket.recv()
print("Expected: some error message")
print("Received reply:L %s" % message3)