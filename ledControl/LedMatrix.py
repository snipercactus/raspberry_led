import time
from neopixel import *


class LedMatrix:
    # LED strip configuration:
    LED_COUNT      = 64      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    #LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 10     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    alphabet = {'A': [42, 43, 44, 45, 46, 33, 36, 25, 28, 18, 19, 20, 21, 22],
                'B': [41, 42, 43, 44, 45, 46, 33, 35, 38, 25, 27, 30, 18, 20, 21],
                'C': [42, 43, 44, 45, 33, 38, 25, 30, 18, 21],
                'D': [41, 42, 43, 44, 45, 46, 33, 38, 25, 30, 18, 19, 20, 21],
                'E': [41, 42, 43, 44, 45, 46, 33, 35, 38, 25, 27, 30, 17, 22],
                'F': [41, 42, 43, 44, 45, 46, 33, 35, 25, 27, 17],
                'G': [42, 43, 44, 45, 33, 38, 25, 28, 30, 18, 20, 21],
                'H': [41, 42, 43, 44, 45, 46, 35, 27, 17, 18, 19, 20, 21, 22],
                'I': [41, 33, 25, 34, 35, 36, 37, 38, 46, 30],
                'J': [44, 45, 38, 30, 17, 18, 19, 20, 21],
                'K': [41, 42, 43, 44, 45, 46, 35, 26, 28, 17, 21, 22],
                'L': [41, 42, 43, 44, 45, 46, 38, 30, 22],
                'M': [49, 50, 51, 52, 53, 54, 42, 35, 27, 18, 9, 10, 11, 12, 13, 14],
                'N': [41, 42, 43, 44, 45, 46, 35, 28, 17, 18, 19, 20, 21, 22],
                'O': [42, 43, 44, 45, 33, 38, 25, 30, 18, 19, 20, 21],
                'P': [41, 33, 25, 18, 19, 28, 36, 44, 43, 42, 45, 46],
                'Q': [42, 33, 25, 18, 19, 20, 21, 45, 44, 43, 38, 30, 22, 14],
                'R': [46, 45, 44, 22, 21, 28, 36, 19, 18, 25, 33, 41, 42, 43],
                'S': [38, 30, 21, 45, 28, 35, 42, 33, 25, 18],
                'T': [41, 33, 25, 17, 49, 34, 35, 36, 37, 38],
                'U': [46, 38, 30, 22, 21, 20, 19, 18, 17, 41, 42, 43, 44, 45],
                'V': [38, 30, 21, 45, 20, 19, 18, 17, 41, 42, 43, 44],
                'W': [46, 30, 37, 36, 53, 52, 51, 50, 18, 19, 20, 21, 17, 49],
                'X': [41, 42, 17, 18, 27, 35, 44, 45, 46, 20, 21, 22],
                'Y': [49, 50, 17, 18, 43, 27, 36, 37, 38],
                'Z': [46, 38, 30, 22, 45, 36, 27, 18, 17, 25, 33, 41]}

    def __init__(self, iconSet=0):
        # if iconset=0:
        cloudIds = [1, 2, 8, 9, 10, 11, 16, 17, 18, 19, 24, 25, 26, 27, 32, 33,
                    34, 35, 40, 41, 42, 43, 48, 49, 50, 51, 57, 58]
        showerRainIds = [21, 23, 37, 39, 53, 55]
        rainIds = [20, 21, 22, 23, 36, 37, 38, 39, 52, 53, 54, 55]
        clearSkyIds = [0, 3, 7, 9, 14, 19, 20, 26, 27, 28, 29, 31, 32, 34, 35,
                       36, 37, 43, 44, 49, 54, 56, 60, 63]

        # icons with structure: [[color,ledIDs],[color,ledIDs],...]
        self.icons = {'cloud': [[Color(255, 255, 255), cloudIds]],
                      'shower_rain': [[Color(255, 255, 255), cloudIds],
                                      [Color(0, 0, 255), showerRainIds]],
                      'rain': [[Color(255, 255, 255), cloudIds],
                               [Color(0, 0, 255), rainIds]],
                      'clear_sky': [[Color(255, 255, 0), clearSkyIds]]}

        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ,
                                       self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS,
                                       self.LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def colorWipe(self, color=Color(0, 0, 0), wait_ms=50):
        # Wipe color across display a pixel at a time.
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def showIcon(self, iconText, wait_ms=50):
        if iconText in self.icons:
            icon = self.icons[iconText]

            for subIcon in icon:
                self.draw(subIcon[0], subIcon[1])
        else:
            print('unknown icon: {}'.format(iconText))

    def draw(self, color, points, wait_ms=50):
        for point in points:
            if point > 0 and point < (self.LED_COUNT-1):
                self.strip.setPixelColor(point, color)
                time.sleep(wait_ms/1000)
        self.strip.show()

    def stringToList(self, text):
        output = []
        # toDo: implement also lower case letter and remove this
        text = text.upper()
        for letter in text:
            if letter in self.alphabet:
                output.append(self.alphabet[letter])
            else:
                # append questionmark
                print("unknown symbol {}".format(letter))
        return output

    def write(self, color, text, wait_ms=50):
        textList = self.stringToList(text)
        formattedText = []
        flatText = []
        counter = 0
        for letter in textList:
            formattedText.append([x-(64*counter) for x in letter])
            counter = counter + 1

        # flatten the text lists to one list
        flatText = [item for sublist in formattedText for item in sublist]
        # sort the text list
        flatText.sort()
        # reverse text list
        flatText = flatText[::-1]

        while flatText[-1] < 63:
            # clear screen
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 0, 0))
            # draw the current text list
            self.draw(color, flatText, 0)
            self.strip.show()
            time.sleep(250/1000.0)
            # move text 1 coloumn to the left
            flatText = [x+8 for x in flatText]

        # clear screen
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
# a short Demo
if __name__ == "__main__":
    matrix = LedMatrix()

    matrix.write(Color(0, 0, 255), 'Hello')

    matrix.showIcon('clear_sky')

    time.sleep(1)

    matrix.colorWipe()
