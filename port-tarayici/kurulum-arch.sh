#!/bin/bash

echo "Python3, Lua ve LuaRocks yükleniyor..."
sudo pacman -S --noconfirm python lua luarocks

echo "Luasocket ve dkjson kütüphaneleri yükleniyor..."

luarocks install luasocket
if [ $? -eq 0 ]; then
    echo "Luasocket başarıyla yüklendi."
else
    echo "Luasocket yüklenirken bir hata oluştu."
fi

luarocks install dkjson
if [ $? -eq 0 ]; then
    echo "dkjson başarıyla yüklendi."
else
    echo "dkjson yüklenirken bir hata oluştu."
fi

echo "Yükleme işlemi tamamlandı."
