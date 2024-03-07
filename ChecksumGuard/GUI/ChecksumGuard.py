import customtkinter
from GUI.GenerateTab import GenerateTab
from GUI.VerifyTab import VerifiyTab
from GUI.ConfigureTab import ConfigureTab
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