# CCTV login automation - Selenium
The script opens a browser, logs into the CCTV system, opens a specific camera and runs it in full screen mode on the second monitor.  
This particular script is unlikely to be used by you, but I think it may help if you create your own similar script in selenium. I hope it will help you solve some problems or better understand Selenium

# Background story
One of the users at my work needed to have a view of the camera on the second monitor. This script is my idea to automate the process of starting the camera and prevent accidental closing of the browser window

# What I learned in this project
- How to use the Selenium framework
- Better understanding the impact of automation on the user's work, and how the user can unintentionally break the automation process
- Drawing simple forms in Python
- Working with threading in Python

# Technologies used
- Python
- Selenium framework
- ChromeDriver

# Features of my automatization

- Checks whether the PC that runs the script, is in the company domain
- Username and password for the CCTV system is automatically entered on the page but an additional (different) password is required to run the script for security reasons - this is the only thing the user needs to do 
- It opens the browser in kiosk mode so that it is not possible to exit full-screen mode
- After opening, it moves the browser to the second monitor
- Changes the background color from white to black for eye comfort
- My camera system pauses the video if it does not detect any activity for 5 minutes. Therefore, the script moves the "virtual mouse" between the two buttons visible on the screen (it does not affect the user's mouse)
- If the window is minimized the script will automatically maximize it
- It automatically closes every newly opened tab
- One note - the file must be in ".pyw" format, not ".py", otherwise a console window will appear
- At the end you need to export the script to an exe file using e.g., “auto-py-to-exe”  
https://pypi.org/project/auto-py-to-exe/
