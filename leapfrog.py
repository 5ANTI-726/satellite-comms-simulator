import math
from playsound import playsound

#Open files for coordinates, gravity and gravity components.
#Concider velocity data too.
coo = open("coordinates.txt", "w+")
gs = open("gs.txt", "w+")
xgs = open("xgs.txt", "w+")
ygs = open("ygs.txt", "w+")
vx = open("vx.txt", "w+")
vy = open("vy.txt", "w+")
dr = open("r.txt", "w+")
area1 = open("area1.txt", "w+")
area2 = open("area2.txt", "w+")

#Get initial velocity and orientation.
#Concider giving heading in terms of an angle or a different point in space.

def vcomp(v,theta):
    #No idea which is more expensive...
    x = abs(v)*math.cos(theta)
    y = math.sqrt(math.pow(v,2)-math.pow(x,2))
    return round(x,6), round(y,6)

#Get the acceleration component at any point in space with
#respect to a static point (0,0) and using the normal
#gravitational constant and earth mass.

#I will eventually allow for a moving earth and have to create separate methods
#for the accelerations from different bodies. Another option is giving the name
#of the body (e.g. moon, earth, sun) and selecting and appropriate submethod.
def acomp(x,y,count,ok):
    #acceleration for bodies
    moon = ''
    if moon == 'body':
        gravc = 6.67408*math.pow(10,-11)
        massearth = 5.972*math.pow(10,24)
        d = math.sqrt(math.pow(x,2)+math.pow(y,2))

        #Calculate the components
        a = gravc*massearth/math.pow(d,2)
        if x == 0:
            ax = 0
            ay = -a*y/abs(y)
        if y == 0:
            ax = -a*x/abs(x)
            ay = 0
        else:
            ax = -a*x/d
            ay = -a*y/d

        g = a/9.81964973772
        return(float(a),float(ax),float(ay),float(g))

    #parameters of gravity field
    else:
        gravc = 6.67408*math.pow(10,-11)
        massearth = 5.972*math.pow(10,24)
        dearth = math.sqrt(math.pow(x,2)+math.pow(y,2))

        #Calculate the components
        aearth = gravc*massearth/math.pow(dearth,2)
        if x == 0:
            axearth = 0
            ayearth = -aearth*y/abs(y)
        if y == 0:
            axearth = -aearth*x/abs(x)
            ayearth = 0
        else:
            axearth = -aearth*x/dearth
            ayearth = -aearth*y/dearth

        if ok:
            dr.write('('+str(count)+','+str(dearth)+')')
            dr.write("\n")

        a = aearth
        ax = axearth
        ay = ayearth

        return(a,ax,ay,g)

#Check to see if the coordinates of the object are within the earth
#according a radius of 6,371,000 meters. This would mean collision.
def Inside(x,y):
    if math.sqrt(math.pow(x,2) + math.pow(y,2)) <= 6371000:
        return True
    else:
        return False

#########################input and resolve parameters###########################

print('****************************************************************')

#Parameters: ['name',x-position, y-position, initial-x velocity,
#initial-y velocity, max-g-coordinates, max-g].
satellite_A = ['sat_a',0,0,0,0,0,0,0]

#Defining the variables of the moon: Located at 'right' of the earth and at
#apogee (with it's lowest speed)
#Parameters: ['x-position', 'y-position', ???, ???]
moon = [4.067*math.pow(10,8),0,0,970]

#Get the initial x and y positions.
satellite_A[1] = float(input('x coordinates: '))
satellite_A[2] = float(input('y coordinates: '))
satellite_A[3] = satellite_A[1]
satellite_A[4] = satellite_A[2]

ok = False

#Write down the initial position, gravity and gravity components.
coo.write('('+str(satellite_A[3])+','+str(satellite_A[4])+')')
coo.write("\n")
gs.write('('+str(0)+','+str(acomp(satellite_A[3],satellite_A[4],0,ok)[0])+')')
gs.write("\n")
xgs.write("("+str(0)+","+str(acomp(satellite_A[3],satellite_A[4],0,ok)[1])+")")
xgs.write("\n")
ygs.write('('+str(0)+','+str(acomp(satellite_A[3],satellite_A[4],0,ok)[2])+')')
ygs.write("\n")

#Get the initial velocity and angle.
v = float(input('Velocity (m/s): '))
theta = float(input('Angle: '))

#Get the inital velocity components and save into a velocity vector.
velocity = ['','']
inter = vcomp(v, theta)
velocity[0] = inter[0]
velocity[1] = inter[1]

#Get the number of points wanted which will be used in the modulo conditional
#so as to only record data in the .txt files a limited number of times
#for even the largest trajectories.
points = float(input('Number of points: '))

#Resolution of calculations. Here we have the drift of the satellite
#according to the resolution.
##acceleration error of -2.07184969376e-5 (m/s^2) per second, resolution of 5
##acceleration error of -4.65279355e-7 (m/s^2) per second, resolution of 0.1
##acceleration error of -4.66440071e-8 (m/s^2) per second, resolution of 0.01
##acceleration error of -4.67268049e-9 (m/s^2) per second, resolution of 0.001
resolution = float(input('Time resolution: '))

#Simulation length in seconds.
time = float(input('Clock: '))

#Establishing stores for the maximum acceleration observed, in g's,
#the coordinantes for the max g, the error (crash) variable that inidicates
#if a crash ocurred, the frequency of writing down coordinates in terms
#of points skipped (espacio), and the control variables.

error = False
remover = 0
count = 0
espacio = round(time/points/resolution)

accsuite = acomp(satellite_A[1],satellite_A[2],0,True)
velocity[0] = velocity[0] + 0.5*resolution*accsuite[1]
velocity[1] = velocity[1] + 0.5*resolution*accsuite[2]

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
