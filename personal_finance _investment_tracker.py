import pandas as pd
from datetime import datetime
import os
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = "transactions.csv"

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["Date", "type", "Category", "amount", "Notes"])
    df.to_csv(FILE_NAME, index=False)

def add_transaction():
        date = date_entry.get()
        t_type = type_var.get()
        amount = amount_entry.get()
        category = category_entry.get()
        notes = notes_entry.get()
        if date and t_type and amount and category:
             df = pd.read_csv(FILE_NAME)
             df.loc[len(df)] = [date, t_type, category, float(amount), notes]
             df.to_csv(FILE_NAME, index=False)
             messagebox.showinfo("Success", "Transaction Added!")
             clear_entries()
        else:
             messagebox.showwarning("Input Error", "All fields except Notes are required!")

def clear_entries():
    date_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    notes_entry.delete(0, tk.END)

def view_transactions():
    for row in tree.get_children():
        tree.delete(row)

    df = pd.read_csv(FILE_NAME)
    for index, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

def analyze_transactions():
    df = pd.read_csv(FILE_NAME)
    if df.empty:
        messagebox.showinfo("Info", "No transactions to analyze!")
        return

    total_income = df[df['type'] == 'Income']['amount'].sum()
    total_expense = df[df['type'] == 'Expense']['amount'].sum()
    savings = total_income - total_expense

    for widget in graph_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie([total_income, total_expense, savings],
           labels=["Income", "Expenses", "Savings"],
           autopct="%1.1f%%", startangle=90, colors=["green", "red", "blue"])
    ax.set_title("Financial Overview")

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

root = tk.Tk()
root.title("Personal Finance & Investment Tracker")
root.geometry("700x600")

tk.Label(root, text="Date (YYYY-MM-DD):").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="type:").pack()
type_var = tk.StringVar(value="Income")
tk.OptionMenu(root, type_var, "Income", "Expense").pack()

tk.Label(root, text="amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Category:").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Notes:").pack()
notes_entry = tk.Entry(root)
notes_entry.pack()

tk.Button(root, text="Add Transaction", command=add_transaction).pack(pady=5)
tk.Button(root, text="View Transactions", command=view_transactions).pack(pady=5)
tk.Button(root, text="Analyze Transactions", command=analyze_transactions).pack(pady=5)

tree = ttk.Treeview(root, columns=("Date", "type", "amount", "Category", "Notes"), show="headings")
for col in ("Date", "type", "amount", "Category", "Notes"):
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True, pady=10)

graph_frame = tk.Frame(root)
graph_frame.pack()

root.mainloop()