import customtkinter
from GUI.FileSelector import FileSelector
from Logic.GenerateHash import GenerateHash
class GenerateTab:
    def __init__(self, tabview):
        self.tabs = tabview
        self.fileselector = FileSelector(self.tabs, "Generate")
        self.algorithms = ['SHA512', 'MD5']
        self.var1 = customtkinter.IntVar()
        self.var2 = customtkinter.IntVar()
        self.checkbox1 = customtkinter.CTkCheckBox(master=self.tabs.tab("Generate"), text=self.algorithms[0], variable=self.var1)
        self.checkbox1.pack(padx=5, pady=5)
        self.checkbox2 = customtkinter.CTkCheckBox(master=self.tabs.tab("Generate"), text=self.algorithms[1], variable=self.var2)
        self.checkbox2.pack(padx=5, pady=5)

        self.generate_button = customtkinter.CTkButton(master=self.tabs.tab("Generate"), text="Generate", command=self.generate)
        self.generate_button.pack(padx=5, pady=5)
        self.display_frame=customtkinter.CTkScrollableFrame(master=self.tabs.tab("Generate"), width=700, height=200)
        self.display_frame.pack(padx=5, pady=5)
        self.display_label = customtkinter.CTkLabel(master=self.display_frame, text="Click generate to get hash value")
        self.display_label.pack(padx=5, pady=5)
        self.save_button = customtkinter.CTkButton(master=self.tabs.tab("Generate"), text="Save Hash Values", command=self.save)
        self.save_button.pack(padx=5, pady=5)
        self.send_button = customtkinter.CTkButton(master=self.tabs.tab("Generate"), text="Send Email", command=self.send)
        self.send_button.pack(padx=5, pady=5)

        self.hashgenerator = None

    def generate(self):
        path = self.fileselector.temp_label.cget("text")
        self.checked_algorithms = [algo for algo, var in zip(self.algorithms, [self.var1, self.var2]) if var.get()]
        self.hashgenerator = GenerateHash(path, self.checked_algorithms, self.display_label)
        self.hashgenerator.generatehash()

    def save(self):
        if self.hashgenerator:
            try:
                self.hashgenerator.save_hash_values()
            except Exception as e:
                self.display_label.configure(text='Generate hash first', text_color='red')
        else:
            self.display_label.configure(text='Generate hash first', text_color='red')

    def send(self):
        if self.hashgenerator:
            self.hashgenerator.send_email_prompt()
        else:
            self.display_label.configure(text='Generate hash first', text_color='red')