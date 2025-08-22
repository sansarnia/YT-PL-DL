### ffmpeg.exe : 


download the latest prebuilt Windows binaries here:  
👉 [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)

Look for the file named:

Download `ffmpeg-git-full.7z`

When you extract it, you’ll see something like:

ffmpeg-2025-08-20-git-...\
 └─ bin\
     ├─ ffmpeg.exe
     ├─ ffplay.exe
     └─ ffprobe.exe


The file you need is `bin/ffmpeg.exe`.
Just copy that `ffmpeg.exe` into the same folder as your Python script / app `.exe`.


command for .exe build : 
$ pyinstaller MusicdlGUI.spec