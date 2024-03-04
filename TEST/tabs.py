import hashlib
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import ttk  # Import ttk for the Notebook widget


class FileSelectorApp:
    def __init__(self, parent_frame, callback):
        self.parent_frame = parent_frame

        self.folder_button = tk.Button(parent_frame, text="Select Folder", command=self.select_folder)
        self.folder_button.pack(pady=10)

        self.file_button = tk.Button(parent_frame, text="Select File", command=self.select_file)
        self.file_button.pack(pady=10)

        self.callback = callback

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.callback(folder_selected)

    def select_file(self):
        file_selected = filedialog.askopenfilename()
        if file_selected:
            self.callback(file_selected)

class GenerateTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

        self.path_label = tk.Label(parent_frame, text="")
        self.path_label.pack(pady=10)

        self.algorithms = ["sha512", "md5", "sha1", "sha224", "sha256"]
        self.selected_algorithms = tk.StringVar(value=["sha256"])  # Default algorithm(s)

        self.listbox = tk.Listbox(parent_frame, selectmode=tk.MULTIPLE)
        for algorithm in self.algorithms:
            self.listbox.insert(tk.END, algorithm.upper())
        self.listbox.pack(anchor=tk.W)

        self.generate_button = tk.Button(parent_frame, text="Generate", command=self.generate_hash)
        self.generate_button.pack(pady=10)

        self.save_button = tk.Button(parent_frame, text="Save Hash Values", command=self.save_hash_values)
        self.save_button.pack(pady=10)

        self.email_button = tk.Button(parent_frame, text="Send Email", command=self.send_email)
        self.email_button.pack(pady=10)

        self.hash_label = tk.Label(parent_frame, text="")
        self.hash_label.pack(pady=10)

        self.generated_hash_values = None  # To store the hash values for verification
        self.generate_hash()
    def choose_path(self, path):
        if os.path.isdir(path):
            self.path_label.config(text=f"Selected Folder: {path}")
        elif os.path.isfile(path):
            self.path_label.config(text=f"Selected File: {path}")

    def generate_hash(self):
        path = self.path_label.cget("text").replace("Selected Folder: ", "").replace("Selected File: ", "")
        if path:
            selected_algorithms = self.listbox.curselection()
            hash_values = []

            if os.path.isfile(path):
                for index in selected_algorithms:
                    algorithm = self.algorithms[index]
                    hash_value = generate_hash(path, algorithm=algorithm)
                    hash_values.append(f"Hash value ({algorithm.upper()}): {hash_value}")
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        for index in selected_algorithms:
                            algorithm = self.algorithms[index]
                            hash_value = generate_hash(file_path, algorithm=algorithm)
                            hash_values.append(f"Hash value ({algorithm.upper()}) for '{file_path}': {hash_value}")

            self.generated_hash_values = hash_values
            self.hash_label.config(text="\n".join(hash_values))
            self.hash_values = hash_values

    def save_hash_values(self):
        if hasattr(self, 'hash_values') and self.hash_values:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write("\n".join(self.hash_values))
                print(f"Hash values saved to: {file_path}")
                self.saved_file_path = file_path  # Store the path of the saved file
            else:
                print("Saving operation cancelled.")

    def send_email(self):
        file_window = tk.Toplevel(self.parent_frame)
        file_window.geometry("560x200")
        file_window.title("Enter Credentials")
        email_label = tk.Label(file_window,text="Sender Email")
        smtp_label = tk.Label(file_window,text="SMTP Password")
        receiver_label = tk.Label(file_window,text="Receiver Email")
        email_entry = tk.Entry(file_window, width=60)
        smtp_entry = tk.Entry(file_window, width=60,show="*")
        receiver_entry = tk.Entry(file_window, width=60)
        email_label.grid(row=1,column=0)
        email_entry.grid(row=1,column=1)
        smtp_label.grid(row=2,column=0)
        smtp_entry.grid(row=2,column=1)
        receiver_label.grid(row=3,column=0)
        receiver_entry.grid(row=3,column=1)
        if hasattr(self, 'hash_values') and self.hash_values:
            email_address = email_entry.get()
            email_password = smtp_entry.get()
            to_email =  receiver_entry.get()

            if email_address and email_password and to_email:
                subject = "Hash Values"
                body = "\n".join(self.hash_values)

                msg = MIMEMultipart()
                msg['From'] = email_address
                msg['To'] = to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(body, 'plain'))
                if self.saved_file_path:
                    with open(self.saved_file_path, 'rb') as file:
                        attachment = MIMEApplication(file.read(), Name=os.path.basename(self.saved_file_path))
                        attachment['Content-Disposition'] = f'attachment; filename="{os.path.basename(self.saved_file_path)}"'
                        msg.attach(attachment)
                else:
                    self.path='hashes.txt'
                    with open(self.path, 'w') as file:
                        file.write("\n".join(self.hash_values))
                    with open(self.path, 'rb') as file:
                        attachment = MIMEApplication(file.read(), self.path)
                        attachment['Content-Disposition'] = f'attachment; filename="{self.path}"'
                        msg.attach(attachment)
                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(email_address, email_password)
                    server.sendmail(email_address, to_email, msg.as_string())
                    server.quit()
                    print("Email sent successfully!")
                    os.remove(self.path)
                except Exception as e:
                    print(f"Error sending email: {e}")
            else:
                print("Email sending operation cancelled.")

        
class VerifyTab:
    def __init__(self, parent_frame, generate_tab_instance):
        self.parent_frame = parent_frame
        self.generate_tab_instance=generate_tab_instance
        self.verify_button = tk.Button(parent_frame, text="Verify", command=self.verify_hash)
        self.verify_button.pack(pady=10)
        

    def verify_hash(self):
        if self.generate_tab_instance.generated_hash_values:
            verification_path = filedialog.askopenfilename(title="Select the verification file")
            if verification_path:
                verification_hash_values = []

                with open(verification_path, 'r') as verification_file:
                    verification_hash_values = verification_file.read().splitlines()

                match = all(item in verification_hash_values for item in self.generate_tab_instance.generated_hash_values)

                if match:
                    print("File verification successful! Hash values match.")
                else:
                    print("File verification failed! Hash values do not match.")
            else:
                print("Verification operation cancelled.")
        else:
            print("Please generate hash values first.")

class ConfigurationTab:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

        self.config = Configuration()

        self.file_path_entry = tk.Entry(parent_frame)
        self.file_path_entry.grid(row=0, column=1)
        self.file_path_entry.insert(0, "Select file or folder")
        self.file_path_entry.bind("<Button-1>", self.select_file_or_folder)
        self.file_path_entry.bind("<FocusOut>", self.clear_file_path_entry)
        self.sender_email_entry = tk.Entry(parent_frame)
        self.sender_email_entry.grid(row=1, column=1)
        self.password_entry = tk.Entry(parent_frame, show="*")
        self.password_entry.grid(row=2, column=1)
        self.receiver_email_entry = tk.Entry(parent_frame)
        self.receiver_email_entry.grid(row=3, column=1)
        self.time_var = tk.StringVar()
        self.time_entry = ttk.Entry(parent_frame, textvariable=self.time_var, width=10)
        self.time_entry.grid(row=4, column=1, pady=(10, 0))

        self.time_button = ttk.Button(parent_frame, text="Select Time", command=self.select_time)
        self.time_button.grid(row=4, column=2, pady=(10, 0))

        tk.Label(parent_frame, text="Time:").grid(row=4, column=0)
        tk.Label(parent_frame, text="File/Folder Path:").grid(row=0, column=0)
        tk.Label(parent_frame, text="Sender Email:").grid(row=1, column=0)
        tk.Label(parent_frame, text="Password:").grid(row=2, column=0)
        tk.Label(parent_frame, text="Receiver's Email:").grid(row=3, column=0)

        self.save_button = tk.Button(parent_frame, text="Save Configuration", command=self.save_configuration)
        self.save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def select_file_or_folder(self, event):
        file_selected = filedialog.askopenfilename() if os.path.exists(self.file_path_entry.get()) else filedialog.askdirectory()
        if file_selected:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_selected)

    def clear_file_path_entry(self, event):
        if self.file_path_entry.get() == "Select file or folder":
            self.file_path_entry.delete(0, tk.END)

    def select_time(self):
        hour = simpledialog.askinteger("Select Time", "Enter hour (0-23):")
        minute = simpledialog.askinteger("Select Time", "Enter minute (0-59):")
        self.time_var.set(f"{hour:02d}:{minute:02d}")

    def save_configuration(self):
        file_path = self.file_path_entry.get()
        sender_email = self.sender_email_entry.get()
        password = self.password_entry.get()
        receiver_email = self.receiver_email_entry.get()

        self.config.set_file_folder_path(file_path)
        self.config.set_sender_email(sender_email)
        self.config.set_password(password)
        self.config.set_receiver_email(receiver_email)

        filename = "config.txt"  # You can change the filename as needed
        self.config.save_config(filename)
        print("Configuration saved to:", filename)

class FileHashGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("File Hash Generator")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)

        self.generate_tab = tk.Frame(self.notebook)
        self.verify_tab = tk.Frame(self.notebook)
        self.configure_tab = tk.Frame(self.notebook)

        self.notebook.add(self.generate_tab, text="Generate")
        self.notebook.add(self.verify_tab, text="Verify")
        self.notebook.add(self.configure_tab, text="Configure")

        self.file_selector_app = FileSelectorApp(self.generate_tab, self.choose_path)
        self.generate_tab_content = GenerateTab(self.generate_tab)
        self.verify_tab_content = VerifyTab(self.verify_tab,self.generate_tab_content)
        self.configuration_tab_content = ConfigurationTab(self.configure_tab)

    def choose_path(self, path):
        self.generate_tab_content.choose_path(path)

class Configuration:
    def __init__(self):
        self.file_folder_path = ""
        self.sender_email = ""
        self.password = ""
        self.receiver_email = ""

    def set_file_folder_path(self, path):
        self.file_folder_path = path

    def set_sender_email(self, email):
        self.sender_email = email

    def set_password(self, password):
        self.password = password

    def set_receiver_email(self, email):
        self.receiver_email = email

    def get_file_folder_path(self):
        return self.file_folder_path

    def get_sender_email(self):
        return self.sender_email

    def get_password(self):
        return self.password

    def get_receiver_email(self):
        return self.receiver_email

    def save_config(self, filename):
        with open(filename, 'w') as file:
            file.write(f"File/Folder Path: {self.file_folder_path}\n")
            file.write(f"Sender Email: {self.sender_email}\n")
            file.write(f"Password: {self.password}\n")
            file.write(f"Receiver's Email: {self.receiver_email}\n")

def generate_hash(file_path, algorithm="sha256", buffer_size=65536):
    """Generate hash value for a given file."""
    hasher = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        buffer = file.read(buffer_size)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = file.read(buffer_size)
    return hasher.hexdigest()

def main():
    root = tk.Tk()
    app = FileHashGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
