import pyautogui

pyautogui.PAUSE = .4
pyautogui.FAILSAFE = True

#top left is norgate data view
#bottom right is notepad++

WIDTH, HEIGHT = pyautogui.size()

with open('C:/Users/mcdof/Documents/norgate_us_equities.txt', 'r') as f:
    for line in f:
        line = line.strip()
        #Press next
        pyautogui.click(50,150)
        #click in stock area
        #pyautogui.moveTo(800,350)
        #left clock
        pyautogui.click(800, 350)
        #select all
        pyautogui.hotkey('ctrl', 'a')
        #copy to clipboard
        pyautogui.hotkey('ctrl', 'c')
        #click in notepad++
        pyautogui.click(1800,800)
        #paste
        pyautogui.hotkey('ctrl', 'v')
        #save
        pyautogui.hotkey('ctrl', 'alt','s')
        #write the name
        pyautogui.typewrite(line + '.csv', interval=.1)
        #save
        pyautogui.click(1700,900)
        #close file
        pyautogui.hotkey('ctrl', 'w')


