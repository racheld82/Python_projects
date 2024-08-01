import openai
import tkinter as tk
from tkinter import scrolledtext, messagebox

openai.api_key = ''

def send_message():
    user_input = user_entry.get()
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter a message.")
        return

    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "You: " + user_input + "\n")
    chat_history.config(state=tk.DISABLED)

    response = get_chatbot_response(user_input)
    
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, "Bot: " + response + "\n\n")
    chat_history.config(state=tk.DISABLED)

    user_entry.delete(0, tk.END)

def get_chatbot_response(message):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        max_tokens=150
    )
    return response.choices[0].text.strip()

root = tk.Tk()
root.title("Simple Chatbot")
root.geometry("400x500")

chat_history = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD)
chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

user_entry = tk.Entry(root, width=50)
user_entry.pack(padx=10, pady=10, fill=tk.X)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=10)

root.mainloop()
