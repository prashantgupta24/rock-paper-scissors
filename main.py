import json
import random
from os.path import abspath

import cv2

from vr import classifyImage


def captureImage():
    cap = cv2.VideoCapture(0)

    # user
    rock_user = img = cv2.imread('resources/rock_user.jpg', 0)
    paper_user = cv2.imread('resources/paper_user.jpg', 0)
    scissors_user = cv2.imread('resources/scissors_user.jpg', 0)
    user_items = {}
    user_items["rock"] = rock_user
    user_items["paper"] = paper_user
    user_items["scissors"] = scissors_user
    # computer
    rock_comp = img = cv2.imread('resources/rock_comp.jpg', 0)
    paper_comp = cv2.imread('resources/paper_comp.jpg', 0)
    scissors_comp = cv2.imread('resources/scissors_comp.jpg', 0)
    comp_items = {}
    comp_items["rock"] = rock_comp
    comp_items["paper"] = paper_comp
    comp_items["scissors"] = scissors_comp
    # error
    error = cv2.imread('resources/error.jpg', 0)

    # pixels
    frame1_x = 50
    frame1_y = 50

    while(True):
        ret, frame = cap.read()
        # if ret == True:
        #     frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        #cv2.namedWindow("frame1", flags=cv2.WINDOW_FULLSCREEN)
        # cv2.SetWindowProperty("frame1", CV_WND_PROP_FULLSCREEN,
        #                       CV_WINDOW_FULLSCREEN)
        cv2.imshow('frame1', rgb)
        cv2.moveWindow('frame1', frame1_x, frame1_y)

        if cv2.waitKey(1) & 0xFF == ord('p'):
            cv2.imwrite('resources/capture.jpg', frame)
            users_choice = classifyCurrentImage()
            # print(users_choice)

            # cv2.destroyWindow('frame1')
            # cv2.imshow('image', rock)
            # cv2.waitKey()
            # cv2.destroyWindow('image')

            # if users_choice == "rock":
            #     cv2.imshow('frame1', rock)
            # else if users_choice == "paper":
            #     cv2.imshow('frame1', paper)
            # else if users_choice == "scissors":
            #     cv2.imshow('frame1', scissors)
            if users_choice in user_items:
                cv2.imshow('frame1', user_items.get(users_choice))
                comp_choice, comp_image = random.choice(
                    list(comp_items.items()))
                cv2.imshow('frame2', comp_image)
                cv2.moveWindow('frame2', frame1_x+800, frame1_y)

                showRoundWinner(users_choice=users_choice,
                                comp_choice=comp_choice, frame1_x=frame1_x,
                                frame1_y=frame1_y)

            else:
                cv2.imshow('frame1', error)
                print("could not classify with confidence, please try again")

            cv2.waitKey()
            cv2.destroyWindow('frame2')
            cv2.destroyWindow('frame3')
            # break

    cap.release()
    cv2.destroyAllWindows()


def classifyCurrentImage():
    image_file = abspath('resources/capture.jpg')
    classes = classifyImage(image_file=image_file, threshold='0.7')
    #print(json.dumps(classes, indent=2))
    if len(classes) > 0:
        return classes[0]["class"]
    else:
        return "error"


def showRoundWinner(users_choice, comp_choice, frame1_x, frame1_y):
    winning_party = ""

    rock = "rock"
    paper = "paper"
    scissors = "scissors"

    winning_combinations = {}
    winning_combinations[rock] = paper
    winning_combinations[paper] = scissors
    winning_combinations[scissors] = rock

    if users_choice == comp_choice:
        winning_party = "draw"
    elif winning_combinations[users_choice] == comp_choice:
        winning_party = "comp"
    else:
        winning_party = "user"

    you_won = img = cv2.imread('resources/you_won.jpg', 0)
    you_lose = cv2.imread('resources/you_lose.jpeg', 0)
    draw = cv2.imread('resources/draw.jpeg', 0)

    if winning_party == "user":
        cv2.imshow('frame3', you_won)
    elif winning_party == "comp":
        cv2.imshow('frame3', you_lose)
    else:
        cv2.imshow('frame3', draw)

    cv2.moveWindow('frame3', frame1_x+400, frame1_y+300)
    print(
        f"user made {users_choice}, comp made {comp_choice}, {winning_party} won!")
    return "frame3"


if __name__ == "__main__":
    captureImage()
