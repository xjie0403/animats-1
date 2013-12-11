import Image

'''
----------------------------------
CreateImage Class
This class creates an image based on the animats behavior
----------------------------------
'''
class CreateImage:

    def __init__(self):
        self.behaviorDict = dict()

    #creates a bmp image based on the fileName, the animates behaviors
    def createBMP(self, fileName, animats, behaviors):

        newBehaviors = self.setBestBehaviorAsLastElement(behaviors)

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

    #sets the best behavior as the last element in the list
    #so that it will be colored white
    def setBestBehaviorAsLastElement(self, behaviors):

        if '01 01' in behaviors:
            behaviors.append(behaviors.pop(behaviors.index('01 01')))

        return behaviors

    #creates a behavior dictionary where each behavior is the key
    #and the color is the entry
    def createBehaviorDictionary(self, behaviors):

        colorVariation = 255/(len(behaviors)-1)

        print "color variation: " + str(colorVariation)

        counter = 0

        for behavior in behaviors:
            self.behaviorDict[behavior] = counter
            counter = counter + colorVariation

    #paints the pixel based on the behavior
    def paintPixel(self, behaviorString, x, y, pixels):
        pixels[x,y] = (self.behaviorDict[behaviorString], self.behaviorDict[behaviorString], self.behaviorDict[behaviorString])
        #print "printing pixel with RGB: " + str(self.behaviorDict[behaviorString])

