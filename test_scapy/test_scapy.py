from scapy.all import *
from scapy.layers.l2 import Ether
import functools # 匯入 functools
import sys # 用於 sys.exit
from datetime import datetime, timezone, timedelta # 匯入 datetime 相關模組

# 定義目標介面的 IP 位址
TARGET_INTERFACE_IP = "192.168.200.1"
# 定義抓取 LLDP 封包的目標數量
TARGET_LLDP_COUNT = 3

# 全域變數，用於計算已抓取到的 LLDP 封包數量
lldp_packet_count = 0

def find_interface_by_ip(target_ip):
    """
    搜尋具有指定 IP 位址的網路介面。
    如果找到則返回介面名稱，否則返回 None。
    """
    search_msg = f"正在搜尋 IP 位址為 {target_ip} 的網路介面..."
    try:
        console_encoding = sys.stdout.encoding or 'utf-8'
        print(search_msg.encode('utf-8', errors='replace').decode(console_encoding, errors='replace'))
    except Exception:
        print(search_msg.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))

    available_interfaces_info = []
    for iface_candidate in get_if_list():
        try:
            ip_addr = get_if_addr(iface_candidate)
            available_interfaces_info.append({'name': iface_candidate, 'ip': ip_addr})
            if ip_addr == target_ip:
                found_msg = f"已找到目標介面: {iface_candidate} (IP: {ip_addr})"
                try:
                    console_encoding = sys.stdout.encoding or 'utf-8'
                    print(found_msg.encode('utf-8', errors='replace').decode(console_encoding, errors='replace'))
                except Exception:
                    print(found_msg.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
                return iface_candidate
        except Exception:
            available_interfaces_info.append({'name': iface_candidate, 'ip': 'N/A 或無法取得'})
            pass # 忽略獲取 IP 時出錯的介面
    
    not_found_msg = f"未找到 IP 位址為 {target_ip} 的介面。"
    print(not_found_msg.encode('utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8', errors='replace'))
    if available_interfaces_info:
        print("可用的網路介面:")
        for if_info in available_interfaces_info:
            print(f"  - {if_info['name']}: {if_info['ip']}")
    else:
        print("未找到任何網路介面。")
    return None

def parse_lldp(pkt):
    global lldp_packet_count # 宣告使用全域變數
    output_lines = []
    if pkt.haslayer(Ether) and pkt.type == 0x88cc:  # LLDP EtherType
        lldp_packet_count += 1 # 遞增已抓取的 LLDP 封包計數
        # 獲取 UTC+8 時間
        utc_plus_8 = timezone(timedelta(hours=8))
        current_time_utc8 = datetime.now(utc_plus_8).strftime("%Y-%m-%d %H:%M:%S %Z%z")
        output_lines.append(f"Timestamp (UTC+8): {current_time_utc8}")
        output_lines.append(f"LLDP Packet Captured ({lldp_packet_count}/{TARGET_LLDP_COUNT})") # 顯示計數
        raw = bytes(pkt.payload)

        index = 0
        while index < len(raw):
            if index + 2 > len(raw):
                break
            tlv_header = raw[index:index+2]
            tlv_type = tlv_header[0] >> 1
            tlv_len = ((tlv_header[0] & 0x01) << 8) | tlv_header[1]
            value = raw[index+2:index+2+tlv_len]

            if tlv_type == 0:
                output_lines.append("End of LLDPDU")
                break
            elif tlv_type == 1:
                subtype = value[0]
                mac = ':'.join(f"{b:02x}" for b in value[1:])
                output_lines.append(f"Chassis ID (MAC): {mac}")
            elif tlv_type == 2:
                subtype = value[0]
                port_id = value[1:].decode(errors="ignore")
                output_lines.append(f"Port ID: {port_id}")
            elif tlv_type == 5:
                name = value.decode(errors="ignore")
                output_lines.append(f"System Name: {name}")
            elif tlv_type == 6:
                desc = value.decode(errors="ignore")
                output_lines.append(f"System Description: {desc}")
            elif tlv_type == 8: # 管理位址 TLV
                ip_addr_val = ".".join(str(b) for b in value[-4:]) # 修改變數名稱以避免衝突
                output_lines.append(f"Management IP: {ip_addr_val}")
            elif tlv_type == 127:
                oui = value[:3]
                subtype = value[3]
                if oui == b'\x00\x12\xbb':  # MED OUI for LLDP-MED
                    med_subtype = value[4]
                    med_value = value[5:].decode(errors="ignore")
                    if med_subtype == 6:
                        output_lines.append(f"Firmware: {med_value}")
                    elif med_subtype == 8:
                        output_lines.append(f"Serial Number: {med_value}")
                    elif med_subtype == 9:
                        output_lines.append(f"Manufacturer: {med_value}")
                    elif med_subtype == 10:
                        output_lines.append(f"Model: {med_value}")

            index += 2 + tlv_len
        
        # 同時輸出到控制台和日誌檔案
        for line in output_lines:
            print(line)
        print("-" * 20) # 新增分隔線以便閱讀

def stop_sniffing_filter(pkt):
    """
    停止 sniff 的過濾器函式。
    當抓取到指定數量的 LLDP 封包後返回 True。
    """
    global lldp_packet_count
    if lldp_packet_count >= TARGET_LLDP_COUNT:
        return True
    return False

if __name__ == "__main__":
    # 檢查是否有提供命令列參數
    if len(sys.argv) > 1:
        TARGET_INTERFACE_IP = sys.argv[1]  # 使用第一個參數作為目標 IP 位址
        print(f"使用命令列參數指定的目標 IP 位址: {TARGET_INTERFACE_IP}")
    # 自動搜尋並設定網路介面
    iface_name = find_interface_by_ip(TARGET_INTERFACE_IP)

    if iface_name is None:
        print(f"錯誤: 無法自動找到 IP 位址為 {TARGET_INTERFACE_IP} 的網路介面。")
        print("請檢查您的網路設定，或在腳本中手動指定介面名稱。")
        sys.exit(1)

    print(f"Start sniffing LLDP packets (target: {TARGET_LLDP_COUNT} packets)...")
    sniff(iface=iface_name, filter="ether proto 0x88cc", prn=parse_lldp, store=0, stop_filter=stop_sniffing_filter)

    print(f"LLDP sniffing complete. Captured {lldp_packet_count} packets.")
