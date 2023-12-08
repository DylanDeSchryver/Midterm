import tkinter as tk
from tkinter import *
from tkinter import messagebox
from sql_program import *
import requests  # pip install requests
import datetime
import os


def send_command(direction):  #eg. 'forward'
  ip = '192.168.1.28'  # uses ip address of raspberry pi
  url = f'http://192.168.1.28:4200/move'
  data = {
      'direction': direction
  }  # creates dictionary which stores the direction the tank should move in

  response = requests.post(url, json=data)
  if response.status_code == 200:  # 200 means it is successful
    print(f"Command '{direction}' sent successfully.")
  else:
    print(f"Failed to send command '{direction}'")


# Create global variables to store user information
user_info = {'name': '', 'last_name': '', 'username': '', 'password': ''}


def window():
  global root  # create tkinter window with labels and buttons
  root = Tk()
  root.geometry("600x400")
  root.title("Window")
  root.configure(bg="#ffffff")
  label2 = Label(root, text="Login or create an account.")
  label2.pack()
  add_button = Button(root, text='Create an Account', command=create) #calls create function to create an account
  add_button.pack()
  login_button = Button(root, text='Login', command=login) #calls login function to login to an account
  login_button.pack()
  button = Button(root, text='Save and Exit', command=root.destroy) #destroys window
  button.pack()
  root.mainloop()


def create():
  global root  # make the create account window with labels and entry fields
  root = Tk()
  root.geometry("600x400")
  root.title("Create an Account")
  root.configure(bg='white')

  name = Label(root, text="Name: ")
  name.pack()
  name_entry = Entry(root)
  name_entry.pack()

  last = Label(root, text="Last Name: ")
  last.pack()
  last_entry = Entry(root)
  last_entry.pack()

  user = Label(root, text="User: ")
  user.pack()
  user_entry = Entry(root)
  user_entry.pack()

  passw = Label(root, text="Password: ")
  passw.pack()
  passw_entry = Entry(root, show='*') #hides password with *
  passw_entry.pack()

  def save_info():
    # Save user information to global variables, then run save_sql(), which has access to the dictionary.
    user_info['name'] = name_entry.get() #gets first name
    user_info['last_name'] = last_entry.get() #gets last name
    user_info['username'] = user_entry.get() #gets username
    user_info['password'] = passw_entry.get() #gets passw
    save_sql()  # run save_sql
    root.destroy()  # close window

  save_button = Button(root, text='Save and Exit', command=save_info)
  save_button.pack()

  root.mainloop()


def login():  # make login window with entry fields and buttons
  global root
  root = Tk()
  root.geometry("600x400")
  root.title("Log In")

  user = Label(root, text="User: ")
  user.pack()
  user_entry = Entry(root)
  user_entry.pack()

  passw = Label(root, text="Password: ")
  passw.pack()
  passw_entry = Entry(root, show='*')
  passw_entry.pack()

  def check_login():  # check if the user name and passwords work.
    username = user_entry.get() #gets username
    password = passw_entry.get() #gets password
    key = get_sql(username, password) #runs get_sql with var username and password
    if key != []: #when running get_sql, if a username and password are found, matching the username and password passed to the get_sql function, key will be a list with the username and password, meaning the person does have an account, and can login.
      pass
    else:
      messagebox.showerror('Error', "Incorrect Username or Password.")
      root.destroy()

    name = first(username, password) #gets first name corresponding to the successful username and password

    # key will be the key which corresponds to the user and password in db, and the user and password entered in the login.

    if key != []:  # if the key does exist, open menu. this check is redundant, however it makes the code easier to read.
      root.destroy()
      loggedin(username, password, key, name) 

    else:  # else preswnt error and destory window
      messagebox.showerror('Error', "Incorrect Username or Password.")
      root.destroy()

  login_button = Button(root, text='Log In', command=check_login)
  login_button.pack()


def loggedin(username, password, key,
             name):  # currently do not need password, but maybe in future
  current_time = datetime.datetime.now() #gets current time
  today = current_time.strftime("%x") #gets current day
  today_time = current_time.strftime("%X")
  filename = username + ' ' + today + ' ' + today_time + '.txt'
  today = today.replace('/', '-') #replaces slashes with dashes because there was an error with the filename having a slash
  # Get the directory of the current script
  script_directory = os.path.dirname(__file__)

  # Construct the full path to the log file
  filename = f"{script_directory}/{username} {today} {today_time}.txt"
  
  with open(filename, 'w') as f:
    f.write(f'New Log File @{username}!') #create the new log file
    print("filename")

  def forward(): #called when pressing the forward button. Collects new day and time information, however re uses the old 'filename' variable to edit the log file. 
    current_time = datetime.datetime.now()
    log_message("Move Forward")
    today = current_time.strftime("%x")
    today_time = current_time.strftime("%X")
    today = today.replace('/', '-')
    with open(filename, 'at') as f: #opened for appending text
      f.write(f'\n{username}/Move Forward {today} {today_time}')

  def backward(): #called when pressing the backward button. Collects new day and time information, however re uses the old 'filename' variable to edit the log file. 
    current_time = datetime.datetime.now()
    log_message("Move Backward")
    today = current_time.strftime("%x")
    today_time = current_time.strftime("%X")
    today = today.replace('/', '-')
    with open(filename, 'at') as f:  #opened for appending text
      f.write(f'\n{username}/Move Backward {today} {today_time}')

  def left(): #called when pressing the left button. Collects new day and time information, however re uses the old 'filename' variable to edit the log file. 
    current_time = datetime.datetime.now()
    log_message("Turn Left")
    today = current_time.strftime("%x")
    today_time = current_time.strftime("%X")
    today = today.replace('/', '-')
    with open(filename, 'at') as f:  #opened for appending text
      f.write(f'\n{username}/Turn Left {today} {today_time}')

  def right(): #called when pressing the right button. Collects new day and time information, however re uses the old 'filename' variable to edit the log file. 
    current_time = datetime.datetime.now()
    log_message("Turn Right")
    today = current_time.strftime("%x")
    today_time = current_time.strftime("%X")
    today = today.replace('/', '-')
    with open(filename, 'at') as f:  #opened for appending text
      f.write(f'\n{username}/Turn Right {today} {today_time}')

  def stop(): #called when pressing the stop button. Collects new day and time information, however re uses the old 'filename' variable to edit the log file. 
    current_time = datetime.datetime.now()
    log_message("Stop")
    today = current_time.strftime("%x")
    today_time = current_time.strftime("%X")
    today = today.replace('/', '-')
    with open(filename, 'at') as f:  #opened for appending text
      f.write(f'\n{username}/Stop {today} {today_time}')

  def logout(): #called when pressing the logout button. Collects new day and time information, however re uses the old 'filename' variable to edit the log file. 
    current_time = datetime.datetime.now()
    log_message("Logged Out")
    root.destroy()
    window()
    today = current_time.strftime("%x")
    today_time = current_time.strftime("%X")
    today = today.replace('/', '-')
    with open(filename, 'at') as f:  #opened for appending text
      f.write(f'\n{username}/Logout {today} {today_time}')

  def log_message(message):
    current_text = log_label.cget(
        "text"
    )  # cget just gets the current values of the widget (log quadrant), similar to +=1
    new_text = f"{message}\n{current_text}" #combines new movement log with previous logs
    log_label.config(text=new_text) #inserts the new log with new movement log

  # Create the main window
  root = tk.Tk()
  root.geometry("800x600")
  root.title("Logged In")

  # Create frames for each part of the grid
  top_left_frame = tk.Frame(root, bg="white", width=400, height=300)
  top_right_frame = tk.Frame(root, bg="black", width=400, height=300)
  bottom_left_frame = tk.Frame(root,
                               relief=tk.SUNKEN,
                               borderwidth=2,
                               width=400,
                               height=300,
                               bg='pink')  # just makes empty frame look nice
  bottom_right_frame = tk.Frame(root, width=400, height=300)

  top_left_frame.grid(row=0, column=0, sticky="nsew")
  top_right_frame.grid(row=0, column=1, sticky="nsew")
  bottom_left_frame.grid(
      row=1, column=0,
      sticky="nsew")  # nsew just fills in all extra space within each frame
  bottom_right_frame.grid(row=1, column=1, sticky="nsew")

  # Place labels and buttons in the frames
  camera_label = tk.Label(top_left_frame, text="CAMERA")
  camera_label.pack()

  log_label = tk.Label(top_right_frame,
                       text=f"Welcome {name}",
                       fg="white",
                       bg="black",
                       anchor="nw")
  log_label.pack(fill="both", expand=True)

  button_frame = tk.Frame(top_right_frame, bg="black")
  button_frame.pack(side="bottom", fill="both", expand=True)

  forward_button = tk.Button(
      bottom_right_frame,
      text="   ^   ",
      # We use lamdba for the following, to send for eg. 'forward' back to the previous function send_command, we wouldnt be able to just do command = send_command('forward'), we need lambda.
      command=lambda: [send_command('forward'),
                       forward()])
  backward_button = tk.Button(
      bottom_right_frame,
      text="   v   ",
      command=lambda: [send_command('backward'),
                       backward()])
  left_button = tk.Button(
      bottom_right_frame,
      text="<   ",
      command=lambda: [send_command('left'), left()])
  right_button = tk.Button(
      bottom_right_frame,
      text="   >",
      command=lambda: [send_command('right'), right()
                       ])  # place move buttons, and call their functions
  stop_button = tk.Button(
      bottom_right_frame,
      text="   U+1F7E5   ",
      command=lambda: [send_command('stop'), stop()])
  logout_button = tk.Button(bottom_right_frame,
                            text="   Logout   ",
                            command=lambda: [send_command('stop'), logout()])

  forward_button.grid(row=0, column=1)
  backward_button.grid(row=2, column=1)
  left_button.grid(row=1, column=0)
  right_button.grid(row=1, column=2)
  stop_button.grid(row=1, column=1)
  logout_button.grid(row=2, column=2)

  root.grid_rowconfigure(0, weight=1)
  root.grid_rowconfigure(
      1, weight=1
  )  # this code makes it so everything has the same weight (power) so everything gets the same amount of space.
  root.grid_columnconfigure(0, weight=1)
  root.grid_columnconfigure(1, weight=1)

  # Make the log area fill the available space
  top_right_frame.pack_propagate(
      False
  )  # i googled this because the log frame was smaller than the camera frame?
  log_label.pack(fill="both", expand=True)

  root.mainloop()


def save():  # exit the windows and exit code
  global root
  root = Tk()
  root.geometry("600x400")
  root.title("Save and Exit")
  label3 = Label(root, text="")
  label3.pack()
  button = Button(root, text='Save and Exit', command=exit())
