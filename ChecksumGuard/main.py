import customtkinter
from GUI.ChecksumGuard import ChecksumGuard
import pyuac
def main():
    app = customtkinter.CTk()
    app.geometry('700x700')
    checksum = ChecksumGuard(app)
    app.mainloop()


if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:        
        main()
# if __name__ == "__main__":
#     main()