import os

import numpy as np
import networkx as nx
from music21 import *


def get_musics(path_to_musics_folder="music/", verbose=True):
    musics_available = [filename for filename in os.listdir(path_to_musics_folder) if not filename[0] == '.']
    
    if verbose:
        print("Index\tMusic")
        for i, music in enumerate(musics_available):
            print("{}\t{}".format(i, music))

    path_to_musics_available = [os.path.join(path_to_musics_folder, folder) for folder in musics_available]
    
    return path_to_musics_available


def generate_graph_from_melody(melody):
    G = nx.DiGraph()

    nodes_list = list(set(melody))
    G.add_nodes_from(nodes_list)

    for i in range(1, len(melody)):
        if G.has_edge(melody[i], melody[i-1]):
            G[melody[i]][melody[i-1]]['weight'] += 1
        else:
            G.add_edge(melody[i], melody[i-1], weight=1)
            
    return G


def get_graph_and_melody_from_music(path_to_music):
    melody = []
    b = converter.parse(path_to_music)

    for note in b.parts[0].semiFlat.notesAndRests:
        if(note.isRest):
            melody.append(note.fullName)
        elif(note.isChord):
            melody.append(note.notes[-1].nameWithOctave + ' ' + note.notes[-1].duration.type)
        else:
            melody.append(note.nameWithOctave + ' ' + note.duration.type)

    G = generate_graph_from_melody(melody)

    return G, melody


def get_graph_and_melody_from_musics(path_to_folder):
    melody_musics = []

    for file in os.listdir(path_to_folder):
        file = os.path.join(path_to_folder, file)
        if file.endswith(".mxl"):
            _, melody = get_graph_and_melody_from_music(file)
            melody_musics.extend(melody)

    G_musics = generate_graph_from_melody(melody_musics)
            
    return G_musics, melody_musics
