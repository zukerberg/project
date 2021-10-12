# Import QRCode from pyqrcode
import pyqrcode
import png
from pyqrcode import QRCode
  
  
# String which represents the QR code
# s = "https://docs.google.com/forms/d/e/1FAIpQLSc7aJrdEoyUPFzBCM3B8uryB4KY9oXsPNK6oGXtAvqWW2-ZTA/viewform?usp=sf_link"
s = "https://docs.google.com/forms/d/e/1FAIpQLSd10dMAGlEzbQ-uF_c5Jm7Th00NgU6ULxG35i4BI_NYNDGwjA/viewform?usp=sf_link"
  
# Generate QR code
url = pyqrcode.create(s)
  
# Create and save the svg file naming "myqr.svg"
url.svg("myqr.svg", scale = 8)
  
# Create and save the png file naming "myqr.png"
url.png('myqr.png', scale = 6)