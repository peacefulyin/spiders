from PIL import Image
img  = Image.open('0.jpg')

w,h = img.size

img.thumbnail((w//3, h//3),Image.ANTIALIAS)

img.save('a.jpg')
