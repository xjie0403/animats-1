import Image

class CreateImage:

    def __init__(self):
        self.behaviorDict = dict()
        self.perfectStrategy1 = '00011011 00011011'
        self.perfectStrategy2 = '00100111 00100111'

    def createBMP(self, fileName, animats, behaviors):

        newBehaviors = self.setBestBehaviors(behaviors)
        #newBehaviors = behaviors

        self.createBehaviorDictionary(newBehaviors)

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

        img.save(fileName)

    def setBestBehaviors(self, behaviors):

        if self.perfectStrategy2 in behaviors:

            temp = behaviors[0]
            behaviors.pop(behaviors.index(self.perfectStrategy2))
            behaviors[0] = self.perfectStrategy2
            behaviors.append(temp)

        if self.perfectStrategy1 in behaviors:
            behaviors.append(behaviors.pop(behaviors.index(self.perfectStrategy1)))

        return behaviors


    def createBehaviorDictionary(self, behaviors):

        #commented code to set the color variation based on the length
        #colorVariation = 255/(len(behaviors)-1)
        #if colorVariation == 0:
        #    colorVariation = 1

        colorVariation = 1

        print "color variation: " + str(colorVariation)

        counter = 0

        for behavior in behaviors:
            if colorVariation == 1:
                colorNumber = (float(counter)/len(behaviors))*256.
                self.behaviorDict[behavior] = int(colorNumber)
            else:
                self.behaviorDict[behavior] = counter
            counter = counter + colorVariation

    def paintPixel(self, behaviorString, x, y, pixels):
        pixels[x,y] = (self.behaviorDict[behaviorString], self.behaviorDict[behaviorString], self.behaviorDict[behaviorString])
        #print "printing pixel with RGB: " + str(self.behaviorDict[behaviorString])

