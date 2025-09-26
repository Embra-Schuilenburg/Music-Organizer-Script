from pathlib import Path, WindowsPath
import os
from os import walk
import shutil
import eyed3
import logging

eyed3.log.setLevel(logging.ERROR)  # only show errors, not warnings


# Method Definitions
def initializeInvalidFilesFolder(directories):
    """

    :type directories: dict
    """
    # check if an "InvalidFiles" directory exists, if not then make one
    for directory in directories:
        if directory == "InvalidFiles":
            return
    os.mkdir("InvalidFiles")


import re

def replaceSpecialCharacters(s: str) -> str:
    if not isinstance(s, str):
        return ""
    # characters Windows forbids anywhere in names
    illegal_chars = '<>:"/\\|?*\'\u2026'  # include the ellipsis character U+2026
    for ch in illegal_chars:
        s = s.replace(ch, "$")
    # Windows forbids trailing dots/spaces in path components
    s = re.sub(r"[\. ]+$", "", s)  # strip any run of dots/spaces at the end
    if not s:
        s = "_"  # avoid empty names after stripping
    return s

def containsIllegalCharacters(s: str) -> bool:
    if not isinstance(s, str):
        return True
    # check for any forbidden char OR trailing dot/space
    if any(c in '<>:"/\\|*\'\u2026' for c in s):
        return True
    return bool(re.search(r"[\. ]+$", s))  # trailing dots/spaces are illegal



# Path Initialization
# Enter the path of the music folder
# get destination TODO: implement scripting execution with pipx & remove hardcoded value
os.chdir("C:\\Users\\Em\\Desktop\\Music")
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
for name in musicFiles[:]:
    if containsIllegalCharacters(name):
        p = Path(cwd) / name
        p.rename(p.with_name(replaceSpecialCharacters(name)))
musicFiles = [
    replaceSpecialCharacters(file) if containsIllegalCharacters(file) else file
    for file in musicFiles
]
print("Input Validated")

# Album Directory Creation
for musicFile in musicFiles[:]:
    song = eyed3.load(musicFile)
    try:
        if (
            song.tag.album_artist is not None
            and song.tag.album_artist != "Various Artists"
        ):
            os.mkdir(replaceSpecialCharacters(song.tag.album_artist))
        elif song.tag.artist is None or song.tag.artist == "Various Artists":
            shutil.move(
                os.path.join(cwd, musicFile),
                os.path.join(cwd, "InvalidFiles", musicFile),
            )
            musicFiles.remove(musicFile)
        else:
            os.mkdir(replaceSpecialCharacters(song.tag.artist))
    except FileExistsError:
        pass
print("Album Directories Created")

# File Sorting By Artist
for musicFile in musicFiles[:]:
    song = eyed3.load(musicFile)
    try:
        if song.tag.album_artist is not None and song.tag.album_artist != "Various Artists":
            shutil.move(
                os.path.join(cwd, musicFile),
                os.path.join(cwd, replaceSpecialCharacters(song.tag.album_artist), musicFile),
            )
            musicFiles.remove(musicFile)
        elif song.tag.artist is None or song.tag.artist == "Various Artists":
            shutil.move(
                os.path.join(cwd, musicFile), os.path.join(cwd, "InvalidFiles", musicFile)
            )
            musicFiles.remove(musicFile)
        else:
            shutil.move(
                os.path.join(cwd, musicFile), os.path.join(cwd, replaceSpecialCharacters(song.tag.artist), musicFile)
            )
            musicFiles.remove(musicFile)
    except WindowsError:
        pass
print("Songs Sorted By Artist")

# Within Artist Album Sorting
for dirpath, dirnames, filenames in walk(os.getcwd()):
    musicFiles.extend(filenames)
    directories.extend(dirnames)
    break

for directory in directories[:]:
    if directory == "InvalidFiles":
        continue
    artistSongs = []
    artistAlbums = []
    for dirpath, artistAlbums, artistSongs in walk(
        os.path.join(os.getcwd(), directory)
    ):
        musicFiles.extend(artistSongs)
        directories.extend(artistAlbums)
        break

    for artistSong in artistSongs[:]:
        print("Processing: ", artistSong)
        currentArtistSongFile = eyed3.load(os.path.join(directory, artistSong))
        if currentArtistSongFile.tag.album is None:
            shutil.move(
                os.path.join(cwd, directory, artistSong),
                os.path.join(cwd, "InvalidFiles", artistSong),
            )
        try:
            os.mkdir(
                os.path.join(
                    cwd,
                    directory,
                    replaceSpecialCharacters(currentArtistSongFile.tag.album),
                )
            )
            shutil.move(
                os.path.join(cwd, directory, artistSong),
                os.path.join(
                    cwd,
                    directory,
                    replaceSpecialCharacters(currentArtistSongFile.tag.album),
                ),
            )
        except FileExistsError:
            try:
                shutil.move(
                    os.path.join(cwd, directory, artistSong),
                    os.path.join(
                        cwd,
                        directory,
                        replaceSpecialCharacters(currentArtistSongFile.tag.album),
                    ),
                )
            except WindowsError:
                 print("WindowsError")
                 shutil.move(
                     os.path.join(cwd, directory, artistSong), os.path.join(cwd, "InvalidFiles", artistSong)
                 )
        except WindowsError:
            shutil.move(
                os.path.join(cwd, directory, artistSong), os.path.join(cwd, "InvalidFiles", artistSong)
            )
