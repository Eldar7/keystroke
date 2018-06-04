https://github.com/mhammond/pywin32/releases
reg add HKLM\SOFTWARE\Python\PythonCore\3.5\InstallPath /ve /t REG_SZ /d "C:\ProgramData\Anaconda3" /f
Перед установкой остановить все юпитер и питон процессы на компе



https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook
Python 3.5.4 :: Anaconda custom (64-bit)
Возникает ошибка на Win7:
TypeError: KeyboardSwitch() missing 8 required positional arguments: 'msg', 'vk_code', 'scan_code', 'ascii', 'flags', 'time', 'hwnd', and 'win_name'

Python 3.6.5 - same shit

Python 3.4 - мистический способ исправления установки

c:\Soft\Python34\Scripts\pip.exe install pyHook-1.5.1-cp34-cp34m-win_amd64.whl
pyHook-1.5.1-cp34-cp34m-win_amd64.whl is not a supported wheel on this platform.

https://stackoverflow.com/a/46889002/2436590

c:\Soft\Python34\Scripts\pip.exe install pyHook-1.5.1-cp34-none-win_amd64.whl
Processing .\pyhook-1.5.1-cp34-none-win_amd64.whl
Installing collected packages: pyHook
Successfully installed pyHook-1.5.1