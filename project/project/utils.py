import os

import powerlaw
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from music21 import *
from scipy import optimize


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

    for i in range(len(melody) - 1):
        if G.has_edge(melody[i], melody[i + 1]):
            G[melody[i]][melody[i + 1]]['weight'] += 1
        else:
            G.add_edge(melody[i], melody[i + 1], weight=1)

    return G


def get_graph_and_melody_from_music(path_to_music):
    melody = []
    b = converter.parse(path_to_music)

    for note in b.parts[0].semiFlat.notesAndRests:
        try:
            if (note.isRest):
                melody.append(note.fullName)
            elif (note.isChord):
                melody.append(note.notes[-1].nameWithOctave + ' ' + note.notes[-1].duration.type)
            else:
                melody.append(note.nameWithOctave + ' ' + note.duration.type)
        except duration.DurationException:
            pass

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


def show_network_info(network):
    network_info = nx.info(network)
    network_info = '\n'.join(network_info.split("\n")[2:])

    degrees = np.array([network.degree(n) for n in network.nodes()])

    connected_components = sorted(nx.connected_components(network.to_undirected()), key=len, reverse=True)
    average_distance = nx.average_shortest_path_length(network)

    cc  = nx.clustering(network)
    average_cc = nx.average_clustering(network)

    print(network_info)
    print("Number of connected components: {}".format(len(connected_components)))
    print("Average distance: {:.6f}".format(average_distance))
    print("Average cluster coefficient <C>: {:.4f}".format(average_cc))
    print("Assortativity coefficient: " + str(nx.degree_assortativity_coefficient(network)))


def get_degree_distribution_linear_binning(frequency_array):
    N = frequency_array.shape[0]

    K = [freq[0] for freq in frequency_array]

    pk = []
    for freq in frequency_array:
        pk.append(freq[1] / N)
    pk = np.array(pk)

    return K, pk


def get_degree_distribution_cumulative(frequency_array):
    N = frequency_array.shape[0]

    K, pk = get_degree_distribution_linear_binning(frequency_array)

    pk_c = []
    for i in range(len(pk) - 1):
        pk_i = np.sum(pk[i + 1:len(pk)])
        pk_c.append(pk_i)
    pk_c = np.array(pk_c)
    K = K[:-1]

    return K, pk_c


def powerlaw_function(x, a, b, c):
    # ax^(-b) + c
    return a * x**(-b) + c


def get_frequency_array(degrees):
    degrees_nonzero = degrees[degrees.nonzero()[0]]  # For the degree distribution we don't add p0 (pk with k = 0)
    unique, counts = np.unique(degrees_nonzero, return_counts=True)
    frequency_array = np.asarray((unique, counts)).T

    return frequency_array


def plot_degree_distribution(G, in_degree=True, binning_type="linear"):
    if in_degree:
        degrees = np.array([G.in_degree(n) for n in G.nodes()])
    else:
        degrees = np.array([G.out_degree(n) for n in G.nodes()])

    frequency_array = get_frequency_array(degrees)

    if in_degree:
        plot_title = "In "
    else:
        plot_title = "Out "

    plot_title += "Degree distribution - log-log scale, "
    if binning_type == "linear":
        plot_title += "Linear Binning"
        K, pk = get_degree_distribution_linear_binning(frequency_array)
    else:  # cumulative
        plot_title += "Cumulative"
        K, pk = get_degree_distribution_cumulative(frequency_array)

    #fit = powerlaw.Fit(degrees)

    #plot_title += " alpha = " + str(fit.alpha)
    plt.figure(figsize=(10, 5))
    plt.title(plot_title)
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel("Pk")
    plt.xlabel("K")

    plt.plot(K, pk, marker='o', linestyle='None')

    plt.show()
