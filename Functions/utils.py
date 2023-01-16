import random


def get_random_color(name_idx: int) -> tuple[int, int, int]:
    """
    Génère une couleur aléatoire pour un objet
    @param name_idx: Identifiant de l'objet
    @return: Couleur aléatoire
    """
    random.seed(name_idx)
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b