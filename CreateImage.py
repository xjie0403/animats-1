import Image

class CreateImage:

    def __init__(self):
        self.behaviorDict = dict()
        self.perfectStrategy1 = '00011011 00011011'
        self.perfectStrategy2 = '00100111 00100111'

    def createBMP(self, fileName, animats, behaviors):

        (newBehaviors, bestBehavior1, bestBehavior1RGB, bestBehavior2, bestBehavior2RGB) = self.setBestBehaviors(behaviors)

        self.createKey(bestBehavior1, bestBehavior1RGB, bestBehavior2, bestBehavior2RGB)

        self.createBehaviorDictionary(newBehaviors)

        #print "here's what's in the dict: "
        #print self.behaviorDict

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

        bestBehavior1 = ''
        bestBehavior2 = ''
        bestBehavior1RGB = 0
        bestBehavior2RGB = 0

        if self.perfectStrategy2 in behaviors:
            temp = behaviors[0]
            behaviors.pop(behaviors.index(self.perfectStrategy2))
            behaviors[0] = self.perfectStrategy2
            behaviors.append(temp)
            bestBehavior1 = behaviors[0]
            bestBehavior1RGB = 0

        if self.perfectStrategy1 in behaviors:
            behaviors.append(behaviors.pop(behaviors.index(self.perfectStrategy1)))
            bestBehavior2 = behaviors[len(behaviors)-1]
            bestBehavior2RGB = 256

        return (behaviors, bestBehavior1, bestBehavior1RGB, bestBehavior2, bestBehavior2RGB)


    def createBehaviorDictionary(self, behaviors):

        colorVariation = 241/(len(behaviors)-1)

        #print "HERE IS THE LEN OF BEHAVIORS: " + str(len(behaviors))
        #print "HERE IS THE COLOR VARIATION NUMBER: " + str(colorVariation)
        if colorVariation == 0:
            colorVariation = 1

        print "color variation: " + str(colorVariation)

        counter = 15

        for behavior in behaviors:
            if colorVariation == 1:
                colorNumber = (float(counter)/len(behaviors))*226.
                self.behaviorDict[behavior] = int(colorNumber)
            else:
                self.behaviorDict[behavior] = counter
            counter = counter + colorVariation

        if self.behaviorDict[self.perfectStrategy1] < 256:
            self.behaviorDict[self.perfectStrategy1] = 256
        if self.behaviorDict[self.perfectStrategy2] > 0:
            self.behaviorDict[self.perfectStrategy2] = 0


    def paintPixel(self, behaviorString, x, y, pixels):
        if behaviorString in self.behaviorDict:
            pixels[x,y] = (self.behaviorDict[behaviorString], self.behaviorDict[behaviorString], self.behaviorDict[behaviorString])
        else:
            pixels[x,y] = (128,128,128)

    def createKey(self, bestBehavior1, bestBehavior1RGB, bestBehavior2, bestBehavior2RGB):
        output = open("key.txt", "w")
        output.write("The behavior: " + bestBehavior1 + " has an RGB of: " + str(bestBehavior1RGB) + " - black\n")
        output.write("The behavior: " + bestBehavior2 + " has an RGB of: " + str(bestBehavior2RGB) + " - white")
        output.close()