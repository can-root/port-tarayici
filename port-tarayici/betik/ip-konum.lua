local dkjson = require("dkjson")
local socket = require("socket")

local function get_ip_info(ip)
    local api_url = string.format("https://ipinfo.io/%s/json", ip)
    local handle = io.popen(string.format("curl -s '%s'", api_url))  -- API'ye istek yap
    local json_response = handle:read("*a")  -- Çıktıyı oku
    handle:close()

    if json_response == nil or json_response == "" then
        print("Geçersiz API yanıtı.")
        return
    end

    local data, pos, err = dkjson.decode(json_response, 1, nil)
    if err then
        print("JSON çözümleme hatası:", err)
        return
    end

    print("Şehir:", data.city or "Bilinmiyor")
    print("Ülke:", data.country or "Bilinmiyor")
    print("Enlem:", data.loc and data.loc:match("([^,]+)") or "Bilinmiyor")
    print("Boylam:", data.loc and data.loc:match(",([^,]+)") or "Bilinmiyor")
end

print("Bir IP adresi girin:")
local ip = io.read()
get_ip_info(ip)
