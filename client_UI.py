import tkinter as tk
from tkinter import ttk, scrolledtext
from socket import socket, AF_INET, SOCK_STREAM


def connect_to_server():
    global client_socket
    server_address = ('localhost', 2525)
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(server_address)
    except Exception as e:
        update_chat_box(f"连接错误：无法连接到服务器: {e}", "system")


def send_id():
    user_id = entry_id.get()
    update_chat_box(f"发送ID：{user_id}", "client")
    client_socket.send(user_id.encode())
    response = client_socket.recv(1024).decode()
    update_chat_box(response, "server")
    if response == "500 sp AUTH REQUIRED!":
        toggle_entry(entry_id, button_send_id, False)
        toggle_entry(entry_password, button_send_password, True)


def send_password():
    user_password = entry_password.get()
    update_chat_box("发送密码", "client")
    client_socket.sendall(user_password.encode())
    response = client_socket.recv(1024).decode()
    update_chat_box(response, "server")
    toggle_entry(entry_password, button_send_password, response == "525 OK!")
    toggle_entry(entry_withdraw, button_send_withdraw, response == "525 OK!")


def send_withdraw():
    user_withdraw = entry_withdraw.get()
    update_chat_box(f"请求取款：{user_withdraw}", "client")
    client_socket.sendall(user_withdraw.encode())
    response = client_socket.recv(1024).decode()
    update_chat_box(response, "server")
    successful_withdraw = float(response.split(':')[-1].strip()) >= float(user_withdraw)
    toggle_entry(entry_withdraw, button_send_withdraw, not successful_withdraw)
    toggle_entry(entry_over, button_send_over, not successful_withdraw)


def send_over():
    user_over = entry_over.get()
    update_chat_box(user_over, "client")
    client_socket.sendall(user_over.encode())
    response = client_socket.recv(1024).decode()
    update_chat_box(response, "server")
    toggle_entry(entry_over, button_send_over, False)
    client_socket.close()


def update_chat_box(message, sender):
    chat_box.config(state='normal')
    sender_tag = {"client": "您：", "server": "服务器：", "system": ""}[sender]
    chat_box.insert(tk.END, f"{sender_tag}{message}\n\n", sender)
    chat_box.config(state='disabled')
    chat_box.see(tk.END)


def toggle_entry(entry_widget, button_widget, state):
    state = 'normal' if state else 'disabled'
    entry_widget.config(state=state)
    button_widget.config(state=state)


root = tk.Tk()
root.title("ATM客户端")

style = ttk.Style(root)
style.theme_use("alt")

main_frame = ttk.Frame(root, padding=20)
main_frame.grid(row=0, column=0, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

labels = ["请输入您的ID：", "请输入您的密码：", "请输入取款金额：", "确认或取消："]
entries = []
buttons = [send_id, send_password, send_withdraw, send_over]
button_texts = ["发送ID", "发送密码", "取款", "发送"]
for i, (label_text, button_func, btn_text) in enumerate(zip(labels, buttons, button_texts)):
    ttk.Label(main_frame, text=label_text).grid(row=i*2, column=0, padx=5, pady=5, sticky="e")
    entry = ttk.Entry(main_frame, show="*" if i == 1 else "")
    entry.grid(row=i*2, column=1, padx=5, pady=5)
    entries.append(entry)
    button = ttk.Button(main_frame, text=btn_text, command=button_func, state='disabled' if i else 'normal')
    button.grid(row=i*2+1, column=1, padx=5, pady=5)
    if i:  # Disable all entries and buttons initially except ID
        entry.config(state='disabled')

(entry_id, entry_password, entry_withdraw, entry_over) = entries
(button_send_id, button_send_password, button_send_withdraw, button_send_over) = [btn for btn in main_frame.winfo_children() if isinstance(btn, ttk.Button)]

chat_box = scrolledtext.ScrolledText(main_frame, state='disabled', width=40, height=10)
chat_box.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

chat_box.tag_configure("client", background="#d9edf7", foreground="black")
chat_box.tag_configure("server", background="#f0f0f0", foreground="black")
chat_box.tag_configure("system", foreground="red")

connect_to_server()

root.mainloop()