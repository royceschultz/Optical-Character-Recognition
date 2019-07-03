from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random
import numpy as np
import os

class Gen:
    size = (32, 32)
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    fonts = ['/Library/Fonts/Arial.ttf',
        '/Library/Fonts/Times New Roman.ttf',
        '/Library/Fonts/Apple Chancery.ttf',
        '/Library/Fonts/AppleMyungjo.ttf',
        '/Library/Fonts/AppleMyungjo.ttf',
        '/Library/Fonts/BigCaslon.ttf',
        '/Library/Fonts/Bradley Hand Bold.ttf',
        '/Library/Fonts/Brush Script.ttf',
        '/Library/Fonts/Chalkduster.ttf',
        '/Library/Fonts/Georgia.ttf',
        '/Library/Fonts/Herculanum.ttf',
        '/Library/Fonts/Luminari.ttf'
        ]

    def char2idx(self,c):
        for i in range(len(self.letters)):
            if self.letters[i] == c:
                return i
    last = 'c'
    def generateLetter(self, letter, name, font, fontSize, txtColor, backColor, skew, noise, save):
        if random.random() < .5:
            letter = letter.lower()
        filename = 'folder/' + letter + '-' + name + '.png'

        img = Image.new('RGB', self.size, color = backColor)

        fnt = ImageFont.truetype(font,24)
        d = ImageDraw.Draw(img)
        d.text((random.randint(0,15), 3), letter, font=fnt, fill=txtColor)

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

    def colorDist(self,x,y):
        s = 0
        for i in range(len(x)):
            s += abs(x[i]-y[i])
        return s

    def shuffle(self,x,y):
        x = list(x)
        y = list(y)
        if len(x) == len(y):
            print('shuffling...')
            for i in range(len(x)):
                r = random.randint(0,len(x)-1)
                if r != i:
                    x[i],x[r] = x[r],x[i]
                    y[i],y[r] = y[r],y[i]
        return np.array(x), np.array(y)

    def generateSet(self, n, letters, fonts):
        for i in range(n):
            textColor = self.randomColor()
            backColor = self.randomColor()

            #textColor = (0,0,0)
            #backColor = (255,255,255)
            while self.colorDist(textColor,backColor) < 100:
                backColor = self.randomColor()
            self.generateLetter(random.choice(letters),str(i),random.choice(fonts),10, textColor, backColor, random.randint(-15,15), 10, True)

    def generateNumpySet(self, n, letters, fonts):
        set = []
        label = []
        for k in range(n):
            print("Generating training set: ", k,'/',n, end='\r')
            randLetter = random.choice(letters)
            textColor = self.randomColor()
            backColor = self.randomColor()

            #textColor = (0,0,0)
            #backColor = (255,255,255)
            while self.colorDist(textColor,backColor) < 100:
                backColor = self.randomColor()

            set.append(self.generateLetter(randLetter,'',random.choice(fonts),random.randint(10,14), textColor, backColor, random.randint(-20,20), 30, False))
            label.append(self.char2idx(randLetter))
        print(' ')
        return (np.array(set),np.array(label))

    def generateFromFolder(self,folderName):
        i = 0
        out = []
        labels = []
        # = '/Users/royceschultz/Documents/untitled folder/'
        path = os.path.dirname(os.path.realpath(__file__))
        path += '/' + folderName
        for filename in os.listdir(path):
            if filename[-4:] == '.png':
                src = folderName + '/' + filename
                img = Image.open(src)
                img = img.convert('RGB')
                img = ImageEnhance.Contrast(img).enhance(2.0)
                out.append(np.array(img))
                labels.append(self.char2idx(filename[0]))
                i += 1
        return np.array(out), np.array(labels)
