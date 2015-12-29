from time import sleep
from utils import clear
from algo import algo_cfop

SPEED = 2 #écrans / sec

def tuto(cube, mouvements):
    """
    tuto

    :Args:
        cube        {Cube}      Un cube à la sortie de lecture_cube
        mouvements  {List}      Suite de mouvements à appliquer sur le cube
                                pour le résoudre, calculée par algo_cfop()
    """
    clear()
    print(cube)

    for m in mouvements:
        clear()
        method = getattr(cube, 'rot_' + m)
        method()
        print(cube)
        print(m)
        sleep(1 / SPEED)

if __name__ == '__main__':
    from lire_entree import lecture_cube
    cube = 'OGRBWYBGBGYYOYOWOWGRYOOOBGBRRYRBWWWRBWYGROWGRYBRGYWBOG'
    error, c = lecture_cube(cube)
    if error:
        raise Error(error)

    c0 = c.copy()

    mouvements = algo_cfop(c)

    tuto(c0, mouvements)
