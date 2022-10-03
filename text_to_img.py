import stanza
import re
import sqlite3
import cv2
import pandas as pd
import os
import time
import shutil


def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

#stanza.download('es')
nlp = stanza.Pipeline('es')


text = "Yo azul"


doc = nlp(text)

print(doc)




w = [word.lemma for sent in doc.sentences for word in sent.words]
print(w)


conn = sqlite3.connect('Capstone_Project') 
c = conn.cursor()


c.execute('''
        SELECT *
        FROM Traductor
        ''')
df = pd.DataFrame(c.fetchall(), columns=['ID','Palabra','Imagen'])


for filename in os.listdir("result_img"):
    file_path = os.path.join("result_img", filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))



num_imgs = 0
for word in w:
    is_in_dict = df.Palabra.eq(word).values.tolist()
    if True in is_in_dict:
        idx = is_in_dict.index(True)
        img_blob = df.iloc[idx].Imagen
        num_imgs += 1
        writeTofile(img_blob, "result_img/{0}_{1}.png".format(num_imgs, word))

    else:
        letters = [*word]
        for l in letters:
            is_in_dict = df.Palabra.eq(l).values.tolist()
            idx = is_in_dict.index(True)
            img_blob = df.iloc[idx].Imagen
            num_imgs += 1
            writeTofile(img_blob, "result_img/{0}_{1}.png".format(num_imgs, l))


for filename in os.listdir("result_img"):
    f = os.path.join("result_img", filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(filename)
        img = cv2.imread(f)
        cv2.waitKey(500)
        cv2.imshow("xd",img)
        cv2.waitKey(500)
        