#imports
import keyboard
import mss
import pyautogui
import time
import numpy
import cv2
import pprint


def loop():
    #Stage represents what stage of fishing the game is in
    # 0 = Waiting for a bite
    # 1 = Click to sink the hook
    # 2 = Reel in the fish
    # 3 = spam left click so you don't start looking everywhere
    stage = 0

    #Stage pictures
    stage_0_night = cv2.imread('stage0lfday.jpg')
    stage_0_day   = cv2.imread('stage0lfday.jpg')
    stage_1 = cv2.imread('stage1lf.jpg')

    #dimensions
    dimensions1 = {
        'left': 0,
        'top': 0,
        'width': 2560,
        'height': 1440
    }

    while True:
        if stage == 0:
            sct = takeScreenshot()

            # Cut off alpha
            scr = numpy.array(sct.grab(dimensions1))
            scr_remove = scr[:,:,:3]

            #Check night
            if(stage_0_check_night(scr_remove, stage_0_night) == True):
                print("you did it Spencer!")
                stage = 1
                time.sleep(2.25)
            elif(stage_0_check_day(scr_remove, stage_0_day) == True):
                print("you did it Spencer!")
                stage = 1
                time.sleep(2.25)
            else:
                print("retry")

        elif stage == 1:
            print("Stage 1")
            f = True
            while f == True:
                #Reel in
                if(reel(stage_1) == True):
                    stage = 2
                    f = False

                #Brief Pause
                time.sleep(.1)

                #break check
                if keyboard.is_pressed('f6'):
                    break

        elif stage == 2:
            print("Stage 2")

            #wait a hot sec for things to reset
            pyautogui.click()
            time.sleep(8)

            #Reset stage
            stage = 0

            #Cast again
            cast()

        #Check if user cancelled execution
        if keyboard.is_pressed('f6'):
            break

def stage_0_check_night(scr_remove, stage_0_night):
    #Run the match template
    result = cv2.matchTemplate(scr_remove, stage_0_night, cv2.TM_CCOEFF_NORMED)

    #Get minMax values
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    #Print max values
    #print(f"Max Val: {max_val} Max Loc: {max_loc}")

    if max_val > .85:
        pyautogui.click()
        return True
    else:
        return False

def stage_0_check_day(scr_remove, stage_0_day):
    #Run the match template
    result = cv2.matchTemplate(scr_remove, stage_0_day, cv2.TM_CCOEFF_NORMED)

    #Get minMax values
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    #Print max values
    #print(f"Max Val: {max_val} Max Loc: {max_loc}")

    if max_val > .85:
        pyautogui.click()
        return True
    else:
        return False

def stage_1_check(stage_1):
    dimensions2 = {
        'left': 0,
        'top': 1100,
        'width': 2560,
        'height': 340
    }

    #check if we need to stop
    sct = takeScreenshot()

    # Cut off alpha
    scr = numpy.array(sct.grab(dimensions2))
    scr_remove = scr[:,:,:3]

    #Run the match template
    result = cv2.matchTemplate(scr_remove, stage_1, cv2.TM_CCOEFF_NORMED)

    #Get minMax values
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    #Print max values
    print(f"Max Val: {max_val} Max Loc: {max_loc}")

    if max_val > .70:
        #print("Fish Caught!")
        #pyautogui.click()
        #stage = 2
        #f = False
        return True
    else:
        #print("Just keep reeling!")
        return False

def reel(stage_1):
    pyautogui.mouseDown()
    if(stage_1_check(stage_1) == True):
        return True
    time.sleep(.15)
    if(stage_1_check(stage_1) == True):
        return True
    time.sleep(.15)
    if(stage_1_check(stage_1) == True):
        return True
    pyautogui.mouseUp()
    return False

def takeScreenshot():
    return mss.mss()

def cast():
    pyautogui.mouseDown()
    time.sleep(1.2)
    pyautogui.mouseUp()

def printInstructions():
    print("Navigate to the water, open fishing and equip any bait you may want.")
    print("Press 'F6' to start fishing.")
    print("Once content, press 'F6' again to quit.")

def main():
    #Print instructions
    printInstructions()

    #Wait for user input to start
    keyboard.wait('f6')

    #Cast the rod
    cast()

    #Start the execution loop
    loop()
    

if __name__ == "__main__":
    main()