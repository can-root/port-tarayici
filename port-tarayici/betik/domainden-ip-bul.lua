function ip_bul(url)
    if not url:match("^http://") and not url:match("^https://") then
        url = "http://" .. url
    end

    print("Web sitesi için IP adresi aranıyor: " .. url)

    local domain = url:match("://(.-)/") or url:match("://(.*)")

    local komut = "ping -c 1 " .. domain .. " | grep 'PING' | awk -F' ' '{print $3}' | tr -d '()' > ip_sonucu.txt"
    os.execute(komut)

    local dosya = io.open("ip_sonucu.txt", "r")
    if not dosya then
        print("IP adresi bulunamadı.")
        return
    end

    local ip_adres = dosya:read("*l")
    dosya:close()
    os.remove("ip_sonucu.txt")

    if ip_adres and ip_adres ~= "" then
        print(string.format("Web sitesi: %s, IP Adresi: %s", url, ip_adres))
    else
        print("IP adresi bulunamadı.")
    end
end

function main()
    io.write("IP adresi bulunacak web sitesinin URL'sini girin: ")
    local url = io.read()
    ip_bul(url)
end

main()
