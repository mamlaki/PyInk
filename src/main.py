import tkinter as tk
from tkinter import ttk, Menu, messagebox
import platform

class NoteApp:
  def __init__(self, root):
    self.root = root
    root.title('PyInk')
    
    self.menu_bar = Menu(root)
    root.config(menu=self.menu_bar)

    if platform.system() == 'Darwin':
      hotkey = '⌘ T'
    else:
      hotkey = '^ T'

    self.file_menu = Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label='File', menu=self.file_menu)
    self.file_menu.add_command(label=f'New Tab ({hotkey})', command=self.new_tab)
    self.file_menu.add_command(label='New Window')
    self.file_menu.add_command(label='Open')
    self.file_menu.add_command(label='Save')
    self.file_menu.add_separator()
    self.file_menu.add_command(label='Exit', command=self.exit_app)

    self.edit_menu = Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)
    self.edit_menu.add_command(label='Cut', command=self.cut_text)
    self.edit_menu.add_command(label='Copy', command=self.copy_text)
    self.edit_menu.add_command(label='Paste', command=self.paste_text)

    self.notebook = ttk.Notebook(root)
    self.notebook.pack(expand=1, fill='both')

    self.new_tab()

    root.bind('<Command-t>', self.new_tab)
    root.bind('<Control-t>', self.new_tab)

  def exit_app(self):
    user_response = messagebox.askokcancel('Exit', 'Are you sure you want to exit?')
    if user_response:
      self.root.destroy()
    self.root.destroy()

  def new_tab(self, event=None):
    tab = tk.Frame(self.notebook)
    self.notebook.add(tab, text='Untitled')
    text_widget = tk.Text(tab, wrap='word')
    text_widget.pack(expand=1, fill='both')

  def cut_text(self):
    current_tab = self.notebook.select()
    text_widget = self.notebook.nametowidget(current_tab).winfo_children()[0]
    text_widget.event_generate('<<Cut>>')

  def copy_text(self):
    current_tab = self.notebook.select()
    text_widget = self.notebook.nametowidget(current_tab).winfo_children()[0]
    text_widget.event_generate('<<Copy>>')

  def paste_text(self):
    current_tab = self.notebook.select()
    text_widget = self.notebook.nametowidget(current_tab).winfo_children()[0]
    text_widget.event_generate('<<Paste>>')

def run():
  root = tk.Tk()
  app = NoteApp(root)
  root.mainloop()

if __name__ == '__main__':
  run()