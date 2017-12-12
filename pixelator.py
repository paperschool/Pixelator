from PIL import Image
import math,sys

picture = Image.open(sys.argv[1])
FORMAT = picture.format
col = int(math.floor(picture.size[0] / 2)) * 2
row = int(math.floor(picture.size[1] / 2)) * 2
longSide = 0

colorBoost = 1.0;

if(row > col):
    longSide = row
else:
    longSide = col

def getVoxel():
    voxels = []
    for i in range(1,longSide):
        if(row % i == 0 and col % i == 0):
            voxels.append(int(i))

    print "\nAvailable Voxels ",voxels
    print

    while True:
        voxel = raw_input("Enter A Voxel Size: ")
        if(not voxel.isdigit()):
            print "\n - Input Not An Integer\n"
            continue
        if(voxel in voxels):
            print "\n - Input Not A Suitable Voxel\n"
            continue
        break

    return int(voxel),int(voxel)

def getModeCol(colors):
    MAX = 0
    for color in colors:
        if(color[4] > MAX):
            MAX = color[4]
            modeColor = (int(color[0]*colorBoost),
                         int(color[1]*colorBoost),
                         int(color[2]*colorBoost),
                         color[3])

    modeColor = preProcessing(modeColor)

    return modeColor

def countColor(i,j,colors):
    if(FORMAT == "PNG"):
        r,g,b,a = picture.getpixel((i,j))
    else:
        r,g,b = picture.getpixel((i,j))
        a = 0

    for color in colors:
        if(color[0] == r and color[1] == g and color[2] == b and color[3] == a):
            count = color[4] + 1
            color[4] = count
            return colors

    colors.append([r,g,b,a,1])
    return colors

def getAverageCol(y,x,voxel):
    colors = []
    for i in xrange(y,y + voxel):
        for j in xrange(x,x + voxel):
            if(i <= row or j <= col):
                colors = countColor(j,i,colors)

    return getModeCol(colors)

def debugLoading(total,current,message):
    if(current == 1):
        sys.stdout.write(message + ": ")
    bar = float(current)/float(total) * 100

    if(bar == 100):
        sys.stdout.write("> DONE\n")
    if(bar % 1 == 0):
        #print bar,total,current
        sys.stdout.write("|")

def VoxeliseImage(voxel):
    newPixelArray = []
    progress = 0
    for y in xrange(0,row-1,voxel):
        imageRow = []
        for x in xrange(0,col-1,voxel):
            imageRow.append(getAverageCol(y,x,voxel))
            progress+=1
            debugLoading(row/voxel*col/voxel,progress,"Voxelisation")

        newPixelArray.append(imageRow)
    return newPixelArray

## preProcessing

def preProcessing(modeColor):
    if(len(sys.argv) == 3):
        return modeColor
    if(sys.argv[3] == "--halfsat"):
        saturation(1.1,modeColor)
    elif(sys.argv[3] == "--fullsat"):
        saturation(1.5,modeColor)

def saturation(boost,modeColor):
    for i in modeColor:
        i = i * boost

    return modeColor


## Effects ##

def effectSelection(newPixel,newPixelArray,output):
    if(sys.argv[2] == "--drag"):
        DragEffect(newPixel,newPixelArray,output)
    elif(sys.argv[2] == "--vdrag"):
        VDragEffect(newPixel,newPixelArray,output)
    elif(sys.argv[2] == "--cross"):
        CrossEffect(newPixel,newPixelArray,output)
    elif(sys.argv[2] == "--dot"):
        DotEffect(newPixel,newPixelArray,output)
    elif(sys.argv[2] == "--circle"):
        CircleEffect(newPixel,newPixelArray,output)
    elif(sys.argv[2] == "--none"):
        NormalVoxel(newPixel,newPixelArray,output)
    else:
        print "No effect Selected, choosing Normal Effect"
        NormalVoxel(newPixel,newPixelArray,output)



## not yet working as circle generation is incorrect
def CircleEffect(newPixel,newPixelArray,output):
    finalimagey = 0
    for y in newPixelArray:
        finalimagex = 0
        for x in y:
            for i in range(0,360-1):
                xpoint = (finalimagex + newPixel/2) + (newPixel-2/2) * math.cos(math.radians(i))
                ypoint = (finalimagex + newPixel/2) + (newPixel-2/2) * math.sin(math.radians(i))
                output[xpoint,ypoint] = x

            debugLoading(finalimagex*finalimagey,finalimagex+finalimagex,"Circle Effect")
            finalimagex+=newPixel
        finalimagey+=newPixel

def DotEffect(newPixel,newPixelArray,output):
    finalimagey = 0
    for y in newPixelArray:
        finalimagex = 0
        for x in y:
            output[finalimagex + newPixel/2,finalimagey + newPixel/2] = x
            debugLoading(finalimagex*finalimagey,finalimagex+finalimagex,"Circle Effect")
            finalimagex+=newPixel
        finalimagey+=newPixel

def CrossEffect(newPixel,newPixelArray,output):
    finalimagey = 0
    for y in newPixelArray:
        finalimagex = 0
        for x in y:
            for i in range(newPixel):
                output[(finalimagex+newPixel-1) - i,finalimagey + i] = x
                output[finalimagex + i,finalimagey + i] = x
            finalimagex+=newPixel
        finalimagey+=newPixel

def VDragEffect(newPixel,newPixelArray,output):
    finalimagey = 0

    for y in newPixelArray:
        finalimagex = 0
        for x in y:
            output[finalimagex + newPixel/2,finalimagey + newPixel/2] = x
            for i in range(newPixel/2):
                output[finalimagex + newPixel-1,finalimagey + i+(newPixel/2)] = x
                output[finalimagex + i+(newPixel/2),finalimagey + newPixel-1] = x
            finalimagex+=newPixel
        finalimagey+=newPixel

def DragEffect(newPixel,newPixelArray,output):
    finalimagey = 0
    for y in newPixelArray:
        finalimagex = 0
        for x in y:
            for i in range(newPixel):
                output[finalimagex + i,finalimagey + i] = x

            finalimagex+=newPixel
        finalimagey+=newPixel

def NormalVoxel(newPixel,newPixelArray,output):
    finalimagey = 0
    for y in newPixelArray:
        finalimagex = 0
        for x in y:
            for i in range(newPixel):
                for j in range(newPixel):
                    output[finalimagex + i,finalimagey + j] = x
            finalimagex+=newPixel
        finalimagey+=newPixel

def main():


    print "Image Height: %d Image Width: %d" % (row,col)

    print picture.format

    voxel,newPixel = getVoxel()

    newImage = Image.new("RGB",(col,row),"black")
    output = newImage.load()

    # voxelisation process
    newPixelArray = VoxeliseImage(voxel)

    if(len(sys.argv) == 3):
        effectSelection(newPixel,newPixelArray,output)

    if(FORMAT == "JPEG"):
        EXTENSION = "jpg"
    else:
        EXTENSION = "png"

    newImage.save("/home/overlord/Programming Projects/Image Pixelator/newImage."+EXTENSION,FORMAT)

main()
