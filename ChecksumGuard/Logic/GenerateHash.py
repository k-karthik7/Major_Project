import os
import hashlib
import tkinter.filedialog as filedialog
import tkinter
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import  smtplib
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
            self.display_label.configure(text="\n".join(self.generated_hash_values), text_color="white")
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
            self.send_email_window = tkinter.Toplevel()
            self.send_email_window.geometry('500x300')
            self.send_email_window.title("Send Email")

            def send():
                try:
                    self.send_email(self.email_entry.get(), self.smtp_entry.get(), self.receiver_entry.get(), self.send_label)
                except Exception as e:
                    self.display_label.configure(text='Error sending email', text_color='red')

            email_label = tkinter.Label(self.send_email_window, text="Sender Email")
            smtp_label = tkinter.Label(self.send_email_window, text="SMTP Password")
            receiver_label = tkinter.Label(self.send_email_window, text="Receiver Email")
            self.email_entry = tkinter.Entry(self.send_email_window, width=60)
            self.smtp_entry = tkinter.Entry(self.send_email_window, width=60, show="*")
            self.receiver_entry = tkinter.Entry(self.send_email_window, width=60)
            self.send_label = tkinter.Label(self.send_email_window, text="Click to send mail-->")
            send_button = tkinter.Button(self.send_email_window, text="Send", command=send)
            load_config_btn=tkinter.Button(self.send_email_window, text="Load Credentials", command=self.load_config)

            email_label.grid(row=1, column=0, pady=5)
            self.email_entry.grid(row=1, column=1, pady=5, columnspan=2)
            smtp_label.grid(row=2, column=0, pady=5)
            self.smtp_entry.grid(row=2, column=1, pady=5, columnspan=2)
            receiver_label.grid(row=3, column=0, pady=5)
            self.receiver_entry.grid(row=3, column=1, pady=5, columnspan=2)
            self.send_label.grid(row=4, column=1, pady=5)
            send_button.grid(row=4, column=2,padx=10, pady=5)
            load_config_btn.grid(row=4, column=0,padx=10, pady=5)
        else:
            self.display_label.configure(text='Generate hash first', text_color='red')

    def load_config(self):
        try:
            with open("config.txt", "r") as file:
                lines=file.readlines()
                values={}
                for line in lines:
                    key, value= line.strip().split(": ")
                    values[key]=value
            self.email_entry.delete(0, tkinter.END)
            self.email_entry.insert(0, values["Sender Email"])

            self.smtp_entry.delete(0, tkinter.END)
            self.smtp_entry.insert(0, values["Password"])

            self.receiver_entry.delete(0, tkinter.END)
            self.receiver_entry.insert(0, values["Receiver's Email"])

        except FileNotFoundError:
            print("File Not Found")
            self.send_label.configure(text="No Configuration File Found")
    

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