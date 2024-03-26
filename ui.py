import customtkinter
import start
from csv import writer
import string

def main():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    root = customtkinter.CTk()
    root.geometry("500x500")
    root.title("frapf")
    entry = customtkinter.CTkEntry(master=root, width=200, height=25, corner_radius=0)
    entry.place(relx=0.25, rely=0.4, anchor=customtkinter.CENTER)

    def runQuery():
        query = entry.get()
        start.start(query)

    buttonRun = customtkinter.CTkButton(master=root, corner_radius=0, command = runQuery, text="Run")
    buttonRun.place(relx=0.60, rely=0.4, anchor=customtkinter.CENTER)


    def insertWindow():
        child = customtkinter.CTk()
        child.geometry("400x500")
        child.title("frapf/insertTransaction")

        entryAmount = customtkinter.CTkEntry(master=child, width=200, height=25, corner_radius=0)
        entryAmount.place(relx=0.3, rely=0.1, anchor=customtkinter.CENTER)

        entryReason = customtkinter.CTkEntry(master=child, width=200, height=25, corner_radius=0)
        entryReason.place(relx=0.3, rely=0.2, anchor=customtkinter.CENTER)

        entryAccount = customtkinter.CTkEntry(master=child, width=200, height=25, corner_radius=0)
        entryAccount.place(relx=0.3, rely=0.3, anchor=customtkinter.CENTER)

        entryDate = customtkinter.CTkEntry(master=child, width=200, height=25, corner_radius=0)
        entryDate.place(relx=0.3, rely=0.4, anchor=customtkinter.CENTER)

        entryCurrency = customtkinter.CTkEntry(master=child, width=200, height=25, corner_radius=0)
        entryCurrency.place(relx=0.3, rely=0.5, anchor=customtkinter.CENTER)

        entryTag = customtkinter.CTkEntry(master=child, width=200, height=25, corner_radius=0)
        entryTag.place(relx=0.3, rely=0.6, anchor=customtkinter.CENTER)

        def insertTransaction():
            with open('./personal_finance.csv', 'a') as csvfile:
                data = [entryAmount.get(),entryReason.get(),entryAccount.get(),entryDate.get(),entryCurrency.get(),entryTag.get(),"\n"]
                csvfile.write(",".join(data))
                child.destroy()

        buttonStartInsert = customtkinter.CTkButton(master=child, corner_radius=0, command = insertTransaction, text="Enter")
        buttonStartInsert.place(relx=0.30, rely=0.7, anchor=customtkinter.CENTER)

        child.mainloop()


    buttonInsert = customtkinter.CTkButton(master=root, corner_radius=0, command = insertWindow, text="Insert")
    buttonInsert.place(relx=0.60, rely=0.5, anchor=customtkinter.CENTER)


    root.mainloop()

if __name__ == '__main__':
    main()
