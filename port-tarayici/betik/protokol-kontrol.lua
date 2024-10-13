local socket = require("socket")
local io = require("io")
local os = require("os")

local function ping_ip(ip)
    local result = os.execute(command)
    return result == 0
end

local function check_tcp(ip, port)
    local tcp_socket = socket.tcp()
    tcp_socket:settimeout(1)  -- Timeout süresi
    local result, err = tcp_socket:connect(ip, port)
    tcp_socket:close()
    return result ~= nil
end

local function check_udp(ip, port)
    local udp_socket = socket.udp()
    udp_socket:settimeout(1)  -- Timeout süresi
    local result, err = udp_socket:sendto("", ip, port)

    if not result then
        udp_socket:close()
        return false
    end

    local response, err = udp_socket:receive()
    udp_socket:close()

    return response ~= nil
end

local function check_protocols(ip, tcp_ports, udp_ports)
    local protocols = {}

    -- ICMP Kontrolü
    if ping_ip(ip) then
        table.insert(protocols, "ICMP: Açık")
    else
        table.insert(protocols, "ICMP: Kapalı")
    end

    -- TCP Kontrolleri
    for _, port in ipairs(tcp_ports) do
        if check_tcp(ip, port) then
            table.insert(protocols, "TCP Port " .. port .. ": Bağlantı Var")
        else
            table.insert(protocols, "TCP Port " .. port .. ": Bağlantı Yok")
        end
    end

    -- UDP Kontrolleri
    for _, port in ipairs(udp_ports) do
        if check_udp(ip, port) then
            table.insert(protocols, "UDP Port " .. port .. ": Açık (Yanıt Alındı)")
        else
            local icmp_response = ping_ip(ip)
            if icmp_response then
                table.insert(protocols, "UDP Port " .. port .. ": Kapalı (ICMP Yanıt Alındı)")
            else
                table.insert(protocols, "UDP Port " .. port .. ": Filtrelenmiş/Açık (Yanıt Alınmadı)")
            end
        end
    end

    return protocols
end

io.write("Bir IP adresi girin: ")
local target_ip = io.read()

io.write("TCP portlarını (virgül ile ayırarak) girin: ")
local tcp_ports_input = io.read()
local tcp_ports = {}
for port in string.gmatch(tcp_ports_input, "%d+") do
    table.insert(tcp_ports, tonumber(port))
end

io.write("UDP portlarını (virgül ile ayırarak) girin: ")
local udp_ports_input = io.read()
local udp_ports = {}
for port in string.gmatch(udp_ports_input, "%d+") do
    table.insert(udp_ports, tonumber(port))
end

local supported_protocols = check_protocols(target_ip, tcp_ports, udp_ports)

print("Desteklenen Protokoller:")
for _, protocol in ipairs(supported_protocols) do
    print(protocol)
end
