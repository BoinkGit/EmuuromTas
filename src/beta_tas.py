from pynput.keyboard import Controller, Key
from time import sleep
from sys import platform

if platform == 'win32':
    movesList = open('assets\\get_scanner.txt', 'r')
else:
    movesList = open('assets/get_scanner.txt', 'r')

moves = []
for line in movesList:
    moves.append(line.removesuffix("\n"))


movesList.close()

#kb: Keyboard
kb = Controller()

def changeToKeys(lst):
    ret = []
    for character in lst:
        if character == 'u':
            character = Key.up
        elif character == 'd':
            character = Key.down
        elif character == 'l':
            character = Key.left
        elif character == 'r':
            character = Key.right
        elif character == 'e':
            character = Key.esc


        ret.append(character)
    return ret


def runKeys(keys):
    for currentKeyString in keys:
        try: 
            loops = int(currentKeyString) - 1
            for i in range(loops):
                for key in currentKeyList:
                    kb.press(key)
                sleep(0.05)
                for key in currentKeyList:
                    kb.release(key)
        except ValueError: 
            if len(currentKeyString) == 1:
                currentKeyList = [currentKeyString]
            else:
                currentKeyList = [currentKeyString[i] for i in range(len(currentKeyString))]
            currentKeyList = changeToKeys(currentKeyList)
            for key in currentKeyList:
                kb.press(key)
            sleep(0.05)
            for key in currentKeyList:
                kb.release(key)
        
sleep(.05)
print("START")
runKeys(moves)
print('FINISHED')
