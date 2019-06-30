from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np

class Gen:
    size = (32, 32)
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' #abcdefghijklmnopqrstuvwxyz
    fonts = ['/Library/Fonts/Arial.ttf']

    def char2idx(self,c):
        for i in range(len(self.letters)):
            if self.letters[i] == c:
                return i

    def generateLetter(self, letter, name, font, fontSize, txtColor, backColor, skew, noise, save):
        filename = 'folder/' + letter + '-' + name + '.png'

        img = Image.new('RGB', self.size, color = backColor)

        fnt = ImageFont.truetype(font,24)
        d = ImageDraw.Draw(img)
        d.text((random.randint(5,10), random.randint(5,10)), letter, font=fnt, fill=txtColor)

        img = img.rotate(skew, fillcolor=backColor)

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                px = list(img.getpixel((i,j)))
                for k in range(len(px)):
                    px[k] = int((noise*random.random()) - (noise/2) + px[k])
                    px[k] = min(max(px[k],0),255)
                img.putpixel((i,j),tuple(px))
        if save:
            img.save(filename)
        return np.array(img)


    def randomColor(self):
        return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    def generateSet(self, n, letters, fonts):
        for i in range(n):
            self.generateLetter(random.choice(letters),str(i),random.choice(fonts),24, self.randomColor(), self.randomColor(), random.randint(-15,15), 10, True)

    def generateNumpySet(self, n, letters, fonts):
        set = []
        label = []
        for k in range(n):
            print("Generating training set: ", k,'/',n)
            randLetter = random.choice(letters)
            set.append(self.generateLetter(randLetter,'',random.choice(fonts),24, (0,0,0), (255,255,255), random.randint(-10,10), 50, False))
            label.append(self.char2idx(randLetter))
        return (np.array(set),np.array(label))
