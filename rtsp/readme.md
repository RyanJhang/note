
## KEYWORD
 - Hardware Accelerated decode
 - GPU decode

## How to check coders in windows10?
```
ffmpeg.exe -encoders

bash
ffmpeg.exe -encoders | grep 264

ffmpeg.exe -encoders | grep qsv
```
https://www.youtube.com/watch?v=H81fgnaXkHY
https://trac.ffmpeg.org/wiki/Hardware/QuickSync

## What is qsv?
Intel Quick Sync Video is Intel's brand for its dedicated video encoding and decoding hardware core.
Unlike video encoding on a CPU or a general-purpose GPU, Quick Sync is a dedicated hardware core on the processor die.
https://en.wikipedia.org/wiki/Intel_Quick_Sync_Video

## Intel® Quick Sync Video and FFmpeg Performance
https://www.intel.com/content/dam/www/public/us/en/documents/white-papers/cloud-computing-quicksync-video-ffmpeg-white-paper.pdf


## ffprobe 使用小结
https://www.jianshu.com/p/789244ad10d8


## pyaudio download
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio