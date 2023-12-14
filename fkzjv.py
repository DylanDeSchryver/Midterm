# Place labels and buttons in the frames
camera_label = tk.Label(top_left_frame, text="CAMERA")
camera_label.pack()


# Function to update the camera feed
def update_camera_feed():
    global global_photo
    response = requests.get('http://192.168.1.28:4200/camera', stream=True)
    if response.status_code == 200:
        # Open the image using PIL
        image = Image.open(BytesIO(response.content))
        # Resize the image to fit the label
        image = image.resize((400, 300), resample=Image.LANCZOS)
        # Convert the image to PhotoImage format
        new_photo = ImageTk.PhotoImage(image)
        # Update the label with the new image
        camera_label.configure(image=new_photo)
        # Update the global variable to keep a reference
        global_photo = new_photo
        # Schedule the function to be called after 100 milliseconds (adjust as needed)
        root.after(100, update_camera_feed)


# Call the function to start updating the camera feed
update_camera_feed()
