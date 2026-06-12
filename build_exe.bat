@echo off
set ICON_PATH=gui\logo.png
set MAGIKA_PATH=venv\Lib\site-packages\magika

:: Google API ve diger agir kutuphaneleri cikariyoruz.
:: Bu kutuphaneler markitdown'in Google Drive/Bing destegi icin gerekli ama biz kullanmiyoruz.
.\venv\Scripts\pyinstaller --noconsole --onefile ^
    --icon=%ICON_PATH% ^
    --add-data "gui;gui" ^
    --add-data "%MAGIKA_PATH%;magika" ^
    --exclude-module googleapiclient ^
    --exclude-module google_auth_oauthlib ^
    --exclude-module google ^
    --exclude-module oauth2client ^
    --exclude-module openai ^
    --exclude-module matplotlib ^
    --exclude-module networkx ^
    --exclude-module notebook ^
    --exclude-module jedi ^
    --name "MarkItDownDesktop" ^
    gui\markitdown_gui.py

echo.
echo Ultra Optimize edilmis Build tamamlandi!
pause
