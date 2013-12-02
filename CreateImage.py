import Image

class CreateImage:

    def __init__(self):
        self.behaviorDict = dict()

    def createBMP(self, fileName, animats, behaviors):

        self.createBehaviorDictionary(behaviors)

        #create a white image
        img = Image.new('RGB', (len(animats), len(animats)), "white")

        # create the pixel map
        pixels = img.load()

        xLocation = 0
        for i in range(len(animats)):
            yLocation = 0
            for j in range(len(animats)):
                self.paintPixel(animats[i][j][0].getBehaviorString(), xLocation, yLocation, pixels)
                yLocation = yLocation + 1
            xLocation = xLocation + 1


        '''
        for i in range(25):    # for every pixel:
            for j in range(50):
                pixels[i,j] = (0, 0, 0) # set the colour accordingly
        '''

        img.save(fileName)

    def createBehaviorDictionary(self, behaviors):

        colorVariation = 255/len(behaviors)

        #print "color variation: " + str(colorVariation)

        counter = 0
        for behavior in behaviors:
            self.behaviorDict[behavior] = counter
            counter = counter + colorVariation

    def paintPixel(self, behaviorString, x, y, pixels):
        pixels[x,y] = (self.behaviorDict[behaviorString], self.behaviorDict[behaviorString], self.behaviorDict[behaviorString])
        #print "printing pixel with RGB: " + str(self.behaviorDict[behaviorString])

