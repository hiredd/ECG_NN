import wfdb
import numpy as np
import matplotlib.pyplot as plt

def kill_beat(latidos, anotaciones, latido_a_eliminar,cant_org,tam):
    new_beats = np.zeros([cant_org-1,2*tam])
    new_an = np.chararray(cant_org-1)
    for i in range(0,latido_a_eliminar):
        new_beats[i] = latidos[i]
        new_an[i] = anotaciones[i]
    for i in range(latido_a_eliminar+1,cant_org):
        new_beats[i-1] = latidos[i]
        new_an[i-1] = anotaciones[i]
    return new_beats, new_an

def crate_training_cases(latidos, anotaciones, char, cant_training, cant_org, tam):
    training_set = np.zeros([cant_training,2*tam])
    for i in range(0,cant_training):
        for j in range(0,cant_org):
            if anotaciones[j] == char:
                training_set[i] = latidos[j]
                [latidos, anotaciones] = kill_beat(latidos,anotaciones,j,cant_org,tam)
                cant_org -= 1
                break

    return training_set,latidos,anotaciones

signals2, fields2= wfdb.srdsamp('data/14172', channels=[0, 1])
annotation = wfdb.rdann('data/14172', 'atr')
picos=annotation.annsamp
#Me quedo con los picos de cada ECG que es donde estan las anotaciones
picos=annotation.annsamp

#Transpongo las senales leidas para poder operar mas comodamente
signals=np.matrix.transpose(signals2)
picos[-1]=0 #descarto el ultimo pico por si el latido esta interrumpido
tam=125 #Tamano del latido que tomo a la izquierda y a la derecha de la anotacion
cantLatidos=sum(picos>tam) #Cuento la cantidad de anotaciones en el segemento a analizar
latidos=np.zeros([cantLatidos,2*tam]) #Reservo espacio para la matriz de datos cantLatidos x 2*tam
latidosNorm=np.zeros([cantLatidos,2*tam])#Reservo espacio para la matriz de datos normalizados
numLat=0 #Inicializo en cero para procesar cada uno de los picos
for i in picos:
    if i>tam: # i>tam por si el primer latido esta trunco
        latidos[numLat]=signals[0][i-tam:i+tam] #tomo tam muestras a la izquerda y a la derecha de la anotacion
        numLat+=1 #incremento el numero de latidos

#El set de latidos esta en latidos y el largo de cada latido es de tam muestras

for i in range(0,cantLatidos):
    latidosNorm[i] = latidos[i] - np.mean(latidos[i])
    latidosNorm[i] /= np.std(latidosNorm[i])


anotaciones = annotation.anntype

#genero training set
N = 10  #cantidad de latidos normales en el training set
V = 10  #cantidad de latidos ventriculares en el training set
S = 10  #cantidad de latidos superventriculares prematuros en el training set
J = 10  #cantidad de latidos nodales prematuros en el training set
print anotaciones
training_set_N =np.zeros([N,tam*2])
training_set_N[0]=latidosNorm[0]
training_set_N[1]=latidosNorm[2]
training_set_N[2]=latidosNorm[3]
training_set_N[3]=latidosNorm[4]
training_set_N[4]=latidosNorm[5]
training_set_N[5]=latidosNorm[8]
training_set_N[6]=latidosNorm[9]
training_set_N[7]=latidosNorm[12]
training_set_N[8]=latidosNorm[13]
training_set_N[9]=latidosNorm[16]
plt.figure()
for i in range(0,10):
    plt.plot(training_set_N[i])

print 'N'
[training_set_N,latidosNorm,anotaciones] = crate_training_cases(latidosNorm,anotaciones,'N',N,cantLatidos,tam)
cantLatidos -= N
print 'V'
[training_set_V,latidosNorm,anotaciones] = crate_training_cases(latidosNorm,anotaciones,'V',V,cantLatidos,tam)
cantLatidos -= V
print 'S'
[training_set_S,latidosNorm,anotaciones] = crate_training_cases(latidosNorm,anotaciones,'S',S,cantLatidos,tam)
cantLatidos -= S
print 'J'
[training_set_J,latidosNorm,anotaciones] = crate_training_cases(latidosNorm,anotaciones,'J',J,cantLatidos,tam)
cantLatidos -= J
plt.figure()
for i in range(0,10):
    plt.plot(training_set_N[i])
plt.show()