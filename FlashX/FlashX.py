import socket, os  # Import socket module

print("""
#####################################################
#        ______ _           _    __   __            #
#       |  ____| |         | |   \ \ / /            #
#       | |__  | | __ _ ___| |__  \ V /             #
#       |  __| | |/ _` / __| '_ \  > <              #
#       | |    | | (_| \__ \ | | |/ . \             #
#       |_|    |_|\__,_|___/_| |_/_/ \_\            #
#####################################################
""")


def receive(): # for recieving file
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    # host = socket.gethostname()  # Get local machine name
    myHost = input("Enter Lhost: ")
    host = myHost
    port = 55555  # Reserve a port for your service.
    s.bind((host, port))  # Bind to the port
    fileToSendPath = input("Enter path to save output:> ")
    realFileToSendPath = os.path.realpath(fileToSendPath)

    fileToSend = open(realFileToSendPath, 'wb')

    s.listen(5)  # Now wait for client connection.
    while True: 
        try:
            c, addr = s.accept()  # Establish connection with client.
            print("-" * 20)
            print('Got connection from', addr)
            print("Receiving...")
            print("-" * 20)
            print("\n")

            l = c.recv(10000024)
            while (l): # if you are connected, keep recieving
                print("Receiving...")
                fileToSend.write(l)
                if "Done Sending" in l.decode("unicode_escape"): # quit if you see "Done Sending"
                    print("Done Receiving")
                    fileToSend.close()
                    quitPromt = input("Do you wan to quit? Y/n ") # Continue recieving if you wish
                    if quitPromt == "n":
                        fileToSend.close()
                        quit()
                    elif quitPromt == "Y":
                        print("Continuing to recieve...")
                        l = c.recv(10000024)
                else:
                    l = c.recv(10000024)

            c.send(bytes('Thank you for connecting', encoding="utf-8"))
            c.close()  # Close the connection
        except Exception as e: # Capture all exceptions
            pass


def send(): # for sending file
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    myHost = input("Enter Lhost to connect: ")
    fileToSend = input("Enter file path to send: ")
    host = myHost
    port = 55555  # Reserve a port for your service.
    x = ""

    s.connect((host, port)) # connect to server
    realfileToSendPath = os.path.realpath(fileToSend) # convert the file path entered to real file path
    f = open(realfileToSendPath, 'rb')
    print('Sending...')
    l = f.read(10000024)
    while (l): # if you are connected, keep sending
        print('Sending...')
        s.send(l)
        l = f.read(10000024)
    f.close()
    print("Done Sending")

    while x: # Continue sending if you wish
        fileToSend = input("Enter file path to send: ")
        if fileToSend == "quit" or fileToSend == "Quit":
            quit()
        realfileToSendPath = os.path.realpath(fileToSend) # convert the file path entered to real file path
        f = open(realfileToSendPath, 'rb')
        print('Sending...')
        l = f.read(10000024)
        while (l): # if you are connected, keep sending
            print('Sending...')
            s.send(l)
            l = f.read(10000024)
        f.close()
    s.send("Done Sending".encode("utf-8"))
    print(s.recv(10000024).decode("utf-8"))
    s.close() # close the connection


def serverFunc():
    choice = input("Do you want to send or receive? ")
    if choice == "send" or choice == "Send":
        send() # call the send function
    else:
        receive() # call the recieve function


serverFunc()


