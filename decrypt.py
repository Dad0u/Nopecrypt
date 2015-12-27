#coding: utf-8

def pause():
    a = ''
    input(a)
    
def read_chunk_backward(filename, chunksize):
    with open(filename, "rb") as f:
        f.seek(0,2)
        length = f.tell()
        reste = length % l
        if reste == 0:
            reste = l
        f.seek(-reste,2)
        chunk = f.read(chunksize)
        yield chunk
        f.seek(-reste-l,2)
        while True:
            chunk = f.read(chunksize)
            yield chunk
            try:
                f.seek(-2*l,1)
            except:
                break
            
                
def decale_bw(M,bytes):
    global l
    if len(M) == l:
        del M[l-1]
    M.insert(0,bytes)
    return M
    
def dechiffr(M):
    global l
    S = []
    for i in M[0]:
        S.append(int(i))
    for i in range(len(S)):     #Pas forcément = l ! (cas de fin de fichier par ex)
        for j in range(1,l):
            try:
                S[i] ^= M[j].ljust(l,bytes(1))[i]
            except:
                print("Problème de chiffrage:")
                print(M)
                print("Ne permet pas d'encoder correctement")
                pause()
    #if len(M[0]) != 8:
    #    print("Pouet")
    return bytes(S)             # PAS FORCEMENT DE LONGUEUR l !


l = ''      #-----------Début du prompt utilisateur
print('Profondeur ? (déf:8)')
input(l)
try:
    l = int(l)
except:
    l = 8
if l < 1:
    l = 8

print('nom/chemin du ficher ?')
nom_source = input()
try:
    f = open(nom_source,'r')
    f.close()
except:
    print('Impossible d\'ouvrir le fichier à déchiffrer')
    exit(-1)
    
print('Saisir la clé (s) ou utilier un fichier (f): ')
choix = ''
while choix != 's' and choix != 'f':
    choix = input()
if choix == 's':
    print('Veuillez taper la clé:')
    key = input()
else:
    print('Veuillez saisir l\'adresse de la clé:')
    key_addr = input()
    try:
        f = open(key_addr)
        key = f.read()
    except:
        print('Impossible d\'ouvrir le fichier clé')
        exit(-1)
print('Fichier à écrire ? (défaut: out):')

nom_dest = input()
if nom_dest == '':
    nom_dest = 'out'
print('input: {}'.format(nom_source))
print('key: {}'.format(key))
print('depth: {}'.format(l))
print('output: {}'.format(nom_dest))
print('Confirmer les paramètres (y/n)?')
ok = input()
if ok.lower() not in ['y','o']:
    print("Annulation.")
    exit(0)               #---------- Fin du prompt utilisateur

#l = 8       #Valeurs de test
#nom_source = "out.dea"
#key = "1234568"
#nom_dest = "out.txt" #---

while len(key) < l*(l-1): # Pour avoir une clé de la bonne longueur
    key +=key
key = key[:l*(l-1)]

with open(nom_source) as f:    #Calcule la longueur du ficher chiffré
    f.seek(0,2)
    lsource = f.tell()

print("Creation du ficher destination vide...")
dest=open(nom_dest,"wb")
dest.write(bytes(lsource))
row = ''
M = []
for i in key:                       # Remplissage de la matrice avec la clé
    row += i
    if len(row) == 8:
        M.append(bytes(row,'utf-8'))
        row = ''

reste = lsource % l
if reste == 0:
    reste = l
dest.seek(-reste,2)
first = True
for i in read_chunk_backward(nom_source,l):    # Boucle principale (déchiffrage)
    M = decale_bw(M,i)
    d = dechiffr(M)
    dest.write(d)
    M[0] = d
    try:
        dest.seek(-2*l,1)
    except: #Rentre dans ce cas si lsource % l == 0 car il y a un tour de moins à faire. (pas de problème)
        pass
    if first:
        first = False
        dest.seek(8-reste,1)

dest.close()


