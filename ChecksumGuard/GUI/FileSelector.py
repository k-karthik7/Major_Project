import customtkinter
from tkinter import filedialog
class FileSelector:
    def __init__(self, tabview, tabtitle):
        self.tabs = tabview
        self.tabtitle = tabtitle
        
        def select_file():
            filepath = filedialog.askopenfilename(initialdir="/", title="Select a file")
            if filepath:
                self.temp_label.configure(text=filepath)
        
        def select_folder():
            folderpath = filedialog.askdirectory(initialdir="/", title='Select a folder')
            if folderpath:
                self.temp_label.configure(text=folderpath)
        
        self.select_file_button = customtkinter.CTkButton(master=self.tabs.tab(tabtitle), text="Select File", command=select_file, width=5)
        self.select_file_button.pack(padx=5, pady=5)

        self.select_folder_button = customtkinter.CTkButton(master=self.tabs.tab(tabtitle), text="Select Folder", command=select_folder, width=5)
        self.select_folder_button.pack(padx=5, pady=5)

        self.temp_label = customtkinter.CTkLabel(master=self.tabs.tab(tabtitle), text='No file/folder Selected')
        self.temp_label.pack()