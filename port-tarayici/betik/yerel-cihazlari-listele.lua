function cihazlari_listele()
    print("Ağınızdaki cihazlar taranıyor...")

    local komut = "ip neigh | awk '$5 != \"\" {print $1, $5}' > cihazlar.txt"
    os.execute(komut)

    local dosya = io.open("cihazlar.txt", "r")
    if not dosya then
        print("Çıktı dosyası açılamadı.")
        return
    end

    print("\nTespit edilen IP ve MAC adresleri:")
    for line in dosya:lines() do
        if line ~= "" then
            local ip, mac = line:match("([^ ]+) ([^ ]+)")
            if ip and mac then
                print(string.format("IP: %s MAC: %s", ip, mac))
            end
        end
    end
    dosya:close()

    -- Geçici dosyayı sil
    os.remove("cihazlar.txt")
end

function main()
    cihazlari_listele()
end

main()
