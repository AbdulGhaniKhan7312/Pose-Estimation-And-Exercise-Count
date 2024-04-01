from customtkinter import *
from PIL import Image
import tkinter
import requests
from CTkTable import CTkTable
from CTkMessagebox import CTkMessagebox
import os

class App(CTk):

    def __init__(self, **kw):
        super().__init__( **kw)
        self.geometry("750x550")
        self.resizable(0,0)
        set_appearance_mode("dark")

        self.build_sidebar_ui()

        self.main_view = CTkFrame(master=self, fg_color="#204B6B", corner_radius=0, width=580, height=550)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left")

        self.switch_main_view("LOGIN")
        
    def build_sidebar_ui(self):
        sidebar_frame = CTkFrame(master=self, fg_color="#4385B7",  width=170, height=550, corner_radius=0)
        sidebar_frame.pack_propagate(0)
        sidebar_frame.pack(fill="y", anchor="w", side="left")

        logo_img_data = Image.open("Gym.png")
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(150,150))

        CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

        self.sidebar_workout_window_btn = CTkButton(master=sidebar_frame, text="Workout Window", fg_color="transparent", font=("Arial Bold", 14), hover_color="#204B6B", anchor="w", command=lambda: self.switch_main_view("WORKOUT_WINDOW"))

        self.sidebar_create_order_btn = CTkButton(master=sidebar_frame, text="Add Data", fg_color="transparent", font=("Arial Bold", 14), hover_color="#204B6B", anchor="w", command=lambda: self.switch_main_view("CREATE_ORDER"))

        self.sidebar_all_orders_btn = CTkButton(master=sidebar_frame, text="User Data", fg_color="transparent", font=("Arial Bold", 14), hover_color="#204B6B", anchor="w", command=lambda: self.switch_main_view("ALL_ORDERS"))

        self.sidebar_login_btn = CTkButton(master=sidebar_frame, text="Login", fg_color="transparent", font=("Arial Bold", 14), hover_color="#204B6B", anchor="w", command=lambda: self.switch_main_view("LOGIN"))
 

    def clear_main_view(self):
        for child in self.main_view.winfo_children():
            child.destroy()

    def switch_main_view(self, view):
        self.view = view
        self.clear_main_view()

        for btn in [self.sidebar_all_orders_btn, self.sidebar_create_order_btn, self.sidebar_login_btn, self.sidebar_workout_window_btn]:
            btn.configure(fg_color="transparent")

        if self.view == "CREATE_ORDER":
            self.build_create_order_ui()
            self.sidebar_create_order_btn.configure(fg_color="#204B6B")

            self.sidebar_login_btn.pack_forget()
            self.sidebar_create_order_btn.pack(anchor="center", ipady=5, pady=(30, 0))
            self.sidebar_all_orders_btn.pack(anchor="center", ipady=5, pady=(15, 0))
            self.sidebar_workout_window_btn.pack(anchor="center", ipady=5, pady=(15, 0))

        elif self.view == "ALL_ORDERS":
            self.build_all_orders_ui()
            self.sidebar_all_orders_btn.configure(fg_color="#204B6B")

            self.sidebar_login_btn.pack_forget()
            self.sidebar_create_order_btn.pack(anchor="center", ipady=5, pady=(30, 0))
            self.sidebar_all_orders_btn.pack(anchor="center", ipady=5, pady=(15, 0))
            self.sidebar_workout_window_btn.pack(anchor="center", ipady=5, pady=(15, 0))

        elif self.view == "LOGIN":
            self.build_login_ui()
            self.sidebar_login_btn.configure(fg_color="#204B6B")

            self.sidebar_login_btn.pack(anchor="center", ipady=5, pady=(15, 0))
            self.sidebar_create_order_btn.pack_forget()
            self.sidebar_all_orders_btn.pack_forget()

        elif self.view == "WORKOUT_WINDOW":
            self.build_workout_window_ui()
            self.sidebar_workout_window_btn.configure(fg_color="#204B6B")

            self.sidebar_login_btn.pack_forget()
            self.sidebar_create_order_btn.pack(anchor="center", ipady=5, pady=(30, 0))
            self.sidebar_all_orders_btn.pack(anchor="center", ipady=5, pady=(15, 0))
            self.sidebar_workout_window_btn.pack(anchor="center", ipady=5, pady=(15, 0))
                
    def create_order(self):
        url = "https://firestore.googleapis.com/v1/projects/fitbox-gui/databases/(default)/documents/userInfo"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        input_data = {
            "fields": {
                "Date": {
                    "stringValue": self.date.get()
                },
                "Time": {
                    "integerValue": self.workoutTime.get()
                },
                "Weight": {
                    "integerValue": self.weight.get()
                },
                "Calories": {
                    "integerValue": self.kcal.get()
                },
                "Workouts": {
                    "integerValue": self.total.get()
                }
            }
        }

        response = requests.post(url, json=input_data, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            CTkMessagebox(title="Success", message="Data Added successfully", icon="check")
        else:
            error_message = response_data["error"]["message"]
            CTkMessagebox(title="Error", message=error_message, icon="cancel")

    def build_create_order_ui(self):
        CTkLabel(master=self.main_view, text="Add Data", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

        CTkLabel(master=self.main_view, text="Date", font=("Arial Bold", 17), text_color="#fff").pack(anchor="nw", pady=(25,0), padx=27)

        self.date = CTkEntry(master=self.main_view, fg_color="#F0F0F0", text_color="#000", border_width=0)
        self.date.pack(fill="x", pady=(12,0), padx=27, ipady=10)

        grid = CTkFrame(master=self.main_view, fg_color="transparent")
        grid.pack(fill="both", padx=27, pady=(31,0))

        CTkLabel(master=grid, text="Workout Time (mins)", font=("Arial Bold", 17), text_color="#fff", justify="left").grid(row=0, column=0, sticky="w")
        self.workoutTime = CTkEntry(master=grid, fg_color="#F0F0F0", text_color="#000", border_width=0, width=250)
        self.workoutTime.grid(row=1, column=0, ipady=10)

        CTkLabel(master=grid, text="Weight (kg)", font=("Arial Bold", 17), text_color="#fff", justify="left").grid(row=0, column=1, sticky="w", padx=(25,0))
        self.weight = CTkEntry(master=grid, fg_color="#F0F0F0", text_color="#000", border_width=0, width=250)
        self.weight.grid(row=1, column=1, ipady=10, sticky='w', padx=(25,0))

        grid = CTkFrame(master=self.main_view, fg_color="transparent")
        grid.pack(fill="both", padx=27, pady=(31,0))

        CTkLabel(master=grid, text="Calories Burnt (kcal)", font=("Arial Bold", 17), text_color="#fff", justify="left").grid(row=0, column=0, sticky="w")
        self.kcal = CTkEntry(master=grid, fg_color="#F0F0F0", text_color="#000", border_width=0, width=250)
        self.kcal.grid(row=1, column=0, ipady=10)

        CTkLabel(master=grid, text="Total Workouts", font=("Arial Bold", 17), text_color="#fff", justify="left").grid(row=0, column=1, sticky="w", padx=(25,0))
        self.total = CTkEntry(master=grid, fg_color="#F0F0F0", text_color="#000", border_width=0, width=250)
        self.total.grid(row=1, column=1, ipady=10, sticky='w', padx=(25,0))

        CTkButton(master=self.main_view, text="Add Data", width=300, font=("Arial Bold", 17), hover_color="#B0510C", fg_color="#EE6B06", text_color="#fff", command=self.create_order).pack(fill="both", side="bottom", pady=(0, 25), ipady=10, padx=(27,27))

    def update_quantity(self, new_quantity):
        if new_quantity < 1:
            return

        self.quantity = new_quantity
        self.quantity_label.configure(text=str(self.quantity).zfill(2))

    def query_all_orders(self):
        url = "https://firestore.googleapis.com/v1/projects/fitbox-gui/databases/(default)/documents/userInfo"

        params = {
            "mask.fieldPaths": ["Date", "Time", "Weight", "Calories", "Workouts"]
        }

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        response = requests.get(url, params=params, headers=headers)
        response_data = response.json()

        table_data = [
            ["Date", "Workout Time (mins)", "Weight (kg)", "Calories Burnt (kcal)", "Total Workouts"],
            # ["MacBook Pro", "John Doe", "123 Main St", "Shipped", "1"],
            # ["Galaxy S21", "Jane Smith", "456 Park Ave", "Delivered", "2"],
            # ["PlayStation 5", "Bob Johnson", "789 Broadway", "Processing", "1"],
        ]

        for doc in response_data["documents"]:
            row = []
            if "fields" in doc:
                fields = doc["fields"]
                row.append(fields["Date"]["stringValue"])
                row.append(fields["Time"]["integerValue"])
                row.append(fields["Weight"]["integerValue"])
                row.append(fields["Calories"]["integerValue"])
                row.append(fields["Workouts"]["integerValue"])
            
                table_data.append(row)

        print(response_data)
        
        return table_data
    
    def build_all_orders_ui(self):
        table_data = self.query_all_orders()
        
        CTkLabel(master=self.main_view, text="User Data", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

        table_frame = CTkScrollableFrame(master=self.main_view, fg_color="transparent")
        table_frame.pack(expand=True, fill="both", padx=27, pady=21)

        table = CTkTable(master=table_frame, column=5, values=table_data, font=("Arial", 11), text_color="#000", header_color="#F6830D", colors=["#FFCD32", "#f8b907"])
        table.pack(expand=True)

    

    def build_workout_window_ui(self):
        CTkLabel(master=self.main_view, text="Workout Window", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)

        def runDumbbell():
            os.system('python dumbbell.py')

        def runPushups():
            os.system('python pushups.py')

        def runShoulderPress():
            os.system('python shoulderPress.py')

        def runSitups():
            os.system('python situps.py')

        def runSquats():
            os.system('python squats.py')

        # Button 1
        btn1 = CTkButton(master=self.main_view, text="Run Dumbbell Exercise", width=300, font=("Arial Bold", 17), hover_color="#B0510C", fg_color="#EE6B06", text_color="#fff", command=runDumbbell)
        btn1.pack(fill="both", side="top", pady=(0, 25), ipady=10, padx=(27,27))

        # Button 2
        btn2 = CTkButton(master=self.main_view, text="Run Pushups", width=300, font=("Arial Bold", 17), hover_color="#B0510C", fg_color="#EE6B06", text_color="#fff", command=runPushups)
        btn2.pack(fill="both", side="top", pady=(0, 25), ipady=10, padx=(27,27))

        # Button 3
        btn3 = CTkButton(master=self.main_view, text="Run Shoulder Press", width=300, font=("Arial Bold", 17), hover_color="#B0510C", fg_color="#EE6B06", text_color="#fff", command=runShoulderPress)
        btn3.pack(fill="both", side="top", pady=(0, 25), ipady=10, padx=(27,27))

        # Button 4
        btn4 = CTkButton(master=self.main_view, text="Run Situps", width=300, font=("Arial Bold", 17), hover_color="#B0510C", fg_color="#EE6B06", text_color="#fff", command=runSitups)
        btn4.pack(fill="both", side="top", pady=(0, 25), ipady=10, padx=(27,27))

        # Button 5
        btn5 = CTkButton(master=self.main_view, text="Run Squats", width=300, font=("Arial Bold", 17), hover_color="#B0510C", fg_color="#EE6B06", text_color="#fff", command=runSquats)
        btn5.pack(fill="both", side="top", pady=(0, 25), ipady=10, padx=(27,27))




     
    def login_handler(self):
        input_data = {
            "email": self.email.get(),
            "password": self.password.get(),
            "returnSecureToken": True
        }

        response = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyAwGzkULlpBBWaDPrFTLlCXCd-E0P-MkdQ", 
                                  json=input_data)

        response_data = response.json()

        if response.status_code == 200:
            self.token = response_data["idToken"]
            self.switch_main_view("CREATE_ORDER")
            CTkMessagebox(icon="check", message="Login successful")
        else:
            error_message = response_data["error"]["message"]
            CTkMessagebox(icon="cancel", message=error_message)

    def build_login_ui(self):
       CTkLabel(master=self.main_view, text="Login", font=("Arial Black", 25), text_color="#fff").pack(anchor="nw", pady=(29,0), padx=27)
       
       CTkLabel(master=self.main_view, text="Email", font=("Arial Bold", 17), text_color="#fff").pack(anchor="nw", pady=(25,0), padx=27)

       self.email = CTkEntry(master=self.main_view, fg_color="#F0F0F0", text_color="#000", border_width=0)
       self.email.pack(fill="x", pady=(12,0), padx=27, ipady=10)

       CTkLabel(master=self.main_view, text="Password", font=("Arial Bold", 17), text_color="#fff").pack(anchor="nw", pady=(25,0), padx=27)

       self.password = CTkEntry(master=self.main_view, fg_color="#F0F0F0", text_color="#000", border_width=0, show="*")
       self.password.pack(fill="x", pady=(12,0), padx=27, ipady=10)
       
       CTkButton(master=self.main_view, text="Login", width=300, font=("Arial Bold", 17), hover_color="#B0510C", fg_color="#EE6B06", text_color="#fff", command=self.login_handler).pack(fill="both", side="bottom", pady=(0, 50), ipady=10, padx=(27,27))

    
if __name__ == "__main__":
    app = App()
    app.mainloop()