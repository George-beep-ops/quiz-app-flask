# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 18:20:11 2025

@author: nilsc
"""

import qrcode

# 🔁 IP-Adresse deines Computers im lokalen WLAN:
# Ersetze diesen Link durch DEINE IP-Adresse:
local_ip = "http://192.168.0.189:5000"


img = qrcode.make(local_ip)
img.save("qr_test.png")
print(f"QR-Code für {local_ip} wurde gespeichert als qr_test.png")
