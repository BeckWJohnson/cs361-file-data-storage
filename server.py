import re
import zmq

context = zmq.Context()
PORT = 5555
SEPARATOR = b'\x21' # ! ASCII

# First part: Matches any amount of alphanumeric characters, parenthesis,
#   brackets, dots, or spaces
# Second part: Must match previous character set AND not end with
#   a period or space
PATTERN = re.compile(r"^[\w\-()\[\]\.\ ]*[\w\-()\[\]]$")

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
        print(f"Recieved message: {message}")
        buffer = bytearray()
        buffer.extend(message)

        # Get desired operation
        operation_idx = buffer.find(SEPARATOR)
        operation = buffer[0:operation_idx].decode()
        # Delete extra character to remove separator
        del buffer[:operation_idx + 1] 
        # Do some checking to make sure it's valid
        print(f"Mode: {operation}")

        # Get filename
        filename_idx = buffer.find(SEPARATOR)
        filename = buffer[0:filename_idx].decode()
        del buffer[:filename_idx + 1]
        print(f"Filename: {filename}")

        # Make sure filename is valid
        match = PATTERN.fullmatch(filename)
        if not match:
            socket.send(b"Error: Invalid file name.")
            print()
            continue

        # Get data to write
        data = buffer.decode()
        print(f"Data: {data}")

        match operation:
            case "append":
                write(filename, "a+", data)
            case "overwrite":
                write(filename, "w+", data)
            case "delete":
                write(filename, "w+", '')
            case _:
                socket.send(b'Error: Invalid operation. ' \
                    b'Must be "append", "overwrite", or "delete"')
                print()
                continue
        

        #  Send reply back to client
        socket.send(b"Success: Data saved")
        print()

