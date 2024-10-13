import os
import subprocess
import colorama
from colorama import Fore, Style

def lua_kutuphanesini_kontrol_et(kutuphane):
    try:
        lua = subprocess.run(['lua', '-e', f'require("{kutuphane}")'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def lua_dosyalarını_listele(dizin):
    lua_dosyaları = [f for f in os.listdir(dizin) if f.endswith('.lua')]
    return lua_dosyaları

def kutuphane_yukle(kutuphane):
    print(Fore.YELLOW + f"{kutuphane} kütüphanesi eksik. Yükleniyor..." + Style.RESET_ALL)
    try:
        subprocess.run(['luarocks', 'install', kutuphane], check=True)
        print(Fore.GREEN + f"{kutuphane} kütüphanesi başarıyla yüklendi." + Style.RESET_ALL)
    except subprocess.CalledProcessError:
        print(Fore.RED + f"{kutuphane} kütüphanesi yüklenirken bir hata oluştu." + Style.RESET_ALL)

def lua_dosyası_yürüt(file_path):
    print(Fore.BLUE + f"{file_path} dosyası yürütülüyor..." + Style.RESET_ALL)
    try:
        subprocess.run(['lua', file_path], check=True)
        print(Fore.GREEN + "Yürütme tamamlandı." + Style.RESET_ALL)
    except subprocess.CalledProcessError:
        print(Fore.RED + "Betik yürütülürken bir hata oluştu." + Style.RESET_ALL)

def ana():
    dizin = "betik"
    kutuphaneler = ["dkjson"]  # Kontrol edilecek kütüphaneler listesi

    lua_dosyaları = lua_dosyalarını_listele(dizin)

    if not lua_dosyaları:
        print(Fore.RED + "Klasörde hiç Lua dosyası bulunamadı." + Style.RESET_ALL)
        return

    print(Fore.GREEN + "Lua dosyaları:" + Style.RESET_ALL)
    for index, lua_dosyası in enumerate(lua_dosyaları):
        print(f"{Fore.CYAN}{index + 1}: {lua_dosyası}{Style.RESET_ALL}")

    seçim = input(Fore.YELLOW + "Hangi dosyayı yürütmek istersiniz? (numara girin): " + Style.RESET_ALL)

    try:
        seçim_indeksi = int(seçim) - 1
        if 0 <= seçim_indeksi < len(lua_dosyaları):
            dosya_yolu = os.path.join(dizin, lua_dosyaları[seçim_indeksi])

            # Lua betiğini okumak için gerekli kütüphaneleri kontrol et
            for kutuphane in kutuphaneler:
                if not lua_kutuphanesini_kontrol_et(kutuphane):
                    kutuphane_yukle(kutuphane)  # Eksik kütüphane yükle

            lua_dosyası_yürüt(dosya_yolu)  # Lua betiğini çalıştır
        else:
            print(Fore.RED + "Geçersiz seçim." + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "Lütfen geçerli bir sayı girin." + Style.RESET_ALL)

if __name__ == "__main__":
    colorama.init(autoreset=True)
    ana()
