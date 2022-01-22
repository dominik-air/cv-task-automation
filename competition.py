import time
import cv2
import numpy as np
import pyautogui

# button images
start_quiz = cv2.imread("abb_competition_images/zacznij_quiz.png", cv2.IMREAD_GRAYSCALE)
next_q = cv2.imread("abb_competition_images/dalej.png", cv2.IMREAD_GRAYSCALE)
questions = [cv2.imread(f"abb_competition_images/p{i}.png", cv2.IMREAD_GRAYSCALE) for i in range(1, 11)]

actions = []
for q in questions:
    actions.append(q)
    actions.append(next_q)


def win_competition(screenshot):
    stages = [start_quiz] + actions
    for stage in stages:
        while True:
            height, width = stage.shape
            img = screenshot.copy()
            result = cv2.matchTemplate(img, stage, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val >= 0.8:
                top_left_corner = max_loc
                bottom_right_corner = (top_left_corner[0] + width, top_left_corner[1] + height)
                pyautogui.click(int((top_left_corner[0] + bottom_right_corner[0]) / 2),
                                int((top_left_corner[1] + bottom_right_corner[1]) / 2))
                break
            screenshot = cv2.cvtColor(
                     np.array(pyautogui.screenshot()), cv2.COLOR_RGB2GRAY
                    )


while True:
    time.sleep(10)
    screen = cv2.cvtColor(
        np.array(pyautogui.screenshot()), cv2.COLOR_RGB2GRAY
    )
    win_competition(screen)
