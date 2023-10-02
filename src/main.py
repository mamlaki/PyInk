import tkinter as tk
from tkinter import Menu, messagebox

class NoteApp:
  def __init__(self, root):
    self.root = root
    root.title('PyInk')
    
    self.menu_bar = Menu(root)
    root.config(menu=self.menu_bar)

    self.file_menu = Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label='File', menu=self.file_menu)
    self.file_menu.add_command(label='New')
    self.file_menu.add_command(label='Open')
    self.file_menu.add_command(label='Save')
    self.file_menu.add_separator()
    self.file_menu.add_command(label='Exit', command=self.exit_app)

    self.edit_menu = Menu(self.menu_bar, tearoff=0)
    self.menu_bar.add_cascade(label='Edit', menu=self.edit_menu)
    self.edit_menu.add_command(label='Cut', command=self.cut_text)
    self.edit_menu.add_command(label='Copy', command=self.copy_text)
    self.edit_menu.add_command(label='Paste', command=self.paste_text)

    self.text_widget = tk.Text(root, wrap='word')
    self.text_widget.pack(expand=1, fill='both')

  def exit_app(self):
    user_response = messagebox.askokcancel('Exit', 'Are you sure you want to exit?')
    if user_response:
      self.root.destroy()
    self.root.destroy()

  def cut_text(self):
    self.text_widget.event_generate('<<Cut>>')

  def copy_text(self):
    self.text_widget.event.generate('<<Copy>>')

  def paste_text(self):
    self.text_widget.event_generate('<<Paste>>')

def run():
  root = tk.Tk()
  app = NoteApp(root)
  root.mainloop()

if __name__ == '__main__':
  run()