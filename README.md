## Download and Run

1. Go to the `Releases` page.  
2. Download the file `MusicdlGUI.zip`.  
3. Unzip the archive.  
4. Launch the `MusicdlGUI.exe`.  

**Note:** Your Youtube playlist must be **public**. Private playlists will not work.


### Note to self
for the ffmpeg.exe : 
download the latest prebuilt Windows binaries here:  
👉 [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)

Look for the file named:

Download `ffmpeg-git-full.7z`

When you extract it, you’ll see something like:

ffmpeg-2025-08-20-git-...
    
    └─bin\
     ├─ ffmpeg.exe
     ├─ ffplay.exe
     └─ ffprobe.exe

The file you need is `bin/ffmpeg.exe`.
Just copy that `ffmpeg.exe` into the same folder as the Python script `MusicdlGUI.py`.


command for .exe build : 
$ pyinstaller --clean -y MusicdlGUI.spec