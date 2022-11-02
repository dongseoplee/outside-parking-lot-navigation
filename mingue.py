from multiprocessing import process
from threading import Thread
import cv2
import time
import io
import os
# from google.cloud import vision
from djitellopy import tello
from utils import *
from yolo import *
from multiprocessing import Process, Queue
import keyboard


def main(drone):
    drone.streamon()

    isCar = False
    while True:

        img = drone.get_frame_read().frame
        img = cv2.resize(img, (1280, 720))
        img, isCar = detectCar(img)
        cv2.imshow("Image", img)  # 박스 쳐진 이미지
        if isCar:
            print("is car", isCar)

            cv2.imwrite('./photo/carTest.png', img)
            cv2.waitKey(1)
            print("사진")
            find_parking_right(drone)
            continue

        # cv2.imwrite("./personTest.png", img)  # 사진 저장, 욜로로 차량임이 확인되면 이미지 저장 후 ocr 인식


def movingDrone(drone):
    drone.takeoff()
    drone.move_up(40)
    time.sleep(1)

    drone.streamon()  # 카메라 on

    # cv2.imshow("Image", img )#박스 쳐진 이미지

    img = drone.get_frame_read().frame
    img = cv2.resize(img, (1280, 720))
    cv2.imshow("Image", img)  # 박스 쳐진 이미지

    drone.move_back(50)
    time.sleep(1)

    drone.send_rc_control(0, 0, 0, 0)
    time.sleep(3)

    distance = drone.get_distance_tof()  # 드론 밑 센서 기준 얼만나 떨어졌는 지확인

    print("distance", distance)

    drone.land
    drone.streamoff()  # 끄기


def test(drone):
    drone.takeoff()
    # drone.set_video_resolution(Tello.CAMERA_DOWNWARD) #카메라 땅 방향 on
    # drone.streamon() #카메라 on
    drone.move_up(100)
    drone.g(-30, 320, 0, 50)  # xyz -500 ~ 500 speed 10 ~100
    drone.g(-30, 320, 0, 50)  # xyz -500 ~ 500 speed 10 ~10-0

    drone.rotate_counter_clockwise(250)

    # drone.curve_xyz_speed(100, 100, 0, -100, 450, 0, 55)   #대각선 이동
    # drone.rotate_counter_clockwise(90)

    # drone.flip_back() #저번에 보내준 영상처럼 뒤로 뒤집는거
    # drone.flip_forward() #  앞으로 뒤집기

    # drone.g (100, 50, 0, 50) #xyz -500~ 500 speed 10 ~100
    # drone.rotate_counter_clockwise(230)
    time.sleep(1)

    return 0


def find_parking_right(drone):
    drone.takeoff()

    drone.move_up(150)
    drone.g(-30, 280, 0, 50)  # xyz -500 ~ 500 speed 10 ~100
    drone.g(-30, 280, 0, 50)  # xyz -500 ~ 500 speed 10 ~100

    drone.rotate_counter_clockwise(220)

    cnt = 6  # 주차 가능 구역 수
    right_parkingLot = []

    for i in range(cnt):

        distance = drone.get_distance_tof()  # 드론 밑 센서 기준 얼만나 떨어졌는지확인 단위 cm
        drone.move_forward(220)  # 20cm ~ 500cm 차량 가로폭 *(너비) 250cm
        print("distance", distance)

        if distance > 200:  # 드론이 땅에서 1m 보다 높게 떨어져 있으면 주차 빈 구역
            # drone.rotate_clockwise(360) #드론 360도 회전
            right_parkingLot.append(True) #주차 빈 구역이면 리스트에 true값
        else:
            right_parkingLot.append(False) #주차 빈 구역 아니면 리스트에 false값


    return right_parkingLot  # parkingLot list에 False 값인 인덱스 위치는 주차구역에 자동차가 있는 구역

def moveToNextParkingLot(drone):
    drone.move_left(400)
    drone.rotate_clockwise(180)


#
def find_parking_left(drone):

    cnt = 5
    left_parkingLot = []

    for i in range(cnt):
        distance = drone.get_distance_tof()  # 드론 밑 센서 기준 얼만나 떨어졌는지확인 단위 cm
        drone.move_forward(220)  # 20cm ~ 500cm 차량 가로폭 *(너비) 250cm
        print("distance", distance)

        if distance > 200:  # 드론이 땅에서 1m 보다 높게 떨어져 있으면 주차 빈 구역
            # drone.rotate_clockwise(360) #드론 360도 회전
            left_parkingLot.append(True) #주차 빈 구역이면 리스트에 true값
        else:
            left_parkingLot.append(False) #주차 빈 구역 아니면 리스트에 false값

    return left_parkingLot





def find_parking_left(drone):
    drone.move_left(400)
    drone.rotate_clockwise(220)
    cnt = 5
    left_parkingLot = []

    for i in range(cnt):

        distance = drone.get_distance_tof()  # 드론 밑 센서 기준 얼만나 떨어졌는지확인 단위 cm
        drone.move_forward(220)  # 20cm ~ 500cm 차량 가로폭 *(너비) 250cm
        print("distance", distance)

        if distance > 200:  # 드론이 땅에서 1m 보다 높게 떨어져 있으면 주차 빈 구역
            # drone.rotate_clockwise(360) #드론 360도 회전
            left_parkingLot.append(i)

    return left_parkingLot  # parkingLot list에 False 값인 인덱스 위치는 주차구역에 자동차가 있는 구역


def right_empty(drone, empty):  # 운전자에게 오른쪽 빈자리로 가서 알려주기
    drone.g(-30, 230, 0, 50)
    drone.rotate_counter_clockwise(220)

    if empty[0] == 0:  # 첫번째 list에서 빈자리가 우측 0번째일 때

        drone.flip_back()  # flip로 빈자리 알려줌
        drone.flip_forward()

        drone.rotate_clockwise(220)  # 왔던길 다시 돌아감.
        drone.g(-30, -230, 0, 50)
        drone.land()

        del empty[0]  # list에서 첫번째 값 뺴서 빈자리 제거
        return empty

    else:
        num = empty[0]  # 빈자리 받기
        for i in range(num):  # 빈자리 앞으로 이동
            drone.move_forward(220)

        drone.flip_back()  # 빈자리 flip으로 알려줌
        drone.flip_forward()

        drone.rotate_clockwise(220)  # 되돌아가기
        for i in range(num):
            drone.move_forward(220)

        drone.g(-30, -230, 0, 50)
        drone.land()

        del empty[0]  # list에서 첫번째 값 뺴서 빈자리 제거
        return empty


if __name__ == "__main__":
    drone = tello.Tello()
    drone.connect()
    print(drone.get_battery())
    # test(drone)
    right_parkingLot = find_parking_right(drone)  # 주차장 우측 빈자리 확인
    print("right_empty", right_parkingLot)

    left_parkingLot = find_parking_right(drone)
    print("left_empty", left_parkingLot)

    # left_parkingLot = find_parking_left(drone)  #주차장 좌측 빈자리 확인
    # print("left", left_parkingLot)

    # if len(right_parkingLot) != 0:   #우측에 빈자리가 있다면
    #    right_parkingLot = right_empty(drone, right_parkingLot, right_parkingLot)

    # elif len(left_parkingLot) != 0:    #좌측에 빈자리가 있다면
    #    left_parkingLot = right_empty(drone, right_parkingLot, left_parkingLot)

    # else:  #좌우측 빈자리 없음
    #    drone.rotate_clockwise(360)