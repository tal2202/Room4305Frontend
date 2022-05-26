import json
import time
import torch
import cv2
import numpy as np
from flask import Flask, request, jsonify, abort
from flask_cors import cross_origin
from threading import Thread

app = Flask(__name__)

users = {}

# Consts
VERSION = "0.3"
NAMES = {
    0: "Eli",
    1: "Tal",
    2: "Yonatan",
    3: "Empty"
}
SCORE_THRESHOLD = 6
DELTA_THRESHOLD = 10
MODEL_PATH = "models/model6"
device = torch.device('cpu')


def get_man_predicted(the_model, img):
    start = time.time()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = np.transpose(img, (2, 0, 1))
    img = torch.tensor(img)
    img.unsqueeze_(0)
    img = img.float()
    img = img.to(device)

    outputs = the_model(img)
    score = torch.max(outputs)
    _, user = torch.max(outputs, 1)
    end = time.time()
    print(f"user: {NAMES[int(user)]}. score: {float(score)}. time: {end - start}")
    if score < SCORE_THRESHOLD:
        return -1, -1
    return score, user


def get_result(chosen_img):
    # chosen_img = cv2.imread("people/0/16.jpg")
    model = torch.load(MODEL_PATH)
    score, user = get_man_predicted(model, chosen_img)
    # if score != -1:
    #     print(f"Name: {NAMES[user[0].item()]}, Score: {float(score)}")
    # else:
    #     print("No one detected above threshold")
    return int(user)


def check_close_time_deltas(last):
    delta = time.time() - last
    if delta < DELTA_THRESHOLD:
        return False
    return True


def handle_result(user):
    if user != -1:
        if user not in users.keys():
            # New user
            users[user] = {"ir": True, "last": time.time()}
        else:
            # Check delta time
            if check_close_time_deltas(users[user]["last"]):
                if users[user]["ir"] is True:
                    ir = False
                    ir_text = "in"
                else:
                    ir = True
                    ir_text = "out"
                users[user] = {"ir": ir, "last": time.time()}
                print(f"{NAMES[user]} is {ir_text}")
                # print("DELTA OK")
            else:
                pass
                # print("Delta too soon")


@app.route("/getUpdated", methods=['GET'])
@cross_origin()
def get_users():
    arr = []
    for user in users:
        arr.append({"id": user, "ir": users[user]["ir"], "last": users[user]["last"]})
    final = {"users": arr, "version": VERSION}
    return final


def camera():
    video_cap = cv2.VideoCapture(0)
    if video_cap.isOpened():
        while True:
            ret, frame = video_cap.read()
            if ret:
                user = get_result(frame)
                handle_result(user)
                # time.sleep(2)
    else:
        print("cannot open camera")


if __name__ == '__main__':
    print("Started")

    # Camera
    worker = Thread(target=camera)
    worker.daemon = True
    worker.start()

    # Flask
    app.run(host='0.0.0.0', port=4180)
