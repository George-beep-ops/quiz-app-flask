# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 19:48:20 2025

@author: nilsc
"""

import qrcode

url = "https://quiz-app-flask.onrender.com"  # DEINE Render-URL hier einfügen

img = qrcode.make(url)
img.save("qr_online.png")
print("QR-Code gespeichert als 'qr_online.png'")
