#!/bin/bash

# Python3, Lua ve LuaRocks yükleme
echo "Python3, Lua ve LuaRocks yükleniyor..."
sudo apt update
sudo apt install -y python3 lua5.3 luarocks

# Lua için gerekli kütüphaneleri yükle
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
