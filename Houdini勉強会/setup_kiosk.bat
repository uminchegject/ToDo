set EXE="C:\Program Files\Side Effects Software\Houdini 21.0.671\bin\houdini.exe"
set HIP_FILE="C:\Users\yusuke.nakamura\Desktop\kiosk_test.hip"
set PYTHON_SCRIPT="C:\Users\yusuke.nakamura\Desktop\setup_kiosk.py"

start "" %EXE% -s tops %HIP_FILE% waitforui %PYTHON_SCRIPT%