from utils import *

if __name__=="__main__":
    myDrone = initTello()
    def movingDrone(drone):
        drone.move_left(200)
        time.sleep(2)
        drone.move_back(200)
        time.sleep(1)
        drone.move_right(200)
        time.sleep(1)
        drone.move_forward(200)
        time.sleep(1)
        drone.move_left(200)
        time.sleep(1)


        drone.land()