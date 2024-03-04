import customtkinter
from tkinter import filedialog
import os
import hashlib
import tkinter
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

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


class VerifiyTab:
    def __init__(self, tabview, generate_tab_instance):
        self.tabs = tabview
        self.generate_tab_instance = generate_tab_instance
        self.verify_button = customtkinter.CTkButton(master=self.tabs.tab('Verify'), text='Verify', command=self.verify_hash)
        self.verify_button.pack(padx=5, pady=5)

    def verify_hash(self):
        generated_hash_values = getattr(self.generate_tab_instance.hashgenerator, 'generated_hash_values', None)
        if generated_hash_values:
            verification_path = filedialog.askopenfilename(title="Select the verification file")
            if verification_path:
                verification_hash_values = []
                with open(verification_path, 'r') as verification_file:
                    verification_hash_values = verification_file.read().splitlines()
                match = all(item in verification_hash_values for item in generated_hash_values)
                if match:
                    print("File verification successful! Hash values match.")
                else:
                    print("File verification failed! Hash values do not match.")
            else:
                print("Verification operation cancelled.")
        else:
            print("Please generate hash values first.")


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

class Configuration:
    def __init__(self, cfg_lbl):
        self.cfg_label=cfg_lbl
    def save_config(self, filename, config_data):
        with open(filename, 'w') as file:
            file.write(f"File/Folder Path: {config_data['path']}\n")
            file.write(f"Sender Email: {config_data['sender_email']}\n")
            file.write(f"Password: {config_data['password']}\n")
            file.write(f"Receiver's Email: {config_data['receiver_email']}\n")
        self.cfg_label.configure(text="Configuration saved successfully", text_color="green")
class GenerateHash:
    def __init__(self, path, checked_algorithms, display_label):
        self.path = path
        self.checked_algorithms = checked_algorithms
        self.display_label = display_label
        self.saved_file_path = None
        self.generatehash()

    def generatehash(self):
        path = self.path
        if path:
            hash_values = []
            if os.path.isfile(path):
                for i in self.checked_algorithms:
                    hash_value = self.generate_hash(path, algorithm=i)
                    hash_values.append(f"Hash value ({i}): {hash_value}")
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        for i in self.checked_algorithms:
                            hash_value = self.generate_hash(file_path, algorithm=i)
                            hash_values.append(f"Hash value ({i}) for '{file_path}': {hash_value}")
            self.generated_hash_values = hash_values
            self.display_label.configure(text="\n".join(self.generated_hash_values))
            self.hash_values = hash_values

    def generate_hash(self, file_path, algorithm="", buffer_size=65536):
        hasher = hashlib.new(algorithm)
        with open(file_path, 'rb') as file:
            buffer = file.read(buffer_size)
            while len(buffer) > 0:
                hasher.update(buffer)
                buffer = file.read(buffer_size)
        return hasher.hexdigest()

    def save_hash_values(self):
        if hasattr(self, 'hash_values') and self.hash_values:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write("\n".join(self.hash_values))
                self.display_label.configure(text=f"Hash values saved to: {file_path}")
                self.saved_file_path = file_path  # Store the path of the saved file
            else:
                self.display_label.configure(text="Saving operation cancelled.")

    def send_email_prompt(self):
        if hasattr(self, 'hash_values') and self.hash_values:
            send_email_window = tkinter.Toplevel()
            send_email_window.geometry('500x300')
            send_email_window.title("Send Email")

            def send():
                try:
                    self.send_email(email_entry.get(), smtp_entry.get(), receiver_entry.get(), send_label)
                except Exception as e:
                    self.display_label.configure(text='Error sending email', text_color='red')

            email_label = tkinter.Label(send_email_window, text="Sender Email")
            smtp_label = tkinter.Label(send_email_window, text="SMTP Password")
            receiver_label = tkinter.Label(send_email_window, text="Receiver Email")
            email_entry = tkinter.Entry(send_email_window, width=60)
            smtp_entry = tkinter.Entry(send_email_window, width=60, show="*")
            receiver_entry = tkinter.Entry(send_email_window, width=60)
            send_label = tkinter.Label(send_email_window, text="Click to send mail -->")
            send_button = tkinter.Button(send_email_window, text="Send", command=send)

            email_label.grid(row=1, column=0)
            email_entry.grid(row=1, column=1)
            smtp_label.grid(row=2, column=0)
            smtp_entry.grid(row=2, column=1)
            receiver_label.grid(row=3, column=0)
            receiver_entry.grid(row=3, column=1)
            send_label.grid(row=4, column=0)
            send_button.grid(row=4, column=1)
        else:
            self.display_label.configure(text='Generate hash first', text_color='red')

    def send_email(self, smail, pswd, rmail, slabel):
        sender_mail = smail
        smtp_password = pswd
        receiver_mail = rmail
        if sender_mail and smtp_password and receiver_mail:
            subject = "Hash Values"
            body = "\n".join(self.hash_values)

            msg = MIMEMultipart()
            msg['From'] = sender_mail
            msg['To'] = receiver_mail
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))
            if self.saved_file_path:
                with open(self.saved_file_path, 'rb') as file:
                    attachment = MIMEApplication(file.read(), Name=os.path.basename(self.saved_file_path))
                    attachment['Content-Disposition'] = f'attachment; filename="{os.path.basename(self.saved_file_path)}"'
                    msg.attach(attachment)
            else:
                self.path = 'hashes.txt'
                with open(self.path, 'w') as file:
                    file.write("\n".join(self.hash_values))
                with open(self.path, 'rb') as file:
                    attachment = MIMEApplication(file.read(), self.path)
                    attachment['Content-Disposition'] = f'attachment; filename="{self.path}"'
                    msg.attach(attachment)
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_mail, smtp_password)
                server.sendmail(sender_mail, receiver_mail, msg.as_string())
                server.quit()
                slabel.configure(text="Email sent successfully")
                print("Email sent successfully!")
                os.remove(self.path)
            except Exception as e:
                print(f"Error sending email: {e}")
        else:
            print("Email sending operation cancelled.")


class ChecksumGuard:
    def __init__(self, gui_root):
        self.gui = gui_root
        self.gui.title("CheckSum Guard")
        self.tabs = customtkinter.CTkTabview(master=self.gui, width=650, height=650, anchor='w')
        self.tabslist = ['Generate', 'Verify', 'Configure']
        for i in self.tabslist:
            self.tabs.add(i)
        self.tabs.set('Generate')
        self.tabs.pack(padx=20, pady=20)

        self.generate_tab_content = GenerateTab(self.tabs)
        self.verify_tab_content = VerifiyTab(self.tabs, self.generate_tab_content)
        self.configure_tab_content = ConfigureTab(self.tabs)


def main():
    app = customtkinter.CTk()
    app.geometry('700x700')
    checksum = ChecksumGuard(app)
    app.mainloop()


if __name__ == '__main__':
    main()
