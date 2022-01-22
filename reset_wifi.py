import time
import cv2
import numpy as np
import pyautogui

from image_manipulation import template_matching

# button images
restart_button = cv2.imread("wifi_reset_images/restart.png", cv2.IMREAD_GRAYSCALE)
password_field = cv2.imread("wifi_reset_images/pole_haslo.png", cv2.IMREAD_GRAYSCALE)
password_manager = cv2.imread("wifi_reset_images/manager_hasel.png", cv2.IMREAD_GRAYSCALE)
login_button = cv2.imread("wifi_reset_images/zaloguj.png", cv2.IMREAD_GRAYSCALE)
goto_network_settings = cv2.imread("wifi_reset_images/zobacz_swoja_siec.png", cv2.IMREAD_GRAYSCALE)
goto_advanced_settings = cv2.imread("wifi_reset_images/zaawansowane.png", cv2.IMREAD_GRAYSCALE)
goto_internet_connection_settings = cv2.imread("wifi_reset_images/polaczenie_z_internetem.png", cv2.IMREAD_GRAYSCALE)


class NoButtonFoundError(Exception):
    pass


def click_something(something, screenshot):
    found_pos = template_matching(template=something, search_img=screenshot)
    if found_pos is None:
        raise NoButtonFoundError
    top_left, bottom_right = found_pos
    center_x = int((top_left[0] + bottom_right[0]) / 2)
    center_y = int((top_left[1] + bottom_right[1]) / 2)
    pyautogui.click(center_x, center_y)


def click_restart(screenshot):
    click_something(something=restart_button, screenshot=screenshot)
    # click under the button to remove the selection frame around it
    pyautogui.moveRel(0, 100)
    pyautogui.click()


def login_to_funbox(screenshot):
    stages = [password_field, password_manager, login_button, goto_network_settings,
              goto_advanced_settings, goto_internet_connection_settings]
    for img in stages:
        try:
            click_something(something=img, screenshot=screenshot)
        except NoButtonFoundError:
            break
        time.sleep(0.5)
        screenshot = cv2.cvtColor(
                np.array(pyautogui.screenshot()), cv2.COLOR_RGB2GRAY
            )


if __name__ == '__main__':
    # internet connection constants
    url = "https://ismyinternetworking.com"
    timeout = 5  # seconds

    just_launched = True

    while True:
        print("No internet connection.")
        if just_launched:
            time.sleep(10)
        else:
            just_launched = False
        print('Trying to reconnect.')
        screen = cv2.cvtColor(
            np.array(pyautogui.screenshot()), cv2.COLOR_RGB2GRAY
        )
        try:
            click_restart(screen)
            print('clicked restart')
        except NoButtonFoundError:
            login_to_funbox(screen)
            print('logged in funbox')
        finally:
            time.sleep(5)

