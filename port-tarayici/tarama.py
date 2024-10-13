import socket
import struct
import json
from colorama import Fore, Style, init
init(autoreset=True)
def portları_yükle():
    try:
        with open('portlar.json', 'r') as dosya:
            return json.load(dosya)
    except Exception as e:
        print(Fore.RED + f"JSON dosyası okunurken hata oluştu: {e}" + Style.RESET_ALL)
        return {}

def servis_adı(port, hizmetler):
    return hizmetler.get(str(port), "Bilinmiyor")
def logo():
    print(f"""{Fore.GREEN}

                              ..... ..
                          ..::XXX XXXXX:...
                        XXXXXXXXXXXXXXXXXXXXX::
                     XXXXX:XXXXXXX:XXXXXXX:XXXXX::
                    ..:IXX::XXXXXX:XXXX::.:':XXXX::
                  ..::::XX:XXXXXX:XXXX:'::':XXXXX::
                  ...:X'.'XXXXXXXXX.XXXXXXXXXXXX'XXX:
                 ....:X.:XXXXXXXXXXXXXXXXXXXXXX:'XXXX
                 ....'X.XXXXXXXXXXXXXXXXX''''' :XXXXXX
                 ...:::....'''''''''''''       :XXXXXXX
                 :..::.....                    :'XXXXX
                  .:::....                     .:XXXXX
                   ::''''                      .:XXXXX
                   .      ....,,      ......    :XXXXX
                    .::'   XXX   ::'   ''':  .XXXX:
                 :.:   :::'MM'''X    .:'MM '.    'X''.
                 ::'     I:..:.:X     .'''.'     .::'
                 ::XI          XI                :::
                  :XX         XI                .::''
                  :X' .:.     /X.              .:::
                  '''....    /XXX.:XX.         ...:
                   ':....    '::''            ...:
                    ':...                      ...
                     :....  :..:II:II:..:     ...
                     ':....  ::.              ..:::
                      ':...   '''''''         .::::
                       .:...               . ..::::
                   ....:::.:...         .:::::'.XXXX::::....
          .....:::XXXXXXXX::::::......:::::'   .XXXXXXXIMMM::
     .::XXXXXXXXXXXXXXXXXX:::::::::::::::'    .XXXXXXXXXMMMMMMM:
   .XXXXXXXXXXXXXXXXXXXXXX'::::::::::::'   .'.:XXXXXXXX:XXXXXXXXXX
  .XXXXXXXXXXXXXXXXXXXXXXX '::::::::::'  .' .XXXXXXXXXX:MMMMMMMMMMM
 .XXXXXXXXXXXXXXXXXXXXXXXX  ':::::::' .'   .XXXXXXXXXXX:MMMMMMMMMMM
.XXXXXXXXXXXXXXXXXXXXXXXXX   ':::::'.'    .XXXXXXXXXXXX:MMMMMMMMMMM
XXXXXXXXXXXXXXXXXXXXXXXXXX   .'WWWW.     .XXXXXXXXXXXXXX'MMMMMMMMMM
XXXXXXXXXXXXXXXXXXXXXXXXX.  .:WWWWWW    .XXXXXXXXXXXXXXX:MMMMMMMMMM
XXXXXXXXXXXXXXXXXXXXXXXXX.  .:WWWW' '   .XXXXXXXXXXXXXXX:MMMMMMMMMM
XXXXXXXXXXXXXXXXXXXXXXXXX  : 'WW'    '  XXXXXXXXXXXXXXXXX.MMMMMMMMM
XXXXXXXXXXXXXXXXXXXXXXXX' :.WWWW'     .XXXXXXXXXXXXXXXXX'MMMMMMMMMM
XXXXXXXXXXXXXXXXXXXXXXXX...WWWWWW....XXXXXXXXXXXXXXXXXXXXMMMMMMMMMM


""")
def tcp_bağlantı_tarama(hedef, portlar, hizmetler):
    print(Fore.BLUE + "TCP Bağlantı Tarama başlatılıyor..." + Style.RESET_ALL)
    print(Fore.BLUE + "{:<10} {:<10} {}".format("Port", "Durum", "Servis") + Style.RESET_ALL)
    for port in portlar:
        try:
            soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soket.settimeout(5)
            sonuç = soket.connect_ex((hedef, port))
            durum = "Açık" if sonuç == 0 else "Kapalı"
            hizmet = servis_adı(port, hizmetler)
            print(Fore.BLUE + "{:<10} {:<10} {}".format(port, durum, hizmet) + Style.RESET_ALL)
        except BrokenPipeError:
            print(Fore.BLUE + "{:<10} {:<10} {}".format(port, "Filtrelenmiş", "Bilinmiyor") + Style.RESET_ALL)
        except Exception as e:
            print(Fore.BLUE + f"Port {port} kontrol edilirken hata oluştu: {e}" + Style.RESET_ALL)
        finally:
            soket.close()

def tcp_syn_tarama(hedef, portlar, hizmetler):
    print(Fore.GREEN + "SYN Tarama başlatılıyor..." + Style.RESET_ALL)
    print(Fore.GREEN + "{:<10} {:<10} {}".format("Port", "Durum", "Servis") + Style.RESET_ALL)
    for port in portlar:
        try:
            soket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            soket.settimeout(5)

            ip_başlığı = struct.pack('!BBHHHBBH4s4s',
                                    69, 0, 40, 54321, 0, 255, socket.IPPROTO_TCP, 0,
                                    socket.inet_aton("0.0.0.0"), socket.inet_aton(hedef))
            tcp_başlığı = struct.pack('!HHLLBBHHH',
                                     12345, port, 0, 0, (5 << 4) | 0x02, 0, socket.htons(8192), 0, 37837)
            paket = ip_başlığı + tcp_başlığı

            soket.sendto(paket, (hedef, port))
            cevap = soket.recv(1024)
            durum = "Açık (SYN Yanıtı)" if cevap else "Kapalı"
            hizmet = servis_adı(port, hizmetler)
            print(Fore.GREEN + "{:<10} {:<10} {}".format(port, durum, hizmet) + Style.RESET_ALL)

        except socket.timeout:
            print(Fore.GREEN + "{:<10} {:<10} {}".format(port, "Filtrelenmiş", "Bilinmiyor") + Style.RESET_ALL)
        except BrokenPipeError:
            print(Fore.GREEN + "{:<10} {:<10} {}".format(port, "Filtrelenmiş", "Bilinmiyor") + Style.RESET_ALL)
        except Exception as e:
            print(Fore.GREEN + f"Port {port} kontrol edilirken hata oluştu: {e}" + Style.RESET_ALL)
        finally:
            soket.close()

def tcp_null_tarama(hedef, portlar, hizmetler):
    print(Fore.YELLOW + "NULL Tarama başlatılıyor..." + Style.RESET_ALL)
    print(Fore.YELLOW + "{:<10} {:<10} {}".format("Port", "Durum", "Servis") + Style.RESET_ALL)
    for port in portlar:
        try:
            soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soket.settimeout(5)
            soket.sendto(b'', (hedef, port))
            cevap = soket.recv(1024)
            hizmet = servis_adı(port, hizmetler)
            print(Fore.YELLOW + "{:<10} {:<10} {}".format(port, "Açık/Filtrelenmiş", hizmet) + Style.RESET_ALL)
        except socket.timeout:
            print(Fore.YELLOW + "{:<10} {:<10} {}".format(port, "Filtrelenmiş", "Bilinmiyor") + Style.RESET_ALL)
        except BrokenPipeError:
            print(Fore.YELLOW + "{:<10} {:<10} {}".format(port, "Filtrelenmiş", "Bilinmiyor") + Style.RESET_ALL)
        except Exception as e:
            print(Fore.YELLOW + f"Port {port} kontrol edilirken hata oluştu: {e}" + Style.RESET_ALL)
        finally:
            soket.close()

def tcp_fin_tarama(hedef, portlar, hizmetler):
    print(Fore.CYAN + "FIN Tarama başlatılıyor..." + Style.RESET_ALL)
    print(Fore.CYAN + "{:<10} {:<10} {}".format("Port", "Durum", "Servis") + Style.RESET_ALL)
    for port in portlar:
        try:
            soket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            soket.settimeout(5)
            tcp_başlığı = struct.pack('!HHLLBBHHH',
                                     12345, port, 0, 0, 1 << 4, 0, socket.htons(8192), 0, 545)
            soket.sendto(tcp_başlığı, (hedef, port))
            cevap = soket.recv(1024)
            hizmet = servis_adı(port, hizmetler)
            print(Fore.CYAN + "{:<10} {:<10} {}".format(port, "Açık/Filtrelenmiş", hizmet) + Style.RESET_ALL)
        except socket.timeout:
            print(Fore.CYAN + "{:<10} {:<10} {}".format(port, "Filtrelenmiş", "Bilinmiyor") + Style.RESET_ALL)
        except BrokenPipeError:
            print(Fore.CYAN + "{:<10} {:<10} {}".format(port, "Filtrelenmiş", "Bilinmiyor") + Style.RESET_ALL)
        except Exception as e:
            print(Fore.CYAN + f"Port {port} kontrol edilirken hata oluştu: {e}" + Style.RESET_ALL)
        finally:
            soket.close()

def tcp_xmas_tarama(hedef, portlar, hizmetler):
    print(Fore.MAGENTA + "Xmas Tarama başlatılıyor..." + Style.RESET_ALL)
    print(Fore.MAGENTA + "{:<10} {:<10} {}".format("Port", "Durum", "Servis") + Style.RESET_ALL)
    for port in portlar:
        try:
            soket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            soket.settimeout(5)
            tcp_başlığı = struct.pack('!HHLLBBHHH',
                                     12345, port, 0, 0, 0x29, 0, socket.htons(8192), 0, 377)
            soket.sendto(tcp_başlığı, (hedef, port))
            cevap = soket.recv(1024)
            hizmet = servis_adı(port, hizmetler)
            print(Fore.MAGENTA + "{:<10} {:<10} {}".format(port, "Açık/Filtrelenmiş", hizmet) + Style.RESET_ALL)
        except socket.timeout:
            print(Fore.MAGENTA + "{:<10} {:<10} {}".format(port, "Filtrelenmiş", "Bilinmiyor") + Style.RESET_ALL)
        except BrokenPipeError:
            print(Fore.MAGENTA + "{:<10} {:<10} {}".format(port, "Filtrelenmiş", "Bilinmiyor") + Style.RESET_ALL)
        except Exception as e:
            print(Fore.MAGENTA + f"Port {port} kontrol edilirken hata oluştu: {e}" + Style.RESET_ALL)
        finally:
            soket.close()

def tcp_ack_tarama(hedef, portlar, hizmetler):
    print(Fore.RED + "ACK Tarama başlatılıyor..." + Style.RESET_ALL)
    print(Fore.RED + "{:<10} {:<10} {}".format("Port", "Durum", "Servis") + Style.RESET_ALL)
    for port in portlar:
        try:
            soket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            soket.settimeout(5)
            tcp_başlığı = struct.pack('!HHLLBBHHH',
                                     12345, port, 0, 0, 0x10, 0, socket.htons(8192), 0, 888)
            soket.sendto(tcp_başlığı, (hedef, port))
            cevap = soket.recv(1024)
            hizmet = servis_adı(port, hizmetler)
            print(Fore.RED + "{:<10} {:<10} {}".format(port, "Açık/Filtrelenmiş", hizmet) + Style.RESET_ALL)
        except socket.timeout:
            print(Fore.RED + "{:<10} {:<10} {}".format(port, "Filtrelenmiş", "Bilinmiyor") + Style.RESET_ALL)
        except BrokenPipeError:
            print(Fore.RED + "{:<10} {:<10} {}".format(port, "Filtrelenmiş", "Bilinmiyor") + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"Port {port} kontrol edilirken hata oluştu: {e}" + Style.RESET_ALL)
        finally:
            soket.close()

def udp_tarama(hedef, portlar, hizmetler):
    print(Fore.YELLOW + "UDP Tarama başlatılıyor..." + Style.RESET_ALL)
    print(Fore.YELLOW + "{:<10} {:<10} {}".format("Port", "Durum", "Servis") + Style.RESET_ALL)
    for port in portlar:
        try:
            soket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            soket.settimeout(5)
            soket.sendto(b'', (hedef, port))
            cevap = soket.recv(1024)
            hizmet = servis_adı(port, hizmetler)
            print(Fore.YELLOW + "{:<10} {:<10} {}".format(port, "Açık (UDP yanıtı)", hizmet) + Style.RESET_ALL)
        except socket.timeout:
            print(Fore.YELLOW + "{:<10} {:<10} {}".format(port, "Filtrelenmiş/Açık", "Bilinmiyor") + Style.RESET_ALL)
        except OSError as e:
            if e.errno == 10054:  # Bağlantı sıfırlandıysa
                print(Fore.YELLOW + "{:<10} {:<10} {}".format(port, "Kapalı (ICMP Yanıtı)", "Bilinmiyor") + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f"Port {port} kontrol edilirken hata oluştu: {e}" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.YELLOW + f"Port {port} kontrol edilirken hata oluştu: {e}" + Style.RESET_ALL)
        finally:
            soket.close()

def ana():
    ip = input("Tarama yapılacak IP adresini girin: ")
    portlar = input("Tarama yapılacak portları girin (virgülle ayırarak): ")
    portlar = [int(p.strip()) for p in portlar.split(",")]

    hizmetler = portları_yükle()

    print("Tarama yöntemlerini seçin:")
    print("1: TCP Bağlantı Tarama")
    print("2: SYN Tarama")
    print("3: NULL Tarama")
    print("4: FIN Tarama")
    print("5: Xmas Tarama")
    print("6: ACK Tarama")
    print("7: UDP Tarama")

    tarama_seçimi = input("Seçenekleri rakamlarla girin (örneğin: 1,2,3): ").strip()
    seçilen_taramalar = tarama_seçimi.split(",")

    for tarama in seçilen_taramalar:
        if tarama.strip() == "1":
            tcp_bağlantı_tarama(ip, portlar, hizmetler)
        elif tarama.strip() == "2":
            tcp_syn_tarama(ip, portlar, hizmetler)
        elif tarama.strip() == "3":
            tcp_null_tarama(ip, portlar, hizmetler)
        elif tarama.strip() == "4":
            tcp_fin_tarama(ip, portlar, hizmetler)
        elif tarama.strip() == "5":
            tcp_xmas_tarama(ip, portlar, hizmetler)
        elif tarama.strip() == "6":
            tcp_ack_tarama(ip, portlar, hizmetler)
        elif tarama.strip() == "7":
            udp_tarama(ip, portlar, hizmetler)
        else:
            print(Fore.RED + "Geçersiz seçenek: " + tarama.strip() + Style.RESET_ALL)

if __name__ == "__main__":
    logo()
    ana()
