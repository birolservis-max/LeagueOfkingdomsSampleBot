@echo off
REM =========================================================================
REM League of Kingdoms Crystal Bot - Windows Kurulum Scripti
REM =========================================================================
REM Bu script Windows ortaminda botu kurmak icin gerekli tum adimlari yapar
REM =========================================================================

echo.
echo =========================================================================
echo  League of Kingdoms Crystal Bot - Kurulum Basladi
echo =========================================================================
echo.

REM Python versiyonunu kontrol et
echo [1/6] Python versiyonu kontrol ediliyor...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo HATA: Python bulunamadi!
    echo Lutfen Python 3.9 veya uzeri yukleyin: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo Python basariyla bulundu!
echo.

REM pip versiyonunu kontrol et
echo [2/6] pip kontrol ediliyor...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo HATA: pip bulunamadi!
    echo pip yuklemek icin: python -m ensurepip --upgrade
    pause
    exit /b 1
)

python -m pip --version
echo pip basariyla bulundu!
echo.

REM pip'i guncelle
echo [3/6] pip guncelleniyor...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo UYARI: pip guncellenirken hata olustu, devam ediliyor...
)
echo.

REM Sanal ortam olustur (opsiyonel ama onerilir)
echo [4/6] Sanal ortam olusturuluyor (venv)...
if exist venv (
    echo Sanal ortam zaten mevcut, atlanıyor...
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo UYARI: Sanal ortam olusturulamadi, ana Python kullanilacak...
    ) else (
        echo Sanal ortam basariyla olusturuldu!
    )
)
echo.

REM Sanal ortami etkinlestir (varsa)
if exist venv\Scripts\activate.bat (
    echo Sanal ortam etkinlestiriliyor...
    call venv\Scripts\activate.bat
    echo Sanal ortam etkinlestirildi!
    echo.
)

REM Gerekli klasorleri olustur
echo [5/6] Gerekli klasorler olusturuluyor...
if not exist logs mkdir logs
if not exist data mkdir data
echo Klasorler hazir!
echo.

REM Bagimli paketleri yukle
echo [6/6] Gerekli Python paketleri yukleniyor...
echo Bu islem birkaç dakika surebilir, lutfen bekleyin...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo HATA: Paketler yuklenirken hata olustu!
    echo Lutfen internet baglantinizi kontrol edin ve tekrar deneyin.
    pause
    exit /b 1
)
echo.

REM Test calistir (opsiyonel)
echo.
echo =========================================================================
echo  Kurulum Tamamlandi!
echo =========================================================================
echo.
echo Bot basariyla kuruldu!
echo.
echo SONRAKI ADIMLAR:
echo.
echo 1. config/settings.py dosyasini duzenleyin
echo    - Oyun sunucu ayarlarini yapilandirin
echo    - Bildirim ayarlarini duzenleyin (Discord/Telegram)
echo    - Hedef kristal seviyelerini belirleyin
echo.
echo 2. Botu test modunda calistirin:
echo    start.bat --dry-run --debug
echo.
echo 3. Gercek modda baslatmak icin:
echo    start.bat
echo.
echo Daha fazla bilgi icin README.md ve QUICKSTART.md dosyalarini okuyun.
echo.
echo =========================================================================
echo.

pause
