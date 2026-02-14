@echo off
REM =========================================================================
REM League of Kingdoms Crystal Bot - Windows Baslat Scripti
REM =========================================================================
REM Bu script botu Windows ortaminda baslatir
REM =========================================================================

echo.
echo =========================================================================
echo  League of Kingdoms Crystal Bot v1.0.0
echo =========================================================================
echo.

REM Python kontrolu
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo HATA: Python bulunamadi!
    echo Lutfen once setup.bat dosyasini calistirin.
    pause
    exit /b 1
)

REM Sanal ortam varsa etkinlestir
if exist venv\Scripts\activate.bat (
    echo Sanal ortam etkinlestiriliyor...
    call venv\Scripts\activate.bat
    echo.
)

REM Gerekli klasorleri kontrol et
if not exist logs mkdir logs
if not exist data mkdir data

REM Bot'u baslatmak icin onay al
echo Bot baslatilacak...
echo.
echo UYARI: 
echo - Oyun ayarlarini config/settings.py dosyasindan kontrol edin
echo - Ilk kez kullaniyorsaniz test modu ile baslatin:
echo     start.bat --dry-run --debug --max-time 30 --no-confirm
echo - Otomatik mod icin --no-confirm parametresini kullanin
echo.

REM Parametreler varsa direkt baslat, yoksa kullaniciya sor
if "%1"=="" (
    set /p confirm="Devam etmek istiyor musunuz? (E/H): "
    if /i not "%confirm%"=="E" (
        if /i not "%confirm%"=="e" (
            echo Iptal edildi.
            pause
            exit /b 0
        )
    )
    echo.
    echo Bot baslatiliyor...
    echo.
    python src/main.py
) else (
    echo Bot parametrelerle baslatiliyor: %*
    echo.
    python src/main.py %*
)

REM Hata kontrolu
if %errorlevel% neq 0 (
    echo.
    echo HATA: Bot calisirken bir hata olustu!
    echo Lutfen logs/crystal_bot.log dosyasini kontrol edin.
    echo.
    echo Yardim icin:
    echo   start.bat --help
    echo.
    pause
    exit /b 1
)

echo.
echo Bot durduruldu.
echo.
pause
