import os.path
import subprocess
import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
import sys
import os


python_executable = os.path.join('venv', 'Scripts', 'python.exe')
face_recognition_path = os.path.join('venv', 'Scripts', 'face_recognition.exe')

face_recognition_path = os.path.abspath(face_recognition_path)


class App:

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = os.path.expanduser("~\\Desktop\\my_database")
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def release_camera(self):
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()

    def login(self):
        unknown_img_path = '.\\.tmt.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        cmd = ['face_recognition', self.db_dir, unknown_img_path]
        print("Executing command:", cmd)
        output = str(subprocess.check_output([python_executable, face_recognition_path, os.path.abspath(self.db_dir), unknown_img_path]))

        name = output.split(',')[1][:-5]
        # print(name)

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box(':(', 'Unknown User! Please register new user or Try Again.')
        else:
            util.msg_box('WELCOME BACK', 'Welcome, {}'.format(name))

            self.release_camera()

            self.main_window.withdraw()


            subprocess.Popen([sys.executable,"dashboard.py"])
            # self.main_window.destroy()


        os.remove(unknown_img_path)


    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept',
                                                                      'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)
        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again',
                                                                      'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please! \nInput Username Below:')
        self.label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()


    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)

        util.msg_box('SUCCESS!', 'User was registered successfully !')

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()
