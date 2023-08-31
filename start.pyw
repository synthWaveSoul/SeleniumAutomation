import pywintypes   # needed for compiler to exe file
from time import sleep
from xmlrpc.client import Boolean, boolean
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import win32gui
import win32con
import threading
import socket
import tkinter as tk
import tkinter.simpledialog
import tkinter.messagebox
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.chrome.service import Service as ChromeService

 # check if PC is in domain, program will run only if it is in your domain
full_name = socket.getfqdn()    # returns pcName.domainName
domain_name = full_name[-11:]   # leaves last 11 characters, should return - "domain.name"
if domain_name == "domain.name":
    pass
else:
    tkinter.messagebox.showerror(title="Violation", message="Not in your Company")
    exit()

 # infinite password request until enter the correct one
correct_password = "password_to_access_app"
error_title = "ERROR"
error_message = "Please enter correct password"

def draw_pass_box():
    tk.Tk().withdraw()
    entered_password = tkinter.simpledialog.askstring("Password", "Enter password for gate camera:", show='*')
    if entered_password == correct_password:
        pass
    else:
        tkinter.messagebox.showerror(title=error_title, message=error_message)
        draw_pass_box()
    
draw_pass_box()

 # username and password used in login process on the webpage
username = "username"
password = "password"

c = webdriver.ChromeOptions()
c.add_argument("--incognito")
c.add_argument("--kiosk")
c.add_experimental_option("excludeSwitches", ['enable-automation'])  # hide "chrome is being controlled by automated software" ribbon

chrome_service = ChromeService('chromedriver')
chrome_service.creationflags = CREATE_NO_WINDOW # prevent logging to console

browser = webdriver.Chrome(options=c, service=chrome_service)

 # get ID of chrome window
hwnd = win32gui.GetForegroundWindow()

browser.implicitly_wait(30)
browser.get("URL to your page")

browser.implicitly_wait(30)
username_input = browser.find_element("name", "email")
username_input.send_keys(username)

login_btn = browser.find_element("xpath", "//button[@type='submit']")
login_btn.click()

browser.implicitly_wait(30)
password_input = browser.find_element("name", "password")
password_input.send_keys(password)

continue_btn = browser.find_element("xpath", "//button[@type='submit']")
continue_btn.click()

browser.implicitly_wait(30)
cam_url = "URL to camera"
browser.get(cam_url)

 # get ID of the tab
original_window = browser.current_window_handle

browser.implicitly_wait(30)
 # move window to second monitor
browser.set_window_position(2000, 0)

browser.implicitly_wait(30)
browser.maximize_window()

 # goes full window mode
def go_full():
    browser.implicitly_wait(30)
    is_exists_full_btn_1 = browser.find_elements("xpath", "//button[@class='sc-hBMVcZ sc-hHEjAm yFckF eGEZbi']").__sizeof__() > 0
    if is_exists_full_btn_1:
        full_window_btn = browser.find_element("xpath", "//button[@class='sc-hBMVcZ sc-hHEjAm yFckF eGEZbi']")
        full_window_btn.click()
    else:
        go_full()
go_full()

 # change title of window - now it is "your URL - Google Chrome"
browser.implicitly_wait(30)
browser.execute_script('document.title = "your_name";')

 # change frame background color from white to black
browser.implicitly_wait(30)
script_background_color = "document.getElementsByClassName('liveVideoContainer__vxTfI')[0].style.backgroundColor = 'black';"
browser.execute_script(script_background_color)

stop_thread = threading.Event()

 # loop moving mouse over different elements to prevent pause video - after 5 min of not moving mouse video is paused
move_element = browser.find_element("xpath", "//button[@class='sc-hBMVcZ sc-hHEjAm cukmPM eGEZbi']")
ActionChains(browser).move_to_element(move_element).perform()
def background_mouse_movement():
    while True:
        if stop_thread.is_set():
            break
        sleep(30)
        is_exists_full_btn = browser.find_elements("xpath", "//button[@class='sc-hBMVcZ sc-hHEjAm cukmPM eGEZbi']").__sizeof__() > 0
        if is_exists_full_btn:
            btn_1 = browser.find_element("xpath", "//button[@class='sc-hBMVcZ sc-hHEjAm cukmPM eGEZbi']")
            ActionChains(browser).move_to_element(btn_1).perform()
        sleep(30)
        is_exists_move_element = browser.find_elements("xpath", "//button[@class='sc-hBMVcZ sc-hHEjAm cukmPM eGEZbi']").__sizeof__() > 0
        if is_exists_move_element:
            btn_2 = browser.find_element("xpath", "//button[@class='sc-hBMVcZ sc-hHEjAm cukmPM eGEZbi'][1]")
            ActionChains(browser).move_to_element(btn_2).perform()

background_1 = threading.Thread(name='name_background_1', target=background_mouse_movement)
background_1.start()


 # chek if window is minimized, if yes then maximize it
def prevent_minimize():
    while True:
        if stop_thread.is_set():
            break
        window_state = win32gui.IsIconic(hwnd)    # 1 - minimized, 2 - maximized
        if window_state == 1:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        sleep(1)

background_2 = threading.Thread(name='name_background_2', target=prevent_minimize)
background_2.start()


 # close any new opened tabs
def tabs_count_check():
    while True:
        if stop_thread.is_set():
            break
        tabs = browser.window_handles
        tabs_count = len(tabs)
        if tabs_count > 1:
            browser.switch_to.window(browser.window_handles[1])
            browser.close()
            browser.switch_to.window(original_window)
        sleep(1)

background_3 = threading.Thread(name='name_background_3', target=tabs_count_check)
background_3.start()


 # stop all threads
def chrome_open_check():
    while True:
        if stop_thread.is_set():
            break
        is_open = win32gui.IsWindow(hwnd)   # 1 - open,  0 - closed
        if is_open == 0:
            stop_thread.set()
            background_1.join()
            background_2.join()
            background_3.join()
            background_4.join()
        sleep(1)

background_4 = threading.Thread(name='name_background_4', target=chrome_open_check)
background_4.start()
