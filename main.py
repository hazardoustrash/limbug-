from pixel_color_detector import get_pixel_color, get_darkened_pixel_color
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


def thirdRowMacro():
    pyautogui.scroll(10)
    pyautogui.moveTo(490, 811)
    pyautogui.leftClick()
    pyautogui.moveTo((110, 890))
    pyautogui.leftClick()
    time.sleep(0.2)
    pyautogui.drag(400, -300, 0.3, button='left')
    time.sleep(0.3)
    pyautogui.moveTo(490, 811)
    pyautogui.leftClick()
    pyautogui.moveTo((110, 890))


def get_skills(sinners, starts, lengths):
    """
    Retrieves the skills for each sinner by moving the cursor to each skill.
    Assumes that the order of sinners does not change between skill rows.

    :param sinners: the list of sinners
    :param starts: starting coordinates for each row
    :param lengths: distances between skill icons in each row
    :return: the skills stored in a dictionary, key = sinner's name, value = [position, skill1, skill2, skill3]
    """
    skills = {sinner: [] for sinner in sinners}

    # First row (detect names and first skill)
    for j in range(len(sinners)):
        coords = (starts[0][0] + j * lengths[0], starts[0][1])
        pyautogui.moveTo(coords)
        name = screenshot_and_detect().strip()  # OCR to detect name
        skill_color, _ = get_pixel_color()  # Detect first skill color
        name, _ = process.extractOne(name, sinners)
        skills[name] = [j, skill_color]  # Store position and first skill

    # Second row (use stored positions)
    for j, sinner in enumerate(sinners):
        coords = (starts[1][0] + skills[sinner][0] * lengths[1], starts[1][1])
        pyautogui.moveTo(coords)
        skill_color, _ = get_pixel_color()  # Detect second skill color
        skills[sinner].append(skill_color)  # Append second skill

    # Third row requires a macro
    thirdRowMacro()

    # Third row (use stored positions)
    for j, sinner in enumerate(sinners):
        coords = (starts[2][0] + skills[sinner][0] * lengths[2], starts[2][1])
        skill_color, _ = get_darkened_pixel_color(coords)  # Detect third skill color
        skills[sinner].append(skill_color)  # Append third skill

    pyautogui.leftClick()

    return skills


def restart_level():
    """
    Restarts the level with a macro for a 14-inch Mac screen.
    """
    setting = (1458, 85)
    restart = (766, 526)
    pyautogui.click(setting)
    time.sleep(0.2)
    pyautogui.click(restart)
    wait_for_game_to_load()


def wait_for_game_to_load():
    """
    Waits for the game to load by checking the color of two pixels.
    """
    t = 0
    while True:
        wrath, _ = get_pixel_color((1454, 153))
        sloth, _ = get_pixel_color((1454, 230))
        if wrath == 'red' and sloth == 'yellow':
            print("Loading complete.")
            break
        if t > 20:
            print("Loading timeout.")
            break
        print('Loading...')
        time.sleep(0.5)
        t += 0.5


def generate_name_dict(characters):
    """
    Generates a dictionary for pronouns used in conditions.
    """
    return {'c' + str(i): char for i, char in enumerate(characters)}


def main():
    """
    Main function to run the script.
    """
    time.sleep(3)
    characters = initialize_sinners(lowerStart, lowerLength, 6)
    name_dict = generate_name_dict(characters)
    print(name_dict)
    input('Press Enter after configuring the conditions...')
    time.sleep(3)
    conditions = parse_conditions_file('conditions.txt', name_dict)
    print(conditions)
    if conditions:
        while True:
            skill_list = get_skills(characters, [lowerStart, middleStart, upperStart], [lowerLength, middleLength, upperLength])
            print(skill_list)
            if check_restart_conditions(skill_list, conditions):
                restart_level()
            else:
                os.system('say "我喜欢你"')  # define your own notifications!
                print("skill set found")
                break

    else:
        print("condition file not loaded")


lowerStart = (490, 811)
lowerLength = 91
middleStart = (518, 759)
middleLength = 77
upperStart = (492, 772)
upperLength = 87

if __name__ == '__main__':
    main()
