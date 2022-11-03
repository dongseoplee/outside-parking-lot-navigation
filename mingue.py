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


def ocr():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "json file path"
    client = vision.ImageAnnotatorClient()

    path = '/Users/leedongseop/PycharmProjects/tello/photo/carTest.png'
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    content = texts[0].description
    content = content.replace(',', '')
    print(content)


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

    drone.land()
    drone.streamoff()  # 끄기


def test(drone):
    drone.takeoff()
    # drone.set_video_resolution(Tello.CAMERA_DOWNWARD) #카메라 땅 방향 on
    # drone.streamon() #카메라 on
    drone.move_up(100)
    drone.go_xyz_speed(-30, 320, 0, 50)  # xyz -500 ~ 500 speed 10 ~100
    drone.go_xyz_speed(-30, 320, 0, 50)  # xyz -500 ~ 500 speed 10 ~10-0

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

    drone.move_up(160)
    drone.go_xyz_speed(-30, 280, 0, 50)  # xyz -500 ~ 500 speed 10 ~100
    drone.go_xyz_speed(-10, 280, 0, 50)  # xyz -500 ~ 500 speed 10 ~100

    drone.rotate_counter_clockwise(220)

    cnt = 5  # 주차 가능 구역 수
    right_parkingLot = []

    for i in range(cnt):

        distance = drone.get_distance_tof()  # 드론 밑 센서 기준 얼만나 떨어졌는지확인 단위 cm

        print("distance", distance)

        if distance > 200:  # 드론이 땅에서 1m 보다 높게 떨어져 있으면 주차 빈 구역
            # drone.rotate_clockwise(360) #드론 360도 회전
            right_parkingLot.append(True)  # 주차 빈 구역이면 리스트에 true값
            print("right ", i, ": ", right_parkingLot[i])
        else:
            right_parkingLot.append(False)  # 주차 빈 구역 아니면 리스트에 false값
            print("right ", i, ": ", right_parkingLot[i])

        if i == 4:
            break

        drone.move_forward(220)  # 20cm ~ 500cm 차량 가로폭 *(너비) 250cm

    return right_parkingLot  # parkingLot list에 False 값인 인덱스 위치는 주차구역에 자동차가 있는 구역


def moveToNextParkingLot(drone):
    drone.move_left(400)
    drone.move_left(400)
    drone.move_left(300)

    drone.rotate_clockwise(180)


def find_parking_left(drone):
    cnt = 4
    left_parkingLot = []

    for i in range(cnt):
        distance = drone.get_distance_tof()  # 드론 밑 센서 기준 얼만나 떨어졌는지확인 단위 cm

        print("distance", distance)

        if distance > 200:  # 드론이 땅에서 1m 보다 높게 떨어져 있으면 주차 빈 구역
            # drone.rotate_clockwise(360) #드론 360도 회전
            left_parkingLot.append(True)  # 주차 빈 구역이면 리스트에 true값
            print("left ", i, ": ", left_parkingLot[i])
        else:
            left_parkingLot.append(False)  # 주차 빈 구역 아니면 리스트에 false값
            print("left ", i, ": ", left_parkingLot[i])

        if i == 3:
            break

        drone.move_forward(240)  # 20cm ~ 500cm 차량 가로폭 *(너비) 250cm

    return left_parkingLot


def rightLine_empty(drone, right_parkingLot):
    # 오른쪽 주차 자리 6칸
    # T T T F T T
    for i in range(6):
        if right_parkingLot[i]:
            drone.takeoff()

            drone.move_up(150)
            drone.go_xyz_speed(-30, 280, 0, 50)  # xyz -500 ~ 500 speed 10 ~100
            drone.go_xyz_speed(-30, 280, 0, 50)
            drone.rotate_counter_clockwise(220)
            for r in range(i):
                drone.move_forward(220)
            # drone.flip_forward()
            # drone.flip_back()
            drone.rotate_clockwise(360)

            right_parkingLot[i] = False
            drone.rotate_clockwise(220)
            for r in range(i):
                drone.move_forward(220)
            drone.go_xyz_speed(30, -280, 0, 50)
            drone.go_xyz_speed(30, -280, 0, 50)
            break

    return right_parkingLot  # F T T F T T


def leftLine_empty(drone, left_parkingLot):
    # 왼쪽 주차 자리 5칸
    # T T T F T
    for i in range(5):
        if left_parkingLot[i]:
            drone.takeoff()

            drone.move_up(150)
            drone.go_xyz_speed(30, 400, 0, 50)  # xyz -500 ~ 500 speed 10 ~100
            drone.go_xyz_speed(30, 400, 0, 50)
            drone.rotate_counter_clockwise(220)
            for r in range(i):
                drone.move_forward(220)
            drone.flip_forward()
            drone.flip_back()
            left_parkingLot[i] = False
            drone.rotate_clockwise(220)
            for r in range(i):
                drone.move_forward(220)
            drone.go_xyz_speed(-30, -400, 0, 50)
            drone.go_xyz_speed(-30, -400, 0, 50)
            break

    return left_parkingLot  # F T T F T


if __name__ == "__main__":
    drone = tello.Tello()
    drone.connect()
    print(drone.get_battery())
    # test(drone)
    right_parkingLot = find_parking_right(drone)  # 주차장 우측 빈자리 확인
    print("right_empty", right_parkingLot)

    moveToNextParkingLot(drone)

    # right = [True, False, False,False, False, False]
    # return_right = rightLine_empty(drone, right)

    left_parkingLot = find_parking_left(drone)
    print("left_empty", left_parkingLot)
    drone.move_left(300)
    drone.move_left(250)
    drone.move_back(60)

    #####차량 출입 시 실행되어야 할 함수 rightLine_empty

    # if True in right_parkingLot: # 빈자리 있는 경우
    #     right_parkingLot = rightLine_empty(drone, right_parkingLot)

    # elif True in left_parkingLot:
    #     left_parkingLot = leftLine_empty(drone, left_parkingLot)

    # else: # 주차 왼쪽 라인, 오른쪽 라인 모두 빈자리 없을때
    #     drone.rotate_clockwise(360)