from __future__ import print_function

import json
import random
from os.path import abspath

import cv2

from ibm_watson import ApiException, VisualRecognitionV3

# constants
rock = "rock"
paper = "paper"
scissors = "scissors"
user = "user"
comp = "comp"
draw = "draw"
# frames
user_frame = "user_frame"  # user actions
comp_frame = "comp_frame"  # comp actions
result_frame = "result_frame"  # result actions
# images
capture_image_path = 'resources/capture.jpg'
you_won_image_path = 'resources/you_won.jpg'
you_lose_image_path = 'resources/you_lost.jpg'
draw_image_path = 'resources/draw.jpeg'


def start():
    user_items, comp_items, error_image = init()
    # pixels
    frame1_x = 50
    frame1_y = 50

    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        cv2.imshow(user_frame, rgb)
        cv2.moveWindow(user_frame, frame1_x, frame1_y)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite(capture_image_path, frame)
            users_choice = classifyImage(image=capture_image_path)
            # print(users_choice)

            users_choice_accepted = False
            if users_choice in user_items:
                users_choice_accepted = True
                # show user's choice
                cv2.imshow(user_frame, user_items.get(users_choice))
                # get a random choice for the computer
                comp_choice, comp_image = random.choice(
                    list(comp_items.items()))
                cv2.imshow(comp_frame, comp_image)
                cv2.moveWindow(comp_frame, frame1_x+800, frame1_y)
                # show results
                showRoundWinner(users_choice=users_choice,
                                comp_choice=comp_choice, x=frame1_x,
                                y=frame1_y, frame=result_frame)
            else:
                cv2.imshow(user_frame, error_image)
                print("could not classify with confidence, please try again")

            cv2.waitKey()
            cv2.destroyWindow(user_frame)
            if users_choice_accepted:
                cv2.destroyWindow(comp_frame)
                cv2.destroyWindow(result_frame)

    cap.release()
    cv2.destroyAllWindows()


def classifyImage(image):
    image_file = abspath(image)
    classes = classifyImageWithVR(image_file=image_file, threshold='0.7')
    #print(json.dumps(classes, indent=2))
    if len(classes) > 0:
        return classes[0]["class"]
    else:
        return "error"


def classifyImageWithVR(image_file, threshold='0.6'):
    service = VisualRecognitionV3('2018-03-19')
    # classifiers = service.list_classifiers().get_result()
    # print(json.dumps(classifiers, indent=2))
    with open(image_file, 'rb') as image_file:
        results = service.classify(
            images_file=image_file,
            threshold=threshold,
            #   classifier_ids=['DefaultCustomModel_981890366']).get_result()
            classifier_ids=['rpsxone_245199051']).get_result()
        #print(json.dumps(results, indent=2))
        classes = results["images"][0]["classifiers"][0]["classes"]
        return classes


def showRoundWinner(users_choice, comp_choice, x, y, frame):
    you_won_image = cv2.imread(you_won_image_path, 0)
    you_lose_image = cv2.imread(you_lose_image_path, 0)
    draw_image = cv2.imread(draw_image_path, 0)

    winning_party = ""

    winning_combinations = {}
    winning_combinations[rock] = paper
    winning_combinations[paper] = scissors
    winning_combinations[scissors] = rock

    if users_choice == comp_choice:
        winning_party = draw
    elif winning_combinations[users_choice] == comp_choice:
        winning_party = comp
    else:
        winning_party = user

    if winning_party == user:
        cv2.imshow(frame, you_won_image)
    elif winning_party == comp:
        cv2.imshow(frame, you_lose_image)
    else:
        cv2.imshow(frame, draw_image)

    cv2.moveWindow(frame, x+400, y+300)

    print(
        f"user made {users_choice}, comp made {comp_choice}, {winning_party} won!")


def init():

    user_items = {}
    comp_items = {}
    # user
    rock_user_image = cv2.imread('resources/rock_user.jpg', 0)
    paper_user_image = cv2.imread('resources/paper_user.jpg', 0)
    scissors_user_image = cv2.imread('resources/scissors_user.jpg', 0)

    user_items[rock] = rock_user_image
    user_items[paper] = paper_user_image
    user_items[scissors] = scissors_user_image
    # computer
    rock_comp_image = cv2.imread('resources/rock_comp.jpg', 0)
    paper_comp_image = cv2.imread('resources/paper_comp.jpg', 0)
    scissors_comp_image = cv2.imread('resources/scissors_comp.jpg', 0)

    comp_items[rock] = rock_comp_image
    comp_items[paper] = paper_comp_image
    comp_items[scissors] = scissors_comp_image
    # error
    error_image = cv2.imread('resources/error.jpg', 0)

    return user_items, comp_items, error_image


if __name__ == "__main__":
    start()
    # service = VisualRecognitionV3('2018-03-19')
    # classifiers = service.list_classifiers().get_result()
    # print(json.dumps(classifiers, indent=2))
