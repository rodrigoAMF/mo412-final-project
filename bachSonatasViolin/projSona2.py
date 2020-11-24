import networkx as nx
from os import listdir
from music21 import *

G = nx.DiGraph();
#print(listdir("./"));

for file in listdir("./"):
    if file.endswith(".mxl"):
        b = converter.parse(file);
        # for note in b.parts[0].semiFlat.notesAndRests:
        #     print(note.fullName);
        melody = [];
        for note in b.parts[0].semiFlat.notesAndRests:
            if(note.isRest):
                melody.append(note.fullName);
            elif(note.isChord):
                melody.append(note.notes[-1].nameWithOctave + ' ' + note.notes[-1].duration.type)
            else:
                melody.append(note.nameWithOctave + ' ' + note.duration.type);
        
            G.add_node(melody[0]);
        
        for i in range(1,len(melody)):
            G.add_node(melody[i]);
            if G.has_edge(melody[i], melody[i-1]):
                G[melody[i]][melody[i-1]]['weight'] += 1;
            else:
                G.add_edge(melody[i], melody[i-1], weight=1);
            
            #print(melody[i])
    #break;
        
nx.write_gexf(G, "sonatasBachViolin2.gexf");