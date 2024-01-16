import tkinter as tk
from tkinter import *
from tkinter import messagebox
from sql_program import *
import requests  # pip install requests
import datetime
import os


def send_command(direction):  #eg. 'forward'
  ip = '192.168.1.30'  # uses ip address of raspberry pi
  url = f'http://192.168.1.30:4200/move'
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
  global win  # create tkinter window with labels and buttons
  win = Tk()
  win.geometry("600x400")
  win.title("Window")
  win.configure(bg="#ffffff")
  label2 = Label(win, text="Login or create an account.")
  label2.pack()
  add_button = Button(win, text='Create an Account', command=(create))
  add_button.pack()
  login_button = Button(win, text='Login', command=(login))
  login_button.pack()
  button = Button(win, text='Save and Exit', command=win.destroy)
  button.pack()
  win.mainloop()


def create():
  win.destroy()
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
  passw_entry = Entry(root, show='*')
  passw_entry.pack()

  def save_info():
    # Save user information to global variables, then run save_sql(), which has access to the dictionary.
    user_info['name'] = name_entry.get()
    user_info['last_name'] = last_entry.get()
    user_info['username'] = user_entry.get()
    user_info['password'] = passw_entry.get()
    save_sql()  # run save_sql
    root.destroy()  # close window

  save_button = Button(root, text='Save and Exit', command=save_info)
  save_button.pack()

  root.mainloop()


def login():  # make login window with entry fields and buttons
  win.destroy()
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
    username = user_entry.get()
    password = passw_entry.get()
    key = get_sql(username, password)
    if key != []:
      pass
    else:
      messagebox.showerror('Error', "Incorrect Username or Password.")
      root.destroy()

    name = first(username, password)

    # key will be the key which corresponds to the user and password in db, and the user and password entered in the login.

    if key != []:  # if the key does exist, open menu
      root.destroy()
      loggedin(username, password, key, name)

    else:  # else preswnt error and destory window
      messagebox.showerror('Error', "Incorrect Username or Password.")
      root.destroy()

  login_button = Button(root, text='Log In', command=check_login)
  login_button.pack()


def loggedin(username, password, key,
             name):  # currently do not need password, but maybe in future
  current_time = datetime.datetime.now()
  today = current_time.strftime("%x")
  today_time = current_time.strftime("%X")
  filename = username + ' ' + today + ' ' + today_time + '.txt'
  today = today.replace('/', '-')
  # Get the directory of the current script
  script_directory = os.path.dirname(__file__)

  # Construct the full path to the log file
  filename = f"{script_directory}/{username} {today} {today_time}.txt"
  #stop
  with open(filename, 'w') as f:
    f.write(f'New Log File @{username}!')
    print("filename")

  def forward():
    current_time = datetime.datetime.now()
    log_message("Move Forward")
    today = current_time.strftime("%x")
    today_time = current_time.strftime("%X")
    today = today.replace('/', '-')
    with open(filename, 'at') as f:
      f.write(f'\n{username}/Move Forward {today} {today_time}')

  def backward():
    current_time = datetime.datetime.now()
    log_message("Move Backward")
    today = current_time.strftime("%x")
    today_time = current_time.strftime("%X")
    today = today.replace('/', '-')
    with open(filename, 'at') as f:
      f.write(f'\n{username}/Move Backward {today} {today_time}')

  def left():
    current_time = datetime.datetime.now()
    log_message("Turn Left")
    today = current_time.strftime("%x")
    today_time = current_time.strftime("%X")
    today = today.replace('/', '-')
    with open(filename, 'at') as f:
      f.write(f'\n{username}/Turn Left {today} {today_time}')

  def right():
    current_time = datetime.datetime.now()
    log_message("Turn Right")
    today = current_time.strftime("%x")
    today_time = current_time.strftime("%X")
    today = today.replace('/', '-')
    with open(filename, 'at') as f:
      f.write(f'\n{username}/Turn Right {today} {today_time}')

  def stop():
    current_time = datetime.datetime.now()
    log_message("Stop")
    today = current_time.strftime("%x")
    today_time = current_time.strftime("%X")
    today = today.replace('/', '-')
    with open(filename, 'at') as f:
      f.write(f'\n{username}/Stop {today} {today_time}')

  def logout():
    current_time = datetime.datetime.now()
    log_message("Logged Out")
    root.destroy()
    window()
    today = current_time.strftime("%x")
    today_time = current_time.strftime("%X")
    today = today.replace('/', '-')
    with open(filename, 'at') as f:
      f.write(f'\n{username}/Logout {today} {today_time}')

  def log_message(message):
    current_text = log_label.cget(
        "text"
    )  # cget just gets the current values of the widget, similar to +=1
    new_text = f"{message}\n{current_text}"
    log_label.config(text=new_text)

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

  log_label = tk.Label(bottom_right_frame,
                       text=f"Welcome {name}",
                       fg="white",
                       bg="black",
                       anchor="nw")
  log_label.pack(fill="both", expand=True)

  button_frame = tk.Frame(bottom_right_frame, bg="black")
  button_frame.pack(side="bottom", fill="both", expand=True)

  forward_button = tk.Button(
      top_right_frame,
      text="   ^   \nForward",
      # We use lamdba for the following, to send for eg. 'forward' back to the previous function send_command, we wouldnt be able to just do command = send_command('forward'), we need lambda.
      command=lambda: [send_command('forward'),
                       forward()])
  backward_button = tk.Button(
      top_right_frame,
      text="Backward\n   v   ",
      command=lambda: [send_command('backward'),
                       backward()])
  left_button = tk.Button(
      top_right_frame,
      text="<   Left",
      command=lambda: [send_command('left'), left()])
  right_button = tk.Button(
      top_right_frame,
      text="Right   >",
      command=lambda: [send_command('right'), right()
                       ])  # place move buttons, and call their functions
  stop_button = tk.Button(
      top_right_frame,
      text="   Stop   ",
      command=lambda: [send_command('stop'), stop()])
  logout_button = tk.Button(top_right_frame,
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
  bottom_right_frame.pack_propagate(
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
