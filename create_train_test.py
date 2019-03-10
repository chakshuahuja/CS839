from os import listdir
import shutil

source = "./labelled/"
dest1 = "./train/"
dest2 = "./test/"

for file in listdir(source):
    if int(file[0:3]) < 201:
        shutil.copyfile(source + file, dest1 + file)
    else:
        shutil.copyfile(source + file, dest2 + file)
