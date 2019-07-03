import os
import random
from PIL import Image

# Function to rename multiple files
def main():
    i = 0
    # = '/Users/royceschultz/Documents/untitled folder/'
    path = os.path.dirname(os.path.realpath(__file__))
    path += '/Images'
    for filename in os.listdir(path):
        if filename == "resize.py":
            continue
        if filename[-4:] == '.png':
            dst ="File" + str(i)+'.png'
            src = 'Images/' + filename
            dst = 'RenamedImages/' + dst
            if not os.path.exists('Images/'):
                print('Error: Images folder does not exist')
            if not os.path.exists('RenamedImages/'):
                os.mkdir('RenamedImages')
            # rename() function will
            # rename all the files
            img = Image.open(src)
            img = img.convert('RGB')
            img = img.resize((32,32))
            img.save(dst,'JPEG')
            i += 1

# Driver Code
if __name__ == '__main__':
    # Calling main() function
    main()
