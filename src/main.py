import tkinter as tk
from tkinter import Menu

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
    self.edit_menu.add_command(label='Cut')
    self.edit_menu.add_command(label='Copy')
    self.edit_menu.add_command(label='Paste')

    self.text_widget = tk.Text(root, wrap='word')
    self.text_widget.pack(expand=1, fill='both')

  def exit_app(self):
    self.root.destroy()

def run():
  root = tk.Tk()
  app = NoteApp(root)
  root.mainloop()

if __name__ == '__main__':
  run()