import networkx as nx
from os import listdir
from music21 import *
import matplotlib.pyplot as plt
from scipy import optimize
import powerlaw
import numpy as np
import random
import warnings
warnings.filterwarnings("ignore")

random.seed(777);

def func(x, a, b, c):
    return a*x**(-b) + c

def criaNet(tipo = 'mxl'):
    print("Creating network:\n");
    G = nx.DiGraph();
    #print(listdir("./"));
    
    for file in listdir("./"):
        #print(file);
        if file.endswith(tipo):
            b = converter.parse(file);
            # for nota in b.parts[0].semiFlat.notesAndRests:
            #     print(nota.fullName);
            melody = [];
            for nota in b.parts[0].semiFlat.notesAndRests:
                try:
                    if(nota.isRest):
                        melody.append(nota.fullName);
                    elif(nota.isChord):
                        melody.append(nota.notes[-1].nameWithOctave + ' ' + nota.notes[-1].duration.type)
                    else:
                        melody.append(nota.nameWithOctave + ' ' + nota.duration.type);
                
                    G.add_node(melody[0]);
                except duration.DurationException:
                    pass;
            
            for i in range(1,len(melody)):
                G.add_node(melody[i]);
                if G.has_edge(melody[i-1], melody[i]):
                    G[melody[i-1]][melody[i]]['weight'] += 1;
                else:
                    G.add_edge(melody[i-1], melody[i], weight=1);
                
                #print(melody[i])
        #break;

    return(G);
    
def analise(G,name):
    print("\nanalising " + name + "\n")
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
    fit = powerlaw.Fit(degsOut);
    
    t = np.arange(0, n, 1).astype(float);
    x = np.arange(5, n, 1).astype(float);
    
    params, params_covariance = optimize.curve_fit(func, x, degsOut[5:n], p0=[1, 3,0])
    plt.loglog(t, func(t, params[0], params[1], 0), 'k--')
    
    plt.title(name + " alpha = " + str(fit.power_law.alpha));
    plt.xlabel('kOut');
    plt.ylabel('pk');
    plt.show();
    
    plt.loglog(range(n),degsIn[0:n], 'bo');
    fit = powerlaw.Fit(degsIn);
    
    t = np.arange(0, n, 1).astype(float);
    x = np.arange(5, n, 1).astype(float);
    
    params, params_covariance = optimize.curve_fit(func, x, degsIn[5:n], p0=[1, 3,0])
    plt.plot(t, func(t, params[0], params[1], 0), 'k--')
    
    plt.title(name + " alpha = " + str(fit.power_law.alpha));
    plt.xlabel('kIn');
    plt.ylabel('pk');
    plt.show();
    
    plt.loglog(range(n),degs[0:n], 'go');
    fit = powerlaw.Fit(degs);
    
    t = np.arange(0, n, 1).astype(float);
    x = np.arange(5, n, 1).astype(float);
    
    params, params_covariance = optimize.curve_fit(func, x, degs[5:n], p0=[1, 3,0])
    plt.plot(t, func(t, params[0], params[1], 0), 'k--')
    
    plt.title(name + " alpha = " + str(fit.power_law.alpha));
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
    #print(nota.split());
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
                if(G.neighbors(nota) != []):
                    nota = i[0];
                    break;
        #print(nota);
    return s1;

G = criaNet();
name = "NocturnesChopin.gexf";
nx.write_gexf(G, name);
analise(G, name);
s1 = construirMel(G,dictCSharp,t=1000);
print(s1.analyze('key'))
s1.write('midi', fp="./" + name + ".mid")
G2 = criaNet("mid")
analise(G2,name + " created");