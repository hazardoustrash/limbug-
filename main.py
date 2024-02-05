from pixel_color_detector import get_pixel_color
import pyautogui
from fuzzywuzzy import process
from name_recognition import screenshot_and_detect
from restart_decision import parse_conditions_file, check_restart_conditions
import time
import os


def initialize_sinners(start, length, num):
    """
    gives the list of sinners in the battle
    :param start: The starting coordinate, aka the coordinate of the skill on the bottem left
    :param length: The distance between two skill icons
    :param num: the number of sinners in the battle
    :return: the list of detected sinner names after OCR
    """
    sinners = []
    for i in range(num):
        pyautogui.moveTo((start[0] + i * length), start[1])
        name = screenshot_and_detect().strip()
        sinners.append(name)

    return sinners


def get_skills(sinners, start, length):
    """

    :param sinners: the list of sinners
    :param start: starting coordinates, same as above
    :param length: same as initialize_sinners
    :return: the skills stored in a dictionary, key = sinner's name, value = [place, skill1, skill2]
    """
    skills = {sinner: [] for sinner in sinners}
    for i in range(len(start)):
        for j in range(len(sinners)):
            pyautogui.moveTo((start[i][0] + j * length[i]), start[i][1])
            detected = screenshot_and_detect().strip()
            name, _ = process.extractOne(detected, sinners)
            skill_color, colorRgb = get_pixel_color()
            if i == 0:
                skills[name].append(j)
            skills[name].append(skill_color)

    return skills


def restart_level():
    """
    macro for restarting the level, needs changes based on the screen size, this one is for Mac 14 inch
    :return:
    """
    setting = (1458, 85)
    restart = (766, 526)
    pyautogui.leftClick(setting)
    time.sleep(0.2)
    pyautogui.leftClick(restart)
    time.sleep(3)
    t = 0
    while True:
        wrath, _ = get_pixel_color((1454, 153))
        sloth, _ = get_pixel_color((1454, 230))
        if (wrath == 'red' and sloth == 'yellow') or t > 20:
            print("loading complete")
            break
        else:
            print('loading')
            time.sleep(0.5)
            t += 0.5


lowerStart = (490, 811)
lowerLength = 91
upperStart = (518, 759)
upperLength = 77

if __name__ == '__main__':
    time.sleep(3)
    characters = initialize_sinners(lowerStart, lowerLength, 6)
    # generate the dictionary for the pronouns used, allows easier config for the conditions
    name_dict = {}
    for i in range(len(characters)):
        name_dict['c' + str(i)] = characters[i]

    print(name_dict)
    _ = input('press enter after you have configured the conditions')
    time.sleep(3)
    # now switch back to the game session, and wait for the notification
    conditions = parse_conditions_file('conditions.txt', name_dict)
    print(conditions)
    if conditions:
        while True:
            skill_list = get_skills(characters, [lowerStart, upperStart], [lowerLength, upperLength])
            if check_restart_conditions(skill_list, conditions):
                restart_level()
            else:
                os.system('say "我喜欢你"')  # define your own notifications!
                print("skill set found")
                break
            print(skill_list)

    else:
        print("condition file not loaded")
