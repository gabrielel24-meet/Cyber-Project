from CServerBL import *
from protocol import *


class CServerGUI(CServerBL):

    def __init__(self, host, port):
        super().__init__(host,port)

        # Attributes
        self._root = None
        self._canvas = None
        self._img_bg = None
        self._img_btn = None


        self._btn_start = None
        self._btn_stop = None

        self._escape = None

        # GUI initialization
        self.create_ui()

    def create_ui(self):

        self._root = tk.Tk()
        self._root.title("Server GUI")

        self._img_bg = PhotoImage(file=BG_IMAGE)
        img_width = 900
        img_height = 400

        self._root.geometry(f'{img_width}x{img_height}')
        self._root.resizable(True,True)

        self._canvas = tk.Canvas(self._root)
        self._canvas.config(width=img_width,height=img_height)
        self._canvas.pack(fill='both',expand=True)
        self._canvas.create_image(0,0,anchor="nw",image=self._img_bg)


        self._img_btn = PhotoImage(file=BTN_IMAGE)
        img_btn_w = self._img_btn.width()
        img_btn_h = self._img_btn.height()

        self._btn_start = tk.Button(self._canvas,text="Start",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                    width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0,
                                    command=self.on_click_start)
        self._btn_start.place(relx=0.45,rely=0.3)

        self._btn_stop = tk.Button(self._canvas,text="Stop",font=FONT_BUTTON,fg="#c0c0c0",compound="center",
                                   width=img_btn_w,height=img_btn_h,image=self._img_btn,bd=0,
                                   command=self.on_click_stop,state="disabled")
        self._btn_stop.place(relx=0.45,rely=0.5)


    def run(self):
        try:
            self._root.mainloop()
        except KeyboardInterrupt as e:
            pass

    def on_click_start(self):
        self._btn_start.config(state="disabled")
        self._btn_stop.config(state="normal")

        self.stop_event.clear()
        self._server_thread = threading.Thread(target=self.start_server, daemon=True)
        self._server_thread.start()

    def on_click_stop(self):
        self._btn_start.config(state="normal")
        self._btn_stop.config(state="disabled")
        self.stop_server()



if __name__ == "__main__":
    server = CServerGUI(SERVER_HOST, PORT)
    server.run()
