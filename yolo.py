import cv2
import numpy as np
import time  # -- 프레임 계산을 위해 사용

# https://prlabhotelshoe.tistory.com/15

#vedio_path = './video2.mp4'  # -- 사용할 영상 경로
min_confidence = 0.5


def detectCar(frame):
    isCar = False
    start_time = time.time()
    img = cv2.resize(frame, (1280, 720))
    height, width, channels = img.shape
    # cv2.imshow("Original Image", img)

    # -- 창 크기 설정
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # -- 탐지한 객체의 클래스 예측
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # -- 원하는 class id 입력 / coco.names의 id에서 -1 할 것
            if class_id == 2 and confidence > min_confidence:

                isCar = True #차량 확인

                # -- 탐지한 객체 박싱
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, 0.4)
    font = cv2.FONT_HERSHEY_DUPLEX
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = "{}: {:.2f}".format(classes[class_ids[i]], confidences[i] * 100)
            print(i, label)
            color = colors[i]  # -- 경계 상자 컬러 설정 / 단일 생상 사용시 (255,255,255)사용(B,G,R)
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
    end_time = time.time()
    process_time = end_time - start_time
    print("=== A frame took {:.3f} seconds".format(process_time))
    return img, isCar

#
# -- yolo 포맷 및 클래스명 불러오기
model_file = 'yolo/yolov3-tiny.weights'  # -- 본인 개발 환경에 맞게 변경할 것
config_file = 'yolo/yolov3-tiny.cfg'  # -- 본인 개발 환경에 맞게 변경할 것
#
# model_file = 'yolo/yolov3.weights'  # -- 본인 개발 환경에 맞게 변경할 것
# config_file = 'yolo/yolov3.cfg'  # -- 본인 개발 환경에 맞게 변경할 것

net = cv2.dnn.readNet(model_file, config_file)

# -- GPU 사용
# net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
# net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# -- 클래스(names파일) 오픈 / 본인 개발 환경에 맞게 변경할 것
classes = []
with open("yolo/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
