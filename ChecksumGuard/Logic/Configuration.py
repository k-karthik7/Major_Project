class Configuration:
    def __init__(self, cfg_lbl):
        self.cfg_label=cfg_lbl
    def save_config(self, filename, config_data):
        with open(filename, 'w') as file:
            file.write(f"Original File/Folder Path: {config_data['path']}\n")
            file.write(f"Hash Values Path: {config_data['hash_path']}\n")
            file.write(f"Sender Email: {config_data['sender_email']}\n")
            file.write(f"Password: {config_data['password']}\n")
            file.write(f"Receiver's Email: {config_data['receiver_email']}\n")
            file.write(f"Automate time: {config_data['time']}")
        self.cfg_label.configure(text="Configuration saved successfully", text_color="green")
    def automate(self):
        import pyuac
        if not pyuac.isUserAdmin():
            pyuac.runAsAdmin()
        else:
            import subprocess
            try:
                with open("config.txt", "r") as file:
                    lines=file.readlines()
                    values={}
                    for line in lines:
                        key, value=line.strip().split(": ")
                        values[key]=value
            except Exception as e:
                pass
            time=values['Automate time']
            # Command to execute
            command = 'schtasks /create /tn "CheckSumGuard" /tr "C:\\Program Files (x86)\\ChecksumGuard\\auto_generate_verify.exe" /sc daily /st {} /f'.format(time)

            # Execute the command
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            # Get the output and error (if any)
            output, error = process.communicate()

            # Decode the output and error (if any) from bytes to string
            output_str = output.decode('utf-8')
            error_str = error.decode('utf-8')