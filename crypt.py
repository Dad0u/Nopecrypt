#coding: utf-8

def pause():
    a = ''
    input(a)
    
def read_chunk(f, chunksize):
    while True:
        chunk = f.read(chunksize)
        if chunk:
           yield chunk
        else:
            break
                
def decale(M,bytes):
    global l
    if len(M) == l:
        del M[0]
    M.append(bytes)
    return M
    
def chiffr(M):
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
    return bytes(S)             # PAS FORCEMENT DE LONGUEUR 8 !
    
if False:    
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
        print('Impossible d\'ouvrir le fichier à chiffrer')
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
    print('Fichier à écrire ? (défaut: out.dea):')

    nom_dest = input()
    if nom_dest == '':
        nom_dest = 'out.dea'
    print('input: {}'.format(nom_source))
    print('key: {}'.format(key))
    print('depth: {}'.format(l))
    print('output: {}'.format(nom_dest))
    print('Confirmer les paramètres (y/n)?')
    ok = input()
    if ok not in ['y','Y','o','O']:
        exit(0)               #---------- Fin du prompt utilisateur


l = 8       #Valeurs de test
nom_source = "a.txt"
key = "1234568"
nom_dest = "out.dea" #---




while len(key) < l*(l-1): # Pour avoir une clé de la bonne longueur
    key +=key
key = key[:l*(l-1)]

print(key)
source = open(nom_source,"rb")
dest = open(nom_dest,"wb")
M = []

for i in read_chunk(source, l):     #Chiffrage du fichier sans utiliser la clé
    M = decale(M, i)
    if len(M) == l:
        S = chiffr(M)
        dest.write(S)
source.close()

row = ''
for i in key:                       # Chiffrage de la fin, en utilisant la clé
    row += i
    if len(row) == 8:
        M = decale(M,bytes(row,'utf-8'))
        dest.write(chiffr(M))
        row = ''
        


dest.close()


