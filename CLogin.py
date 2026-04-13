import time

from protocol import *
from CClientBL import *
from CRegister import *
# Set appearance mode and color theme

class CLogin:

    def __init__(self, root, previous_page, callback_login, callback_register):

        self.root = root
        self.root.title("Finance Plan")
        self.root.geometry("1100x700")

        self.previous_page = previous_page
        self.callback_login = callback_login
        self.callback_register = callback_register

        # Configure purple color scheme
        self.primary_color = ("#6A0DAD", "#2D1B4E")
        self.secondary_color = ("#8A2BE2", "#3E2A6D")
        self.accent_color = ("#9370DB", "#9B5DE5")
        self.text_color = "#FFFFFF"
        self.entry_color = ("#aa80d9","#c49fed")
        self.link_color = ("blue","#565fc7")


        # Set the background color
        self.root.configure(fg_color=self.primary_color)

        self.register_page = None

        # Time updating thread
        self.time_thread = threading.Thread(target=self.update_time, daemon=True)
        self.time_label = None

        # Client's IP and port
        self._entry_Port = PORT
        self._entry_IP = socket.gethostbyname(socket.gethostname())
        self.id_entry = None

        self.choose_flag = False
        self.form_flag = False
        self.face_id_flag = False

        # Camera
        self.video_capture = None
        self.face_frame = []
        self.face_encodings = []
        self.face_recognized = False
        self.face_matches = None
        self.id_exists = None

        self.white_bg = ctk.CTkImage(
            light_image=Image.open("Images/WhiteBG.png"),
            dark_image=Image.open("Images/WhiteBG.png"),
            size=(400, 300),
        )


    def create_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.secondary_color)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Bank name header
        self.Login_label = ctk.CTkLabel(
            self.main_frame,
            text="Sign In",
            font=("Arial", 30, "bold"),
            text_color=self.text_color,
        )
        self.Login_label.pack(pady=(40, 20))

        # Time display
        self.time_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Arial", 16),
            text_color="#ada6b3"
        )
        self.time_label.place(relx=0.01,rely=0.01, anchor="nw")

        self.register_button = ctk.CTkButton(
            self.main_frame,
            text="sign up",
            width=110,
            height=30,
            border_width=2,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            command=self.open_register_page

        )


        self.back_button = ctk.CTkButton(
            self.main_frame,
            text="back",
            font = ("Arial", 16, "underline"),
            fg_color="transparent",
            hover_color=self.secondary_color,
            border_width=0,
            text_color=self.text_color,
            width=0,
            command=self.open_previous_page

        )
        self.back_button.place(relx=0.01, rely=0.05, anchor="nw")

        # Choose Frame
        self.choose_frame = ctk.CTkFrame(
            self.main_frame,
            width=700,
            height=500,
            fg_color=self.secondary_color,
        )
        self.choose_label = ctk.CTkLabel(
            self.choose_frame,
            text="Choose your preferred way of Signing in:",
            font=("Arial", 20,"bold"),
            text_color=self.text_color,
        )
        self.choose_label.place(relx = 0.23, rely = 0.1)

        # Face ID button
        self.face_id_img = ctk.CTkImage(
            light_image=Image.open("Images/face_id.png"),
            dark_image=Image.open("Images/face_id.png"),
            size=(170, 170),
        )
        self.face_id_button = ctk.CTkButton(
            self.choose_frame,
            image= self.face_id_img,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            width=190,
            height=190,
            text="",
            command=self.open_face_id
        )

        self.face_id_label = ctk.CTkLabel(
            self.choose_frame,
            text="Face ID",
            font=("Arial", 18, "bold"),
            text_color=self.text_color,
        )
        self.face_id_button.place(relx = 0.2, rely = 0.2)
        self.face_id_label.place(relx=0.295, rely=0.6)

        # Form button
        self.form_img = ctk.CTkImage(
            light_image=Image.open("Images/form.png"),
            dark_image=Image.open("Images/form.png"),
            size=(170, 170),
        )
        self.form_button = ctk.CTkButton(
            self.choose_frame,
            image=self.form_img,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            width=190,
            height=190,
            text="",
            command=self.show_regular_login
        )
        self.form_label = ctk.CTkLabel(
            self.choose_frame,
            text="Regular Form",
            font=("Arial", 18, "bold"),
            text_color=self.text_color,
        )
        self.form_button.place(relx=0.53, rely=0.2)
        self.form_label.place(relx=0.58, rely=0.6)

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
            font=("Arial", 22, "bold"),
            text_color = self.text_color,

        )
        self.fce_id_result_label = ctk.CTkLabel(
            self.camera_frame,
            text="",
            font=("Arial", 20, "bold"),
            text_color=self.text_color,
        )
        self.submit_face_id_button = ctk.CTkButton(
            self.camera_frame,
            text="continue",
            width=80,
            height=30,
            font=("Arial", 18),
            border_width=2,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            command=self.submit_face_id_button,
        )
        self.id_error_message = ctk.CTkLabel(
            self.camera_frame,
            text="ID not found",
            font=("Arial",18,"bold"),
            text_color=self.text_color,
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
            text_color = self.text_color,
            width=0,
            command=self.try_again_later,
        )

        # Sign Up label
        self.sign_up_label = ctk.CTkLabel(
            self.choose_frame,
            text="Don't have an account?",
            font=("Arial", 15, "bold"),
            text_color = self.text_color,
        )
        self.second_sign_up_button = ctk.CTkButton(
            self.choose_frame,
            text="Sign Up",
            font=("Arial", 16, "underline"),
            fg_color="transparent",
            hover_color=self.secondary_color,
            border_width=0,
            text_color=self.link_color,
            width=0,
            command=self.open_register_page

        )
        self.sign_up_label.place(relx=0.33, rely=0.8)
        self.second_sign_up_button.place(relx=0.58, rely=0.8)

        self.show_choose_frame()

        self.empty_entry_error_message = ctk.CTkLabel(self.main_frame,text="Please enter all fields",font=("Arial",18,"bold"))
        self.submit_button = ctk.CTkButton(
            self.main_frame,
            text="Submit",
            width=150,
            height=40,
            font=("Arial",25),
            border_width=2,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            command=self.on_click_login,
        )


        # self.connection_status = ctk.CTkLabel(
        #     self.main_frame,
        #     text="connected",
        #     text_color = self.text_color,

        # )
        # self.connection_status.pack()
        # self.connection_status.place(relx=0.01, rely=1.0, anchor="sw")
        self.time_thread.start()



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

        return frame,textbox

    def show_choose_frame(self,):
        if not self.choose_flag:
            self.id_error_message.place_forget()
            self.back_button.place(relx=0.01, rely=0.05, anchor="nw")
            self.hide_regular_login()
            self.close_camera()
            self.choose_frame.place(relx = 0.17, rely = 0.15)
            self.choose_flag = True

    def hide_choose_frame(self,):
        if self.choose_flag:
            self.choose_frame.place_forget()
            self.choose_flag = False


    def show_regular_login(self):
        if not self.form_flag:
            self.hide_choose_frame()
            self.id_frame, self.id_entry = self.create_entry(self.main_frame, "ID",0.4,0.2)
            self.phone_number_frame, self.phone_number_entry = self.create_entry(self.main_frame, "Phone Number",0.4, 0.4)
            self.phone_error_message = ctk.CTkLabel(self.main_frame,text="Please enter numbers only")
            self.password_frame, self.password_entry = self.create_entry(self.main_frame, "Password",0.4, 0.6)
            self.submit_button.place(relx=0.45,rely=0.8)
            self.form_flag = True

    def hide_regular_login(self):
        if self.form_flag:
            self.id_frame.place_forget()
            self.phone_number_frame.place_forget()
            self.phone_error_message.pack_forget()
            self.password_frame.place_forget()
            self.submit_button.place_forget()
            self.form_flag = False

    def open_face_id(self):
        self.hide_choose_frame()
        self.camera_frame.place(relx= 0.17, rely=0.15)

        self.id_frame, self.id_entry = self.create_entry(self.camera_frame, "ID", 0.35, 0.4)
        self.submit_face_id_button.place(relx = 0.45, rely = 0.55)

    def submit_face_id_button(self):
        self.id_exists = None

        def return_answer():
            if self.id_exists != None:
                if self.id_exists:
                    self.id_error_message.place_forget()
                    self.open_camera()
                else:
                    self.id_error_message.configure(text=f"ID '{self.id_entry.get()}' not found")
                    self.id_error_message.place(relx=0.4, rely=0.65)
                    self.id_entry.delete(0, "end")
                    self.camera_label.after(1000, self.id_error_message.place_forget)
                    self.id_exists = None

                return
            else:
                self.camera_label.after(10, return_answer)

        self.id_check()
        return_answer()


    def open_camera(self):
        self.id_frame.place_forget()
        self.submit_face_id_button.place_forget()

        self.camera_label.place(relx = 0.2, rely = 0.15)
        self.camera_instructions_label.place(relx = 0.3, rely = 0.1)

        self.video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.timer = 500
        self.found_face_flag = False
        self.face_recognized = False
        self.face_matches = None

        def start_camera():
            self.back_button.place_forget()

            ret, frame = self.video_capture.read()
            if not ret:
                return

            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(frame, model="hog")  # Detects face from camera
            face_encodings = face_recognition.face_encodings(frame, face_locations)  # Encodes the face


            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                if len(face_locations) > 1:
                    cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)
                    self.camera_label.after(1500, lambda: more_than_one_face_detected(len(face_locations)))
                elif self.face_recognized:
                    if self.face_matches:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
                        cv2.putText(frame, "MATCH!", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
                        self.camera_label.after(1500, face_match_func)
                    else:
                        cv2.rectangle(frame, (left, top), (right, bottom), (255,0,0), 2)
                        cv2.putText(frame, "NOT MATCH!", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
                        self.camera_label.after(1500, face_not_match_func)
                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)



            captured_image = Image.fromarray(frame)
            face_image = ctk.CTkImage(
                light_image=captured_image,
                dark_image=captured_image,
                size=(400, 300),
            )
            self.camera_label.configure(image=face_image)
            self.camera_label.image = face_image

            if not self.found_face_flag and len(face_encodings) > 0 and self.timer < 450:
                self.found_face_flag = True
                self.face_encodings = face_encodings
                self.face_encodings = self.face_encodings[0].tolist()
                self.face_encodings = json.dumps(self.face_encodings)
                self.face_id_login()

            self.timer -= 10

            if self.timer <= 0:
                return

            self.camera_label.after(10, start_camera)


        def face_not_match_func():
            stop_camera()
            self.fce_id_result_label.configure(text="Face not recognized. please try again")
            self.fce_id_result_label.place(relx=0.25, rely=0.3)
            self.try_again_button.place(relx=0.47, rely=0.4)
            self.try_again_later_button.place(relx=0.42, rely=0.52)

        def face_match_func():
            stop_camera()
            self.fce_id_result_label.configure(text="Face recognized successfully!")
            self.fce_id_result_label.place(relx=0.33, rely=0.3)
            self.camera_label.after(2500, self.show_home_page)


        def more_than_one_face_detected(num):
            stop_camera()
            self.fce_id_result_label.configure(text=f"{num} face recognized. please try again")
            self.fce_id_result_label.place(relx=0.25, rely=0.3)
            self.try_again_button.place(relx=0.47, rely=0.4)
            self.try_again_later_button.place(relx=0.42, rely=0.52)

        def stop_camera():
            self.video_capture.release()
            cv2.destroyAllWindows()
            self.camera_instructions_label.place_forget()
            self.camera_label.place_forget()

        start_camera()

    def close_camera(self):
        self.camera_frame.place_forget()

    def try_again(self):
        self.hide_regular_login()
        self.fce_id_result_label.place_forget()
        self.try_again_button.place_forget()
        self.try_again_later_button.place_forget()
        self.open_camera()

    def try_again_later(self):
        self.camera_frame.place_forget()
        self.fce_id_result_label.place_forget()
        self.try_again_button.place_forget()
        self.try_again_later_button.place_forget()
        self.show_choose_frame()

    def open_previous_page(self):
        self.main_frame.pack_forget()
        self.previous_page.pack(fill="both", expand=True, padx=20, pady=20)

    def open_register_page(self):
        self.main_frame.pack_forget()

        if self.register_page == None:
            self.register_page = CRegister(self.root, self.main_frame, self.callback_register)
            self.register_page.run()
        else:
            self.register_page.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            self.register_page.show_form()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"{current_time}")
        self.root.after(1000, self.update_time)  # Update every second

    def show_page(self, next_frame, previous_frame):
        next_frame.pack(fill="both", expand=True, padx=20, pady=20)
        previous_frame.pack_forget()

    def show_home_page(self):
        self.close_camera()
        self.show_page(self.previous_page, self.main_frame)

    def run(self):
        self.create_ui()
        self.root.mainloop()


    def on_click_login(self):
        self.empty_entry_error_message.pack_forget()
        self.phone_error_message.pack_forget()

        flag = self.handle_error_messages()

        if flag:
            data = {"id": self.id_entry.get(),
                    "phone_number": self.phone_number_entry.get(),
                    "password": self.password_entry.get(),
            }
            self.callback_login(("LOGIN-1",data))

    def face_id_login(self):
        data = {"id": self.id_entry.get(),
                "face_encodings": self.face_encodings}

        self.callback_login(("LOGIN-2", data))

    def id_check(self):
        data = {"id": self.id_entry.get(),}
        self.callback_login(("CHECK_ID", data))

    def handle_error_messages(self):
        if self.id_entry.get() == "" or self.phone_number_entry.get() == "" or self.password_entry.get() == "":
            self.empty_entry_error_message.place(relx=0.4, rely=0.7)
            return False

        return True

if __name__ == "__main__":
    pass
