import math

#Open files for coordinates, gravity and gravity components.
#Concider velocity data too.
coo = open("coordinates.txt", "w+")
gs = open("gs.txt", "w+")
xgs = open("xgs.txt", "w+")
ygs = open("ygs.txt", "w+")

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
def acomp(x,y):
    #parameters of gravity field
    gravc = 6.67408*math.pow(10,-11)
    massearth = 5.972*math.pow(10,24)
    massmoon = 7.347*math.pow(10,22)
    dearth = math.sqrt(math.pow(x,2)+math.pow(y,2))
    dmoon = math.sqrt(math.pow(x-3.85*math.pow(10,8),2)+math.pow(y,2))

    #Calculate the components
    aearth = gravc*massearth/math.pow(dearth,2)
    if x == 0:
        axearth = 0
        ayearth = -aearth*abs(y)/y
    else:
        axearth = -aearth*x/dearth
        ayearth = -aearth*y/dearth

    amoon = gravc*massmoon/math.pow(dmoon,2)
    if x == 3.85*math.pow(10,8):
        axmoon = 0
        aymoon = -amoon*abs(y)/y
    else:
        axmoon = -amoon*(x-3.85*math.pow(10,8))/dmoon
        aymoon = -amoon*y/dmoon

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

#Get the initial x and y positions.
x = float(input('x coordinates: '))
y = float(input('y coordinates: '))
x0 = x
y0 = y

#Write down the initial position, gravity and gravity components.
coo.write('('+str(x)+','+str(y)+')')
coo.write("\n")
gs.write('('+str(0)+','+str(acomp(x,y)[0])+')')
gs.write("\n")
xgs.write("("+str(0)+","+str(acomp(x,y)[1])+")")
xgs.write("\n")
ygs.write('('+str(0)+','+str(acomp(x,y)[2])+')')
ygs.write("\n")

#Get the initial velocity and angle.
v = float(input('Velocity (m/s): '))
theta = float(input('Angle: '))

#Get the inital velocity components.
vx = vcomp(v, theta)[0]
vy = vcomp(v, theta)[1]

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

maxg = 0
error = False
xd = 0
yd = 0
remover = 0
count = 0
espacio = round(time/points/resolution)

#Begin simulation
while count < time:
    #store acceleration data for this step to avoid seven times the
    #acceleration calculations.
    accsuite = acomp(x,y)

    #Check for max g. Must occur before the change in position because the
    #original position is the one used for accsuite in this simulation step.
    if float(accsuite[3]) > maxg:
        maxg = accsuite[3]
        xd = x
        yd = y

    #Change position according to velocity.
    x = x + vx*resolution
    y = y + vy*resolution

    #Check for crash and break if occurs. Occurs after position change
    #to avoid a false negative and calculation of the first point within
    #the planet.
    if Inside(x,y):
        print("Broke")
        error = True
        break

    #Change velocity according to position/acceleration.
    vx = vx + resolution*accsuite[1]
    vy = vy + resolution*accsuite[2]

    #Write data only every certain number of steps.
    if remover%espacio == 0:
        coo.write('('+str(x)+','+str(y)+')')
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

#################################text-based UI##################################
#If there was no crash with the planet...
if error == False:

    print("\n****************************************************************")
    print('x factor velocity: ', str(vx))
    print('y factor velocity: ', str(vy),"\n")
    print('Initial acceleration parameters')
    print(acomp(x0,y0))
    print("Max Gs: " + str(maxg))

    #Print the positions at max g
    print("At...")
    print("x: "+ str(xd))
    print("y: "+ str(yd))
    print("****************************************************************")

#If you fudged it up...
else:
    print('\n****************************************************************')
    print("There goes the neighborhood")
    print("Max Gs: " + str(maxg))
    print("Crashed after: " + str(count) + " seconds.")
    print("****************************************************************")

    #Allow for data retention of last velocity components
    #and initial acceleration parameters.
    quit = ''
    while quit != 'quit':
        quit = input()
        if quit == 'vx':
            print('x factor velocity: ', str(vx))
        elif quit == 'vy':
            print('y factor velocity: ', str(vy))
        elif quit == 'initial acomp':
            print('Initial acceleration parameters')
            print(acomp(x0,y0))
