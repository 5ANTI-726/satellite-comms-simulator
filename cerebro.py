import math
import pandas as pd
#from playsound import playsound

#Cuando quieras agregar más cuerpos debes 1) hacer más archivos y
#agregarlos al método escribir_todo() en la línea 89,
#2) declarar el/los objeto(s) en la línea 172, 3) agregar su referencia
#a la lista all_bodies[] en la línea 178, 4) agregarlo a todas las instancias
#del método escribir_todo en main(), 5) agregarlo a los cálculos de
#primeros cambios de posición y velocidad en el bloque 211-226
#(debe ser un algoritmo recursivo basado en all_bodies), 6)

#¿Qué queremos guardar? Queremos velocidades, distancia del centro,
#energía cinética/potencial/total, coordenadas, momento lineal total
#(+componentes) y momento angular después (+de cada cuerpo).  Son 17 archivos.

#Primero pondremos el método que convierte los archivos .txt a comma
#separated files (.csv) que se puedan leer en Matlab.

#Coordenadas 1
co1 = []
#Coordenadas 2
co2 = []
#Coordenadas 3
co3 = []

#Velocidades
vx1 = []
vy1 = []
vz1 = []
vx2 = []
vy2 = []
vz2 = []
vx3 = []
vy3 = []
vz3 = []

f1 = []

f2 = []

f3 = []

f3_1 = []
f3_2 = []

peri=[0,0]


#Energías
e_cinetica = []
e_potencial = []

#Momentos lineales
P = []
Px = []
Py = []
Pz = []

#Momentos angulares
#PA = open("momento_angular.txt", "w+")    #15
#PA_A = open("momento_angular_A.txt", "w+") #16
#PA_B = open("momento_angular_B.txt", "w+") #17

#Decompose velocity vector.
def vcomp(v,theta,phi):
    #No idea which is more expensive...
    x = abs(v)*math.cos(theta)*math.sin(phi)
    y = abs(v)*math.sin(theta)*math.sin(phi)
    z = abs(v)*math.cos(phi)
    return round(x,6), round(y,6), round(y,6)

#Check to see if the coordinates of any two objects are closer
#than their radii allow.
def crash(all_bodies):
    status = False
    cum_r = 0
    for i in range(0,len(all_bodies)-1):
        for k in range(i+1,len(all_bodies)):
            cum_r = (all_bodies[i].radio + all_bodies[k].radio)
            if cum_r >= all_bodies[i].distancia(all_bodies[k]):
                status = True

    return(status)

#Energía potencial total.
def potencial(all_bodies,U0):
    U = 0
    #Limitado a len(...)-2 porque el objeto número
    #all_bodies[len(all_bodies)-1] ya va a haber sido comparado con
    #todos los objetos de indice 0 a len(all_bodies)-1.
    for i in range(0,len(all_bodies)-1):
        #Este tipo de algoritmo recursivo empieza range() la k en i si no
        #quiere repetir el cálculo i-k como k-i. Si los dos empiezan
        #range() en 0, se haran los cálculos "duplicados" i-k y k-i.
        for k in range(i+1,len(all_bodies)):
            d = 2*all_bodies[i].distancia(all_bodies[k])
            U = U + all_bodies[i].c_grav*all_bodies[i].masa*all_bodies[k].masa/d

    U = -U
    return(U)

    #De cuando la energía potencial se tomaba en 0 para condiciones iniciales.
    #if(U0 == 0):
        #return(U)
    #else:
        #return(U0-U)

#Energía cinética total.
def cinetica(all_bodies):
    T = 0
    for i in range(0,len(all_bodies)):
        vx = all_bodies[i].vel[0]
        vy = all_bodies[i].vel[1]
        vz = all_bodies[i].vel[2]
        v = math.sqrt(math.pow(vx,2)+math.pow(vy,2)+math.pow(vz,2))

        T += 0.5*all_bodies[i].masa*math.pow(v,2)

    return(T)

#Momento lineal total.
def momento_lineal(all_bodies):
    P = 0
    Px = math.pow(momento_lineal_comp(all_bodies,0),2)
    Py = math.pow(momento_lineal_comp(all_bodies,1),2)
    Pz = math.pow(momento_lineal_comp(all_bodies,2),2)
    P = math.sqrt(Px+Py+Pz)

    return(P)
#Momento lineal en componente i.
def momento_lineal_comp(all_bodies,i):
    Pi = 0
    for k in range(0,len(all_bodies)):
        Pi += all_bodies[k].vel[i]*all_bodies[k].masa
    return(Pi)

#Momento angular total.
def momento_angular(all_bodies):
    return(PA)
#Momento angular del cuerpo con índice j.
def momento_angular_i(all_bodies,j):
    return(PAj)

#Aceptan cualquier tipo de datos y los convierten a tipo string en sus
#respectivas listas.
def escribir2(archivo,c,d):
    archivo.append([c,d])
def escribir3(archivo,e,f,g,h):
    archivo.append([e,f,g,h])
#Compilación de todos los datos posibles en un mismo tiempo
#gracias a que el método es velocity verlett.
def escribir_todo(A,B,count,delta,all_bodies,U0):
    #Coordenadas
    escribir3(co1,all_bodies[0].pos[0],all_bodies[0].pos[1],
    all_bodies[0].pos[2],count+delta)
    escribir3(co2,all_bodies[1].pos[0],all_bodies[1].pos[1],
    all_bodies[1].pos[2],count+delta)
    escribir3(co3,all_bodies[2].pos[0],all_bodies[2].pos[1],
    all_bodies[2].pos[2],count+delta)
    #Velocidades
    escribir2(vx1,count+delta,all_bodies[0].vel[0])
    escribir2(vy1,count+delta,all_bodies[0].vel[1])
    escribir2(vz1,count+delta,all_bodies[0].vel[2])
    escribir2(vx2,count+delta,all_bodies[1].vel[0])
    escribir2(vy2,count+delta,all_bodies[1].vel[1])
    escribir2(vz2,count+delta,all_bodies[1].vel[2])
    escribir2(vx3,count+delta,all_bodies[2].vel[0])
    escribir2(vy3,count+delta,all_bodies[2].vel[1])
    escribir2(vz3,count+delta,all_bodies[2].vel[2])
    #Energía cinética
    escribir2(e_cinetica,count+delta,cinetica(all_bodies))
    #Energía potencial
    escribir2(e_potencial,count+delta,potencial(all_bodies,0))
    #Momentos lineales
    escribir2(P,count+delta,momento_lineal(all_bodies))
    escribir2(Px,count+delta,momento_lineal_comp(all_bodies,0))
    escribir2(Py,count+delta,momento_lineal_comp(all_bodies,1))
    escribir2(Pz,count+delta,momento_lineal_comp(all_bodies,2))
    #Momentos angulares
    #escribir2(PA,count+delta,momento_angular(all_bodies))
    #escribir2(PA_A,count+delta,momento_angular_comp(all_bodies,0))
    #escribir2(PA_B,count+delta,momento_angular_comp(all_bodies,1))

####################################cuerpos####################################
class Cuerpo:
    c_grav = 6.67408*math.pow(10,-11)
    def __init__(self, nombre, radio, masa, position, velocity):
        self.nombre = nombre  #1
        self.masa = masa      #2
        self.radio = radio    #3
        self.pos = position   #4
        self.vel = velocity   #5
    def asignacion(self):
        #Asignación del radio del cuerpo
        self.radio = input("Radio del cuerpo, " + str(self.nombre) + ": ")
        #Asignación de valores del cuerpo
        self.x_pos = input("Posición en x: ")
        self.y_pos = input("Posición en y: ")
        self.z_pos = input("Posición en z: ")
        #Velocidad con ángulos o velocidades
        choice = input("Velocidad a través de ángulos o velocidades? ")
        if choice == "velocidades":
            self.x_vel = input("Velocidad en x: ")
            self.y_vel = input("Velocidad en y: ")
            self.z_vel = input("Velocidad en z: ")
        else:
            vel = input("Velocidad: ")
            theta = input("Ángulo theta: ")
            phi = input("Ángulo phi: ")
            v = vcomp(vel,theta,phi)
            self.x_vel = v[0]
            self.y_vel = v[1]
            self.z_vel = v[2]
    def fuerza(self,otro):
        d = self.distancia(otro)
        x = self.pos[0]-otro.pos[0]
        y = self.pos[1]-otro.pos[1]
        z = self.pos[2]-otro.pos[2]

        f = self.c_grav*self.masa*otro.masa/math.pow(d,2)

        fx = -f*(x)/d
        fy = -f*(y)/d
        fz = -f*(z)/d

        return(fx,fy,fz)
    def distancia(self,otro):
        x = math.pow(self.pos[0] - otro.pos[0],2)
        y = math.pow(self.pos[1] - otro.pos[1],2)
        z = math.pow(self.pos[2] - otro.pos[2],2)

        d = math.sqrt(x+y+z)

        return(d)

#(nombre, radio, masa, posición [x,y,z], velocidad [vx,vy,vz])
A = Cuerpo('Sol',696.34*math.pow(10,6),1.9885*math.pow(10,30),
[0,0,0],[0,0,0])
B = Cuerpo('Júpiter',69.911*math.pow(10,6),1.898*math.pow(10,27),
[701.337*math.pow(10,9),237.789*math.pow(10,9),0],[-3867,7800,0])
#Densidad típica de 4 g/cm, radio de 500 metros y masa de
#2.094*math.pow(10,12) kg
C = Cuerpo('Asteroide',500,2.094*math.pow(10,12),
[-580.522*math.pow(10,9),520*math.pow(10,9),0],[6280.5,-9958.0,0])

#Activar para asignar parámetros. Si no, dejar valores existentes.
#A.asignacion()
#B.asignacion()
#C.asignacion()

#Estructura de datos por si a caso.
#De echo la usaremos para revisar detectar colisiones entre cualquier cuerpo.
all_bodies = [A,B,C]

#Definimos el potencial al inicio.
#U0 = potencial(all_bodies,0)

#########################input and resolve parameters###########################

print('****************************************************************')

#Get the number of points wanted which will be used in the modulo conditional
#so as to only record data in the .txt files a limited number of times
#for even the largest trajectories.
#points = float(input('Número de puntos guardados: '))
points = 4000

#Resolution of calculations (∆t).
#delta = float(input('Resolución de tiempo: '))
delta = 250

#Simulation length in seconds. Antes se llamaba resolution.
#time = float(input('Tiempo de simulación: '))
time = 175000000

#Establishing stores for the error (crash) variable that inidicates
#if a crash ocurred, the frequency of writing down coordinates in terms
#of points skipped, and the control variables.
error = False
#Cada cuanto tiempo escribir variables.
frecuencia = round(time/points/delta)
remover = 0
count = 0

########Establecemos primer cambio de velocidad y posición.#########
#Escribimos la primeras posiciones, velocidades, etc. En lugar de un vector
#de fuerza debería calcular una matriz de todos los vectores de fuerza
#para cada par única de interacciones y luego invertirlo para la
#interacción opuesta (F(A-B) = -F(B-A)). El primer objeto es el que
#siente la fuerza. A.fuerza(B) sería la primera hilera, segunda columna.
#Tiene la forma:

#F   A    B    C    D   ...   m

#A   0   A-B  A-C  A-D  ...  A-m    Fuerzas de A

#B  B-A   0   B-C  B-D  ...  B-m    Fuerzas de B

#C  C-A  C-B   0   C-D  ...  C-m    Fuerzas de C

#D  D-A  D-B  D-C   0   ...  D-m    Fuerzas de D

#.  ...  ...  ...  ...  ...  ...

#n  n-A  n-B  n-C  n-D  ...  n-m    Fuerzas de n

#Guardamos los valores iniciales (t=0).
escribir_todo(A,B,count,0,all_bodies,0)

######Cambiemos primeras posiciones
F = [[[0,0,0],[0,0,0],[0,0,0]],
     [[0,0,0],[0,0,0],[0,0,0]],
     [[0,0,0],[0,0,0],[0,0,0]]]
#Para el cuerpo i...
for i in range(0,len(all_bodies)):
    #Interacción con cuerpo m.
    for m in range(0,i):
        if i != m:
            h = all_bodies[i].fuerza(all_bodies[m])
            #Dimensión k de [x,y,z] = [0,1,2].
            for k in range(0,3):
                F[i][m][k] = h[k]
                F[m][i][k] = -F[i][m][k]
print("Initial forces: ")
print(F)
#Para el cuerpo i...
for i in range(0,len(all_bodies)):
    #Dimensión k de [x,y,z] = [0,1,2].
    for k in range(0,3):
        #Interacción con cuerpo m.
        for m in range(0,len(all_bodies)):
            a = all_bodies[i].pos[k]
            b = all_bodies[i].vel[k]*delta
            c = math.pow(delta,2)*F[i][m][k]/all_bodies[i].masa
            all_bodies[i].pos[k] = a +b + c/2

######Cambiemos primeras velocidades
F2 = [[[0,0,0],[0,0,0],[0,0,0]],
     [[0,0,0],[0,0,0],[0,0,0]],
     [[0,0,0],[0,0,0],[0,0,0]]]
#Para el cuerpo i...
for i in range(0,len(all_bodies)):
    #Dimensión k de [x,y,z] = [0,1,2].
    for k in range(0,i):
        if i != k:
            h = all_bodies[i].fuerza(all_bodies[k])
            #Interacción con cuerpo m.
            for m in range(0,3):
                F2[i][k][m] = h[m]
                F2[k][i][m] = -F2[i][k][m]
##Efecto de las fuerzas
#Para el cuerpo i...
for i in range(0,len(all_bodies)):
    #Dimensión k de [x,y,z] = [0,1,2].
    for k in range(0,3):
        #Interacción con cuerpo m.
        for m in range(0,len(all_bodies)):
            a = F[i][m][k]/all_bodies[i].masa
            b = F2[i][m][k]/all_bodies[i].masa
            all_bodies[i].vel[k] = all_bodies[i].vel[k] + delta*(a + b)/2

#Cambiamos el tiempo porque ya se calcularon las primeras
#coordenadas/velocidades después del inicio.
count += delta

#Decimales de la ∆t. Permitirá corregir el reloj ya que
#no siempre se mueve por la cantidad correcta (∆t).
decimals = 0
holdinterval = delta
while holdinterval%1 != 0:
    holdinterval = holdinterval*10
    decimals += 1

#Calcular tiempos en los que se alcanza n% de la simulación.
checkin = []
for i in range(1,101):
    point = round(time*i/100)
    checkin.append(point)

#################################EXECUTION######################################
while count <= time:
    #Corregir desviaciones del tiempo actual por las decimales de ∆t.
    count = round(count,decimals)


    F = [[[0,0,0],[0,0,0],[0,0,0]],
         [[0,0,0],[0,0,0],[0,0,0]],
         [[0,0,0],[0,0,0],[0,0,0]]]
    #Calcularemos el tensor de fuerzas.
    for i in range(0,len(all_bodies)):
        for k in range(0,i):
            if i != k:
                h = all_bodies[i].fuerza(all_bodies[k])
                for m in range(0,3):
                    F[i][k][m] = h[m]
                    F[k][i][m] = -F[i][k][m]
    ######Velocidad intermedia (v(t+0.5*∆t)). Solo se usa para la posición nueva.
    #Para el cuerpo i...
    for i in range(0,len(all_bodies)):
        #Dimensión k de [x,y,z] = [0,1,2].
        for k in range(0,3):
            #Interacción con cuerpo m.
            for m in range(0,len(all_bodies)):
                all_bodies[i].vel[k] = all_bodies[i].vel[k]
                + delta*(F2[i][m][k]/all_bodies[i].masa)/2

    ######Posición nueva en base a la velocidad intermedia (de hace media ∆t).
    for i in range(0,len(all_bodies)):
        for k in range(0,3):
            all_bodies[i].pos[k] = (all_bodies[i].pos[k]) +
            delta*(all_bodies[i].vel[k])


    F = [[[0,0,0],[0,0,0],[0,0,0]],
         [[0,0,0],[0,0,0],[0,0,0]],
         [[0,0,0],[0,0,0],[0,0,0]]]
    #Calcularemos el tensor de fuerzas.
    for i in range(0,len(all_bodies)):
        for k in range(0,i):
            if i != k:
                h = all_bodies[i].fuerza(all_bodies[k])
                for m in range(0,3):
                    F[i][k][m] = h[m]
                    F[k][i][m] = -F[i][k][m]
    #######Ahora sí obtenemos la velocidad que corresponde al tiempo actual
    #######con la aceleración y posición nuevas (v(t+∆t)=v(t+0.5*∆t)+a(i(t+∆t))).
    #Para el cuerpo i...
    for i in range(0,len(all_bodies)):
        #Dimensión k de [x,y,z] = [0,1,2].
        for k in range(0,3):
            #Interacción con cuerpo m.
            for m in range(0,len(all_bodies)):
                a = all_bodies[i].vel[k]
                b = 0.5*delta*(F[i][m][k]/all_bodies[i].masa)
                all_bodies[i].vel[k] = a + b

    #Revisamos el case de colisiones antes de guardar las posiciones y
    #demás variables ya que no serán  posibles si ocurrió una colisión.
    if crash(all_bodies):
        print("Broke")
        error = True
        break

    ##Escribiremos los resultados de la última simulación con el
    #parámetro de desplacamiento en el tiempo delta ya que corresponden
    #a pos/vel(t+∆t). Quizás tenga que volver a guardar 'todo'
    #después de la última iteración, fuera del loop.
    if remover%frecuencia == 0:
        escribir_todo(A,B,count,delta,all_bodies,0)
        a = F[2][0][0]
        b = F[2][0][1]
        c = F[2][0][2]
        d = math.sqrt(math.pow(a,2) + math.pow(b,2) + math.pow(c,2))
        f3_1.append([count,a,b,c,d])

        a = F[2][1][0]
        b = F[2][1][1]
        c = F[2][1][2]
        d = math.sqrt(math.pow(a,2) + math.pow(b,2) + math.pow(c,2))
        f3_2.append([count,a,b,c,d])

        x = F[0][1][0] + F[0][2][0]
        y = F[0][1][1] + F[0][2][1]
        z = F[0][1][2] + F[0][2][2]
        f1.append([count,math.sqrt(math.pow(x,2)+math.pow(y,2)+math.pow(z,2))])

        x = F[1][0][0] + F[1][2][0]
        y = F[1][0][1] + F[1][2][1]
        z = F[1][0][2] + F[1][2][2]
        f2.append([count,math.sqrt(math.pow(x,2)+math.pow(y,2)+math.pow(z,2))])

        x = F[2][0][0] + F[2][1][0]
        y = F[2][0][1] + F[2][1][1]
        z = F[2][0][2] + F[2][1][2]
        f3.append([count,math.sqrt(math.pow(x,2)+math.pow(y,2)+math.pow(z,2))])

    #Increase counters.
    remover = remover + 1
    count = count + delta

    #Revisamos el progreso de la simulación.
    if count in checkin:
        print(str(100*count/time),"%")

####Primer caso prueba:
####A(r = 0.05,pos[1,0,0],vel[0,0,0])
####B(r = 0.05,pos[-1,0,0,vel[0,0,0])
####y revisar los archivos para revisar choque. Debe de ocurrir
####con las posiciones finales [-0.05,0,0] y [0.05,0,0]######
x = co2[i][1]-co3[i][1]
y = co2[i][2]-co3[i][2]
z = co2[i][3]-co3[i][3]
d = math.sqrt(math.pow(x,2)+math.pow(y,2)+math.pow(z,2))
peri[0] = d
peri[1] = 0
for i in range(0,len(co2)):
    x = co2[i][0]-co3[i][0]
    y = co2[i][1]-co3[i][1]
    z = co2[i][2]-co3[i][2]
    d = math.sqrt(math.pow(x,2)+math.pow(y,2)+math.pow(z,2))
    if peri[0] >= d:
        if x >= 0:
            peri[0] = d
            peri[1] = co2[i][3]
        else:
            peri[0] = -d
            peri[1] = co2[i][3]


#################################text-based UI##################################
#Para cambir el output location
#print("File path:") path = input() path = path + "/" + "coordenadas1.csv"
##Convertir las listas en DataFrames para convertirlos en archivos .csv
#Posiciones
dataframe1 = pd.DataFrame(co1, columns = ['X (m)', 'Y (m)', 'Z (m)', 't (s)'])
print(dataframe1)
dataframe1.to_csv('/Users/santi/Desktop/Execution environment/coordenadas1.csv',
index = None)
dataframe2 = pd.DataFrame(co2, columns = ['X (m)', 'Y (m)', 'Z (m)', 't (s)'])
print(dataframe2)
dataframe2.to_csv('/Users/santi/Desktop/Execution environment/coordenadas2.csv',
index = None)
dataframe15 = pd.DataFrame(co3, columns = ['X (m)', 'Y (m)', 'Z (m)', 't (s)'])
print(dataframe15)
dataframe15.to_csv('/Users/santi/Desktop/Execution environment/coordenadas3.csv',
index = None)

#Coordenadas del Sol
dataframe3 = pd.DataFrame(vx1, columns = ['t (s)', 'Vx (m/s)'])
print(dataframe3)
dataframe3.to_csv('/Users/santi/Desktop/Execution environment/vx1.csv',
index = None)
dataframe4 = pd.DataFrame(vy1, columns = ['t (s)', 'Vy (m/s)'])
print(dataframe4)
dataframe4.to_csv('/Users/santi/Desktop/Execution environment/vy1.csv',
index = None)
dataframe5 = pd.DataFrame(vz1, columns = ['t (s)', 'Vz (m/s)'])
print(dataframe5)
dataframe5.to_csv('/Users/santi/Desktop/Execution environment/vz1.csv',
index = None)

#Coordenadas de Jupiter
dataframe6 = pd.DataFrame(vx2, columns = ['t (s)', 'Vx (m/s)'])
print(dataframe6)
dataframe6.to_csv('/Users/santi/Desktop/Execution environment/vx2.csv',
index = None)
dataframe7 = pd.DataFrame(vy2, columns = ['t (s)', 'Vy (m/s)'])
print(dataframe7)
dataframe7.to_csv('/Users/santi/Desktop/Execution environment/vy2.csv',
index = None)
dataframe8 = pd.DataFrame(vz2, columns = ['t (s)', 'Vz (m/s)'])
print(dataframe8)
dataframe8.to_csv('/Users/santi/Desktop/Execution environment/vz2.csv',
index = None)

#Coordenadas del asteroide
dataframe16 = pd.DataFrame(vx3, columns = ['t (s)', 'Vx (m/s)'])
print(dataframe16)
dataframe16.to_csv('/Users/santi/Desktop/Execution environment/vx3.csv',
index = None)
dataframe17 = pd.DataFrame(vy3, columns = ['t (s)', 'Vy (m/s)'])
print(dataframe17)
dataframe17.to_csv('/Users/santi/Desktop/Execution environment/vy3.csv',
index = None)
dataframe18 = pd.DataFrame(vz3, columns = ['t (s)', 'Vz (m/s)'])
print(dataframe18)
dataframe18.to_csv('/Users/santi/Desktop/Execution environment/vz3.csv',
index = None)

dataframe19 = pd.DataFrame(f3_1, columns =
['t (s)', 'Fx', 'Fy', 'Fz', 'F (N)'])
print(dataframe19)
dataframe19.to_csv('/Users/santi/Desktop/Execution environment/f_asteroide_sol.csv',
index = None)
dataframe20 = pd.DataFrame(f3_2, columns = ['t (s)', 'Fx', 'Fy', 'Fz', 'F(N) '])
print(dataframe20)
dataframe20.to_csv('/Users/santi/Desktop/Execution environment/f_asteroide_jupiter.csv',
index = None)

dataframe21 = pd.DataFrame(f1, columns = ['t (s)','F (N)'])
print(dataframe21)
dataframe21.to_csv('/Users/santi/Desktop/Execution environment/f_sol.csv',
index = None)
dataframe22 = pd.DataFrame(f2, columns = ['t (s)', 'F(N) '])
print(dataframe22)
dataframe22.to_csv('/Users/santi/Desktop/Execution environment/f_jupiter.csv',
index = None)
dataframe23 = pd.DataFrame(f3, columns = ['t (s)', 'F (N)'])
print(dataframe23)
dataframe23.to_csv('/Users/santi/Desktop/Execution environment/f_asteroide.csv',
index = None)

#Energías del sistema
dataframe9 = pd.DataFrame(e_cinetica, columns = ['t (s)', 'T (J)'])
print(dataframe9)
dataframe9.to_csv('/Users/santi/Desktop/Execution environment/cinetica.csv',
index = None)
dataframe10 = pd.DataFrame(e_potencial, columns = ['t (s)', 'U (J)'])
print(dataframe10)
dataframe10.to_csv('/Users/santi/Desktop/Execution environment/potencial.csv',
index = None)

#Momentos lineales del sistema
dataframe11 = pd.DataFrame(P, columns = ['t (s)', 'P (kg*m/s)'])
print(dataframe11)
dataframe11.to_csv('/Users/santi/Desktop/Execution environment/momento_lineal.csv',
index = None)
dataframe12 = pd.DataFrame(Px, columns = ['t (s)', 'Px (kg*m/s)'])
print(dataframe12)
dataframe12.to_csv('/Users/santi/Desktop/Execution environment/momento_lineal_x.csv',
index = None)
dataframe13 = pd.DataFrame(Py, columns = ['t (s)', 'Py (kg*m/s)'])
print(dataframe13)
dataframe13.to_csv('/Users/santi/Desktop/Execution environment/momento_lineal_y.csv',
index = None)
dataframe14 = pd.DataFrame(Pz, columns = ['t (s)', 'Pz (kg*m/s)'])
print(dataframe14)
dataframe14.to_csv('/Users/santi/Desktop/Execution environment/momento_lineal_z.csv',
index = None)

#If there was no crash with the planet...
if error == False:

    print("\n****************************************************************")
    print("Simulation done!!!")
    #playsound('siren.mp3')
    print("****************************************************************")

#If you crashed...
else:
    print('\n****************************************************************')
    print("There goes the neighborhood")
    print("Your trajectory was deffective in accuracy")
    print("Crashed after: " + str(count) + " seconds.")
    print("****************************************************************")

print("D: " + str(peri[0]))
print("T: " + str(peri[1]))
