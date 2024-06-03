from os import makedirs,path

def create_path(file_path:str):
    """
    Crée un chemin complet, y compris tous les répertoires intermédiaires nécessaires, et crée un fichier à la fin du chemin.

    Args:
        file_path (str): Le chemin complet du fichier à créer.
    """
    try:
        makedirs(path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            pass
    except FileExistsError:
        print(f"Le chemin ou le fichier existe déjà : {file_path}")
    except Exception as e:
        print(f"Erreur lors de la création du chemin ou du fichier : {e}")