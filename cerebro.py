
import math
from playsound import playsound

#¿Qué queremos guardar? Queremos velocidades, distancia del centro,
#energía cinética/potencial, coordenadas y momento total. Son 12 archivos.
co1 = open("coordinates1.txt", "w+")
co2 = open("coordinates2.txt", "w+")
vx1 = open("vx1.txt", "w+")
vy1 = open("vy1.txt", "w+")
vz1 = open("vz1.txt", "w+")
vx2 = open("vx2.txt", "w+")
vy2 = open("vy2.txt", "w+")
vz2 = open("vz2.txt", "w+")
radio1 = open("r1.txt", "w+")
radio2 = open("r2.txt", "w+")
T = open("cinetica.txt", "w+")
U = open("potencial.txt", "w+")
P = open("momento.txt", "w+")
H = open("hamilton.txt", "w+")

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

    for i in range(0,len(all_bodies)-1):
        for k in range(i+1,len(all_bodies)-1):
                cum_r = (all_bodies[i].radio + all_bodies[k].radio)
            if cum_r <= all_bodies[i].distancia(all_bodies[k]):
                status = True

    return status

def escribir2(archivo,c,d):
    archivo.write('('+str(c)+','+str(d)+')')
    archivo.write("\n")
def escribir3(archivo,e,f,g):
    archivo.write('('+str(e)+','+str(f)+','+str(g)')')
    archivo.write("\n")


###########################cuerpos###########################
class Cuerpo:
    c_grav = 6.67408*math.pow(10,-11)
    def __init__(self, nombre, masa, pos, vel):
        self.nombre = nombre #1
        self.masa = masa     #2
        self.pos[0] = x_pos   #3
        self.pos[1] = y_pos   #4
        self.pos[2] = z_pos   #5
        self.vel[0] = x_vel   #6
        self.vel[1] = y_vel   #7
        self.vel[2] = z_vel   #8
    def asignacion(self):
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



A = Cuerpo('Tierra',5.9736*math.pow(10,24),[0,0,0],
[0,0,0])
B = Cuerpo('Luna',7.34767*math.pow(10,21),[406700000,0,100000],
[970,0,-20])
#Activar para asignar parámetros. Si no, dejar valores existentes.
#A.asignacion()
#B.asignacion()

#Estructura de datos por si a caso.
all_bodies = [A,B]

#########################input and resolve parameters###########################

print('****************************************************************')

#Get the number of points wanted which will be used in the modulo conditional
#so as to only record data in the .txt files a limited number of times
#for even the largest trajectories.
points = float(input('Número de puntos por guardar: '))

ok = False

#Write down the initial position, gravity and gravity components.
escribir3(co1,A.pos[0],A.pos[1],A.pos[2])
escribir3(co2,B.pos[0],B.pos[1],B.pos[2])

#Resolution of calculations (∆t).
resolution = float(input('Resolución de tiempo: '))

#Simulation length in seconds.
time = float(input('Tiempo de simulación: '))

#Establishing stores for the error (crash) variable that inidicates
#if a crash ocurred, the frequency of writing down coordinates in terms
#of points skipped, and the control variables.

error = False
frecuencia_escribir = round(time/points/resolution)
remover = 0
count = 0

#Get the first velocities ready for the leapfrog method.
all_vel =
[[A.vel[0],A.vel[1],A.vel[2]]
,[B.vel[0],B.vel[1],B.vel[2]]]

#Establecemos velocity vertlett con medio paso de Euler para t + ∆t/2.
A.vel[0]

A.vel[0]A.fuerza(B,A.distancia(B))/A.masa

ar1 = 0
ar2 = 0

#get number of decimals of the resolution
decimals = 0
holdinterval = resolution
while holdinterval%1 != 0:
    holdinterval = holdinterval*10
    decimals += 1

checkin = []

for i in range(1,101):
    point = round(time*i/100)
    checkin.append(point)

#Begin simulation
while count < time:

    count = round(count,decimals)

    #count progress of simulation
    if count in checkin:
        print(str(100*count/time),"%")

    ok = False
    if remover%espacio == 0:
        vx.write('('+str(count+0.5*resolution)+','+str(velocity[0])+')')
        vx.write("\n")
        vy.write('('+str(count+0.5*resolution)+','+str(velocity[1])+')')
        vy.write("\n")
        ok = True

    one = satellite_A[1]
    two = satellite_A[2]

    #Change position according to velocity.
    satellite_A[1] = satellite_A[1] + velocity[0]*resolution
    satellite_A[2] = satellite_A[2] + velocity[1]*resolution

    if count <= 8000:
        one = abs(one - satellite_A[1])
        two = abs(two - satellite_A[2])
        three = math.sqrt(math.pow(one,2)+math.pow(two,2))/2

        if count <= 3999:
            ar1 = ar1 + math.sqrt(math.pow(satellite_A[1],2)+
            math.pow(satellite_A[2],2))*three
        elif count <= 8000:
            ar2 = ar2 + math.sqrt(math.pow(satellite_A[1],2)
            +math.pow(satellite_A[2],2))*three
    if count == 8000:
            print("Area 1: ")
            print(ar1)
            print("Area 2: ")
            print(ar2)


    #Check for crash and break if occurs. Occurs after position change
    #so that the last valid point (last loop) is recorded.
    if Inside(satellite_A[1],satellite_A[2]):
        print("Broke")
        error = True
        break

    #store acceleration data as the first step to avoid recalculating
    #it seven times.
    accsuite = acomp(satellite_A[1],satellite_A[2],count,ok)

    #Change velocity according to position/acceleration.
    velocity[0] = velocity[0] + resolution*accsuite[1]
    velocity[1] = velocity[1] + resolution*accsuite[2]

    #Write position and acceleration data only every certain number
    #of steps to save memory.
    if remover%espacio == 0:
        #For the satellite...
        coo.write('('+str(satellite_A[1])+','+str(satellite_A[2])+')')
        coo.write("\n")
        xgs.write('('+str(count)+','+str(accsuite[1])+')')
        xgs.write("\n")
        ygs.write('('+str(count)+','+str(accsuite[2])+')')
        ygs.write("\n")
        gs.write('('+str(count)+','+str(accsuite[0])+')')
        gs.write("\n")

    #Increase counters.
    remover = remover + 1
    count = count + resolution

#Done with program.
playsound('siren.mp3')

#################################text-based UI##################################
#If there was no crash with the planet...
if error == False:

    print("\n****************************************************************")
    print('final velocity in x: ', str(velocity[0]))
    print('final velocity in y: ', str(velocity[1]),"\n")
    #The [3] and [4] were never changed because velocity was retained
    #in the velocity[] list.
    print('Initial acceleration parameters')
    print(acomp(satellite_A[3],satellite_A[4],0,ok))
    print("Maximum acceleration in 'Gs': " + str(satellite_A[7]))

    #Print the coordinates where max g ocurred.
    print("At...")
    print("x: "+ str(satellite_A[5]))
    print("y: "+ str(satellite_A[6]))
    print("****************************************************************")


#If you crashed...
else:
    print('\n****************************************************************')
    print("There goes the neighborhood")
    print("Max Gs: " + str(satellite_A[7]))
    print("Crashed after: " + str(count) + " seconds.")
    print("Menu: vx, vy, 'initial acomp', quit")
    print("****************************************************************")

    #Allow for data retention of last velocity in x and y directions
    #and initial acceleration parameters.
    quit = ''
    while quit != 'quit':
        quit = input()
        if quit == 'vx':
            print('x factor velocity: ', str(velocity[0]))
        elif quit == 'vy':
            print('y factor velocity: ', str(velocity[1]))
        elif quit == 'initial acomp':
            print('Initial acceleration parameters')
            print(acomp(satellite_A[3],satellite_A[4],0,ok))
