from pathlib import Path, WindowsPath
import os
from os import walk
import shutil
import eyed3
import logging

eyed3.log.setLevel(logging.ERROR)  # only show errors, not warnings


# Method Definitions
def initializeInvalidFilesFolder(intialDirectories):
    # check if an "InvalidFiles" directory exists, if not then make one
    for directory in intialDirectories:
        if directory == "InvalidFiles":
            return
    os.mkdir("InvalidFiles")


def containsIllegalCharacters(name: str) -> bool:
    if name is None:
        raise TypeError("Name cannot be None")
    if name is "":
        return True
    for character in name:
        if character in ".,\\|<>:\"/?*& '":
            return True


def isReservedWord(name: str) -> bool:
    if name is None:
        raise TypeError("Name cannot be None")
    reservedWords = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "COM¹",
        "COM²",
        "COM³",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
        "LPT¹",
        "LPT²",
        "LPT³",
    }
    if name in reservedWords:
        return True


def replaceSpecialCharacters(oldName: str) -> str:
    if oldName is None:
        raise RuntimeError(f"Old name cannot be None")
    if oldName is "":
        return "_"
    newName = ""
    for ch in oldName:
        if ch in ".,\\|<>:\"/?*& '":
            newName += "_"
        else:
            newName += ch
    return newName


def adjustReservedWords(reservedName: str) -> str:
    if reservedName is None:
        raise RuntimeError(f"Old name cannot be None")
    if reservedName == "":
        replaceSpecialCharacters(reservedName)
    return "_" + reservedName + "_"


# Path Initialization
# Enter the path of the music folder
# get destination TODO: implement scripting execution with pipx & remove hardcoded value
os.chdir("C:\\Users\\Em\\Desktop\\Music")
cwd = os.getcwd()

# File and Directory Name Collection
initialMusicFiles = []
initialDirectories = []
for dirpath, dirnames, filenames in walk(os.getcwd()):
    initialMusicFiles.extend(filenames)
    initialDirectories.extend(dirnames)
    break

initializeInvalidFilesFolder(initialDirectories)

# Input Validation
for file in initialMusicFiles:
    if containsIllegalCharacters(file):
        file = replaceSpecialCharacters(file)
    if isReservedWord(file):
        file = adjustReservedWords(file)

# Album Directory Creation
# for musicFile in musicFiles[:]:
#     song = eyed3.load(musicFile)
#     try:
#         if (
#             song.tag.album_artist is not None
#             and song.tag.album_artist != "Various Artists"
#         ):
#             os.mkdir(replaceSpecialCharacters(song.tag.album_artist))
#         elif song.tag.artist is None or song.tag.artist == "Various Artists":
#             shutil.move(
#                 os.path.join(cwd, musicFile),
#                 os.path.join(cwd, "InvalidFiles", musicFile),
#             )
#             musicFiles.remove(musicFile)
#         else:
#             os.mkdir(replaceSpecialCharacters(song.tag.artist))
#     except FileExistsError:
#         pass
# print("Album Directories Created")
#
# # File Sorting By Artist
# for musicFile in musicFiles[:]:
#     song = eyed3.load(musicFile)
#     try:
#         if (
#             song.tag.album_artist is not None
#             and song.tag.album_artist != "Various Artists"
#         ):
#             shutil.move(
#                 os.path.join(cwd, musicFile),
#                 os.path.join(
#                     cwd, replaceSpecialCharacters(song.tag.album_artist), musicFile
#                 ),
#             )
#             musicFiles.remove(musicFile)
#         elif song.tag.artist is None or song.tag.artist == "Various Artists":
#             shutil.move(
#                 os.path.join(cwd, musicFile),
#                 os.path.join(cwd, "InvalidFiles", musicFile),
#             )
#             musicFiles.remove(musicFile)
#         else:
#             shutil.move(
#                 os.path.join(cwd, musicFile),
#                 os.path.join(cwd, replaceSpecialCharacters(song.tag.artist), musicFile),
#             )
#             musicFiles.remove(musicFile)
#     except WindowsError:
#         pass
# print("Songs Sorted By Artist")
#
# # Within Artist Album Sorting
# for dirpath, dirnames, filenames in walk(os.getcwd()):
#     musicFiles.extend(filenames)
#     directories.extend(dirnames)
#     break
#
# for directory in directories[:]:
#     if directory == "InvalidFiles":
#         continue
#     artistSongs = []
#     artistAlbums = []
#     for dirpath, artistAlbums, artistSongs in walk(
#         os.path.join(os.getcwd(), directory)
#     ):
#         musicFiles.extend(artistSongs)
#         directories.extend(artistAlbums)
#         break
#
#     for artistSong in artistSongs[:]:
#         print("Processing: ", artistSong)
#         currentArtistSongFile = eyed3.load(os.path.join(directory, artistSong))
#         if currentArtistSongFile.tag.album is None:
#             shutil.move(
#                 os.path.join(cwd, directory, artistSong),
#                 os.path.join(cwd, "InvalidFiles", artistSong),
#             )
#         try:
#             os.mkdir(
#                 os.path.join(
#                     cwd,
#                     directory,
#                     replaceSpecialCharacters(currentArtistSongFile.tag.album),
#                 )
#             )
#             shutil.move(
#                 os.path.join(cwd, directory, artistSong),
#                 os.path.join(
#                     cwd,
#                     directory,
#                     replaceSpecialCharacters(currentArtistSongFile.tag.album),
#                 ),
#             )
#         except FileExistsError:
#             try:
#                 shutil.move(
#                     os.path.join(cwd, directory, artistSong),
#                     os.path.join(
#                         cwd,
#                         directory,
#                         replaceSpecialCharacters(currentArtistSongFile.tag.album),
#                     ),
#                 )
#             except WindowsError:
#                 print("WindowsError")
#                 shutil.move(
#                     os.path.join(cwd, directory, artistSong),
#                     os.path.join(cwd, "InvalidFiles", artistSong),
#                 )
#         except WindowsError:
#             shutil.move(
#                 os.path.join(cwd, directory, artistSong),
#                 os.path.join(cwd, "InvalidFiles", artistSong),
#             )
