@REM rmdir /s /q .\build\
@REM rmdir /s /q .\dist\
pyinstaller -D -c --clean --noconfirm "C:\Users\jhang\Documents\ryan\note\opencv\cuda\get_streaming_by_cuda\get_streaming_by_cuda.py" ^
--add-binary="C:\OpenCV_Build\install\x64\vc16\bin\;." ^
--paths="C:\Anaconda3\Lib\site-packages\cv2\python-3.8\" ^
--hidden-import "pkg_resources.py2_warn" ^
--hidden-import "pkg_resources.markers"

@REM pyinstaller -D --clean "C:\Users\jhang\Documents\ryan\note\opencv\cuda\get_streaming_by_cuda\get_streaming_by_cuda.py" ^
@REM --add-binary="C:\OpenCV_Build\install\x64\vc16\bin\;." ^
@REM --paths="C:\Anaconda3\Lib\site-packages\cv2" ^
@REM --paths="C:\Anaconda3\Lib\site-packages\cv2\python-3.8\" ^
@REM -n myApp

@REM --clean




@REM --paths="C:\Anaconda3\Lib\site-packages" ^
@REM -n myApp

@REM --clean

@REM 22267 WARNING: Hidden import "pkg_resources.py2_warn" not found!
@REM 22268 WARNING: Hidden import "pkg_resources.markers" not found!

@REM 50566 INFO: Import to be excluded not found: 'setuptools.py33compat'
@REM 50567 INFO: Import to be excluded not found: 'setuptools.py27compat'