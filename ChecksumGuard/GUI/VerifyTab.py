import customtkinter
from tkinter import filedialog
class VerifiyTab:
    def __init__(self, tabview, generate_tab_instance):
        self.tabs = tabview
        self.generate_tab_instance = generate_tab_instance
        self.verify_button = customtkinter.CTkButton(master=self.tabs.tab('Verify'), text='Verify', command=self.verify_hash)
        self.verify_button.pack(padx=5, pady=5)
        self.verify_label=customtkinter.CTkLabel(master=self.tabs.tab("Verify"), text="")
        self.verify_label.pack(padx=5, pady=5)

    def verify_hash(self):
        generated_hash_values = getattr(self.generate_tab_instance.hashgenerator, 'generated_hash_values', None)
        if generated_hash_values:
            verification_path = filedialog.askopenfilename(title="Select the verification file")
            if verification_path:
                verification_hash_values = []
                with open(verification_path, 'r') as verification_file:
                    verification_hash_values = verification_file.read().splitlines()
                match = any(item in verification_hash_values for item in generated_hash_values)
                if match:
                    print("File verification successful! Hash values match.")
                    self.verify_label.configure(text="File verification successful! Hash values match.", text_color="green")
                else:
                    print("File verification failed! Hash values do not match.")
                    self.verify_label.configure(text="File verification failed! Hash values do not match.", text_color="red")
            else:
                print("Verification operation cancelled.")
        else:
            print("Please generate hash values first.")