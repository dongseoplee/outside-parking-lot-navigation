from multiprocessing import process
from threading import Thread
import cv2
import time
import io
import os
from google.cloud import vision
from djitellopy import tello
from utils import *
from yolo import *
from multiprocessing import Process, Queue
import keyboard
#multiprocessing으로 구현 생각해보기

def main():

    drone = tello.Tello()
    drone.connect()
    print(drone.get_battery())
    drone.streamon()

    isCar = False
    while True:

        img = drone.get_frame_read().frame
        img = cv2.resize(img, (1280, 720))
        yolo_img, isCar = detectCar(img)

        if isCar:
            print("is car", isCar)

            cv2.imwrite('./photo/carTest.png', yolo_img)
            #time.sleep(1)



        cv2.imshow("Image", yolo_img)  # 박스 쳐진 이미지
        cv2.waitKey(1)



def find_parking_lot():
    drone = tello.Tello()
    drone.connect()
    print(drone.get_battery())
    drone.streamon()
    parkingLot = []
    drone.takeoff()
    #drone.move_up(50)

    drone.curve_xyz_speed(25, -25, 0, 25, -75, 0, 20) # 원점에서 x2, y2, z2로 이동


    # cnt = 5 #주차 가능 구역 수
    # #리스트 만들어서

    # #총 주차구역 10군데라고 가정
    # for i in range(cnt):
    #     drone.move_forward(80)  # 20cm ~ 500cm 차량 가로폭 *(너비) 250cm
    #     distance = drone.get_distance_tof()  # 드론 밑 센서 기준 얼만나 떨어졌는지확인 단위 cm
    #     print("distance", distance)
    #
    #     if distance > 100: #드론이 땅에서 1m 보다 높게 떨어져 있으면 주차 빈 구역
    #         #drone.rotate_clockwise(360) #드론 360도 회전
    #         drone.flip_back()
    #         parkingLot.append(True)
    #     else:
    #         parkingLot.append(False)
    #
    #     time.sleep(1)

    return parkingLot #parkingLot list에 False 값인 인덱스 위치는 주차구역에 자동차가 있는 구역



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

    # drone.send_rc_control(0, -50, 0, 0)
    # time.sleep(3)
    #
    # drone.send_rc_control(0, 50, 0, 0)
    # time.sleep(3)
    #
    # drone.send_rc_control(50, 0, 0, 0)
    # time.sleep(3)
    #
    # drone.send_rc_control(-50, 0, 0, 0)
    # time.sleep(3)
    #
    # drone.send_rc_control(0, -50, 0, 0)
    # time.sleep(3)
    #
    # drone.send_rc_control(0, 0, 0, 0)
    # time.sleep(3)




def droneTakeoff(drone):
    drone.takeoff()



if __name__ == "__main__":


    parking = []
    parking = find_parking_lot()
    print(parking)

    # th0 = Thread(target=main, args=(drone,))
    # th1 = Thread(target=droneTakeoff, args=(drone,))
    # th2 = Thread(target=movingDrone, args=(drone,))
    # th0.start()
    # th2.start()
    # th1.start()




