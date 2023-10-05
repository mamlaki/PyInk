import tkinter as tk
from tkinter import ttk, font, colorchooser

class SettingsWindow:
  def __init__(self, parent, notebook, note_app):
    self.settings_window = tk.Toplevel(parent)
    self.notebook = notebook
    self.note_app = note_app
    self.settings_window.title('Settings')
    
    self.font_family_var = tk.StringVar(value = 'Arial')
    self.font_size_var = tk.StringVar(value = '12')
    self.font_style_var = tk.StringVar(value = 'normal')
    self.font_color_var = tk.StringVar(value = 'black')
    
    self.font_size_spinbox = tk.Spinbox(self.settings_window, from_ = 1, to = 100, textvariable = self.font_size_var)
    self.font_size_spinbox.pack()

    self.font_family_menu = tk.OptionMenu(self.settings_window, self.font_family_var, *tk.font.families())
    self.font_family_menu.pack()

    style_options = ['normal', 'bold', 'italic', 'bold italic']
    self.font_style_menu = tk.OptionMenu(self.settings_window, self.font_style_var, *style_options)
    self.font_style_menu.pack()

    apply_font_button = ttk.Button(self.settings_window, text='Apply Font', command=lambda: self.apply_font(self.note_app))
    apply_font_button.pack()

    apply_font_to_all_button = ttk.Button(self.settings_window, text = 'Apply to All', command = lambda: self.apply_font_to_all_tabs())
    apply_font_to_all_button.pack()

    self.color_button = ttk.Button(self.settings_window, text = 'Pick Color', command = self.pick_color)
    self.color_button.pack()

    self.settings_window.protocol('WM_DELETE_WINDOW', self.on_closing_settings)
    center_window(self.settings_window, 400, 300)

  def apply_font(self, note_app):
    print('apply_font called')
    font_config = (self.font_family_var.get(), int(self.font_size_var.get()), self.font_style_var.get())
    note_app.apply_font(*font_config, self.font_color_var.get()) 

  def apply_font_to_all_tabs(self):
    font_config = (self.font_family_var.get(), int(self.font_size_var.get()), self.font_style_var.get())
    self.note_app.apply_font_to_all(*font_config, self.font_color_var.get())

  def pick_color(self):
    color = colorchooser.askcolor()[1]
    if color:
      self.font_color_var.set(color)

  def window_exists(self):
    return self.settings_window.winfo_exists()

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
