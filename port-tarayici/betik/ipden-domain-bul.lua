function domain_bul(ip)
    print("IP adresi için alan adı aranıyor: " .. ip)

    local komut = "curl -s 'https://api.hackertarget.com/reverseiplookup/?q=" .. ip .. "' > domain_sonucu.txt"
    os.execute(komut)

    local dosya = io.open("domain_sonucu.txt", "r")
    if not dosya then
        print("Alan adı bulunamadı.")
        return
    end

    local domain_adresi = dosya:read("*l")
    dosya:close()
    os.remove("domain_sonucu.txt")

    if domain_adresi and domain_adresi ~= "" then
        print(string.format("IP Adresi: %s, Alan Adı: %s", ip, domain_adresi))
    else
        print("Alan adı bulunamadı.")
    end
end

function main()
    io.write("Alan adı bulunacak IP adresini girin: ")
    local ip = io.read()
    domain_bul(ip)
end

main()
