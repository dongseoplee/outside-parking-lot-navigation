from djitellopy import Tello
import cv2
import time

def initTello():
    myDrone = Tello()

    # drone connection
    myDrone.connect()

    # set all speed to 0
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0

    print("\n * Drone battery percentage : " + str(myDrone.get_battery()) )
    myDrone.streamoff()
    myDrone.streamon()

    return myDrone

def telloGetFrame(myDrone, w = 360, h = 240):
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w,h))
    return img

def telloGetTof(myDrone):
    myTof = myDrone.get_distance_tof()
    return myTof


def moveTello(myDrone):

    time.sleep(5)
    myDrone.takeoff()
    time.sleep(7)

    resp_back = myDrone.move_back(50)
    print(resp_back)

    if resp_back:
        time.sleep(3)
        resp_land = myDrone.land()
        print(resp_land)
    else:
        resp_land = myDrone.land()
        print(resp_land)






