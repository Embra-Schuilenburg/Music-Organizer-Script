import eyeD3
from pathlib import Path, WindowsPath
import os
from os import walk
import shutil

# Method Definitions
def initializeInvalidFilesFolder(directories):
    # check if an "InvalidFiles" directory exists, if not then make one
    for directory in directories:
        if directory == "InvalidFiles":
            return
    os.mkdir("InvalidFiles")


def containsIllegalCharacters(string):
    illegalCharacters = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]
    return bool(set(string) & set(illegalCharacters))


# Path Initialization
# Enter the path of the music folder
# get destination TODO: implement scripting execution with pipx & remove hardcoded value
os.chdir("C:\\Users\\Em\\Desktop\\MusicScriptTest")
cwd = os.getcwd()

# File and Directory Name Collection
musicFiles = []
directories = []
for dirpath, dirnames, filenames in walk(os.getcwd()):
    musicFiles.extend(filenames)
    directories.extend(dirnames)
    break

initializeInvalidFilesFolder(directories)

# Input Validation
for musicFile in musicFiles[:]:
    if containsIllegalCharacters(musicFile):
        shutil.move(
            os.path.join(cwd, musicFile), os.path.join(cwd, "InvalidFiles", musicFile)
        )
        musicFiles.remove(musicFile)

# Album Directory Creation
songTags = eyeD3.Tag()
for musicFile in musicFiles[:]:


# for each file in cwd
# if contributing artist field is not empty create a new directory corresponding to its 1st cont. artist
# else, if artist field is "Various Artists" or empty, move to file to an InvalidFile Directory
# else, make a folder named after the artist field

# for each file in cwd move to its artist directory

# for each directory except InvalidFiles:
# for each file in directory
# if Album field is empty move file to InvalidFiles folder
# else, make a directory for corresponding to its album field
# for each file move into it's directory corresponding to it's album