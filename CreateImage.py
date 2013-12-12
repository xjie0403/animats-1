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
        self.perfectBehavior = '01 01'

    '''
    Creates a bmp image based on the fileName, the animates behaviors
    '''
    def createBMP(self, fileName, animats, behaviors):

        (newBehaviors, bestBehavior, bestBehaviorRGB) = self.setBestBehaviorAsLastElement(behaviors)

        self.createKey(bestBehavior, bestBehaviorRGB)

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

    '''
    Sets the best behavior as the last element in the list
    so that it will be colored white
    '''
    def setBestBehaviorAsLastElement(self, behaviors):

        bestBehavior = ''
        bestBehaviorRGB = 0

        if self.perfectBehavior in behaviors:
            behaviors.append(behaviors.pop(behaviors.index(self.perfectBehavior)))
            bestBehavior = behaviors[len(behaviors)-1]
            bestBehaviorRGB = 256

        return (behaviors, bestBehavior, bestBehaviorRGB)

    '''
    Creates a behavior dictionary where each
    behavior is the key and the color is the entry
    '''
    def createBehaviorDictionary(self, behaviors):

        colorVariation = 255/(len(behaviors)-1)

        print "color variation: " + str(colorVariation)

        counter = 0

        for behavior in behaviors:
            self.behaviorDict[behavior] = counter
            counter = counter + colorVariation

    '''
    Paints the pixel based on the behavior
    '''
    def paintPixel(self, behaviorString, x, y, pixels):
        if behaviorString in self.behaviorDict:
            pixels[x,y] = (self.behaviorDict[behaviorString], self.behaviorDict[behaviorString], self.behaviorDict[behaviorString])
        else:
            pixels[x,y] = (128,128,128)

    '''
    Creates a text file that lets the user know what color
    a perfect behavior has been assigned
    '''
    def createKey(self, bestBehavior, bestBehaviorRGB):
        output = open("key.txt", "w")
        output.write("The behavior: " + bestBehavior + " has an RGB of: (" + str(bestBehaviorRGB) +", "+ str(bestBehaviorRGB) +", " + str(bestBehaviorRGB) + ") - white\n")
        output.close()

