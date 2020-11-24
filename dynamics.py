import math
from playsound import playsound

#Open files for coordinates, gravity and gravity components.
#Concider velocity data too.
coo = open("coordinates.txt", "w+")
gs = open("gs.txt", "w+")
xgs = open("xgs.txt", "w+")
ygs = open("ygs.txt", "w+")
moon_pos = open("moon_pos.txt", "w+")
amoon = open("amoon.txt", "w+")
axmoon = open("axmoon.txt", "w+")
aymoon = open("aymoon.txt", "w+")

#Get initial velocity components for the velocity and orientation.
#Maybe concider giving a heading option based on a differnt point since.
#It might be more exact than an angle in radians.

def vcomp(v,theta):
    x = abs(v)*math.cos(theta)
    y = math.sqrt(math.pow(v,2)-math.pow(x,2))
    return round(x,6), round(y,6)

#Get the acceleration component at any point in space with
#respect to a static point (0,0) and using the normal
#gravitational constant and earth mass.
#I will eventually allow for a moving earth and maybe split this method
#into earth gravity components and moon/mars/etc components.
def acomp(x,y,moon):
    #acceleration for bodies
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
        return(a,ax,ay,g)

    #parameters of gravity field
    else:
        gravc = 6.67408*math.pow(10,-11)
        massearth = 5.972*math.pow(10,24)
        massmoon = 7.347*math.pow(10,22)
        dearth = math.sqrt(math.pow(x,2)+math.pow(y,2))
        dmoon = math.sqrt(math.pow(x-moon[0],2)+math.pow(y-moon[1],2))

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

        amoon = gravc*massmoon/math.pow(dmoon,2)
        if x == moon[0]:
            axmoon = 0
            aymoon = -amoon*abs(y)/y
        if y == moon[1]:
            axmoon = -amoon*abs(x)/x
            aymoon = 0
        else:
            axmoon = -amoon*(x-moon[0])/dmoon
            aymoon = -amoon*(y-moon[1])/dmoon

        a = amoon + aearth
        ax = axmoon + axearth
        ay = aymoon + ayearth

        g = a/9.81964973772
        return(a,ax,ay,g)

#Check to see if the coordinates of the object are within the earth
#according a radius of 6,371,000 meters.
def Inside(x,y):
    if math.sqrt(math.pow(x,2) + math.pow(y,2)) < 6371000:
        return True
    else:
        return False

#########################input and resolve parameters###########################

print('****************************************************************')

#Parameters: ['name',x-position,y-position,initial-x,initial-y,
#max-g-coordinates,max-g].
satellite_A = ['sat_a',0,0,0,0,0,0,0]

#Definition of the moon, its position starting at a 'right' apogee
#and it's lowest velocity vector.
moon = [4.067*math.pow(10,8),0,0,970]

#Get the initial x and y positions.
satellite_A[1] = float(input('x coordinates: '))
satellite_A[2] = float(input('y coordinates: '))
satellite_A[3] = satellite_A[1]
satellite_A[4] = satellite_A[2]

#Write down the initial position, gravity and gravity components.
coo.write('('+str(satellite_A[3])+','+str(satellite_A[4])+')')
coo.write("\n")
gs.write('('+str(0)+','+str(acomp(satellite_A[3],satellite_A[4],moon)[0])+')')
gs.write("\n")
xgs.write("("+str(0)+","+str(acomp(satellite_A[3],satellite_A[4],moon)[1])+")")
xgs.write("\n")
ygs.write('('+str(0)+','+str(acomp(satellite_A[3],satellite_A[4],moon)[2])+')')
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

##########calculate movement computationally with Euler's method################

#Establishing stores for the maximum acceleration observed, in g's,
#the coordinantes for the max g, the error (crash) variable, the number of
#points to be ignored according to the points variable (espacio),
#and the control variables.

error = False
remover = 0
count = 0
espacio = round(time/points/resolution)

#Begin simulation
while count < time:
    #store acceleration data for this step to avoid seven times the
    #acceleration calculations.
    accsuite = acomp(satellite_A[1],satellite_A[2],moon)
    accsuite_moon = acomp(moon[0],moon[1],'body')

    #Check for max g. Must occur before the change in position because the
    #original position is the one used for accsuite in this simulation step.
    if float(accsuite[3]) > satellite_A[7]:
        satellite_A[7] = accsuite[3]
        satellite_A[5] = satellite_A[1]
        satellite_A[6] = satellite_A[2]

    #Change position according to velocity.
    satellite_A[1] = satellite_A[1] + velocity[0]*resolution
    satellite_A[2] = satellite_A[2] + velocity[1]*resolution

    #Also move the moon.
    moon[0] = moon[0] + resolution*moon[2]
    moon[1] = moon[1] + resolution*moon[3]

    #Check for crash and break if occurs. Occurs after position change
    #to avoid a false negative and calculation of the first point within
    #the planet.
    if Inside(satellite_A[1],satellite_A[2]):
        print("Broke")
        error = True
        break

    #Change velocity according to position/acceleration.
    velocity[0] = velocity[0] + resolution*accsuite[1]
    velocity[1] = velocity[1] + resolution*accsuite[2]

    #Also accelerate the moon.
    moon[2] = moon[2] + resolution*accsuite_moon[1]
    moon[3] = moon[3] + resolution*accsuite_moon[2]

    #Write position and acceleration data only every certain number of steps.
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
        #and the moon.
        moon_pos.write('('+str(moon[0])+','+str(moon[1])+')')
        moon_pos.write("\n")
        axmoon.write('('+str(count)+','+str(accsuite_moon[1])+')')
        axmoon.write("\n")
        aymoon.write('('+str(count)+','+str(accsuite_moon[2])+')')
        aymoon.write("\n")
        amoon.write('('+str(count)+','+str(accsuite_moon[0])+')')
        amoon.write("\n")

    #Increase counters.
    remover = remover + 1
    count = count + resolution

#Done with program.
playsound('siren.mp3')

#################################text-based UI##################################
#If there was no crash with the planet...
if error == False:

    print("\n****************************************************************")
    print('x factor velocity: ', str(velocity[0]))
    print('y factor velocity: ', str(velocity[1]),"\n")
    print('Initial acceleration parameters')
    print(acomp(satellite_A[3],satellite_A[4],moon))
    print("Max Gs: " + str(satellite_A[7]))

    #Print the positions at max g
    print("At...")
    print("x: "+ str(satellite_A[5]))
    print("y: "+ str(satellite_A[6]))
    print("****************************************************************")

#If you fudged it up...
else:
    print('\n****************************************************************')
    print("There goes the neighborhood")
    print("Max Gs: " + str(satellite_A[7]))
    print("Crashed after: " + str(count) + " seconds.")
    print("Menu: vx, vy, 'initial acomp', quit")
    print("****************************************************************")

    #Allow for data retention of last velocity components
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
            print(acomp(satellite_A[3],satellite_A[4],moon))
