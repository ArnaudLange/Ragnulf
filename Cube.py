from utils import Array, codeToColor, codeToGroup
from numpy import copy as np_copy

PETITS_CUBES = ['FU','FRU','FR','FRD','FD','LFD','FL','LFU','LU','LD',
                'BU','RBU','BR','RBD','BD','BLD','BL','BLU','RU','RD']

class Cube():
    """
    Cube

    La structure de donnée modélisant un cube ainsi que les fonctions de
    rotations qui s'y appliquent

    @see https://gitlab.univ-nantes.fr/E132397K/Ragnulf/issues/4 pour
    l'histoirique des choix effectués

    Codage des couleurs :
        White  (W) = 0
        Blue   (B) = 1
        Red    (R) = 2
        Green  (G) = 3
        Orange (0) = 4
        Yellow (Y) = 5

    Convention des couleurs des faces :
        Down  - White
        Front - Blue
        Right - Red
        Back  - Green
        Left  - Orange
        Up    - Yellow
    """

    def __init__(self):
        """
        __init__

        Création d'une nouvelle instance de Cube
        """

        self.cubes = {

            #1ère couronne
            'FU' : Array([1, 5]),
            'FRU': Array([1, 2, 5]),
            'RU' : Array([2, 5]),
            'RBU': Array([2, 3, 5]),
            'BU' : Array([3, 5]),
            'BLU': Array([3, 4, 5]),
            'LU' : Array([4, 5]),
            'LFU': Array([4, 1, 5]),

            #2ème couronne
            'FR' : Array([1, 2]),
            'BR' : Array([3, 2]),
            'BL' : Array([3, 4]),
            'FL' : Array([1, 4]),

            #3ème couronne
            'FD' : Array([1, 0]),
            'FRD': Array([1, 2, 0]),
            'RD' : Array([2, 0]),
            'RBD': Array([2, 3, 0]),
            'BD' : Array([3, 0]),
            'BLD': Array([3, 4, 0]),
            'LD' : Array([4, 0]),
            'LFD': Array([4, 1, 0]),
        }

    def __str__(self):
        """
        On veut retourner une chaîne du genre:
                   O G R
                   B W Y
                   B G B
            G Y Y  O Y O  W O W  G R Y
            O O O  B G B  R R Y  R B W
            W W R  B W Y  G R O  W G R
                   Y B R
                   G Y W
                   B O G
        """

        #Un espace pour constuire le patro ci-dessus
        space = [' ']

        #Une lignes d'espaces pour les blocs vides du patron ci-dessus
        empty = space * 3

        up = [
            [self.cubes['BLU'][2], self.cubes['BU'][1], self.cubes['RBU'][2]],
            [self.cubes['LU'][1],  5,                   self.cubes['RU'][1]],
            [self.cubes['LFU'][2], self.cubes['FU'][1], self.cubes['FRU'][2]],
        ]

        left = [
            [self.cubes['BLU'][1], self.cubes['LU'][0], self.cubes['LFU'][0]],
            [self.cubes['BL'][1],  4,                   self.cubes['FL'][1]],
            [self.cubes['BLD'][1], self.cubes['LD'][0], self.cubes['LFD'][0]],
        ]

        front = [
            [self.cubes['LFU'][1], self.cubes['FU'][0], self.cubes['FRU'][0]],
            [self.cubes['FL'][0],  1,                   self.cubes['FR'][0]],
            [self.cubes['LFD'][1], self.cubes['FD'][0], self.cubes['FRD'][0]],
        ]

        right = [
            [self.cubes['FRU'][1], self.cubes['RU'][0], self.cubes['RBU'][0]],
            [self.cubes['FR'][1],  2,                   self.cubes['BR'][1]],
            [self.cubes['FRD'][1], self.cubes['RD'][0], self.cubes['RBD'][0]],
        ]

        back = [
            [self.cubes['RBU'][1], self.cubes['BU'][0], self.cubes['BLU'][0]],
            [self.cubes['BR'][0],  3,                   self.cubes['BL'][0]],
            [self.cubes['RBD'][1], self.cubes['BD'][0], self.cubes['BLD'][0]],
        ]

        down = [
            [self.cubes['LFD'][2], self.cubes['FD'][1], self.cubes['FRD'][2]],
            [self.cubes['LD'][1],  0,                   self.cubes['RD'][1]],
            [self.cubes['BLD'][2], self.cubes['BD'][1], self.cubes['RBD'][2]],
        ]

        #On convertit tous les entiers en la couleur qui leur correspond
        for face in [up, left, front, right, back, down]:
            for ligne in range(3):
                for c in range(3):
                    #pour chaque case de chaque ligne de chaque face
                    face[ligne][c] = codeToColor(face[ligne][c])

        result = [] #tableau de toutes les lignes à afficher

        #les 3 premières lignes, il n'y a que la face up
        for i in range(3):
            result.append(empty + space + up[i] + space + empty + space + empty)

        #les 3 lignes suivantes, il y a left, front, right et back
        for i in range(3):
            result.append(left[i] + space + front[i] + space + right[i] + \
                    space + back[i])

        #les 3 dernières lignes, il y a que la face down
        for i in range(3):
            result.append(empty + space + down[i] + space + empty)

        return '\n'.join(''.join(l) for l in result) #on convertit la liste en chaîne

    def edit_cube(self, cube, val):
        '''
        edit_cube

        Édite le cube `cube` avec les données `val` en vérifiant sa validité

        On défini 3 groupes :
            - 0 : Blanc (0) et Jaune (5)
            - 1 : Orange (4) et Rouge (2)
            - 2 : Bleu (1) et Vert (3)

        On ne peut pas retrouver un groupe 0, 1 ou 2 plusieurs fois dans `val`

        :Args:
            cube    {String}    Identifiant du cube dans PETITS_CUBES
            val     {List}      Une liste de 2 ou 3 éléments (selon le cube),
                                entiers, codant la couleur (doivent être déjà validés)

        :Returns:
            {Boolean}           False : les valeurs ne représentent pas un cube
                                correct
        '''
        if not cube in PETITS_CUBES:
            return False
        else:
            groupes = [0] * 3
            for c in val:
                i = codeToGroup(c)
                if i == None:
                    return False
                else:
                    groupes[i] += 1

            #on garde les groupes qui sont présent plus d'une fois
            #si il y en a, c'est une erreur
            erreurs = [x for x in groupes if x > 1]
            erreur = len(erreurs) > 0

            if not erreur:
                self.cubes[cube] = Array(val)
                return True
            else:
                return False

    def rot_L(self):
        """
        rot_L

        Rotation de la face gauche (Left)
        """

        temp = np_copy(c.cubes['LFD'])

        c.cubes['LFD'][0] = c.cubes['LFU'][0]
        c.cubes['LFD'][1] = c.cubes['LFU'][2]
        c.cubes['LFD'][2] = c.cubes['LFU'][1]

        c.cubes['LFU'][0] = c.cubes['BLU'][1]
        c.cubes['LFU'][1] = c.cubes['BLU'][2]
        c.cubes['LFU'][2] = c.cubes['BLU'][0]

        c.cubes['BLU'][0] = c.cubes['BLD'][2]
        c.cubes['BLU'][1] = c.cubes['BLD'][1]
        c.cubes['BLU'][2] = c.cubes['BLD'][0]

        c.cubes['BLD'][0] = temp[2]
        c.cubes['BLD'][1] = temp[0]
        c.cubes['BLD'][2] = temp[1]

        temp = np_copy(c.cubes['LD'])

        c.cubes['LD'][0] = c.cubes['FL'][1]
        c.cubes['LD'][1] = c.cubes['FL'][0]

        c.cubes['FL'][0] = c.cubes['LU'][1]
        c.cubes['FL'][1] = c.cubes['LU'][0]

        c.cubes['LU'][0] = c.cubes['BL'][1]
        c.cubes['LU'][1] = c.cubes['BL'][0]

        c.cubes['BL'][0] = temp[1]
        c.cubes['BL'][1] = temp[0]

    def rot_Li(self):
        """
        rot_Li

        Rotation inverse de la face gauche (Left)
        """

        temp = np_copy(c.cubes['BLU'])

        c.cubes['BLU'][0] = c.cubes['LFU'][2]
        c.cubes['BLU'][1] = c.cubes['LFU'][0]
        c.cubes['BLU'][2] = c.cubes['LFU'][1]

        c.cubes['LFU'][0] = c.cubes['LFD'][0]
        c.cubes['LFU'][1] = c.cubes['LFD'][2]
        c.cubes['LFU'][2] = c.cubes['LFD'][1]

        c.cubes['LFD'][0] = c.cubes['BLD'][1]
        c.cubes['LFD'][1] = c.cubes['BLD'][2]
        c.cubes['LFD'][2] = c.cubes['BLD'][0]

        c.cubes['BLD'][0] = temp[2]
        c.cubes['BLD'][1] = temp[1]
        c.cubes['BLD'][2] = temp[0]

        temp = np_copy(c.cubes['LD'])

        c.cubes['LD'][0] = c.cubes['BL'][1]
        c.cubes['LD'][1] = c.cubes['BL'][0]

        c.cubes['BL'][0] = c.cubes['LU'][1]
        c.cubes['BL'][1] = c.cubes['LU'][0]

        c.cubes['LU'][0] = c.cubes['FL'][1]
        c.cubes['LU'][1] = c.cubes['FL'][0]

        c.cubes['FL'][0] = temp[1]
        c.cubes['FL'][1] = temp[0]

    def rot_R(self):
        """
        rot_R

        Rotation de la face droite (Right)
        """

        temp = np_copy(c.cubes['RBU'])

        c.cubes['RBU'][0] = c.cubes['FRU'][1]
        c.cubes['RBU'][1] = c.cubes['FRU'][2]
        c.cubes['RBU'][2] = c.cubes['FRU'][0]

        c.cubes['FRU'][0] = c.cubes['FRD'][2]
        c.cubes['FRU'][1] = c.cubes['FRD'][1]
        c.cubes['FRU'][2] = c.cubes['FRD'][0]

        c.cubes['FRD'][0] = c.cubes['RBD'][2]
        c.cubes['FRD'][1] = c.cubes['RBD'][0]
        c.cubes['FRD'][2] = c.cubes['RBD'][1]

        c.cubes['RBD'][0] = temp[0]
        c.cubes['RBD'][1] = temp[2]
        c.cubes['RBD'][2] = temp[1]

        temp = np_copy(c.cubes['RD'])

        c.cubes['RD'][0] = c.cubes['BR'][1]
        c.cubes['RD'][1] = c.cubes['BR'][0]

        c.cubes['BR'][0] = c.cubes['RU'][1]
        c.cubes['BR'][1] = c.cubes['RU'][0]

        c.cubes['RU'][0] = c.cubes['FR'][1]
        c.cubes['RU'][1] = c.cubes['FR'][0]

        c.cubes['FR'][0] = temp[1]
        c.cubes['FR'][1] = temp[0]

    def rot_Ri(self):
        """
        rot_Ri

        Rotation inverse de la face droite (Right)
        """

        temp = np_copy(c.cubes['FRD'])

        c.cubes['FRD'][0] = c.cubes['FRU'][2]
        c.cubes['FRD'][1] = c.cubes['FRU'][1]
        c.cubes['FRD'][2] = c.cubes['FRU'][0]

        c.cubes['FRU'][0] = c.cubes['RBU'][2]
        c.cubes['FRU'][1] = c.cubes['RBU'][0]
        c.cubes['FRU'][2] = c.cubes['RBU'][1]

        c.cubes['RBU'][0] = c.cubes['RBD'][0]
        c.cubes['RBU'][1] = c.cubes['RBD'][2]
        c.cubes['RBU'][2] = c.cubes['RBD'][1]

        c.cubes['RBD'][0] = temp[1]
        c.cubes['RBD'][1] = temp[2]
        c.cubes['RBD'][2] = temp[0]

        temp = np_copy(c.cubes['LD'])

        c.cubes['RD'][0] = c.cubes['FR'][1]
        c.cubes['RD'][1] = c.cubes['FR'][0]

        c.cubes['FR'][0] = c.cubes['RU'][1]
        c.cubes['FR'][1] = c.cubes['RU'][0]

        c.cubes['RU'][0] = c.cubes['BR'][1]
        c.cubes['RU'][1] = c.cubes['BR'][0]

        c.cubes['BR'][0] = temp[1]
        c.cubes['BR'][1] = temp[0]

    def rot_F(self):
        """
        rot_F

        Rotation de la face avant (Front)
        """
        c.cubes['FRU'], c.cubes['FRD'], c.cubes['FLD'], c.cubes['FLU'] = c.cubes['FRD'],c.cubes['FLD'], c.cubes['FLU'], c.cubes['FRU']
        c.cubes['FU'], c.cubes['FR'], c.cubes['FD'], c.cubes['FL'] = c.cubes['FR'],c.cubes['FD'], c.cubes['FL'], c.cubes['FU']

    def rot_Fi(self):
        """
        rot_Fi

        Rotation inverse de la face avant (Front)
        """
        c.cubes['FRD'],c.cubes['FLD'], c.cubes['FLU'], c.cubes['FRU'] = c.cubes['FRU'], c.cubes['FRD'], c.cubes['FLD'], c.cubes['FLU']
        c.cubes['FR'],c.cubes['FD'], c.cubes['FL'], c.cubes['FU'] = c.cubes['FU'], c.cubes['FR'], c.cubes['FD'], c.cubes['FL']

    def rot_B(self):

        """
        rot_B

        Rotation de la face arrière (Back)
        """
        c.cubes['BRU'],c.cubes['BRD'], c.cubes['BLD'], c.cubes['BLU'] = c.cubes['BRD'], c.cubes['BLD'], c.cubes['BLU'], c.cubes['BRU']
        c.cubes['BR'],c.cubes['BD'], c.cubes['BL'], c.cubes['BU'] = c.cubes['BD'], c.cubes['BL'], c.cubes['BU'], c.cubes['BR']

    def rot_Bi(self):
        """
        rot_Bi

        Rotation inverse de la face arrière (Back)
        """
        #TODO
        pass

    def rot_U(self):
        """
        rot_U

        Rotation de la face du haut (Up)
        """
        c.cubes['FRU'], c.cubes['RBU'], c.cubes['BLU'], c.cubes['LFU'] \
            = c.cubes['RBU'], c.cubes['BLU'], c.cubes['LFU'], c.cubes['FRU']

        c.cubes['FU'], c.cubes['RU'], c.cubes['BU'], c.cubes['LU'] \
            = c.cubes['RU'],c.cubes['BU'], c.cubes['LU'], c.cubes['FU']

    def rot_Ui(self):
        """
        rot_Ui

        Rotation inverse de la face du haut (Up)
        """
        c.cubes['FRU'], c.cubes['RBU'], c.cubes['BLU'], c.cubes['LFU'] \
            = c.cubes['LFU'], c.cubes['FRU'], c.cubes['RBU'], c.cubes['BLU']

        c.cubes['FU'], c.cubes['RU'], c.cubes['BU'], c.cubes['LU'] \
            = c.cubes['LU'],c.cubes['FU'], c.cubes['RU'], c.cubes['BU']

    def rot_D(self):
        """
        rot_D

        Rotation de la face du bas (Down)
        """
        c.cubes['FRD'], c.cubes['RBD'], c.cubes['BLD'], c.cubes['LFD'] \
            = c.cubes['LFD'], c.cubes['FRD'], c.cubes['RBD'], c.cubes['BLD']

        c.cubes['FD'], c.cubes['RD'], c.cubes['BD'], c.cubes['LD'] \
            = c.cubes['LD'],c.cubes['FD'], c.cubes['RD'], c.cubes['BD']

    def rot_Di(self):
        """
        rot_Di

        Rotation inverse de la face du bas (Down)
        """
        c.cubes['FRD'], c.cubes['RBD'], c.cubes['BLD'], c.cubes['LFD'] \
            = c.cubes['RBD'], c.cubes['BLD'], c.cubes['LFD'], c.cubes['FRD']

        c.cubes['FD'], c.cubes['RD'], c.cubes['BD'], c.cubes['LD'] \
            = c.cubes['RD'],c.cubes['BD'], c.cubes['LD'], c.cubes['FD']

if __name__ == '__main__':

    # Exemple d'utilisation du Cube
    c = Cube() #par défaut, ce cube est résolu
    print(c)

    print(c.cubes['FRU'], type(c.cubes['FRU'])) #<calss 'numpy.ndarray'>
    c.cubes['FRU'] = Array([0, 1, 2]) #on remplit avec les couleurs qui vont bien
    c.cubes['FRU'][0] = 4             #ou
    print(c.cubes['FRU'])

    print('Test rotations')

    print('rot_L')
    c = Cube()
    c.rot_L()
    print(c)

    print('rot_Li')
    c = Cube()
    c.rot_Li()
    print(c)

    print('rot_R')
    c = Cube()
    c.rot_R()
    print(c)

    print('rot_Ri')
    c = Cube()
    c.rot_Ri()
    print(c)

    print('rot_U')
    c = Cube()
    c.rot_U()
    print(c)

    print('rot_Ui')
    c = Cube()
    c.rot_Ui()
    print(c)

    print('rot_D')
    c = Cube()
    c.rot_D()
    print(c)

    print('rot_Di')
    c = Cube()
    c.rot_Di()
    print(c)
