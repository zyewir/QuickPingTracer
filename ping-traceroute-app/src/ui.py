from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END
from network import ping, traceroute

class NetworkApp:
    def __init__(self, master):
        self.master = master
        master.title("Ping and Traceroute Application")

        self.label = Label(master, text="Enter Address:")
        self.label.pack()

        self.entry = Entry(master)
        self.entry.pack()

        self.ping_button = Button(master, text="Ping", command=self.perform_ping)
        self.ping_button.pack()

        self.traceroute_button = Button(master, text="Traceroute", command=self.perform_traceroute)
        self.traceroute_button.pack()

        self.result_text = Text(master, wrap='word', height=15, width=50)
        self.result_text.pack()

        self.scrollbar = Scrollbar(master, command=self.result_text.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.result_text['yscrollcommand'] = self.scrollbar.set

    def perform_ping(self):
        address = self.entry.get()
        result = ping(address)
        self.display_result(result)

    def perform_traceroute(self):
        address = self.entry.get()
        result = traceroute(address)
        self.display_result(result)

    def display_result(self, result):
        self.result_text.delete(1.0, END)
        self.result_text.insert(END, result)

if __name__ == "__main__":
    root = Tk()
    app = NetworkApp(root)
    root.mainloop()