import networkx as nx
import matplotlib.pyplot as plt
import powerlaw
import numpy as np
from music21 import *
import random

random.seed(2);

name = "NocturnesChopin.gexf";

G = nx.read_gexf(name);

def analise(G):
    n = G.number_of_nodes();
    m = G.number_of_edges();
    degsIn = [0]*(n);
    degsOut = [0]*(n);
    degs = [0]*(n);
        
    for i in G.nodes():
        degsIn[G.in_degree(i)] += 1;
        degsOut[G.out_degree(i)] += 1;
        degs[G.degree(i)] += 1;
        
    for i in range(n):
        degsIn[i] = degsIn[i]/n;
        degsOut[i] = degsOut[i]/n;
        degs[i] = degs[i]/n;
        
    plt.loglog(range(n),degsOut[0:n], 'ro');
    
    plt.title(name);
    plt.xlabel('kOut');
    plt.ylabel('pk');
    plt.show();
    
    plt.loglog(range(n),degsIn[0:n], 'bo');
    
    plt.title(name);
    plt.xlabel('kIn');
    plt.ylabel('pk');
    plt.show();
    
    plt.loglog(range(n),degs[0:n], 'go');
    
    plt.title(name);
    plt.xlabel('k');
    plt.ylabel('pk');
    plt.show();
    
    print("The average degree is " + str(2*m/n));
    print("The average in-degree is " + str(sum([deg[1] for deg in G.in_degree()])));
    print("The average out-degree is " + str(sum([deg[1] for deg in G.out_degree()])));
    print(str(nx.number_connected_components(G.to_undirected())) + " connected components");
    print("Average distance: " + str(nx.average_shortest_path_length(G)));
    print("Average clustering coefficient: " + str(nx.average_clustering(G)))
    print("Assortativity coefficient: " + str(nx.degree_assortativity_coefficient(G)))


dictCSharp = {
    "C#" : 1,
    "G#" : .9,
    "E" : .8,
    "B" : .4,
    "D#" : .2,
    "F#" : .2,
    "A" : .2,
}


def ajuFit(matriz,dictio):
    soma = 0;
    for i in range(len(matriz)):
        nota = matriz[i][0];
        nota = nota.split()[0][0:-1];
        if(nota in dictio):
            matriz[i] = (matriz[i][0], round(matriz[i][1] * dictio[nota],3))
        elif('Rest' in matriz[i][0]):
            matriz[i] = (matriz[i][0], round(matriz[i][1] * 0.8,3));
        else:
            matriz[i] = (matriz[i][0], round(matriz[i][1] * 0.05,3));
        soma += matriz[i][1];
    return matriz,soma;

def construirMel(G,dictio,scale = "C#4 quarter",t=10):
    nota = scale;
    s1 = stream.Stream();
    print(nota.split())
    for i in range(t):
        if("Rest" in nota):
            try:
                s1.append(note.Rest(type=nota.strip(" Rest").lower()))
            except duration.DurationException:
                #print(nota);
                s1.append(note.Rest(type=nota.strip("Dotted").split()[0].lower()))
                pass;
        else:
            s1.append(note.Note(nota.split()[0], type=nota.split()[1]))
        count = 0;
        matriz = [edges[1:3] for edges in G.edges(nota,data='weight')];
        #print(matriz);
        matriz,soma = ajuFit(matriz,dictio);
        #print(matriz);
        rnd = random.random() * soma;
        for i in matriz:
            count += i[1];
            if(count > rnd):
                if(not ("Rest" in nota and "Rest" in i[0])):
                    nota = i[0];
                    break;
        print(nota);
    return s1;
    
analise(G);
s1 = construirMel(G,dictCSharp,t=500);
print(s1.analyze('key'))
s1.write('midi', fp="./" + name + ".mid")