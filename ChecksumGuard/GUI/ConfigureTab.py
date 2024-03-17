import customtkinter
from tkinter import filedialog
from Logic.Configuration import Configuration
class ConfigureTab:
    def __init__(self, tabview):
        self.tabs=tabview
        def save_config():
            time=self.option_var_hr.get()+':'+self.option_var_min.get()
            config_data = {
                "path": self.original_path.get(),
                "hash_path": self.file_hash_entry.get(),
                "sender_email": self.sender_email_entry.get(),
                "password": self.pswd_entry.get(),
                "receiver_email": self.receiver_email_entry.get(),
                "time": time
            }
            # self.config.save_config("C:\Program Files (x86)\ChecksumGuard\config.txt", config_data)
            self.config.save_config("config.txt", config_data)
            if self.auto_switch_var.get()=='on':
                print("Automate on")
                self.config.automate()
        def browse_file():
            filename = filedialog.askopenfilename()
            if filename:
                self.original_path.set(filename)

        def browse_folder():
            foldername = filedialog.askdirectory()
            if foldername:
                self.original_path.set(foldername)

        def browse_hash_file(event=None):
            filename=filedialog.askopenfilename()
            if filename:
                self.hash_path.set(filename)

        customtkinter.CTkLabel(master=self.tabs.tab("Configure"), text="Original File/Folder path: ").grid(row=0, column=0, padx=5, pady=5)
        customtkinter.CTkLabel(master=self.tabs.tab("Configure"), text="Hash values file path: ").grid(row=1, column=0, padx=5, pady=5)
        customtkinter.CTkLabel(master=self.tabs.tab("Configure"), text="Sender Email: ").grid(row=2, column=0, padx=5, pady=5)
        customtkinter.CTkLabel(master=self.tabs.tab("Configure"), text="Password: ").grid(row=3, column=0, padx=5, pady=5)
        customtkinter.CTkLabel(master=self.tabs.tab("Configure"), text="Receiver Email: ").grid(row=4, column=0, padx=5, pady=5)
        customtkinter.CTkLabel(master=self.tabs.tab("Configure"), text="Select time to automate: ", width=5).grid(row=5, column=0, padx=5, pady=5)
        self.cfg_label=customtkinter.CTkLabel(master=self.tabs.tab("Configure"), text="Click to save configuration-->", text_color="white")
        self.cfg_label.grid(row=6, column=1)

        self.auto_switch_var=customtkinter.StringVar(value='off')
        self.auto_switch=customtkinter.CTkSwitch(master=self.tabs.tab("Configure"), text="Automate", onvalue='on', offvalue='off', variable=self.auto_switch_var)
        self.auto_switch.grid(row=6, column=0, padx=5, pady=5)

        self.original_path=customtkinter.StringVar()
        self.hash_path=customtkinter.StringVar()

        self.original_path_entry=customtkinter.CTkOptionMenu(master=self.tabs.tab("Configure"), variable=self.original_path, values=['Select a file', 'Select a folder'], width=250, dynamic_resizing=False)
        self.original_path_entry.grid(row=0, column=1, padx=5, pady=5)

        self.original_path_btn=customtkinter.CTkButton(master=self.tabs.tab("Configure"), text="Browse", command=lambda: browse_file() if self.original_path.get() == "Select a file" else browse_folder())
        self.original_path_btn.grid(row=0, column=2, padx=5, pady=5)

        self.file_hash_entry=customtkinter.CTkEntry(master=self.tabs.tab("Configure"), width=400, textvariable=self.hash_path)
        self.file_hash_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
        self.file_hash_entry.bind("<Button-1>", browse_hash_file)

        self.sender_email_entry=customtkinter.CTkEntry(master=self.tabs.tab("Configure"), width=400)
        self.sender_email_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

        self.pswd_entry=customtkinter.CTkEntry(master=self.tabs.tab("Configure"), show="*", width=400)
        self.pswd_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2)

        self.receiver_email_entry=customtkinter.CTkEntry(master=self.tabs.tab("Configure"), width=400)
        self.receiver_email_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=2)

        self.option_var_hr=customtkinter.StringVar(value='00')
        self.option_menu_hr=customtkinter.CTkOptionMenu(master=self.tabs.tab("Configure"), values = ['{:02d}'.format(i) for i in range(24)], variable=self.option_var_hr)
        self.option_menu_hr.grid(row=5, column=1, padx=5, pady=5)

        self.option_var_min=customtkinter.StringVar(value='00')
        self.option_menu_min=customtkinter.CTkOptionMenu(master=self.tabs.tab("Configure"), values = ['{:02d}'.format(i) for i in range(60)], variable=self.option_var_min)
        self.option_menu_min.grid(row=5, column=2, padx=5, pady=5)

        self.config_save_btn=customtkinter.CTkButton(master=self.tabs.tab("Configure"), text="Save Configuration", command=save_config)
        self.config_save_btn.grid(row=6, column=2, padx=5, pady=5)

        self.config=Configuration(self.cfg_label)
