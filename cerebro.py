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

#Velocidades
vx1 = []
vy1 = []
vz1 = []
vx2 = []
vy2 = []
vz2 = []

#Energías
e_cinetica = []
e_potencial = []

#Momentos lineales
P = []
Px = []
Py = []
Pz = []

#Momentos angulares
PA = open("momento_angular.txt", "w+")    #15
PA_A = open("momento_angular_A.txt", "w+") #16
PA_B = open("momento_angular_B.txt", "w+") #17

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
def potencial(all_bodies):
    U = 0
    #Limitado a len(...)-2 porque el objeto número
    #all_bodies[len(all_bodies)-1] ya va a haber sido comparado con
    #todos los objetos de indice 0 a len(all_bodies)-1.
    for i in range(0,len(all_bodies)-1):
        #Este tipo de algoritmo recursivo empieza range() la k en i si no
        #quiere repetir el cálculo i-k como k-i. Si los dos empiezan
        #range() en 0, se haran los cálculos "duplicados" i-k y k-i.
        for k in range(i+1,len(all_bodies)):
            d = all_bodies[i].distancia(all_bodies[k])
            U = U + all_bodies[i].masa*all_bodies[k].masa/d

    return(U)

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
    if i != 1:
        return(Pi)
    else:
        return(Pi*math.pow(10,-24))

#Momento angular total.
def momento_angular(all_bodies):
    return(PA)
#Momento angular del cuerpo con índice j.
def momento_angular_i(all_bodies,j):
    return(PAj)

#Aceptan cualquier tipo de datos y los convierten a tipo string.
def escribir2(archivo,c,d):
    archivo.append([c,d])
def escribir3(archivo,e,f,g,h):
    archivo.append([e,f,g,h])
#Compilación de todos los datos posibles en un mismo tiempo
#gracias a que el método es velocity verlett.
def escribir_todo(A,B,count,delta,all_bodies):
    #Coordenadas
    escribir3(co1,A.pos[0],A.pos[1],A.pos[2],count+delta)
    escribir3(co2,B.pos[0],B.pos[1],B.pos[2],count+delta)
    #Velocidades
    escribir2(vx1,count+delta,A.vel[0])
    escribir2(vy1,count+delta,A.vel[1])
    escribir2(vz1,count+delta,A.vel[2])
    escribir2(vx2,count+delta,B.vel[0])
    escribir2(vy2,count+delta,B.vel[1])
    escribir2(vz2,count+delta,B.vel[2])
    #Energía potencial
    escribir2(e_potencial,count+delta,potencial(all_bodies))
    #Energía cinética
    escribir2(e_cinetica,count+delta,cinetica(all_bodies))
    #Momentos lineales
    escribir2(P,count+delta,momento_lineal(all_bodies))
    escribir2(Px,count+delta,momento_lineal_comp(all_bodies,0))
    escribir2(Py,count+delta,momento_lineal_comp(all_bodies,1))
    escribir2(Pz,count+delta,momento_lineal_comp(all_bodies,2))
    #Momentos angulares
    #escribir2(PA,count+delta,momento_angular(all_bodies))
    #escribir2(PA_A,count+delta,momento_angular_comp(all_bodies,0))
    #escribir2(PA_B,count+delta,momento_angular_comp(all_bodies,1))

###########################cuerpos###########################
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

A = Cuerpo('Tierra',6371*math.pow(10,3),5.9736*math.pow(10,24),[0,0,0],
[-1,0,0])
B = Cuerpo('Luna',1737.1*math.pow(10,3),7.34767*math.pow(10,21),[8108.2*math.pow(10,3),0,0],
[1,0,0])

#Activar para asignar parámetros. Si no, dejar valores existentes.
#A.asignacion()
#B.asignacion()

#Estructura de datos por si a caso.
#De echo la usaremos para revisar detectar colisiones entre cualquier cuerpo.
all_bodies = [A,B]

#########################input and resolve parameters###########################

print('****************************************************************')

#Get the number of points wanted which will be used in the modulo conditional
#so as to only record data in the .txt files a limited number of times
#for even the largest trajectories.
points = float(input('Número de puntos guardados: '))

#Resolution of calculations (∆t).
delta = float(input('Resolución de tiempo: '))

#Simulation length in seconds. Antes se llamaba resolution.
time = float(input('Tiempo de simulación: '))

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
#interacción opuesta (F(A-B) = -F(B-A)). Tendría la forma;
#F   A    B    C    D   ...   m

#A   0   B-A  C-A  D-A  ...  m-A

#B  A-B   0   C-B  D-B  ...  m-B

#C  A-C  B-C   0   D-C  ...  m-C

#D  A-D  B-D  C-D   0   ...  m-D

#.  ...  ...  ...  ...  ...  ...

#n  A-n  B-n  C-n  D-n  ...  m-n

#Guardamos los valores iniciales (t=0).
escribir_todo(A,B,count,0,all_bodies)
#Cambios de posición a i(t+∆t) con la F_i(t).
F = A.fuerza(B)
#F2 es la fuerza opuesta a F y la que es aplicada el segundo objeto.
F2 = [0,0,0]
for i in range(0,3):
    A.pos[i] = A.pos[i] + A.vel[i]*delta + (math.pow(delta,2)*F[i]/A.masa)/2
    F2[i] = -F[i]
for i in range(0,3):
    B.pos[i] = B.pos[i] + B.vel[i]*delta + (math.pow(delta,2)*F2[i]/B.masa)/2
#Cambios de velocidad a v_i(t+∆t) con la F_i(t) y F_i(t+∆t).
#Esta fuerza más avanzada es calculada con las nuevas posiciones i(t+∆t).
F3 = A.fuerza(B)
F4 = [0,0,0]
for i in range(0,3):
    A.vel[i] = A.vel[i] + delta*(F[i]/A.masa + F3[i]/A.masa)/2
    F4[i] = -F2[i]
for i in range(0,3):
    B.vel[i] = B.vel[i] + delta*(F2[i]/B.masa + F4[i]/B.masa)/2

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

    #Velocidad intermedia (v(t+0.5*∆t)). Solo se usa para la posición nueva.
    F = A.fuerza(B)
    #Creamos una lista que se pueda invertir.
    F2 = [0,0,0]
    for i in range(0,3):
        F2[i] = F[i]
    for i in range(0,len(all_bodies)):
        for k in range(0,3):
            all_bodies[i].vel[k] = all_bodies[i].vel[k]
            + delta*(F2[k]/all_bodies[i].masa)/2
            #Fuerzas invertidas para el siguiente objeto.
            F2[k] = -F2[k]

    #Posición nueva en base a la velocidad intermedia (de hace media ∆t).
    for i in range(0,len(all_bodies)):
        for k in range(0,3):
            all_bodies[i].pos[k] = (all_bodies[i].pos[k]) + delta*(all_bodies[i].vel[k])

    #Ahora sí obtenemos la velocidad que corresponde al tiempo actual
    #con la aceleración y posición nuevas (v(t+∆t)=v(t+0.5*∆t)+a(i(t+∆t))).
    F = A.fuerza(B)
    F2 = [0,0,0]
    for i in range(0,3):
        F2[i] = F[i]
    for i in range(0,len(all_bodies)):
        for k in range(0,3):
            #Por alguna razón si pongo estas expresiones en la ecuación de
            #forma directa me lee un error de syntax.
            a = all_bodies[i].vel[k]
            b = 0.5*delta*(F2[k]/all_bodies[i].masa)
            all_bodies[i].vel[k] = a + b
            #Fuerzas invertidas para el siguiente objeto.
            F2[k] = -F2[k]


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
        escribir_todo(A,B,count,delta,all_bodies)
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

#################################text-based UI##################################
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
#Para cambir el output location
#print("File path:") path = input() path = path + "/" + "coordenadas1.csv"
##Convertir las listas en DataFrames para convertirlos en archivos .csv
dataframe1 = pd.DataFrame(co1, columns = ['X (m)', 'Y (m)', 'Z (m)', 't (s)'])
print(dataframe1)
dataframe1.to_csv('/Users/santi/Desktop/Execution environment/coordenadas1.csv', index = None)
dataframe2 = pd.DataFrame(co2, columns = ['X (m)', 'Y (m)', 'Z (m)', 't (s)'])
print(dataframe2)
dataframe2.to_csv('/Users/santi/Desktop/Execution environment/coordenadas2.csv', index = None)
dataframe3 = pd.DataFrame(vx1, columns = ['t (s)', 'Vx (m/s)'])
print(dataframe3)
dataframe3.to_csv('/Users/santi/Desktop/Execution environment/vx1.csv', index = None)
dataframe4 = pd.DataFrame(vy1, columns = ['t (s)', 'Vy (m/s)'])
print(dataframe4)
dataframe4.to_csv('/Users/santi/Desktop/Execution environment/vy1.csv', index = None)
dataframe5 = pd.DataFrame(vz1, columns = ['t (s)', 'Vz (m/s)'])
print(dataframe5)
dataframe5.to_csv('/Users/santi/Desktop/Execution environment/vz1.csv', index = None)
dataframe6 = pd.DataFrame(vx2, columns = ['t (s)', 'Vx (m/s)'])
print(dataframe6)
dataframe6.to_csv('/Users/santi/Desktop/Execution environment/vx2.csv', index = None)
dataframe7 = pd.DataFrame(vy2, columns = ['t (s)', 'Vy (m/s)'])
print(dataframe7)
dataframe7.to_csv('/Users/santi/Desktop/Execution environment/vy2.csv', index = None)
dataframe8 = pd.DataFrame(vz2, columns = ['t (s)', 'Vz (m/s)'])
print(dataframe8)
dataframe8.to_csv('/Users/santi/Desktop/Execution environment/vz2.csv', index = None)
dataframe9 = pd.DataFrame(e_cinetica, columns = ['t (s)', 'U (J)'])
print(dataframe9)
dataframe9.to_csv('/Users/santi/Desktop/Execution environment/cinetica.csv', index = None)
dataframe10 = pd.DataFrame(e_potencial, columns = ['t (s)', 'T (J)'])
print(dataframe10)
dataframe10.to_csv('/Users/santi/Desktop/Execution environment/potencial.csv', index = None)
dataframe11 = pd.DataFrame(P, columns = ['t (s)', 'P (kg*m/s)'])
print(dataframe11)
dataframe11.to_csv('/Users/santi/Desktop/Execution environment/momento_lineal.csv', index = None)
dataframe12 = pd.DataFrame(Px, columns = ['t (s)', 'Px (kg*m/s)'])
print(dataframe12)
dataframe12.to_csv('/Users/santi/Desktop/Execution environment/momento_lineal_x.csv', index = None)
dataframe13 = pd.DataFrame(Py, columns = ['t (s)', 'Py (kg*m/s)'])
print(dataframe13)
dataframe13.to_csv('/Users/santi/Desktop/Execution environment/momento_lineal_y.csv', index = None)
dataframe14 = pd.DataFrame(Pz, columns = ['t (s)', 'Pz (kg*m/s)'])
print(dataframe14)
dataframe14.to_csv('/Users/santi/Desktop/Execution environment/momento_lineal_z.csv', index = None)
