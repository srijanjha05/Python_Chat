import customtkinter as ctk
from tkinter import messagebox
from chat_client import ChatClient
import datetime

client = ChatClient()

def update_chat(message):
    timestamp = datetime.datetime.now().strftime("%H:%M")
    chat_display.configure(state="normal")
    chat_display.insert("end", f"[{timestamp}] {message}\n")
    chat_display.configure(state="disabled")
    chat_display.yview("end")

def connect_to_server():
    host = ip_entry.get()
    name = name_entry.get()
    if name.strip() == "":
        messagebox.showerror("Error", "Please enter a name!")
        return
    if client.connect(host, 12345, name):
        client.gui_callback = update_chat
        update_chat("✅ Connected to EchoGrid.")
    else:
        update_chat("❌ Connection failed.")

def send_message():
    msg = message_entry.get()
    if msg:
        client.send(msg)
        message_entry.delete(0, "end")

def on_closing():
    client.disconnect()
    root.destroy()

# ---------- UI Setup ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")  # use 'dark-blue', 'green', or custom

root = ctk.CTk()
root.title("💠 EchoGrid - HyperChat 2077")
root.geometry("950x650")
root.protocol("WM_DELETE_WINDOW", on_closing)

# ---------- HEADER / NAVBAR ----------
header = ctk.CTkFrame(root, fg_color="#1a1a2e", corner_radius=0, height=80)
header.pack(fill="x")

header_label = ctk.CTkLabel(
    header, 
    text="💠 EchoGrid", 
    font=("Orbitron", 28, "bold"), 
    text_color="#66fcf1"
)
header_label.pack(pady=20)

# ---------- CONNECT SECTION ----------
connect_frame = ctk.CTkFrame(root, fg_color="transparent")
connect_frame.pack(pady=15)

ip_entry = ctk.CTkEntry(connect_frame, width=220, placeholder_text="Server IP")
ip_entry.pack(side="left", padx=8)

name_entry = ctk.CTkEntry(connect_frame, width=220, placeholder_text="Your Display Name")
name_entry.pack(side="left", padx=8)

connect_button = ctk.CTkButton(
    connect_frame, 
    text="🔗 Connect", 
    fg_color="#45a29e", 
    hover_color="#66fcf1", 
    command=connect_to_server,
    corner_radius=10
)
connect_button.pack(side="left", padx=8)

# ---------- CHAT DISPLAY ----------
chat_display = ctk.CTkTextbox(
    root, 
    height=360, 
    font=("Fira Code", 14),
    text_color="#00f5ff", 
    corner_radius=12, 
    border_width=2,
    border_color="#45a29e"
)
chat_display.pack(padx=25, pady=15, fill="both", expand=True)
chat_display.configure(state="disabled")

# ---------- MESSAGE ENTRY ----------
bottom_frame = ctk.CTkFrame(root, fg_color="transparent")
bottom_frame.pack(pady=10)

message_entry = ctk.CTkEntry(bottom_frame, width=640, height=40, placeholder_text="Type your message...")
message_entry.pack(side="left", padx=10)

send_button = ctk.CTkButton(
    bottom_frame, 
    text="📨 Send", 
    fg_color="#00f5ff", 
    hover_color="#0ff", 
    command=send_message,
    corner_radius=15
)
send_button.pack(side="left", padx=8)

root.mainloop()