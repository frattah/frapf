import customtkinter as ctk
import start
import globals
from datetime import date
from tkcalendar import Calendar
import pandas as pd

class InsertTransactionWindow(ctk.CTkToplevel):
    entryAmount = None
    entryReason = None
    entryAccount = None
    entryDate = None
    entryCurrency = None
    clickedTag = None


    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('400x550+600+100')
        self.title('frapf/insertTransaction')
        self.grab_set()
        
        i = 0

        ## AMOUNT FIELD #############################################################################################################

        self.entryAmount = ctk.CTkEntry(self, width=200, height=25, corner_radius=0)
        self.entryAmount.place(relx=globals.RELX_MIN_INSERT, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)

        frameAmount = ctk.CTkFrame(self, width=100, height=25, corner_radius=globals.CORNER_ROUND)
        frameAmount.place(relx=globals.RELX_MAX_INSERT, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)

        labelAmount = ctk.CTkLabel(master=frameAmount, text="amount", width=80, height=20, corner_radius=globals.CORNER_ROUND)
        labelAmount.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        i += globals.RELY_INCR_INSERT

        ## REASON FIELD #############################################################################################################

        self.entryReason = ctk.CTkEntry(self, width=200, height=25, corner_radius=0)
        self.entryReason.place(relx=globals.RELX_MIN_INSERT, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)

        frameReason = ctk.CTkFrame(self, width=100, height=25, corner_radius=globals.CORNER_ROUND)
        frameReason.place(relx=globals.RELX_MAX_INSERT, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)

        labelReason = ctk.CTkLabel(master=frameReason, text="reason", width=80, height=20, corner_radius=globals.CORNER_ROUND)
        labelReason.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        i += globals.RELY_INCR_INSERT

        ## ACCOUNT FIELD ############################################################################################################

        self.entryAccount = ctk.CTkEntry(self, width=200, height=25, corner_radius=0)
        self.entryAccount.place(relx=globals.RELX_MIN_INSERT, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)

        frameAccount = ctk.CTkFrame(self, width=100, height=25, corner_radius=globals.CORNER_ROUND)
        frameAccount.place(relx=globals.RELX_MAX_INSERT, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)

        labelReason = ctk.CTkLabel(master=frameAccount, text="account", width=80, height=20, corner_radius=globals.CORNER_ROUND)
        labelReason.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        i += globals.RELY_INCR_INSERT

        ## DATE FIELD ###############################################################################################################

        self.entryDate = ctk.CTkEntry(self, width=200, height=25, corner_radius=0)
        self.entryDate.place(relx=globals.RELX_MIN_INSERT, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)
        self.entryDate.insert(0, date.today())
        self.entryDate.bind("<1>", lambda event: self.entryDate.delete(0, ctk.END))

        buttonFrom = ctk.CTkButton(self, corner_radius=globals.CORNER_ROUND, command = lambda: CalendarWindow(self, self.entryDate), 
                                   text="Calendar",  width=100, height=25)
        buttonFrom.place(relx=globals.RELX_MAX_TEMPLATE+0.3, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER) 
    
        i += globals.RELY_INCR_INSERT

        ## CURRENCY FIELD ###########################################################################################################

        self.entryCurrency = ctk.CTkEntry(self, width=200, height=25, corner_radius=0)
        self.entryCurrency.place(relx=globals.RELX_MIN_INSERT, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)
        self.entryCurrency.insert(0, "EUR")
        self.entryCurrency.bind("<1>", lambda event: self.entryCurrency.delete(0, ctk.END))
        
        frameCurrency = ctk.CTkFrame(self, width=100, height=25, corner_radius=globals.CORNER_ROUND)
        frameCurrency.place(relx=globals.RELX_MAX_INSERT, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)

        labelCurrency = ctk.CTkLabel(master=frameCurrency, text="currency", width=80, height=20, corner_radius=globals.CORNER_ROUND)
        labelCurrency.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        i += globals.RELY_INCR_INSERT

        ## TAG FIELD ################################################################################################################

        self.clickedTag = ctk.StringVar(value="")
        dropTag = ctk.CTkOptionMenu(self, corner_radius=0, values=["","invested","security","transfer"], width=200, height=25, 
                                    fg_color="#343638", bg_color="#565b5e", command= self.optionmenu_callback)
        dropTag.place(relx=globals.RELX_MIN_INSERT, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)

        frameTag = ctk.CTkFrame(self, width=100, height=25, corner_radius=globals.CORNER_ROUND)
        frameTag.place(relx=globals.RELX_MAX_INSERT, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)

        labelTag = ctk.CTkLabel(master=frameTag, text="tag", width=80, height=20, corner_radius=globals.CORNER_ROUND)
        labelTag.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        i += globals.RELY_INCR_INSERT

        ############################################################################################################################

        buttonStartInsert = ctk.CTkButton(self, corner_radius=globals.CORNER_ROUND, command = self.insertTransaction, text="Enter")
        buttonStartInsert.place(relx=globals.RELX_MIN_INSERT, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)       

    def optionmenu_callback(self, choice):
        self.clickedTag.set(choice)

    def insertTransaction(self):
        data = ",".join([str(round(float(self.entryAmount.get()),2)),
                        self.entryReason.get(),
                        self.entryAccount.get().capitalize(),
                        self.entryDate.get(),
                        self.entryCurrency.get().upper(),
                        self.clickedTag.get()])
        data = "".join([data, '\n'])

        with open('./personal_finance.csv', 'a') as csvfile:
            csvfile.write(data)
        self.destroy()

class CalendarWindow(ctk.CTkToplevel):
    def __init__(self, parent, entry):
        super().__init__(parent)

        self.geometry('300x230+600+432')
        self.title('frapf/calendar')
        self.grab_set()
    
        cal = Calendar(self, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.place(x=0, y=0)

        buttonSubmit = ctk.CTkButton(self, corner_radius=globals.CORNER_ROUND, command = lambda: self.submit(cal, entry), text="Submit")
        buttonSubmit.place(x=60, y=190)

    def submit(self, cal, entry):
        entry.delete(0, ctk.END)
        entry.insert(0, cal.get_date())
        self.destroy()

class TemplateQueryWindow(ctk.CTkToplevel):
    reader = pd.read_csv("personal_finance.csv")
    acc_set = set(reader.loc[:,"account"])
    accounts = {}
    for i in acc_set:
        accounts[i] = False

    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('400x300+600+100')
        self.title('frapf/templateQuery')
        self.grab_set()

        i = 0

        ## FROM FIELD ##############################################################################################################

        labelFrom = ctk.CTkLabel(master=self, text="from:", width=80, height=20, corner_radius=globals.CORNER_ROUND)
        labelFrom.place(relx=globals.RELX_MIN_TEMPLATE, rely=globals.RELY_BEGIN, anchor=ctk.CENTER)

        self.entryFrom = ctk.CTkEntry(self, width=150, height=25)
        self.entryFrom.place(relx=globals.RELX_MAX_TEMPLATE, rely=globals.RELY_BEGIN, anchor=ctk.CENTER)
        self.entryFrom.insert(0, "?")
        self.entryFrom.bind("<1>", lambda event: self.entryFrom.delete(0, ctk.END))

        buttonFrom = ctk.CTkButton(self, corner_radius=globals.CORNER_ROUND, command = lambda: CalendarWindow(self, self.entryFrom), text="Calendar", width=50)
        buttonFrom.place(relx=globals.RELX_MAX_TEMPLATE+0.3, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)       

        i += globals.RELY_INCR_TEMPLATE

        ## TO FIELD ################################################################################################################

        labelTo = ctk.CTkLabel(master=self, text="to:", width=80, height=20, corner_radius=globals.CORNER_ROUND)
        labelTo.place(relx=globals.RELX_MIN_TEMPLATE, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)

        self.entryTo = ctk.CTkEntry(self, width=150, height=25)
        self.entryTo.place(relx=globals.RELX_MAX_TEMPLATE, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)
        self.entryTo.insert(0, "?")
        self.entryTo.bind("<1>", lambda event: self.entryTo.delete(0, ctk.END))

        buttonTo = ctk.CTkButton(self, corner_radius=globals.CORNER_ROUND, command = lambda: CalendarWindow(self, self.entryTo), text="Calendar", width=50)
        buttonTo.place(relx=globals.RELX_MAX_TEMPLATE+0.3, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)

        i += globals.RELY_INCR_TEMPLATE

        ## ACCOUNT FIELD ###########################################################################################################

        j = 0
        for acc in self.accounts:
            self.accounts[acc] = ctk.BooleanVar()
            checkAccount = ctk.CTkCheckBox(self, text=acc[:3], variable=self.accounts[acc])
            checkAccount.place(relx=globals.RELX_MIN_TEMPLATE+j+0.1, rely=globals.RELY_BEGIN + i, anchor=ctk.CENTER)
            j += 0.15
        i += globals.RELY_INCR_TEMPLATE

        ## AMOUNT FIELD ##############################################################################################################

        # window 400x400
        labelRevenue = ctk.CTkLabel(master=self, text="revenues", width=80, height=20, corner_radius=globals.CORNER_ROUND)
        labelRevenue.place(relx=0.12, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)
        labelSaving = ctk.CTkLabel(master=self, text="saving", width=80, height=20, corner_radius=globals.CORNER_ROUND)
        labelSaving.place(relx=0.36, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)
        labelExpenses = ctk.CTkLabel(master=self, text="expenses", width=80, height=20, corner_radius=globals.CORNER_ROUND)
        labelExpenses.place(relx=0.6, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)
        labelInvested = ctk.CTkLabel(master=self, text="invested", width=80, height=20, corner_radius=globals.CORNER_ROUND)
        labelInvested.place(relx=0.84, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)

        i += globals.RELY_INCR_TEMPLATE

        self.sliderAmount = ctk.CTkSlider(self, from_=0, to=3, number_of_steps=3, width=300)
        self.sliderAmount.place(relx=0.1, rely=globals.RELY_BEGIN+i)
        self.sliderAmount.set(1)

        i += globals.RELY_INCR_TEMPLATE

        ## RUN #####################################################################################################################

        buttonFrom = ctk.CTkButton(self, corner_radius=globals.CORNER_ROUND, command = self.runQuery, text="Run", width=50)
        buttonFrom.place(relx=globals.RELX_MAX_TEMPLATE+0.3, rely=globals.RELY_BEGIN+i, anchor=ctk.CENTER)
    
    def runQuery(self):
        fromValue = self.entryFrom.get()
        if fromValue == "?":
            fromValue = '!'

        query = f"""
                    ( date > {fromValue} or date == {fromValue} )
                    and
                    ( date < {self.entryTo.get()} or date == {self.entryTo.get()} )                     
                """
        
        foundFirst = False
        for acc in self.accounts:
            if self.accounts[acc].get() == True:
                if foundFirst == True:
                    query += " or "
                if foundFirst == False:
                    query += " and ("
                    foundFirst = True
                query += f"account == {acc}"
        if foundFirst == True:
            query += " )"

        if self.sliderAmount != None and self.sliderAmount.get() == 0:
            query += "and ( amount > 0 ) and ( tag != transfer )"
        if self.sliderAmount != None and self.sliderAmount.get() == 2:
            query += "and ( amount < 0 ) and ( tag != transfer and tag != invested )"
        if self.sliderAmount != None and self.sliderAmount.get() == 3:
            query += "and ( tag == invested )"
        
        start.start(query)

class App(ctk.CTk):

    entryQuery = None
    buttonRun = None
    buttonInsert = None

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.geometry("500x550+100+100")
        self.title("frapf")

        self.entryQuery = ctk.CTkEntry(self, width=200, height=25, corner_radius=0)
        self.entryQuery.place(relx=0.25, rely=0.4, anchor=ctk.CENTER)

        self.buttonRun = ctk.CTkButton(self, corner_radius=10, command = lambda: start.start(self.entryQuery.get()), text="Run")
        self.buttonRun.place(relx=0.60, rely=0.4, anchor=ctk.CENTER)

        self.buttonInsert = ctk.CTkButton(self, corner_radius=10, command = lambda: InsertTransactionWindow(self), text="Insert")
        self.buttonInsert.place(relx=0.60, rely=0.5, anchor=ctk.CENTER)

        self.buttonTemplateQuery = ctk.CTkButton(self, corner_radius=10, command = lambda: TemplateQueryWindow(self), text="Template")
        self.buttonTemplateQuery.place(relx=0.60, rely=0.6, anchor=ctk.CENTER)