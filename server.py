import time
import zmq
import io

context = zmq.Context()
PORT = 5555
SEPARATOR = b'\x21' # ! ASCII

def write(filename, mode, data):
    with open("files/" + filename, mode) as file:
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
        print(buffer)

        # Get desired operation
        operation_idx = buffer.find(SEPARATOR)
        operation = buffer[0:operation_idx].decode()
        del buffer[:operation_idx + 1] # Two extra bytes to account for !
        # Do some checking to make sure it's valid
        print(f"Mode: {operation}")

        # Get filename
        filename_idx = buffer.find(SEPARATOR)
        filename = buffer[0:filename_idx].decode()
        # Do some checking to make sure it's valid
        del buffer[:filename_idx + 1]
        print(f"Filename: {filename}")

        # Get data to write
        data = buffer.decode()
        print(f"Data: {data}")

        # todo: move out into enum
        match operation:
            case "append":
                write(filename, "a", data)
            case "overwrite":
                write(filename, "r+", data)
            case "delete":
                pass
            case _:
                # return falsy value
                pass
        

        # Check to make sure that the filename is valid
        

        #  Send reply back to client
        socket.send(b"Data saved")

