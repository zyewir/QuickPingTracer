from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END, filedialog, Frame, Checkbutton, IntVar, Menu, Toplevel, Message, messagebox
import threading
import subprocess
import psutil
import os
import webbrowser

class QuickPingTracerApp:
    def __init__(self, master):
        self.master = master
        master.title("QuickPingTracer")

        # Create menu
        self.menu = Menu(master)
        master.config(menu=self.menu)

        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=master.quit)

        self.help_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        # Main frame
        self.frame = Frame(master)
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Input frame
        self.input_frame = Frame(self.frame)
        self.input_frame.pack(fill='x', pady=5)

        self.label = Label(self.input_frame, text="Enter Address:")
        self.label.pack(side='left', padx=5, pady=5)

        self.entry = Entry(self.input_frame)
        self.entry.pack(side='left', fill='x', expand=True, padx=5, pady=5)

        self.dns_resolution = IntVar()
        self.dns_checkbutton = Checkbutton(self.input_frame, text="Resolve DNS", variable=self.dns_resolution)
        self.dns_checkbutton.pack(side='left', padx=5, pady=5)

        self.continuous_ping = IntVar()
        self.continuous_ping_checkbutton = Checkbutton(self.input_frame, text="Continuous Ping", variable=self.continuous_ping)
        self.continuous_ping_checkbutton.pack(side='left', padx=5, pady=5)

        # Button frame
        self.button_frame = Frame(self.frame)
        self.button_frame.pack(fill='x', pady=5)

        self.ping_button = Button(self.button_frame, text="Ping", command=self.start_ping)
        self.ping_button.pack(side='left', padx=5, pady=5)

        self.traceroute_button = Button(self.button_frame, text="Traceroute", command=self.start_traceroute)
        self.traceroute_button.pack(side='left', padx=5, pady=5)

        self.stop_button = Button(self.button_frame, text="Stop", command=self.stop_process)
        self.stop_button.pack(side='left', padx=5, pady=5)

        self.clear_button = Button(self.button_frame, text="Clear", command=self.clear_output)
        self.clear_button.pack(side='left', padx=5, pady=5)

        self.save_button = Button(self.button_frame, text="Save", command=self.save_output)
        self.save_button.pack(side='left', padx=5, pady=5)

        # Output frame
        self.output_frame = Frame(self.frame)
        self.output_frame.pack(fill='both', expand=True, pady=10)

        self.text_box = Text(self.output_frame, wrap='word', height=15, width=70)
        self.text_box.pack(side='left', fill='both', expand=True)

        self.scrollbar = Scrollbar(self.output_frame, command=self.text_box.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.text_box['yscrollcommand'] = self.scrollbar.set

        self.process = None
        self.thread = None

    def start_ping(self):
        address = self.entry.get()
        if not address:
            messagebox.showwarning("Warning", "Please enter an address.")
            return
        self.stop_process()
        continuous = self.continuous_ping.get() == 1
        self.thread = threading.Thread(target=self.run_ping, args=(address, continuous))
        self.thread.start()

    def start_traceroute(self):
        address = self.entry.get()
        if not address:
            messagebox.showwarning("Warning", "Please enter an address.")
            return
        self.stop_process()
        resolve_dns = self.dns_resolution.get() == 1
        self.thread = threading.Thread(target=self.run_traceroute, args=(address, resolve_dns))
        self.thread.start()

    def run_ping(self, address, continuous):
        command = ["ping"]
        if not continuous:
            command.extend(["-c", "4"])
        command.append(address)
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.display_output()

    def run_traceroute(self, address, resolve_dns):
        command = ["traceroute"]
        if not resolve_dns:
            command.append("-n")
        command.append(address)
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.display_output()

    def display_output(self):
        for line in iter(self.process.stdout.readline, ''):
            self.text_box.insert(END, line)
            self.text_box.see(END)
        self.process.stdout.close()
        self.process.wait()

    def stop_process(self):
        if self.process:
            try:
                proc = psutil.Process(self.process.pid)
                for p in proc.children(recursive=True):
                    p.terminate()
                proc.terminate()
                proc.wait(timeout=5)  # Wait for the process to terminate
            except psutil.NoSuchProcess:
                pass
            except psutil.TimeoutExpired:
                proc.kill()  # Force kill if terminate doesn't work
            self.process = None
        if self.thread:
            self.thread.join()
            self.thread = None

    def clear_output(self):
        self.text_box.delete(1.0, END)

    def save_output(self):
        if not self.text_box.get(1.0, END).strip():
            messagebox.showwarning("Warning", "No data to save.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_box.get(1.0, END))

    def show_about(self):
        about_window = Toplevel(self.master)
        about_window.title("About")
        about_message = Message(about_window, text="Visit our GitHub page for more information:\nhttps://github.com/zyewir/QuickPingTracer", width=300)
        about_message.pack(padx=10, pady=10)
        about_button = Button(about_window, text="Open GitHub", command=lambda: webbrowser.open("https://github.com/zyewir/QuickPingTracer"))
        about_button.pack(pady=5)

if __name__ == "__main__":
    root = Tk()
    app = QuickPingTracerApp(root)
    root.mainloop()