import hashlib
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import tkinter as tk
from tkinter import filedialog, simpledialog

class FileSelectorApp:
    def __init__(self, root, callback):
        self.root = root
        self.root.title("File Selector")

        self.callback = callback

        self.folder_button = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.folder_button.pack(pady=10)

        self.file_button = tk.Button(root, text="Select File", command=self.select_file)
        self.file_button.pack(pady=10)

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.callback(folder_selected)

    def select_file(self):
        file_selected = filedialog.askopenfilename()
        if file_selected:
            self.callback(file_selected)

class FileHashGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("File Hash Generator")

        self.path_label = tk.Label(master, text="")
        self.path_label.pack(pady=10)

        self.algorithms = ["sha512", "md5", "sha1", "sha224", "sha256"]
        self.selected_algorithms = tk.StringVar(value=["sha256"])  # Default algorithm(s)

        self.listbox = tk.Listbox(master, selectmode=tk.MULTIPLE)
        for algorithm in self.algorithms:
            self.listbox.insert(tk.END, algorithm.upper())
        self.listbox.pack(anchor=tk.W)

        self.generate_button = tk.Button(master, text="Generate", command=self.generate_hash)
        self.generate_button.pack(pady=10)

        self.save_button = tk.Button(master, text="Save Hash Values", command=self.save_hash_values)
        self.save_button.pack(pady=10)

        self.email_button = tk.Button(master, text="Send Email", command=self.send_email)
        self.email_button.pack(pady=10)

        self.hash_label = tk.Label(master, text="")
        self.hash_label.pack(pady=10)

        self.saved_file_path = None  # To store the path of the saved file

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

            self.hash_label.config(text="\n".join(hash_values))
            self.hash_values = hash_values  # Store hash values for saving to file

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
        if hasattr(self, 'hash_values') and self.hash_values:
            email_address = simpledialog.askstring("Email Address", "Enter your email address:")
            email_password = simpledialog.askstring("Email Password", "Enter your email password:", show="*")
            to_email = simpledialog.askstring("To Email Address", "Enter the recipient's email address:")

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
                    server.login(email_address, email_password)
                    server.sendmail(email_address, to_email, msg.as_string())
                    server.quit()
                    print("Email sent successfully!")
                    if os.path.exists(self.path):
                        os.remove(self.path)
                except Exception as e:
                    print(f"Error sending email: {e}")
            else:
                print("Email sending operation cancelled.")

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

    def callback(path):
        app.choose_path(path)

    selector_app = FileSelectorApp(root, callback)
    app = FileHashGeneratorApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()
