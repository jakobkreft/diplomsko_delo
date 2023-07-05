import os
import subprocess
import threading
import time
import datetime
import socket


s = socket.socket()
host = ""
port= 12345
s.bind((host, port))
s.listen(5)

ime = ""
location = "/home/pi/diplomska/posnetki/"
print("enter record duration in seconds")
duration = input()
TIMETOWAITFORABORT = 0.5
#class for controlling the running and shutting down of raspivid
class RaspiVidController(threading.Thread):
    def __init__(self, filePath, timeout, preview, otherOptions=None):
        threading.Thread.__init__(self)

        #setup the raspivid cmd
        self.raspividcmd = ["raspivid"]
        #add file path, timeout and preview to options
        self.raspividcmd.append("-o")
        self.raspividcmd.append(filePath)
        self.raspividcmd.append("-t")
        self.raspividcmd.append(str(timeout))
        self.raspividcmd.append("-pts")
        self.raspividcmd.append("{}testA{}_timestamps.txt".format(location,ime))
        if preview == False: self.raspividcmd.append("-n")

        #if there are other options, add them
        if otherOptions != None:
            self.raspividcmd = self.raspividcmd + otherOptions

        #set state to not running
        self.running = False

    def run(self):
        #run raspivid
        raspivid = subprocess.Popen(self.raspividcmd)

        #loop until its set to stopped or it stops
        self.running = True
        while(self.running and raspivid.poll() is None):
            time.sleep(TIMETOWAITFORABORT)
        self.running = False

        #kill raspivid if still running
        if raspivid.poll() == True: raspivid.kill()

    def stopController(self):
        self.running = False

def init_vid():
    global vidcontrol
    vidcontrol = RaspiVidController("{}testA{}.h264".format(location,ime), duration*1000, True, ["-w","1600","-h","1210","-fps", "25","-rot","180","-b","8000000"])

def start_vid():
    global vidcontrol
    vidcontrol.start()

def stop_vid():
    global vidcontrol
    #stop the controller
    vidcontrol.stopController()
    #wait for the tread to finish if it hasn't already
    vidcontrol.join()

#test program
if __name__ == '__main__':


    print("Waiting...")
    while True:
        try:
            clientsock, addr = s.accept()
        except OSError:
            continue
        message = clientsock.recv(20)


        ime = str(datetime.datetime.now())[-6:]
        init_vid()

        print ("Starting raspivid controller testA{}".format(ime))
        start_vid()
        time.sleep(duration)
        print ("Stopping raspivid controller")
        stop_vid()
        time.sleep(2)
        os.system("MP4Box -add {}testA{}.h264 {}testA{}.mp4".format(location,ime,location,ime))
        print ("Done")
        print("Waiting...")
