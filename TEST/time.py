import customtkinter
app=customtkinter.CTk()
option_var_hr=customtkinter.StringVar(value='hour')
option_menu_hr=customtkinter.CTkOptionMenu(app, values = ['{:02d}'.format(i) for i in range(24)])
option_menu_hr.grid(row=0, column=0, padx=5, pady=5)
option_var_min=customtkinter.StringVar(value='minutes')
option_menu_min=customtkinter.CTkOptionMenu(app, values = ['{:02d}'.format(i) for i in range(60)])
option_menu_min.grid(row=0, column=1, padx=5, pady=5)
def set_time():
    time=option_menu_hr.get()+':'+option_menu_min.get()
    time_lbl.configure(text=time)
slct_btn=customtkinter.CTkButton(app, text='Set time', command=set_time)
slct_btn.grid(row=1, column=0, columnspan=2)
time_lbl=customtkinter.CTkLabel(app, text='')
time_lbl.grid(row=2, column=0, columnspan=2)

app.mainloop()
