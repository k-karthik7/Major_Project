import customtkinter
from Logic.Configuration import Configuration
class ConfigureTab:
    def __init__(self, tabview):
        self.tabs=tabview
        customtkinter.CTkLabel(master=self.tabs.tab("Configure"), text="File/Folder path: ").grid(row=0, column=0, padx=5, pady=5)
        customtkinter.CTkLabel(master=self.tabs.tab("Configure"), text="Sender Email: ").grid(row=1, column=0, padx=5, pady=5)
        customtkinter.CTkLabel(master=self.tabs.tab("Configure"), text="Password: ").grid(row=2, column=0, padx=5, pady=5)
        customtkinter.CTkLabel(master=self.tabs.tab("Configure"), text="Receiver Email: ").grid(row=3, column=0, padx=5, pady=5)
        self.cfg_label=customtkinter.CTkLabel(master=self.tabs.tab("Configure"), text="Click to save configuration-->", text_color="white")
        self.cfg_label.grid(row=4, column=0)
        self.file_folder_entry=customtkinter.CTkEntry(master=self.tabs.tab("Configure"), width=400)
        self.file_folder_entry.grid(row=0, column=1, padx=5, pady=5)
        self.sender_email_entry=customtkinter.CTkEntry(master=self.tabs.tab("Configure"), width=400)
        self.sender_email_entry.grid(row=1, column=1, padx=5, pady=5)
        self.pswd_entry=customtkinter.CTkEntry(master=self.tabs.tab("Configure"), show="*", width=400)
        self.pswd_entry.grid(row=2, column=1, padx=5, pady=5)
        self.receiver_email_entry=customtkinter.CTkEntry(master=self.tabs.tab("Configure"), width=400)
        self.receiver_email_entry.grid(row=3, column=1, padx=5, pady=5)

        self.config=Configuration(self.cfg_label)
        def save_config():
            config_data = {
                "path": self.file_folder_entry.get(),
                "sender_email": self.sender_email_entry.get(),
                "password": self.pswd_entry.get(),
                "receiver_email": self.receiver_email_entry.get(),
            }
            self.config.save_config("config.txt", config_data)

        self.config_save_btn=customtkinter.CTkButton(master=self.tabs.tab("Configure"), text="Save Configuration", command=save_config)
        self.config_save_btn.grid(row=4, column=1, padx=5, pady=5)