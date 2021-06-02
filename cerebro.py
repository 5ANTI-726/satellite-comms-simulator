import math
from playsound import playsound

#Cuando quieras agregar más cuerpos debes 1) hacer más archivos y
#agregarlos al método escribir_todo() en la línea 89,
#2) declarar el/los objeto(s) en la línea 172, 3) agregar su referencia
#a la lista all_bodies[] en la línea 178, 4) agregarlo a todas las instancias
#del método escribir_todo en main(), 5) agregarlo a los cálculos de
#primeros cambios de posición y velocidad en el bloque 211-226
#(debe ser un algoritmo recursivo basado en all_bodies), 6)

#¿Qué queremos guardar? Queremos velocidades, distancia del centro,
#energía cinética/potencial/total, coordenadas, momento lineal total
#(+componentes) y momento angular después (+componentes).  Son 18 archivos.
#Coordenadas
co1 = open("coordenadas1.txt", "w+")
co2 = open("coordernadas2.txt", "w+")
#Velocidades
vx1 = open("vx1.txt", "w+")
vy1 = open("vy1.txt", "w+")
vz1 = open("vz1.txt", "w+")
vx2 = open("vx2.txt", "w+")
vy2 = open("vy2.txt", "w+")
vz2 = open("vz2.txt", "w+")
#Energias totales
T = open("cinetica.txt", "w+")
U = open("potencial.txt", "w+")
#Momentos lineales
P = open("momento_lineal.txt", "w+")
Px = open("momento_lineal_x.txt", "w+")
Py = open("momento_lineal_y.txt", "w+")
Pz = open("momento_lineal_z.txt", "w+")
#Momentos angulares
PA = open("momento_angular.txt", "w+")
PAx = open("momento_angular_x.txt", "w+")
PAy = open("momento_angular_y.txt", "w+")
PAz = open("momento_angular_z.txt", "w+")

#Get initial velocity and orientation.
#Concider giving heading in terms of an angle or a different point in space.

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

    return(Pi)

#Momento angular total.
#def momento_angular(all_bodies):
    return(PA)
#Momento angular en componente i.
#def momento_angular_comp(all_bodies,i):
    return(PAi)

#Aceptan cualquier tipo de datos y los convierten a tipo string.
def escribir2(archivo,c,d):
    archivo.write('('+str(c)+','+str(d)+')')
    archivo.write("\n")
def escribir3(archivo,e,f,g,h):
    archivo.write('('+str(e)+','+str(f)+','+str(g)+','+str(h)+')')
    archivo.write("\n")
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
    escribir2(U,count+delta,potencial(all_bodies))
    #Energía cinética
    escribir2(T,count+delta,cinetica(all_bodies))
    #Momentos lineales
    escribir2(P,count+delta,momento_lineal(all_bodies))
    escribir2(Px,count+delta,momento_lineal_comp(all_bodies,0))
    escribir2(Py,count+delta,momento_lineal_comp(all_bodies,1))
    escribir2(Pz,count+delta,momento_lineal_comp(all_bodies,2))
    #Momentos angulares
    #escribir2(PA,count+delta,momento_angular(all_bodies))
    #escribir2(PAx,count+delta,momento_angular_comp(all_bodies,0))
    #escribir2(PAy,count+delta,momento_angular_comp(all_bodies,1))
    #escribir2(PAz,count+delta,momento_angular_comp(all_bodies,2))

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
        self.radio = input("Radio del cuerpo: ")
        #Asignación de valores del cuerpo
        self.x_pos = input("Posición en x: ")
        self.y_pos = input("Posición en y: ")
        self.z_pos = input("Posición en z: ")
        #Velocidad con ángulos o velocidades
        choice = input("Velocidad a través de ángulos o velocidades")
        if choice == "velocidades":
            self.x_vel = input("Velocidad en x: ")
            self.y_vel = input("Velocidad en y: ")
            self.z_vel = input("Velocidad en z: ")
        else:
            vel = input("Velocidad en x: ")
            theta = input("Ángulo theta: ")
            phi = input("Ángulo phi: ")
            v = vcomp(v,theta,phi)
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
[0,0,0])
B = Cuerpo('Luna',1737.1*math.pow(10,3),7.34767*math.pow(10,21),[406700000,0,100000],
[0,970,-20])
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
#coordenadas/velocidades después del inicio. Tmabién guardamos
#losnuevos parametros.
count = delta
escribir_todo(A,B,count,delta,all_bodies)

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

#############################Begin simulation###################################
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
            if i == 1:
                print(' ')
                print(str(i),str(k))
                print(all_bodies[i].vel[k])
                print(delta*all_bodies[i].vel[k])

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
    playsound('siren.mp3')
    print("****************************************************************")

#If you crashed...
else:
    print('\n****************************************************************')
    print("There goes the neighborhood")
    print("Your trajectory was deffective in accuracy")
    print("Crashed after: " + str(count) + " seconds.")
    print("****************************************************************")
