#coding: utf-8

def pause():
    a = ''
    input(a)
    
    
def read_bytes(filename, chunksize):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
               yield chunk
            else:
                break
                
                
def read_bytes_backward(filename, chunksize):
    with open(filename, "rb") as f:
        f.seek(-l,2)
        chunk = f.read(chunksize)
        yield chunk
        while True:
            try:
                f.seek(-2*l,1)
            except:
                break
            chunk = f.read(chunksize)
            yield chunk
                
                
def decale(M,bytes):
    global l
    if len(M) == l:
        del M[0]
    M.append(bytes)
    return M
    
def decale_bw(M,bytes):
    global l
    if len(M) == l:
        del M[l-1]
    M.insert(0,bytes)
    return M
    
def chiffr(M):
    global l
    S = []
    for i in M[0]:
        S.append(int(i))
    for i in range(l):
        for j in range(1,l):
            try:
                S[i] ^= M[j].ljust(l,bytes(1))[i]
            except:
                print(M)
    return bytes(S)
    
def dechiffr(M):
    return(chiffr(M))
    
l = 8            
source = "a.bmp"
dest = open("out.vef","wb")
cle = open("key.vek","wb")
M = []

print("Chiffrage...")

for i in read_bytes(source, l):     #Chiffrage
    M = decale(M, i)
    #print(M)
    if len(M) == l:
        S = chiffr(M)
        dest.write(S)
    #pause()
print("Ecriture de la cle...")
dest.close()
del M[0]
for i in M:
    cle.write(i)
cle.close()
print("OK.")

csource = "out.vef"
ddest = open("out.bmp","wb")
key = "key.vek"
M=[]

with open(csource) as f:    #Calcule la longueur du ficher chiffré
    f.seek(0,2)
    lsource = f.tell()
 
with open(key) as f:        #Calcule la longueur de la clé
    f.seek(0,2)
    lkey = f.tell()
    
#for i in range (lsource+lkey): #Crée le fichier vide
    #ddest.write(bytes(1))
print("Creation du ficher destination vide...")
ddest.write(bytes(lsource+lkey))

print("Lecture de la cle...")
ddest.seek(-lkey,2)
for i in read_bytes(key,l):     #Ajoute la clé à la matrice et l'écrit au fichier
    ddest.write(i)
    M.append(i)

print("Dechiffrage...")
ddest.seek(lsource-l)
for i in read_bytes_backward(csource,l):    # Boucle principale (déchiffrage)
    M = decale_bw(M,i)
    d = dechiffr(M)
    ddest.write(d)
    M[0] = d
    try:
        ddest.seek(-2*l,1)
    except:
        pass
    
ddest.close()
print("Termine !")
