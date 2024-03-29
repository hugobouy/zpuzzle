# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:23:08 2021

@author: Groupe 3 : Aurélie, Tristan et Hugo BOUY
"""

import tkinter as tk
import random
import math
import os

import crop_image
from tkinter.messagebox import askyesno


class Application():
    '''Contients des objets correspondant à une fenêtre de jeu'''

    # Utilisée pour connaître l'issue du jeu
    victory = False
    # Utilisée pour connaître le type de clic
    clic_type = 0
    # Utilisée pour contrôler la machine à état
    status = 0
    # Utilisée pour le callback de la machie à état
    chrono_stop = True

    def __init__(self, n_pc_w, n_pc_h, image, ratio):
        '''Crée une fenêtre tkinter. Prend en paramètres :
            n_pc_w : nombre de pièces en largeur
            n_pc_h : nombre de pièces en hauteur
            image : image type ImagePuzzle (géré par le fichier crop_image)
            ratio : rapport entre la largeur et la hauteur de l'image'''

        # Mémorisation des paramètres
        self.n_pc_w, self.n_pc_h, self.ratio = n_pc_w, n_pc_h, ratio
        self.image = image

        # Création de la fenêtre
        self.wnd = tk.Tk()
        self.wnd.title("ZPuzzle")

        # On adpate la taille de la fenêtre à la résolution de l'écran
        # de l'utilisateur

        screen_height = self.wnd.winfo_screenheight()
        screen_width = self.wnd.winfo_screenwidth()

        # La hauteur du canvas est égale à 5/10 de la hauteur de l'écran
        self.cnv_height = int((5/10) * screen_height)
        
        # La hauteur de la frame des scores 3/20 de la hauteur du canvas
        self.top_frame_height = int((3/20) * self.cnv_height)

        # On calcul la hauteur d'une pièce
        self.pc_h = int((self.cnv_height - self.top_frame_height)/
            (self.n_pc_h + (1/4)*(self.n_pc_h + 3)))

        # La marge est égale à 1/4 de la hauteur d'une pièce
        self.margin = self.pc_h/4

        # On calcule la largeur d'une pièce avec le ratio de l'image
        self.pc_w = int(self.pc_h*self.ratio)

        # On en déduit la largeur du canvas et de la fenêtre
        self.cnv_width = int(2*self.pc_w*self.n_pc_w +
            self.margin*(self.n_pc_w + 2))
        self.width = self.cnv_width

        # La fenêtre n'est pas redimentionnable
        self.wnd.resizable(width=False, height=False)

        # Positionnement de la fenêtre sur l'écran
        string = '-' + str(int(screen_width/2 - self.width/2)) + '+0'
        self.wnd.geometry(string)

        # Création de la zone de dessin
        self.cnv = tk.Canvas(self.wnd, width=self.cnv_width,
            height=self.cnv_height, bg='white', bd=0, highlightthickness=0,
            relief='ridge')
        self.cnv.pack(side=tk.TOP)

        # Création des éléments servant pour la découpe de l'image

        # Récupération de la liste des tuiles de l'image
        tiles = image.crop(self.n_pc_w * self.n_pc_h)
        list_tiles = image.create_tiles_tk(tiles, self.pc_w, self.pc_h)

        # Ajout d'un indice pour la vérification
        self.list_tiles_i = [[list_tiles[i], i]
                             for i in range(len(list_tiles))]

        # Mélange de la liste
        random.shuffle(self.list_tiles_i)

        # Conversion en matrice self.n_pc_w*self.n_pc_h
        mat_tiles = [[[self.list_tiles_i[i][0], self.list_tiles_i[i][1]]
                     for i in range(j, self.n_pc_w + j)]
                     for j in range(0, self.n_pc_h*self.n_pc_w, self.n_pc_w)]

        # Création de la zone de commande du jeu
        self.frm = tk.Frame(self.wnd,
            width=self.cnv_width, bg='green')
        self.frm.pack(side=tk.BOTTOM, fill=tk.X)

        self.sub_frm = tk.Frame(self.frm, bg='green', width=self.cnv_width)
        self.sub_frm.pack(side=tk.TOP, pady=self.margin)

        # Création de la zone de score

        self.top_frame = tk.Frame(self.cnv, height=self.top_frame_height,
            width=self.cnv_width, bg='green')

        self.top_frame.pack_propagate(0)
        self.top_frame.place(x=0, y=0, anchor=tk.NW)

        # Création des boutons

        self.start_button = tk.Button(self.sub_frm, text='Start', bg='white',
            font=('Franklin Gothic Demi Cond', 10), bd=5, overrelief='raised',
            relief='flat', command=self.start_pause_game)
        self.start_button.grid(column=0, row=1, sticky='n', pady=5)
        tk.Button(self.sub_frm, text='Quitter', bg='white',
            font=('Franklin Gothic Demi Cond', 10), bd=5, overrelief='raised',
            relief='flat', command=self.stop_game)\
            .grid(column=1, row=1, sticky='n', pady=5)
        self.submit_button = tk.Button(self.sub_frm, text='Soumettre',
            bg='white', font=('Franklin Gothic Demi Cond', 10), bd=5,
            overrelief='raised', relief='flat', command=self.submit)
        self.submit_button.grid_forget()

        tk.Button(self.sub_frm, text='Niveau 1', bg='white',
            font=('Franklin Gothic Demi Cond', 10), bd=5, overrelief='raised',
            relief='flat', command=self.first_level)\
            .grid(column=0, row=2, sticky='n', pady=5, padx=self.margin)
        tk.Button(self.sub_frm, text='Niveau 2', bg='white',
            font=('Franklin Gothic Demi Cond', 10), bd=5, overrelief='raised',
            relief='flat', command=self.second_level)\
            .grid(column=1, row=2, sticky='n', pady=5, padx=self.margin)
        tk.Button(self.sub_frm, text='Niveau 3', bg='white',
            font=('Franklin Gothic Demi Cond', 10), bd=5, overrelief='raised',
            relief='flat', command=self.third_level)\
            .grid(column=2, row=2, sticky='n', pady=5, padx=self.margin)
        tk.Button(self.sub_frm, text="Changer d'image", bg='white',
            font=('Franklin Gothic Demi Cond', 10), bd=5, overrelief='raised',
            relief='flat', command=self.change_image)\
            .grid(column=1, row=3, sticky='n', pady=5)

        # Création des Labels d'information

        tk.Label(self.top_frame, text='VOTRE SCORE: ',
            width=14, bg='green', fg='white',
            font=('Franklin Gothic Demi Cond', 12))\
            .pack(side=tk.LEFT, pady=5, padx=5)
        self.attempt_label = tk.Label(self.top_frame, text='Déplacement : 0',
            width=17, bg='green', fg='white',
            font=('Franklin Gothic Demi Cond', 12))
        self.attempt_label.pack(side=tk.LEFT, pady=5, padx=5)
        self.chrono_label = tk.Label(self.top_frame, text='Temps écoulé : 0s',
                               width=30, bg='green', fg='white',
                               font=('Franklin Gothic Demi Cond', 12))
        self.chrono_label.pack(side=tk.LEFT, pady=5, padx=5)
        self.fail_label = tk.Label(self.sub_frm, text='', bg='green',
            fg='red', font=('Franklin Gothic Demi Cond', 12))
        self.fail_label.grid_forget()

        # Remise à zéro du chrono
        self.sec = 0
        self.min = 0
        self.hour = 0
        self.chrono_on = [False, None]
        self.move = 0

        '''Pour fonctionner, le jeu utilise 3 classes suplémentaires:

            ObjectCanvas : Mémorise toutes les informations des tuiles sur le
            canvas (coordonnées, tag...). Chaque tuile a son ObjectCanvas
            correspondant. L'ensemble des ObjectCanvas est ensuite mémorisé
            dans la liste self.object_list

            PlaceCanvas : Mémorise les informations de chaque emplacement
            disponible sur le canvas. Un emplacement est soit l'emplacement
            initiale de la tuile, soit une case du plateau de jeu.
            L'ensemble des PlaceCanvas est mémorisé dans la liste
            self.authorized_pos'

            ObjectSelect : Mémorise lorsqu'un objet est sélectionné :
                - Son ObjectCanvas coorespondant
                - Son emplacement PlaceCanvas initial/de départ
                - Et la bordure verte indiquant que l'objet est sélectionné
        '''

        # Création des éléments de jeux (tuiles + emplacements)
        self.object_list = list()
        self.authorized_pos = list()
        # Variable mémorisant l'objet sélectionné du type ObjectSelect
        self.object = None
        # Utilisé pour le tag canvas de l'objet
        id_p = 0

        # Etape 1: Création du plateau de jeu
        for i in range(self.n_pc_h):
            for j in range(self.n_pc_w):
                x, y = i*self.pc_w + self.margin, j*self.pc_h +\
                    (self.cnv_height - self.top_frame_height -
                     self.n_pc_h*self.pc_h - 2*self.margin)/2 +\
                     self.top_frame_height
                self.cnv.create_rectangle(x, y, x + self.pc_w, y + self.pc_h)
                # Sauvegarde chaque emplacement dessiné
                self.authorized_pos.append(PlaceCanvas(x, y, None))

        # Etape 2 : Affichage des tuiles dans la pioche
        for i in range(self.n_pc_h):
            for j in range(self.n_pc_w):
                # Affichage des images découpés
                xi = self.pc_w*(self.n_pc_w) + self.margin*2 + \
                    i*(self.pc_w + self.margin)
                yi = j*(self.pc_h + self.margin) + self.margin +\
                    self.top_frame_height
                tag = "Object" + str(id_p)
                self.cnv.create_image(xi + self.pc_w/2, yi + self.pc_h/2,
                    image=mat_tiles[i][j][0], tag=tag)
                # Sauvegarde chaque objet crée
                self.object_list.append(ObjectCanvas(xi, yi, tag,
                    mat_tiles[i][j][1]))
                # Sauvegarde l'emplacement correspondant
                self.authorized_pos.append(PlaceCanvas(xi, yi,
                    self.object_list[-1]))
                id_p += 1

        # Création des éléments de dessin graphiques :
        # Création de la sinusoide

        # Configuration
        # Pas suivant x
        x_increment = 1
        # Largeur du sinus
        x_factor = x_increment / 150
        # Amplitude du sinus
        y_amplitude = self.margin

        '''Calcule tous les "x_increment" (pas) la valeur du sinus
        la place dans un tableau de valeur avec l'abscisse, puis crée un
        polygone avec ces coordonnées'''

        xy = list()
        i = 0
        while x < self.cnv_width:
            x = i * x_increment
            xy.append(x)
            y = int(math.sin(i * x_factor) * y_amplitude)
            xy.append(-y + self.cnv_height - y_amplitude)
            i += 1
        xy.append(self.cnv_width)
        xy.append(self.cnv_height)
        xy.append(0)
        xy.append(self.cnv_height)
        self.cnv.create_polygon(xy, fill='green')

        self.wnd.protocol("WM_DELETE_WINDOW", self.stop_game)
        self.wnd.mainloop()

    '''Pour chaque 'clic' de souris différent (clic, relachement du clic
    ou déplacement de la souris avec le clic maintenu), une fonction
    correspondante appelle la machine a état'''

    def clic(self, event):
        '''Appelée si un clic a eu lieu'''
        self.clic_type = 1
        self.state_machine(event.x, event.y)

    def drag_clic(self, event):
        '''Appelée si un déplacement de la souris avec le clic maintenu
        a eu lieu'''
        self.clic_type = 2
        self.state_machine(event.x, event.y)

    def release_clic(self, event):
        '''Appelée quand le clic est relaché'''
        self.clic_type = 3
        self.state_machine(event.x, event.y)

    def submit(self):
        '''Verification du puzzle lorsque l'utilisateur appuis sur le bouton
        soumettre'''
        self.victory = True
        self.start_button.grid_forget()
        self.chrono_on[0] = False
        wrong_pos_object = list()
        # On vérifie emplacement par emplacement si ce dernier est
        # occupé par la bonne pièce
        i = 0
        for k in range(self.n_pc_w * self.n_pc_h):
            if k != self.authorized_pos[k].ob.number:
                i += 1
                self.victory = False
                # En cas de pièce au mauvaise endroit, on affiche
                # un rectangle rouge par dessus
                x, y = self.authorized_pos[k].x, self.authorized_pos[k].y
                rectangle = self.cnv.create_rectangle(x, y, x + self.pc_w, y +
                    self.pc_h, outline='red', fill="red", width=2,
                    stipple="gray50")
                current_object = ObjectSelect(self.authorized_pos[k].ob,
                                              self.authorized_pos[k])
                # On mémorise la pièce et son rectangle dans une liste
                wrong_pos_object.append([current_object, rectangle])
        if not self.victory:
            # En cas de mauvaise combinaison, le bouton Retirer s'affiche
            self.submit_button.config(text="Retirer", command=lambda:
                        self.return_wrong_pos_object(wrong_pos_object))
            # On affiche le nombre de pièce mal positionnées
            string = "Nombre d'erreur : " + str(i)
            self.fail_label.config(text=string)
            self.fail_label.grid(column=1, row=4, sticky='n', pady=5)
            # On désactive les clics
            self.cnv.unbind('<Button-1>')
            self.cnv.unbind('<B1-Motion>')
            self.cnv.unbind('<ButtonRelease-1>')
        else:
            # Sinon c'est la victoire !
            self.chrono_on[0] = False
            Winframe(self.wnd, self.sec, self.min, self.hour, self.move)
            self.cnv.unbind('<Button-1>')
            self.cnv.unbind('<B1-Motion>')
            self.cnv.unbind('<ButtonRelease-1>')

    def return_wrong_pos_object(self, wrong_pos_object):
        '''Retourne les pièces étant à la mauvaise position à un emplacement
        disponible'''
        for i in range(len(wrong_pos_object)):
            self.send_back_object_to_deck(wrong_pos_object[i][0])
            self.cnv.delete(wrong_pos_object[i][1])
        # On enlève le bouton retirer
        self.submit_button.config(text="Soumettre", command=self.submit)
        self.submit_button.grid_forget()
        # On enlève l'affichage du nombre d'erreur
        self.fail_label.grid_forget()
        # On réactive les clics :
        self.chrono_on[0] = True
        self.timer()
        self.start_button.grid(column=0, row=1, sticky='n', pady=5)
        self.cnv.bind('<Button-1>', self.clic)
        self.cnv.bind('<B1-Motion>', self.drag_clic)
        self.cnv.bind('<ButtonRelease-1>', self.release_clic)

    def start_pause_game(self):
        '''Lance la partie ou met en pause la partie'''
        if self.chrono_on[0]:
            # On désactive les clics
            self.cnv.unbind('<Button-1>')
            self.cnv.unbind('<B1-Motion>')
            self.cnv.unbind('<ButtonRelease-1>')
            self.chrono_on[0] = False
            self.start_button.config(text="Play")
        else:
            # Bind des touches de la souris
            self.cnv.bind('<Button-1>', self.clic)
            self.cnv.bind('<B1-Motion>', self.drag_clic)
            self.cnv.bind('<ButtonRelease-1>', self.release_clic)
            # Lance le timer
            self.chrono_on[0] = True
            self.timer()
            self.start_button.config(text="Pause")

    def stop_game(self):
        '''Stop la partie'''
        self.chrono_on[0] = False
        if self.chrono_on[1] is not None:
            self.wnd.after_cancel(self.chrono_on[1])
        self.wnd.destroy()

    def timer(self):
        ''' Méthode permettant le suivi du temps écoulé après le lancement
        du jeu '''
        if self.chrono_on[0]:
            if self.min == 59 and self.sec == 59:
                self.hour += 1
                self.min = 0
                self.sec = 0
            if self.sec == 59:
                self.sec = 0
                self.min += 1
            else:
                self.sec += 1
                string = "Temps écoulé : " + str(self.sec) + " s"
            if self.min > 0:
                string = "Temps écoulé :" + str(self.min) + " m : " +\
                    str(self.sec) + " s"
            if self.hour > 0:
                string = "Temps écoulé : " + str(self.hour) + " h : " +\
                    str(self.min) + " m : " + str(self.sec) + " s"
            self.chrono_on[1] = self.wnd.after(1000, self.timer)
            self.chrono_label.config(text=string)

    def update_score(self):
        '''Méthode affichant le score du joueur'''
        self.move += 1
        string = 'Déplacements: ' + str(self.move)
        self.attempt_label.config(text=string)

    '''
    Pour la machine à état, il existe deux modes de déplacement :
        Mode 1 : L'utilisateur clic une première fois sur un objet puis
        une deuxième fois sur une case vide : l'objet se déplace.
        Mode dit 'clic and move'
        Mode 2 : L'utlisateur clic sur un objet et le déplace avec sa
        souris jusqu'à l'emplacement voulu. Mode dit 'drag and drop'.'''

    def state_machine(self, event_x=None, event_y=None):
        '''Machine à état contrôlant les évènements du jeu'''
        # Status = 0, la machine attend le clic initial
        if self.status == 0:
            # Si c'est un clic qui appelle la machine
            if self.clic_type == 1:
                # Si le clic est sur un emplacement valide
                result = self.is_valid_pos(event_x, event_y)
                if result is not None:
                    # Si l'emplacement n'est pas vide
                    if result.ob is not None:
                        # On active la sélection sur l'objet présent
                        # sur l'emplacement
                        self.status = 1
                        self.active_selection_on_object(result.ob, result)

        # Status = 1, la machine attend l'évènement suivant le clic initial
        elif self.status == 1:
            # Si le clic est relaché
            if self.clic_type == 3:
                # On lance un chrono, ce chrono servira à différencier
                # un double clic rapide sur le même objet, de deux clic
                # espacés dans le temps sur le même objet.
                self.status = 2
                self.chrono_pc_stop = False
                self.cnv.after(200, self.stop_chrono)
            # Si l'évènement est un "drag_clic"
            else:
                self.status = 3

        # Status = 2, la machine attend le prochain clic après le clic initial
        # (mode 1: clic and move)
        elif self.status == 2:
            result = self.is_valid_pos(event_x, event_y)

            # Si le deuxième clic n'est pas sur un emplacement valide
            if result is None:
                # On retire la sélection active
                self.desactivate_curent_selection()

            # Sinon on regarde par qui est occupé l'emplacement
            # Si l'emplacement est libre
            elif result.ob is None:
                # On déplace l'objet et désactive la sélection active
                self.send_object_to_final_pos(self.object, result)

            # Si le clic est effectué une deuxième fois sur le même objet
            elif result.ob == self.object.object:
                # Si le chrono ne s'est pas arrêté,
                # on retourne l'objet dans la pioche
                if not self.chrono_pc_stop:
                    self.send_back_object_to_deck(self.object)
                # Sinon, on attend de nouveau un clic, retour à Status = 1
                else:
                    self.status = 1

            # Si le clic est effectué sur un autre objet
            # On active la sélection sur cet objet
            else:
                self.desactivate_curent_selection()
                self.active_selection_on_object(result.ob, result)
                self.status = 1

        # Status = 3, la machine attend le déplacement
        # ou relachement de la souris (mode 2: drag and drop)
        else:
            # Si la souris se déplace
            if self.clic_type == 2:
                # On fait suivre l'objet
                self.move_object(self.object, event_x - self.pc_w/2,
                                 event_y - self.pc_h/2)
            # Si le clic est relaché
            else:
                # On vérifie l'emplacement
                result = self.is_valid_pos(event_x, event_y)
                # Si l'emplacement est invalide ou occupé
                if (result is None) or (result.ob is not None):
                    # On revoie l'objet à sa position initiale
                    self.move_object(self.object, self.object.init_pos.x,
                                     self.object.init_pos.y)
                    # Si l'utilisateur re-dépose l'objet sur sa case initiale
                    if result is not None and result.ob == self.object.object:
                        # On ne désactive pas la sélection
                        self.status = 2
                    # Si l'utilisateur dépose l'objet sur une case contentant
                    # déjà un autre objet
                    elif result is not None and result.ob is not None:
                        # On échange intervertit les deux objets
                        self.swap_two_object(self.object,
                                             ObjectSelect(result.ob, result))
                    else:
                        # Sinon, on retire la sélection active
                        self.desactivate_curent_selection()
                # Si l'emplacement est libre
                else:
                    # On y déplace l'objet
                    self.send_object_to_final_pos(self.object, result)

    def swap_two_object(self, object1, object2):
        '''Enchange la position de deux objets'''
        # 1 : On déplace les deux objets
        self.move_object(object1, object2.init_pos.x, object2.init_pos.y)
        self.move_object(object2, object1.init_pos.x, object1.init_pos.y)
        # 2 : On met à jour leur emplacement initial
        object1.init_pos.ob = object2.object
        object2.init_pos.ob = object1.object
        # 3 : On désactive la sélection
        self.desactivate_curent_selection()
        # 4 : On vérifie si le puzzle est complet
        self.check_puzzle_complete()
        # 5 : On met à jour le score
        self.update_score()

    def send_object_to_final_pos(self, object_select, pos):
        '''Envoie l'object de type ObjectSelect
        passé en argument vers sa position finale pos'''
        # 1 : On déplace l'objet
        self.move_object(object_select, pos.x, pos.y)
        # 2 : On met à jour l'emplacement initial
        object_select.init_pos.ob = None
        # 3 : On met à jour l'emplacement final
        pos.ob = object_select.object
        # 4 : On désactive la sélection
        if object_select.border is not None:
            self.desactivate_curent_selection()
        # 5 : On vérifie si le puzzle est complet
        self.check_puzzle_complete()
        # 6 : On met à jour le score
        self.update_score()

    def send_back_object_to_deck(self, object_select):
        '''Renvoie l'objet passé en argument dans la pioche'''
        for k in range(self.n_pc_w * self.n_pc_h, len(self.authorized_pos)):
            if self.authorized_pos[k].ob is None:
                # On déplace l'objet dans le premier emplacement libre de la
                # pioche trouvé
                self.send_object_to_final_pos(object_select,
                                              self.authorized_pos[k])
                return

    def move_object(self, object_select, x, y):
        '''Déplace l'objet de type ObjectSelect passé en argument
        dans le canvas aux coordonnées x, y'''
        difx = - (object_select.object.x - x)
        dify = - (object_select.object.y - y)
        # On met à jour les coordonnées de l'objet
        object_select.object.x = x
        object_select.object.y = y
        self.cnv.move(object_select.object.tag, difx, dify)
        # Si l'objet contient une bordure
        if object_select.border is not None:
            self.cnv.move(object_select.border, difx, dify)

    def stop_chrono(self):
        '''Arrête le chrono de la machine à état'''
        self.chrono_pc_stop = True

    def active_selection_on_object(self, object_select, place):
        '''Active la sélection sur l'objet passé en argument.
        Dessine un contour vert autour de lui et le mémorise'''
        # Passe au premier plan l'objet sélectionné
        self.cnv.tag_raise(object_select.tag)
        rectangle = self.cnv.create_rectangle(object_select.x, object_select.y,
            object_select.x + self.pc_w, object_select.y + self.pc_h,
            outline='green', fill="", width=5)
        self.object = ObjectSelect(object_select, place, rectangle)

    def desactivate_curent_selection(self):
        '''Désactive la sélection sur l'objet self.object en cours'''
        self.cnv.delete(self.object.border)
        self.object = None
        self.status = 0

    def is_valid_pos(self, x, y):
        '''Retourne l'emplacement de type PlaceCanvas aux coordonnées passées
        en argument. Retourne None si x, y ne correspond aux coordonnées
        d'aucun emplacement valide'''
        for i in range(len(self.authorized_pos)):
            if (x >= self.authorized_pos[i].x) and \
                    (x <= self.authorized_pos[i].x + self.pc_w):
                if (y >= self.authorized_pos[i].y) and \
                        (y <= self.authorized_pos[i].y + self.pc_h):
                    return self.authorized_pos[i]
        return None

    def check_puzzle_complete(self):
        '''Vérifie si le puzzle est complet.
        Si oui affichage du bouton soumettre'''
        for k in range(self.n_pc_w * self.n_pc_h):
            if self.authorized_pos[k].ob is None:
                self.submit_button.grid_forget()
                return
        self.submit_button.grid(column=2, row=1, sticky='n', pady=5)

    def first_level(self):
        '''Relance l'application avec le premier niveau : 2x2'''
        self.stop_game()
        Application(2, 2, self.image, self.ratio)

    def second_level(self):
        '''Relance l'application avec le second niveau : 5x5'''
        self.stop_game()
        Application(5, 5, self.image, self.ratio)

    def third_level(self):
        '''Relance l'application avec le troisième niveau : 6x6'''
        self.stop_game()
        Application(6, 6, self.image, self.ratio)

    def change_image(self):
        '''Relance l'application sur la fenêtre de selection d'image'''
        self.stop_game()
        SelectImage("images")


class ObjectCanvas():
    '''Contients les caractéristiques d'objets du canvas'''

    def __init__(self, x, y, tag, number):
        '''Mémorise les caractéristiques de l'objet :
            x, y : coordonnées du coin supérieur gauche
            tag : tag de l'objet dans le canvas
            number : numéro de tuile pour la vérification'''
        self.x, self.y, self.tag, self.number = x, y, tag, number

    def __str__(self):
        '''Affiche les caractéristiques de l'objet (pour debug)'''
        r = str(self.x) + ', ' + str(self.y) + ", tag=" + str(self.tag)\
            + " number=" + str(self.number)
        return r


class ObjectSelect():
    '''Contients les caractéristiques de l'objet sélectionné
        object : contient l'objet du type ObjectCanvas
        border : contient le rectangle indiquant que l'objet est
        initPos : contient l'emplacement du type PlaceCanvas de départ
        de l'objet sélectionné'''

    def __init__(self, object_select, init_pos, border=None):
        self.object, self.border = object_select, border
        self.init_pos = init_pos


class PlaceCanvas():
    '''Contients des emplacements possible des pièce de jeu sur le canvas'''

    def __init__(self, x, y, occupied_by):
        '''Mémorise les caractéristiques de l'emplacement :
            x, y : coordonnées du coin supérieur gauche
            occupied_by : objet occupant l'emplacement '''
        self.x, self.y, self.ob = x, y, occupied_by


class Winframe(tk.Toplevel):
    '''Contient les éléments qui résumment le score du joueur'''

    def __init__(self, parent, sec, m, hour, nbcoup):
        super().__init__(parent)
        # Configuration de la fenêtre
        self.geometry("-690+350")
        # Met la fenêtre au premier plan
        self.wm_attributes('-topmost', 1)
        self.title("Score final")
        self.config(bg='white')
        frm = tk.Frame(self, bg='white')
        frm.pack()
        # Définition du score total
        if hour >= 1:
            self.time_total = 'Temps total: ' + str(hour) + " h : " + str(m) +\
                " m : " + str(sec) + " s"
        if m >= 1:
            self.time_total = 'Temps total: ' + str(m) + " m : " +\
                str(sec) + " s"
        else:
            self.time_total = 'Temps total: ' + str(sec) + " s"
        self.nbmove_total = 'Nombre de déplacements totaux : ' + str(nbcoup)
        tk.Label(frm, text="Félicitation ! Vous venez de terminer votre" +
                 " puzzle !", font=('Franklin Gothic Demi Cond', 12),
                 bg='green', fg='white').pack()
        tk.Label(frm, text="\n Voici votre résultat :", bg='white',
                 fg='green').pack()
        tk.Label(frm, text='\n' + self.time_total, bg='white',
                 fg='green').pack(pady=10, padx=50)
        tk.Label(frm, text='\n' + self.nbmove_total, bg='white', fg='green')\
            .pack(pady=10, padx=50)
        # Création des boutons pour rejouer ou quitter
        tk.Button(frm, text="Recommencer",
                  font=('Franklin Gothic Demi Cond', 11), bg='white',
                  relief='flat', overrelief='groove',
                  command=lambda: self.restart(parent)).pack()
        tk.Button(frm, text='Quitter',
                  font=('Franklin Gothic Demi Cond', 11), bg='white',
                  relief='flat', overrelief='groove',
                  command=lambda: self.leave(parent))\
            .pack()

    def leave(self, wnd):
        '''Permet de quitter le jeu à partir de la fenêtre des scores à l'aide
        d'une fenêtre popup'''
        # Affiche la fenêtre popup au premier plan
        wnd.wm_attributes('-topmost', 1)
        if askyesno('Vous êtes sur le point de quitter',
                    'Êtes-vous sûr de vouloir quitter ?'):
            wnd.destroy()

    def restart(self, wnd):
        '''Permet de relancer une partie'''
        wnd.destroy()
        SelectImage("images")


class Rules(tk.Toplevel):
    '''Fenêtre affichant les règles à suivre pour jouer au jeu'''

    def __init__(self, parent):
        super().__init__(parent)
        # Configuration de la fenêtre
        self.title("Règles du jeu")
        self.config(bg='white')
        self.resizable(width=False, height=False)
        # Positionnement au centre de l'écran et en premier plan
        self.geometry("-690+350")
        self.wm_attributes("-topmost", 1)
        # Création des bandeaux de décoration
        frm = tk.Frame(self, height=25, bg='green')
        frm.pack(side=tk.TOP)
        tk.Label(frm, text="Bonjour et bienvenue dans ZPUZZLE !",
                 bg='green', fg='white', font=('Franklin Gothic Demi Cond',
                                               11)).pack()
        tk.Button(self, text='OK', font=('Franklin Gothic Demi Cond', 11),
                  relief='flat', overrelief='groove', fg='white', width=20,
                  bg='green', command=self.destroy).pack(side=tk.BOTTOM)
        # Définition des règles
        txt = " \n Votre objectif est de compléter ce puzzle avec le moins" +\
            " de \n déplacements possible et dans un minimum de temps"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "Pour déplacer une tuile deux choix s'offrent à vous:"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "-Cliquez sur la tuile et cliquez ensuite sur \n" +\
            " l'emplacement que vous voulez"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "-Maintenez le clic sur la tuile et déplacez la en \n la" +\
            " glissant sur le plateau"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "Pour retirer une tuile, double-cliquez sur celle-ci"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "Vous pouvez interchanger deux tuiles en glissant la \n" +\
            " première sur la deuxième"
        tk.Label(self, text=txt, bg='white').pack()
        txt = "Appuyer sur le bouton soumettre lorsque vous aurez complété" +\
            " le puzzle. Vos erreurs seront \n indiquées en rouge et vous" +\
            " pourrez alors retirer les mauvaises tuiles \n en appuyant" +\
            " sur le bouton Retirer"
        tk.Label(self, text=txt, bg='white').pack(padx=5)
        txt = "Si votre puzzle est réussi, une fenêtre popup s'affichera" +\
            " indiquant votre score final.\n Vous aurez alors le choix" +\
            " entre rejouer ou bien quitter l'application \n \n" +\
            "Bon courage ! \n "
        tk.Label(self, text=txt, bg='white').pack()


class SelectImage():
    '''Fenêtre d'accueil permettant de choisir l'image à reconstituer'''

    def __init__(self, folder):
        # Mémorisation du fichier
        self.folder = folder

        # Création de la fenêtre Tkinter et de ses éléments (canva, frames)
        self.win = tk.Tk()
        self.win.title("Selection de l'image")
        self.win.geometry("1300x450")
        self.win.resizable(width=False, height=False)  # Pas de fullscreen

        self.frm_left = tk.Frame(self.win, height=450, width=400, bg="white")
        self.frm_left.pack(side=tk.LEFT)

        self.cnv_middle = tk.Canvas(self.win, height=450, width=500,
                                    bg="white", bd=0,
                                    highlightthickness=0, relief='ridge')
        self.cnv_middle.pack_propagate(0)
        self.cnv_middle.pack(side=tk.LEFT)

        self.frm_right = tk.Canvas(self.win, height=450, width=400, bg="white",
                                   bd=0, highlightthickness=0, relief="ridge")
        self.frm_right.pack(side=tk.RIGHT)

        # Création de la liste des images du fichier
        self.list_images = os.listdir(self.folder)

        # Affichage de la première image du dossier selectionné
        self.num_image = 0
        self.image = crop_image.Image.open("images\\" + self.list_images[0])
        self.ratio_wh = self.image.size[0]/self.image.size[1]
        self.image = self.image.resize((int(300*self.ratio_wh), 300))
        self.image_tk = crop_image.ImageTk.PhotoImage(self.image)
        self.tag = 'image' + str(self.num_image)

        self.cnv_middle.create_image(1000/4, 400/2,
                                     image=self.image_tk, tag=self.tag)

        # Création du label et des boutons
        txt = "Choisissez l'image avec laquelle vous voulez jouer"
        tk.Label(self.cnv_middle, text=txt, bg='white',
                 font=('Franklin Gothic Demi Cond', 11)).pack(side=tk.TOP)
        tk.Button(self.frm_right, text='Image suivante',
                  command=self.next_image).place(x=75, y=190)
        tk.Button(self.frm_left, text='Image précédente',
                  command=self.previous_image).place(x=75, y=190)
        tk.Button(self.frm_left, text='Retourner à la première image',
                  command=self.first_image).place(x=75, y=230)
        tk.Button(self.cnv_middle, text='Jouer avec cette image',
                  command=self.begin_game).pack(side=tk.BOTTOM, pady=10)
        self.win.mainloop()

    def display(self):
        '''Fonction qui sert pour les trois à venir, ouvre l'image, la met à
        la taille souhaitée, la convertie pour être utilisable par Tkinter,
        et l'affiche dans le canva central en mémorisant son tag'''
        self.image = crop_image.Image.open("images\\" +
                                           self.list_images[self.num_image])
        self.ratio_wh = self.image.size[0]/self.image.size[1]
        self.image = self.image.resize((int(300*self.ratio_wh), 300))
        self.image_tk = crop_image.ImageTk.PhotoImage(self.image)
        self.tag = 'image' + str(self.num_image)
        self.cnv_middle.create_image(1000/4, 400/2,
                                     image=self.image_tk, tag=self.tag)

    def next_image(self):
        '''Affiche l'image suivante du dossier images
        Si c'est la dernière image qui est affichée, la fonction ne fait rien
        '''
        if self.num_image == len(self.list_images)-1:
            return
        self.cnv_middle.delete(self.tag)
        self.num_image += 1
        self.display()

    def previous_image(self):
        '''Affiche l'image précédente du dossier images
        Si c'est la premoère image qui est affichée, la fonction ne fait rien
        '''
        if self.num_image == 0:
            return
        self.cnv_middle.delete(self.tag)
        self.num_image -= 1
        self.display()

    def first_image(self):
        '''Retourne au début de la liste d'images'''
        self.cnv_middle.delete(self.tag)
        self.num_image = 0
        self.display()

    def begin_game(self):
        '''Lance le jeu avec l'image affichée à l'écran'''
        image_chosen = self.list_images[self.num_image]
        image = crop_image.ImagePuzzle("images\\" + str(image_chosen))
        ratio_wh = image.width/image.height
        result = Rules(self.win)
        self.win.wait_window(result)
        self.win.destroy()
        Application(2, 2, image, ratio_wh)
