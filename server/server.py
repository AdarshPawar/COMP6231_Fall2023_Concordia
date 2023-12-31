import socket
import random
from threading import Thread
import os
import shutil
from pathlib import Path
import time

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

    def start(self):
        """
        1) Create server, bind and start listening.
        2) Accept clinet connections and serve the requested commands.

        Note: Use ClientThread for each client connection.
        """
            # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Bind the socket to the specified address and port
        s.bind((self.host, self.port))
            # Listen for incoming connections
        s.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            # Accept incoming connections
            connection, client_address = s.accept()
            clientThread = ClientThread(self, connection, client_address)
            clientThread.start()
            print(f"Accepted connection from {client_address}")
            # send random eof token

            # try:
            #     # Handle the client requests using ClientThread
            # except Exception as e:
            #     print(f"Error: {e}")
            # finally:
            #     print("Connection closed.")
            #     client_socket.close()

        #raise NotImplementedError("Your implementation here.")




    def get_working_directory_info(self, working_directory):
        """
        Creates a string representation of a working directory and its contents.
        :param working_directory: path to the directory
        :return: string of the directory and its contents.
        """
        dirs = "\n-- " + "\n-- ".join(
            [i.name for i in Path(working_directory).iterdir() if i.is_dir()]
        )
        files = "\n-- " + "\n-- ".join(
            [i.name for i in Path(working_directory).iterdir() if i.is_file()]
        )
        dir_info = f"Current Directory: {working_directory}:\n|{dirs}{files}"
        return dir_info

    def generate_random_eof_token(self):
        """Helper method to generates a random token that starts with '<' and ends with '>'.
        The total length of the token (including '<' and '>') should be 10.
        Examples: '<1f56xc5d>', '<KfOVnVMV>'
        return: the generated token.
        """
        #raise NotImplementedError("Your implementation here.")
        sampleSpace = 'abcdedghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        global eof
        eof = '<'
        for i in range(8):
            eof = eof + random.choice(sampleSpace)
        eof = eof + '>'
        return eof

    def receive_message_ending_with_token(self, active_socket, buffer_size, eof_token):
        """
        Same implementation as in receive_message_ending_with_token() in client.py
        A helper method to receives a bytearray message of arbitrary size sent on the socket.
        This method returns the message WITHOUT the eof_token at the end of the last packet.
        :param active_socket: a socket object that is connected to the server
        :param buffer_size: the buffer size of each recv() call
        :param eof_token: a token that denotes the end of the message.
        :return: a bytearray message with the eof_token stripped from the end.
        """
        #raise NotImplementedError("Your implementation here.")
        data = bytearray()
        while True:
            packet = active_socket.recv(buffer_size)
            data += packet
            if(packet[-10:] == eof_token.encode()):
                break
        data = data[:-10]
        return data

    def handle_cd(self, current_working_directory, new_working_directory):
        """
        Handles the client cd commands. Reads the client command and changes the current_working_directory variable
        accordingly. Returns the absolute path of the new current working directory.
        :param current_working_directory: string of current working directory
        :param new_working_directory: name of the sub directory or '..' for parent
        :return: absolute path of new current working directory
        """
        #raise NotImplementedError("Your implementation here.")
        os.chdir(new_working_directory)
        current_working_directory = new_working_directory
        return current_working_directory

    def handle_mkdir(self, current_working_directory, directory_name):
        """
        Handles the client mkdir commands. Creates a new sub directory with the given name in the current working directory.
        :param current_working_directory: string of current working directory
        :param directory_name: name of new sub directory
        """
        #raise NotImplementedError("Your implementation here.")
        os.mkdir(current_working_directory+ '\\' +directory_name)

    def handle_rm(self, current_working_directory, object_name):
        """
        Handles the client rm commands. Removes the given file or sub directory. Uses the appropriate removal method
        based on the object type (directory/file).
        :param current_working_directory: string of current working directory
        :param object_name: name of sub directory or file to remove
        """
        #raise NotImplementedError("Your implementation here.")
        objectLocation = Path(current_working_directory+ '\\' +object_name)
        print(objectLocation)
        if objectLocation.is_file():
            os.remove(objectLocation)
        if objectLocation.is_dir():
            shutil.rmtree(objectLocation)

    def handle_ul(
        self, current_working_directory, file_name, service_socket, eof_token
    ):
        """
        Handles the client ul commands. First, it reads the payload, i.e. file content from the client, then creates the
        file in the current working directory.
        Use the helper method: receive_message_ending_with_token() to receive the message from the client.
        :param current_working_directory: string of current working directory
        :param file_name: name of the file to be created.
        :param service_socket: active socket with the client to read the payload/contents from.
        :param eof_token: a token to indicate the end of the message.
        """
        #raise NotImplementedError("Your implementation here.")
        response = self.receive_message_ending_with_token(service_socket,1024,eof_token)
        with open(file_name, 'wb') as file:
            file.write(response)

    def handle_dl(
        self, current_working_directory, file_name, service_socket, eof_token
    ):
        """
        Handles the client dl commands. First, it loads the given file as binary, then sends it to the client via the
        given socket.
        :param current_working_directory: string of current working directory
        :param file_name: name of the file to be sent to client
        :param service_socket: active service socket with the client
        :param eof_token: a token to indicate the end of the message.
        """
        #raise NotImplementedError("Your implementation here.")
        with open(file_name, 'rb') as file:
            filecontents = file.read()
        filecontents = filecontents + eof_token.encode()
        service_socket.sendall(filecontents)

    def handle_info(
        self, current_working_directory, file_name, service_socket, eof_token
    ):
        """
        Handles the client info commands. Reads the size of a given file.
        :param current_working_directory: string of current working directory
        :param file_name: name of sub directory or file to remove
        :param service_socket: active service socket with the client
        :param eof_token: a token to indicate the end of the message.
        """
        #raise NotImplementedError('Your implementation here.')
        file = open(file_name, "rb")
        filecontents = file.read()
        print(len(filecontents))
        service_socket.sendall(str(len(filecontents)).encode()+eof_token.encode())
    
    def handle_mv(self,current_working_directory, file_name, destination_name):
        """
        Handles the client mv commands. First, it looks for the file in the current directory, then it moves or renames 
        to the destination file depending on the nature of the request.
        :param current_working_directory: string of current working directory
        :param file_name: name of the file tp be moved / renamed
        :param destination_name: destination directory or new filename
        """
        #raise NotImplementedError('Your implementation here.')
        fromLocation = Path(current_working_directory + '\\' + file_name)
        print(fromLocation)
        if '/' in destination_name:
            toLocation = Path(destination_name+ '\\' + file_name)
        else:
            toLocation = Path(current_working_directory + '\\' +destination_name)
        print(toLocation)
        os.rename(fromLocation, toLocation)


class ClientThread(Thread):
    def __init__(self, server: Server, service_socket: socket.socket, address: str):
        Thread.__init__(self)
        self.server_obj = server
        self.service_socket = service_socket
        self.address = address

    def run(self):
        print ("Connection from : ", self.address)
        #raise NotImplementedError("Your implementation here.")
        eofToken = self.service_socket.sendall(self.server_obj.generate_random_eof_token().encode())
        # establish working directory
        currDir = self.server_obj.get_working_directory_info(os.getcwd())
        # send the current dir info
        self.service_socket.sendall(currDir.encode())
        while True:
        # get the command and arguments and call the corresponding method
            clientCommand = self.service_socket.recv(1024).decode()
            order = clientCommand.split(' ')
            if ('cd' in clientCommand):
                self.server_obj.handle_cd(os.getcwd(), order[1])
                break
            elif ('mkdir' in clientCommand):
                self.server_obj.handle_mkdir(os.getcwd(), order[1])
                break
            elif ('ul' in clientCommand):
                self.server_obj.handle_ul(os.getcwd(), order[1], self.service_socket, eof)
                break
            elif ('dl' in clientCommand):
                self.server_obj.handle_dl(os.getcwd(), order[1], self.service_socket, eof)
                break
            elif ('rm' in clientCommand):
                self.server_obj.handle_rm(os.getcwd(), order[1])
                break
            elif ('info' in clientCommand):
                self.server_obj.handle_info(os.getcwd(), order[1], self.service_socket, eof)
                break
            elif ('mv' in clientCommand):
                self.server_obj.handle_mv(os.getcwd(), order[1], order[2])
                break
            elif ('exit' in clientCommand):
                print('Exiting application')
                self.service_socket.close()
                return

        # sleep for 1 second
        time.sleep(1)
        # send current dir info
        currDir = self.server_obj.get_working_directory_info(os.getcwd())
        self.service_socket.sendall(currDir.encode()+eof.encode())
        print('Connection closed from:', self.address)


def run_server():
    HOST = "127.0.0.1"
    PORT = 65432

    server = Server(HOST, PORT)
    server.start()


if __name__ == "__main__":
    run_server()
