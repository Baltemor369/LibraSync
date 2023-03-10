from modules.MangaUI import UI
import os

# To do :
# + volume "1-4"=> du volume 1 au 4
# + faire alignement affichage statistique
# + développer module historique(moyenne par semaine/mois voir combien ont été ajout pendant une semaine donnée)
# + fichier backup 

if not os.path.exists("data"):
    os.mkdir("data")
    os.system("type nul > data\data.txt")

ui = UI()
ui.mainloop()