```
python -c "import cv2; print(cv2.getBuildInformation())"

General configuration for OpenCV 4.4.0 =====================================
  Version control:               4.4.0

  Extra modules:
    Location (extra):            C:/Users/appveyor/AppData/Local/Temp/1/pip-req-build-71670poj/opencv_contrib/modules
    Version control (extra):     4.4.0

  Platform:
    Timestamp:                   2020-11-03T00:03:16Z
    Host:                        Windows 6.3.9600 AMD64
    CMake:                       3.18.2
    CMake generator:             Visual Studio 14 2015 Win64
    CMake build tool:            C:/Program Files (x86)/MSBuild/14.0/bin/MSBuild.exe
    MSVC:                        1900

  CPU/HW features:
    Baseline:                    SSE SSE2 SSE3
      requested:                 SSE3
    Dispatched code generation:  SSE4_1 SSE4_2 FP16 AVX AVX2
      requested:                 SSE4_1 SSE4_2 AVX FP16 AVX2 AVX512_SKX
      SSE4_1 (15 files):         + SSSE3 SSE4_1
      SSE4_2 (1 files):          + SSSE3 SSE4_1 POPCNT SSE4_2
      FP16 (0 files):            + SSSE3 SSE4_1 POPCNT SSE4_2 FP16 AVX
      AVX (4 files):             + SSSE3 SSE4_1 POPCNT SSE4_2 AVX
      AVX2 (29 files):           + SSSE3 SSE4_1 POPCNT SSE4_2 FP16 FMA3 AVX AVX2

  C/C++:
    Built as dynamic libs?:      NO
    C++ standard:                11
    C++ Compiler:                C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/x86_amd64/cl.exe  (ver 19.0.24241.7)
    C++ flags (Release):         /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MT /O2 /Ob2 /DNDEBUG
    C++ flags (Debug):           /DWIN32 /D_WINDOWS /W4 /GR  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /EHa /wd4127 /wd4251 /wd4324 /wd4275 /wd4512 /wd4589 /MP  /MTd /Zi /Ob0 /Od /RTC1
    C Compiler:                  C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/x86_amd64/cl.exe
    C flags (Release):           /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP   
/MT /O2 /Ob2 /DNDEBUG
    C flags (Debug):             /DWIN32 /D_WINDOWS /W3  /D _CRT_SECURE_NO_DEPRECATE /D _CRT_NONSTDC_NO_DEPRECATE /D _SCL_SECURE_NO_WARNINGS /Gy /bigobj /Oi  /fp:precise     /MP /MTd /Zi /Ob0 /Od /RTC1
    Linker flags (Release):      /machine:x64  /NODEFAULTLIB:atlthunk.lib /INCREMENTAL:NO  /NODEFAULTLIB:libcmtd.lib /NODEFAULTLIB:libcpmtd.lib /NODEFAULTLIB:msvcrtd.lib
    Linker flags (Debug):        /machine:x64  /NODEFAULTLIB:atlthunk.lib /debug /INCREMENTAL  /NODEFAULTLIB:libcmt.lib /NODEFAULTLIB:libcpmt.lib /NODEFAULTLIB:msvcrt.lib
    ccache:                      NO
    Precompiled headers:         YES
    Extra dependencies:          ade wsock32 comctl32 gdi32 ole32 setupapi ws2_32
    3rdparty dependencies:       ittnotify libprotobuf zlib libjpeg-turbo libwebp libpng libtiff libjasper IlmImf quirc ippiw ippicv

  OpenCV modules:
    To be built:                 aruco bgsegm bioinspired calib3d ccalib core datasets dnn dnn_objdetect dnn_superres dpm face features2d flann fuzzy gapi hfs highgui img_hash imgcodecs imgproc intensity_transform line_descriptor ml objdetect optflow phase_unwrapping photo plot python3 quality rapid reg rgbd saliency shape stereo stitching structured_light superres surface_matching text tracking video videoio videostab xfeatures2d ximgproc xobjdetect xphoto
    Disabled:                    world
    Disabled by dependency:      -
    Unavailable:                 alphamat cnn_3dobj cudaarithm cudabgsegm cudacodec cudafeatures2d cudafilters cudaimgproc cudalegacy cudaobjdetect cudaoptflow cudastereo cudawarping cudev cvv freetype hdf java js julia matlab ovis python2 sfm ts viz
    Applications:                -
    Documentation:               NO
    Non-free algorithms:         NO

  Windows RT support:            NO

  GUI:
    Win32 UI:                    YES
    VTK support:                 NO

  Media I/O:
    ZLib:                        build (ver 1.2.11)
    JPEG:                        build-libjpeg-turbo (ver 2.0.5-62)
    WEBP:                        build (ver encoder: 0x020f)
    PNG:                         build (ver 1.6.37)
    TIFF:                        build (ver 42 - 4.0.10)
    JPEG 2000:                   build Jasper (ver 1.900.1)
    OpenEXR:                     build (ver 2.3.0)
    HDR:                         YES
    SUNRASTER:                   YES
    PXM:                         YES
    PFM:                         YES

  Video I/O:
    DC1394:                      NO
    FFMPEG:                      YES (prebuilt binaries)
      avcodec:                   YES (58.54.100)
      avformat:                  YES (58.29.100)
      avutil:                    YES (56.31.100)
      swscale:                   YES (5.5.100)
      avresample:                YES (4.0.0)
    GStreamer:                   NO
    DirectShow:                  YES
    Media Foundation:            YES
      DXVA:                      NO

  Parallel framework:            Concurrency

  Trace:                         YES (with Intel ITT)

  Other third-party libraries:
    Intel IPP:                   2020.0.0 Gold [2020.0.0]
           at:                   C:/Users/appveyor/AppData/Local/Temp/1/pip-req-build-71670poj/_skbuild/win-amd64-3.8/cmake-build/3rdparty/ippicv/ippicv_win/icv
    Intel IPP IW:                sources (2020.0.0)
              at:                C:/Users/appveyor/AppData/Local/Temp/1/pip-req-build-71670poj/_skbuild/win-amd64-3.8/cmake-build/3rdparty/ippicv/ippicv_win/iw
    Lapack:                      NO
    Eigen:                       NO
    Custom HAL:                  NO
    Protobuf:                    build (3.5.1)

  OpenCL:                        YES (NVD3D11)
    Include path:                C:/Users/appveyor/AppData/Local/Temp/1/pip-req-build-71670poj/opencv/3rdparty/include/opencl/1.2
    Link libraries:              Dynamic load

  Python 3:
    Interpreter:                 C:/Python38-x64/python.exe (ver 3.8)
    Libraries:                   C:/Python38-x64/libs/python38.lib (ver 3.8.0)
    numpy:                       C:/Users/appveyor/AppData/Local/Temp/1/pip-build-env-497e9ax1/overlay/Lib/site-packages/numpy/core/include (ver 1.17.3)
    install path:                python

  Python (for build):            C:/Python27-x64/python.exe

  Java:
    ant:                         NO
    JNI:                         C:/Program Files/Java/jdk1.8.0/include C:/Program Files/Java/jdk1.8.0/include/win32 C:/Program Files/Java/jdk1.8.0/include
    Java wrappers:               NO
    Java tests:                  NO

  Install to:                    C:/Users/appveyor/AppData/Local/Temp/1/pip-req-build-71670poj/_skbuild/win-amd64-3.8/cmake-install
-----------------------------------------------------------------

```