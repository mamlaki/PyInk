import tkinter as tk

class NoteApp:
  def __init__(self, root):
    self.root = root
    root.title('PyInk')
    self.text_widget = tk.Text(root, wrap='word')
    self.text_widget.pack(expand=1, fill='both')

def run():
  root = tk.Tk()
  app = NoteApp(root)
  root.mainloop()

if __name__ == '__main__':
  run()