#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import io

context = zmq.Context()
PORT = 5555
SEPARATOR = b'\x21' # ! ASCII

def overwrite(filename, mode, data):
    with open("files" + filename, mode) as file:
        file.write(data)
    return

if __name__ == "__main__":
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{PORT}")

    print(f"Separator: {SEPARATOR.decode()}")


    while True:
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: %s" % message)
        buffer = bytearray()
        buffer.extend(message)

        # Get desired operation
        operation_idx = buffer.find(SEPARATOR)
        operation = buffer[0:operation_idx].decode()
        del buffer[:operation_idx + 2] # Two extra bytes to account for !
        # Do some checking to make sure it's valid
        print("Mode: {operation}")

        # Get filename
        filename_idx = buffer.find(SEPARATOR)
        filename = buffer[0:filename_idx].decode()
        # Do some checking to make sure it's valid
        del buffer[:filename_idx + 2]
        print("Filename: {filename}")

        # Get data to write
        data = buffer.decode()
        print("Data: {data}")

        # todo: move out into enum
        match operation:
            case "append":
                pass
            case "overwrite":
                overwrite(filename, "br+", data)
            case "delete":
                pass
            case _:
                # return falsy value
                pass
        

        # Check to make sure that the filename is valid
        

        #  Send reply back to client
        socket.send(b"Data saved")

