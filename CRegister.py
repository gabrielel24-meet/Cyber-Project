import time

from fontTools.merge import timer

from protocol import *
from CClientBL import *

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class CRegister:

    def __init__(self, root, previous_page, callback_register):

        self.root = root
        self.root.title("Purple Trust Bank")
        self.root.geometry("1100x700")

        self.previous_page = previous_page
        self.callback_register = callback_register

        # Configure purple color scheme
        self.primary_color = ("#6A0DAD", "#2D1B4E")
        self.secondary_color = ("#8A2BE2", "#3E2A6D")
        self.accent_color = ("#9370DB", "#9B5DE5")
        self.text_color = "#FFFFFF"
        self.entry_color = ("#aa80d9","#c49fed")


        # Set the background color
        self.root.configure(fg_color=self.primary_color)

        # Time updating thread
        self.time_thread = threading.Thread(target=self.update_time, daemon=True)
        self.time_label = None

        # Client's IP and port
        self._entry_Port = PORT
        self._entry_IP = socket.gethostbyname(socket.gethostname())

        # Camera
        self.video_capture = None
        self.face_frame = []
        self.face_encodings = []

        self.white_bg = ctk.CTkImage(
            light_image= Image.open("Images/WhiteBG.png"),
            dark_image= Image.open("Images/WhiteBG.png"),
            size=(400, 300),
        )


    def create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.secondary_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Bank name header
        self.Register_label = ctk.CTkLabel(
            self.main_frame,
            text="Sign up",
            font=("Arial", 25, "bold"),
            text_color= self.text_color,
        )
        self.Register_label.pack(pady=(40, 20))

        # Time display
        self.time_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 16),
            text_color= self.text_color,
        )
        self.time_label.place(relx=0.01,rely=0.01, anchor="nw")

        self.back_button = ctk.CTkButton(
            self.main_frame,
            text="back",
            font=("Arial", 16, "underline"),
            fg_color="transparent",
            hover_color=self.secondary_color,
            border_width=0,
            text_color="white",
            width=0,
            command=self.open_previous_page
        )
        self.back_button.place(relx=0.01, rely=0.05, anchor="nw")


        # Face ID button
        self.face_id_img = ctk.CTkImage(
            light_image=Image.open("Images/face_id.png"),
            dark_image=Image.open("Images/face_id.png"),
            size=(90, 90),
        )
        self.face_id_button = ctk.CTkButton(
            self.main_frame,
            image=self.face_id_img,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            width=100,
            height=100,
            text="",
            command=self.open_camera
        )
        self.face_id_label = ctk.CTkLabel(
            self.main_frame,
            text="Face ID",
            font=("Arial", 18, "bold"),
            text_color= self.text_color,
        )


        self.submit_button = ctk.CTkButton(
            self.main_frame,
            text="Submit",
            width=150,
            height=40,
            font=("Arial",25),
            border_width=2,
            fg_color=self.primary_color,
            command=self.on_click_register,
        )


        self.connection_status = ctk.CTkLabel(
            self.main_frame,
            text="connected",
            text_color=self.text_color,
        )

        # Camera
        self.camera_frame = ctk.CTkFrame(
            self.main_frame,
            width=700,
            height=500,
            fg_color=self.secondary_color,
        )
        self.camera_label = ctk.CTkLabel(
            self.camera_frame,
            text="",
            width=450,
            height=350,
        )
        self.camera_instructions_label = ctk.CTkLabel(
            self.camera_frame,
            text="Please look into the camera:",
            font=("Arial",22,"bold"),
            text_color= self.text_color
        )
        self.face_id_result_label = ctk.CTkLabel(
            self.camera_frame,
            text="",
            font=("Arial", 20, "bold"),
            text_color = self.text_color,
        )

        try_again_img = ctk.CTkImage(
            light_image=Image.open("Images/try_again.png"),
            dark_image=Image.open("Images/try_again.png"),
            size=(30, 30),
        )

        self.try_again_button = ctk.CTkButton(
            self.camera_frame,
            image=try_again_img,
            text="",
            width=20,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            command=self.try_again
        )

        self.try_again_later_button = ctk.CTkButton(
            self.camera_frame,
            text="try again later",
            font=("Arial", 18, "underline"),
            fg_color="transparent",
            hover_color=self.secondary_color,
            border_width=0,
            text_color="white",
            width=0,
            command=self.try_again_later
        )

        self.connection_status.pack()
        self.connection_status.place(relx=0.01, rely=1.0, anchor="sw")
        self.time_thread.start()
        self.create_form()


    def create_entry(self, parent, label_text, x,y):
        frame = ctk.CTkFrame(parent, fg_color=self.secondary_color)
        frame.place(relx=x, rely=y)

        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=("Arial", 15, "bold"),
            text_color=self.text_color,

        )
        label.pack(anchor="w", padx=10)

        textbox = ctk.CTkEntry(
            frame,
            width=220,
            height=25,
            border_width=1,
            border_color="white",
            text_color="black",
            fg_color=self.entry_color,
        )
        textbox.pack()

        return frame, textbox

    def create_form(self):
        self.first_name_frame, self.first_name_entry  = self.create_entry(self.main_frame, "First Name", 0.2, 0.2)
        self.last_name_frame, self.last_name_entry = self.create_entry(self.main_frame, "Last Name", 0.2, 0.4)

        self.id_frame,  self.id_entry = self.create_entry(self.main_frame, "ID", 0.2, 0.6)
        self.id_error_message = ctk.CTkLabel(self.main_frame, text_color= self.text_color, text="ID taken")

        self.phone_number_frame, self.phone_number_entry = self.create_entry(self.main_frame, "Phone Number", 0.6, 0.2)
        self.phone_error_message = ctk.CTkLabel(self.main_frame, text_color= self.text_color, text="Phone Number taken")

        self.password_frame, self.password_entry = self.create_entry(self.main_frame, "Password", 0.6, 0.4)
        self.face_id_label.place(relx=0.67, rely=0.52)
        self.face_id_button.place(relx=0.65, rely=0.57)

        self.submit_button.place(relx=0.45,rely=0.8)

    def show_form(self):
        self.back_button.place(relx=0.01, rely=0.05, anchor="nw")
        self.first_name_frame.place(relx = 0.2, rely = 0.2)
        self.last_name_frame.place(relx = 0.2, rely = 0.4)
        self.id_frame.place(relx = 0.2, rely = 0.6)
        self.phone_number_frame.place(relx = 0.6, rely = 0.2)
        self.password_frame.place(relx = 0.6, rely = 0.4)
        print(len(self.face_encodings))
        if len(self.face_encodings) != 0:
            self.face_id_label.configure(text="Face ID ✅")
            self.face_id_label.place(relx=0.61, rely=0.63)
            self.try_again_button.place(relx=0.7, rely=0.63)
        else:
            self.face_id_label.place(relx=0.67, rely=0.52)
            self.face_id_button.place(relx=0.65, rely=0.57)

        self.submit_button.place(relx=0.45,rely=0.8)

    def hide_form(self):
        self.first_name_frame.place_forget()
        self.last_name_frame.place_forget()
        self.id_frame.place_forget()
        self.phone_number_frame.place_forget()
        self.password_frame.place_forget()
        self.face_id_button.place_forget()
        self.face_id_label.place_forget()
        self.submit_button.place_forget()

    def open_camera(self):
        self.hide_form()

        self.camera_frame.place(relx= 0.17, rely=0.15)
        self.camera_label.place(relx = 0.2, rely = 0.15)
        self.camera_instructions_label.place(relx = 0.3, rely = 0.1)

        self.video_capture = cv2.VideoCapture(0)
        self.timer = 5000

        def start_camera():

            def show_flash_effect():
                self.camera_label.configure(image=self.white_bg)
                self.camera_label.image = self.white_bg

                self.camera_label.after(100, show_captured_image)

            def show_captured_image():
                self.camera_label.configure(image=self.face_img)
                self.camera_label.image = self.face_img

                self.camera_label.after(1500, stop_camera)

            self.back_button.place_forget()

            ret, frame = self.video_capture.read()
            if not ret:
                return

            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if self.timer < 4000 and self.timer > 1000:
                cv2.putText(frame, f"{self.timer//1000}", (550,80), cv2.FONT_HERSHEY_SIMPLEX,3,color=(255,255,255), thickness=10)
            captured_image = Image.fromarray(frame)

            face_image = ctk.CTkImage(
                light_image=captured_image,
                dark_image=captured_image,
                size=(400, 300),
            )
            self.camera_label.configure(image=face_image)
            self.camera_label.image = face_image
            self.timer -= 20

            if self.timer <= 950:
                self.face_frame = frame
                self.face_img = face_image
                show_flash_effect()
                return

            self.camera_label.after(10, start_camera)


        def stop_camera():
            self.video_capture.release()
            cv2.destroyAllWindows()
            self.camera_instructions_label.place_forget()
            self.camera_label.place_forget()
            analyze_frame()

        def analyze_frame():
            self.face_locations = face_recognition.face_locations(self.face_frame, model="hog")
            self.face_encodings = face_recognition.face_encodings(self.face_frame, self.face_locations)  # Encodes the face

            if len(self.face_locations) == 0:
                self.face_id_result_label.configure(text="Face not recognized. please try again:")
                self.face_id_result_label.place(relx = 0.25, rely = 0.3)
                self.try_again_button.place(relx = 0.47, rely = 0.4)
                self.try_again_later_button.place(relx = 0.42, rely = 0.52)
            elif len(self.face_locations) > 1:
                self.face_id_result_label.configure(text=f"{len(self.face_locations)} Faces recognized. please try again:")
                self.face_id_result_label.place(relx = 0.23, rely = 0.3)
                self.try_again_button.place(relx = 0.47, rely = 0.4)
                self.try_again_later_button.place(relx = 0.42, rely = 0.52)
            else:
                self.face_id_result_label.configure(text="Face detected successfully!")
                self.face_encodings = self.face_encodings[0].tolist()
                self.face_encodings = json.dumps(self.face_encodings)
                self.face_id_result_label.place(relx = 0.33, rely = 0.3)
                self.camera_label.after(1500,self.close_camera)

        start_camera()

    def close_camera(self):
        self.camera_frame.place_forget()
        self.show_form()


    def try_again(self):
        self.hide_form()
        self.face_id_result_label.place_forget()
        self.try_again_button.place_forget()
        self.try_again_later_button.place_forget()
        self.open_camera()

    def try_again_later(self):
        self.camera_frame.place_forget()
        self.face_id_result_label.place_forget()
        self.try_again_button.place_forget()
        self.try_again_later_button.place_forget()
        self.show_form()

    def open_previous_page(self):
        self.main_frame.pack_forget()
        self.previous_page.pack(fill="both", expand=True, padx=20, pady=20)

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"{current_time}")
        self.root.after(1000, self.update_time)  # Update every second

    def handle_register_message(self, response):
        if response == "ID_PHONE_TAKEN":
            self.id_error_message.place(relx=0.2, rely=0.68)
            self.phone_error_message.place(relx=0.6, rely=0.28)
        if response == "PHONE_TAKEN":
            self.phone_error_message.place(relx=0.6, rely=0.28)
        if response == "ID_TAKEN":
            self.id_error_message.place(relx=0.2, rely=0.68)
        if response == "REGISTERED":
            self.main_frame.pack_forget()
            self.previous_page.pack(fill="both", expand=True, padx=20, pady=20)



    def run(self):
        self.create_ui()
        self.root.mainloop()

    def on_click_register(self):
        self.phone_error_message.place_forget()
        self.id_error_message.place_forget()

        data = {"first_name": self.first_name_entry.get(),
                "last_name":self.last_name_entry.get(),
                "id": self.id_entry.get(),
                "phone_number": self.phone_number_entry.get(),
                "password": self.password_entry.get(),
                "face_encodings": self.face_encodings}

        self.callback_register(data)



if __name__ == "__main__":
    pass