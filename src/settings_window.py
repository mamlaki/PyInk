import tkinter as tk
from tkinter import ttk, font

class SettingsWindow:
  def __init__(self, parent, notebook):
    self.settings_window = tk.Toplevel(parent)
    self.notebook = notebook
    self.settings_window.title('Settings')
    
    self.font_family_var = tk.StringVar(value = 'Arial')
    self.font_size_var = tk.StringVar(value = '12')
    self.font_style_var = tk.StringVar(value = 'normal')
    
    self.font_size_spinbox = tk.Spinbox(self.settings_window, from_ = 1, to = 100, textvariable = self.font_size_var)
    self.font_size_spinbox.pack()

    self.font_family_menu = tk.OptionMenu(self.settings_window, self.font_family_var, *tk.font.families())
    self.font_family_menu.pack()

    style_options = ['normal', 'bold', 'italic', 'bold italic']
    self.font_style_menu = tk.OptionMenu(self.settings_window, self.font_style_var, *style_options)
    self.font_style_menu.pack()

    apply_font_button = ttk.Button(self.settings_window, text = 'Apply Font', command = self.apply_font)
    apply_font_button.pack()

    self.settings_window.protocol('WM_DELETE_WINDOW', self.on_closing_settings)
    center_window(self.settings_window, 400, 300)

  def window_exists(self):
    return self.settings_window.winfo_exists()

  def apply_font(self):
    font_family = self.font_family_var.get()
    font_size = int(self.font_size_var.get())
    font_style = self.font_style_var.get()
    font_config = (font_family, font_size, font_style)
    for tab in self.notebook.tabs():
      text_widget = self.notebook.nametowidget(tab).winfo_children()[0]
      try:
        selected_text = text_widget.selection_get()
        if selected_text:
          start_index = text_widget.index(tk.SEL_FIRST)
          end_index = text_widget.index(tk.SEL_LAST)
          text_widget.tag_configure('highlighted', font = font_config)
          text_widget.tag_add('highlighted', start_index, end_index)
        else:
          raise tk.TclError
      except tk.TclError:
        text_widget.configure(font = font_config)

  def on_closing_settings(self):
    self.settings_window.destroy()

  def focus(self):
    self.settings_window.focus_set()

def center_window(root, width, height):
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  x_coordinate = (screen_width / 2) - (width  / 2)
  y_coordinate = (screen_height / 2) - (height / 2)
  root.geometry(f'{width}x{height}+{int(x_coordinate)}+{int(y_coordinate)}')
