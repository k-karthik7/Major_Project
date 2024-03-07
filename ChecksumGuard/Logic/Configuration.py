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