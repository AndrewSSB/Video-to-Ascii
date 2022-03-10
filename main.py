import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import math

chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
# chars = "Ñ@#W$9876543210?!abc;:+=-,._ "
charlist = list(chars)                  #make it to be a list
charlen = len(charlist)                 #store the list length
interval=charlen/256                    #this interval will help us to find the right caracter based on a pixel brightness
scale_factor=0.09                       #scale factor of the window (the bigger it is, the slower it moves)

charwidth=10                            #gives the ideea of a grid (space allocated to only one character)
charheight=10

def get_char(i):
    return charlist[math.floor(i*interval)]     #return the character based on a (gray) pixel brigthness

cap=cv2.VideoCapture(0, cv2.CAP_DSHOW)          #this is how you get the real time camera (it can be 0 or 1 or .. depends on how many cameras do you have)

# input_file = input("Enther the path to file: ")   #this is how you get an actual video from your pc
# cap=cv2.VideoCapture(input_file, cv2.CAP_DSHOW)

Font=ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf',12) #this is the font we use to write our characters

while True:
    _, img = cap.read()                 #get the frames (default it should be 30FPS)
    img = cv2.flip(img, 1)              #flip it (to be like an image made with the front camera of a phone)
    img = Image.fromarray(img)          #convert it to an "Image" format (it's easier to work with them)

    width, height = img.size            #get the size of the frame
    img = img.resize((int(scale_factor * width), int(scale_factor * height * (charwidth/charheight))), Image.NEAREST)   #resize it with the scale factor and charWidth/height
                                                                                                                        #to create that grid aspect
    width, height = img.size            #update width and height based on the new frame
    pixel = img.load()                  #load the frame
    outputImage = Image.new("RGB", (charwidth*width, charheight*height), color=(0,0,0))         #create a new black image to write the characters on it
    dest = ImageDraw.Draw(outputImage)                                                          #draw the image

    for i in range(height):
        for j in range(width):
            r, g, b = pixel[j, i]                           #get the pixel's RGB value
            h = int(0.299*r+0.587*g+0.114*b)                #this should be the average ((a+b+c)/3) to convert it to gray
            pixel[j, i] = (h, h, h)                         #convert it to gray
            dest.text((j * charwidth, i * charheight), get_char(h), font=Font, fill=(r,g,b))        #now draw the characters on the new black imaged

    open_cv_image = np.array(outputImage)                   #and now we convert it to cv2 format
    key = cv2.waitKey(1)                                    #exit from the infinite loop
    if key == ord("q"):
        break

    cv2.imshow("Ascii Art", open_cv_image)

cap.release()                   # release software resource; release hardware resource
cv2.destroyAllWindows()         # destroys all the windows we created
