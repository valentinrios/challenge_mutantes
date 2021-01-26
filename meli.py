import re
import numpy as np

def split(word): 
    return [char for char in word]

def isMutant(dna):
    total_matchs = horizontal_matchs(dna) + vertical_matchs(dna) + diagonal_matchs(dna)
    if total_matchs >= 3:
        return True
    else:
        return False
    
def horizontal_matchs(dna):
    matchs = 0
    for dna_string in dna:    
        match = re.search(r'([A,T,C,G])\1{3,3}', dna_string)
        if match is not None and match[0] != "":
            matchs += 1
    return matchs

def vertical_matchs(dna):
    verticals = []
    matchs = 0
    for i in range(len(dna)):
        temporal_string = ""
        for j in range(len(dna)):
            temporal_string += dna[j][i]
        verticals.append(temporal_string)
        
    for vertical in verticals:    
        match = re.search(r'([A,T,C,G])\1{3,3}', vertical)
        if match is not None and match[0] != "":
            matchs += 1
    return matchs

def diagonal_matchs(dna):
    aux=[]
    matchs = 0
    for dna_string in dna:
        #print(split(dna_string))
        aux.append(split(dna_string))
    x = np.array(aux)
    diags = [x[::-1,:].diagonal(i) for i in range(-3,4)]
    diags.extend(x.diagonal(i) for i in range(3,-4,-1))
    for n in diags:    
        match = re.search(r'([A,T,C,G])\1{3,3}', ''.join(n.tolist()))
        if match is not None and match[0] != "":
            matchs += 1
    return matchs

dna =  ["ATGCGAA",
        "CAGTGCA",
        "TTATGTA",
        "AGAAGGA",
        "CCCCTAT",
        "TCACTGT",
        "TTTTTGT"]

print(isMutant(dna))