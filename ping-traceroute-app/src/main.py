from tkinter import Tk, Button, Text, Scrollbar, END
import network

class PingTracerouteApp:
    def __init__(self, master):
        self.master = master
        master.title("Ping and Traceroute Tool")

        self.address_input = Text(master, height=1, width=30)
        self.address_input.pack()

        self.ping_button = Button(master, text="Ping", command=self.perform_ping)
        self.ping_button.pack()

        self.traceroute_button = Button(master, text="Traceroute", command=self.perform_traceroute)
        self.traceroute_button.pack()

        self.result_box = Text(master, height=15, width=50)
        self.result_box.pack()

        self.scrollbar = Scrollbar(master, command=self.result_box.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.result_box.config(yscrollcommand=self.scrollbar.set)

    def perform_ping(self):
        address = self.address_input.get("1.0", END).strip()
        result = network.ping(address)
        self.display_result(result)

    def perform_traceroute(self):
        address = self.address_input.get("1.0", END).strip()
        result = network.traceroute(address)
        self.display_result(result)

    def display_result(self, result):
        self.result_box.delete("1.0", END)
        self.result_box.insert(END, result)

if __name__ == "__main__":
    root = Tk()
    app = PingTracerouteApp(root)
    root.mainloop()