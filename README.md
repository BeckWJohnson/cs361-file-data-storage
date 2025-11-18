# cs361-file-data-storage
Welcome to the File Data Storage Microservice for CS361

To use this microservice in your program you will simply need
to download ZeroMQ (they provide extensive documentation on their website), 
install our microservice file to your project directory,
and follow these steps:

*NOTE*  All example code is written in Python, to adjust to different languages please
        check the ZeroMQ documentation and follow the same steps in your chosen language.
        The process should be largely the same and the request format will be identical.

1. At the beginning of your program include ZeroMQ in your program by inserting the line: 'import zmq'

2. Create a context (ZeroMQ environment) with this line: 'your_context_name = zmq.Context()'

3. Create and bind a request socket:    'your_socket_name = your_context_name.socket(zmq.REQ)
                                         socket.connect("tcp://localhost:5555")'

4. Finally, let's send a request! Requests must follow this format: "writing_method!file_path!string of data"
        I.   writing_method can be append, overwrite, or delete. Append will append the data to the file,      
             overwrite will clear the file, then write the data, and delete will simply clear the file and ignore any data entered.
        II.  file_path is relative to your local directory, so you can either reference a file or directory
             directly, or use the './' to indicate your current directory.
        III. Your string of data can be however long you want, and does not need to be bounded by quotation marks.
             That is, unless you want your data to have quotation marks around it.

5. To send this request you will use this code: 'socket.send(b"writing_method!file_path!string of data")

Congrats! You should see your data appear in your chosen file.

Our program is written to send a confirmation message back to the client program when it has finished, as well as error messages in case of, well, error.
To receive these messages include this code: 'your_variable = socket.recv' immediately after your socket.send call.
You can then print them out wherever you would like.

UML Diagram:
<img width="1114" height="1314" alt="File_microservice_sequence_diagram" src="https://github.com/user-attachments/assets/5fc48633-95c8-4275-ab08-39eae70e93f2" />



