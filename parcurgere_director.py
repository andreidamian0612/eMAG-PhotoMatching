#!/usr/bin/python
import os, sys
from os import walk
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy 
import cv2
from PIL import Image
import shutil

path_originals = "toresize/"	#folderul cu imaginile de comparat(in arhiva o sa fie gol)
path_to_write = "resized/"	#folderul unde punem pozele redimensionate(il stergem dupa ce terminam )
dirs = os.listdir( path_originals )

if os.path.isdir('resized/') == False:
    try:
        os.makedirs('resized/')
    except OSError, e:
        if e.errno != 17:
            raise   
        # time.sleep might help here
        pass

def resize():
    for item in dirs:	#facem resize la 32 pe 32
        if os.path.isfile(path_originals + item):
            im = Image.open(path_originals + item)
            f, e = os.path.splitext(path_to_write+item)
            imResize = im.resize((32,32), Image.ANTIALIAS)
            imResize.convert("RGB").save(f + 'resized.jpg')
            #imResize.save(f + 'resized.jpg', 'JPEG', quality=100)
	    

def compare_images(imageA, imageB):	
	s = ssim(imageA, imageB)	
	return s*100

def execute(ID1, ID2):
	path1 = "resized/" + str(ID1)
	path2 = "resized/" + str(ID2)

	poza1 = cv2.imread(path1)
	poza2 = cv2.imread(path2)
 
	# convert the images to grayscale
	poza1 = cv2.cvtColor(poza1, cv2.COLOR_BGR2GRAY)
	poza2 = cv2.cvtColor(poza2, cv2.COLOR_BGR2GRAY)
 
	# compare the images
	return compare_images(poza1, poza2)

resize()

path = "resized/"
files = os.listdir(path)

g = open("adev.csv",'w')

i = 0
while i < len(files):
	original = files[i]
	original = original[:-11]
	sim = ""
	j = i + 1
	while j < len(files):
		x = execute(files[i],files[j] )
		if x > 80.0 :		#aici setam acuratetea,cu cat e mai mare,avem output mai bun
			sim += ";"	#dar si timpul creste substantial
			sim += files[j]
			sim = sim[:-11]
			files.pop(j)
		else:
			j += 1
			
	if sim != "":
		original += sim
		g.write(original)
		g.write("\n")
	i += 1
					
# f.close()
g.close()

shutil.rmtree('resized')
