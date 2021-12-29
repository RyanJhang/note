@echo on
set version=1
C:\Python38_64\Scripts\pyinstaller -D -c --clean --onefile "C:\Users\ryan.jhang\Documents\ryan\note\rtsp\13get_av_by_pyffmpeg_gpu_draw_by_pyqt_openlg.py"
cd dist
explorer "C:\Users\ryan.jhang\Documents\ryan\note\rtsp\dist"

@REM DEL /Q client_v%version%.exe
@REM ren client.exe client_v%version%.exe
pause
