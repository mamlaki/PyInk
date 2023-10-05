import tkinter as tk
from tkinter import ttk, Menu, messagebox, font
import platform
import subprocess
# import winsound

from settings_window import SettingsWindow

class NoteApp:
  def __init__(self, root):
    self.root = root
    root.title('PyInk')
    self.settings_window = None
    
    self.menu_bar = Menu(root)
    root.config(menu = self.menu_bar)

    self.current_font_config = ('Arial', 12, 'normal')
    self.font_configs = {}

    # Hotkey Labels
    if platform.system() == 'Darwin':
      hotkey_new_tab = '⌘T'
      hotkey_new_window = '⌘N'
      hotkey_close_tab = '⌘W'
      hotkey_cut = '⌘X'
      hotkey_copy = '⌘C'
      hotkey_paste = '⌘P'
    else:
      hotkey_new_tab = '^T'
      hotkey_new_window = '^N'
      hotkey_close_tab = '^W'
      hotkey_cut = '^X'
      hotkey_copy = '^C'
      hotkey_paste = '^P'

    self.file_menu = Menu(self.menu_bar, tearoff = 0)
    self.menu_bar.add_cascade(label = 'File', menu = self.file_menu)
    self.file_menu.add_command(label = f'New Tab ({hotkey_new_tab})', command = self.new_tab)
    self.file_menu.add_command(label = f'New Window ({hotkey_new_window})')
    self.file_menu.add_command(label = f'Close Tab ({hotkey_close_tab})', command = self.close_tab)
    self.file_menu.add_command(label = 'Open')
    self.file_menu.add_command(label = 'Save')
    self.file_menu.add_separator()
    self.file_menu.add_command(label = 'Exit', command = self.exit_app)

    self.edit_menu = Menu(self.menu_bar, tearoff = 0)
    self.menu_bar.add_cascade(label = 'Edit', menu = self.edit_menu)
    self.edit_menu.add_command(label = 'Settings', command = self.open_settings)
    self.edit_menu.add_separator()
    self.edit_menu.add_command(label = f'Cut ({hotkey_cut})', command = self.cut_text)
    self.edit_menu.add_command(label = f'Copy ({hotkey_copy})', command = self.copy_text)
    self.edit_menu.add_command(label = f'Paste ({hotkey_paste})', command = self.paste_text)
    

    self.settings_button = ttk.Button(root, text = '⚙️', command = self.open_settings)
    self.settings_button.pack(side='right')

    self.notebook = ttk.Notebook(root)
    self.notebook.pack(expand=1, fill='both')

    self.new_tab()

    # New Tab Hotkeys
    root.bind('<Command-t>', self.new_tab)
    root.bind('<Control-t>', self.new_tab)

    # New Window Hotkeys
    root.bind('<Command-n>', self.new_window)
    root.bind('<Control-n>', self.new_window)

    # Close Tab Hotkeys
    root.bind('<Command-w>', self.close_tab)
    root.bind('<Control-w>', self.close_tab)

  def clear_existing_font_tags(self, text_widget, start, end):
    for tag in text_widget.tag_names():
      if tag.startswith('font_'):
        text_widget.tag_remove(tag, start, end)

  def configure_and_apply_tag(self, text_widget, font_config, start = '1.0', end = tk.END):
    self.clear_existing_font_tags(text_widget, start, end) 
    tag_name = f'font_{font_config}'
    text_widget.tag_configure(tag_name, font=font_config)
    text_widget.tag_add(tag_name, start, end)
    text_widget.tag_raise(tag_name)  

  def on_focus_in(self, event):
    text_widget = event.widget
    tag_name = f'font_{self.current_font_config}'
    text_widget.tag_configure(tag_name, font=self.current_font_config)

  def update_font(self, text_widget, font_config = None):
        if font_config:
            self.current_font_config = font_config
        tag_name = f'font_{self.current_font_config}'
        text_widget.tag_configure(tag_name, font = self.current_font_config)
        text_widget.tag_add(tag_name, '1.0', tk.END)

  def apply_font(self, font_family, font_size, font_style):
    print('apply_font called')  
    font_config = (font_family, font_size, font_style)
    text_widget = self.get_current_text_widget()
    tag_name = f'font_{font_config}'
    try:
       selected_text_indices = text_widget.tag_ranges('sel')
       print(f'Selected text indices: {selected_text_indices}')  
       if selected_text_indices:
          self.configure_and_apply_tag(text_widget, font_config, *selected_text_indices)  
       else:
          self.current_font_config = font_config 
    except tk.TclError:
       pass
    
  def on_keypress(self, event):
    text_widget = event.widget
    font_config = self.current_font_config  
    tag_name = f'font_{font_config}'
    text_widget.tag_configure(tag_name, font=font_config)
    cursor_index = text_widget.index(tk.INSERT)
    text_widget.tag_add(tag_name, cursor_index + ' -1c', cursor_index) 

  def get_current_text_widget(self):
    current_tab = self.notebook.select()
    text_widget = self.notebook.nametowidget(current_tab).winfo_children()[0]
    return text_widget


  def apply_font_to_all(self, font_family, font_size, font_style):
    font_config = (font_family, font_size, font_style)
    self.current_font_config = font_config 
    for tab in self.notebook.tabs():
      text_widget = self.notebook.nametowidget(tab).winfo_children()[0]
      self.configure_and_apply_tag(text_widget, font_config)

  def get_current_text_widget(self):
    current_tab = self.notebook.select()
    return self.notebook.nametowidget(current_tab).winfo_children()[0]

  def exit_app(self):
    self.play_alert_sound()
    user_response = messagebox.askokcancel('Exit', 'Are you sure you want to exit?')
    if user_response:
      self.root.destroy()
    self.root.destroy()

  def new_tab(self, event = None):
    tab = tk.Frame(self.notebook)
    self.notebook.add(tab, text = 'Untitled')
    text_widget = tk.Text(tab, wrap = 'word')
    text_widget.pack(expand = 1, fill = 'both')
    text_widget.bind('<FocusIn>', self.on_focus_in)
    text_widget.bind('<KeyPress>', self.on_keypress)

  def new_window(self, event = None):
    new_root = tk.Tk()
    new_app = NoteApp(new_root)
    center_window(new_root, 800, 600)
    new_root.mainloop()

  def close_tab(self, event = None):
    current_tab_index = self.notebook.index(self.notebook.select())
    if len(self.notebook.tabs()) > 1:
      self.notebook.forget(current_tab_index)
    else:
      messagebox.showinfo('Cannot close tab', 'At least one tab must remain open.')

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

  def open_settings(self):
    if self.settings_window and self.settings_window.window_exists():
      self.settings_window.focus()
      self.play_alert_sound()
    else:
     self.settings_window = SettingsWindow(self.root, self.notebook, self)

  def on_closing_settings(self):
    self.settings_window.destroy()
    self.settings_window = None

  def play_alert_sound(self):
    if platform.system() == 'Darwin':
      subprocess.Popen(['afplay', '/System/Library/Sounds/Tink.aiff'])
    elif platform.system() == 'Windows':
      # winsound.MessageBeep()
      pass

def center_window(root, width, height):
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  x_coordinate = (screen_width / 2) - (width  / 2)
  y_coordinate = (screen_height / 2) - (height / 2)
  root.geometry(f'{width}x{height}+{int(x_coordinate)}+{int(y_coordinate)}')

def run():
  root = tk.Tk()
  app = NoteApp(root)
  center_window(root, 800, 600)
  root.mainloop()

if __name__ == '__main__':
  run()