from modules.MangaUI import UI
import os

# To do :
# + faire alignement affichage statistique
# + développer module historique(moyenne par semaine/mois voir combien ont été ajout pendant une semaine donnée)
# + fichier backup
# + multiple delete || button "undo"
# + faire liste comme mails page de 10 
# + mettre valeur par default à description et author
# + proposer une couleur de fonds par manga

if not os.path.exists("data"):
    os.mkdir("data")
    os.system("type nul > data\data.txt")

ui = UI()
ui.mainloop()