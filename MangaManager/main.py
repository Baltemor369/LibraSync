from modules.UI2 import UI
import os

# build executable : 
# pyinstaller --name MangaManager --noconsole --onefile --path modules main.py
# drag & drop .exe and asset/

# To do :
# + remake statistic display => a table (?)
# + use sqlite3 for database
# + feature : create a history mod (<=>logs)
# + feature : multiple delete && button "undo"
# + feature : add background design to each tab (theme : Japan)
# + feature : set a background color per manga
# + feature : redirection of "Modify" when "show less", to a tab with the list of the manga with the specific name
# + create a settings section : change colors, 

ui = UI()
ui.run()