# # Import QRCode from pyqrcode
# import pyqrcode
# import png
# from pyqrcode import QRCode
  
  
# # String which represents the QR code
# # s = "https://docs.google.com/forms/d/e/1FAIpQLSc7aJrdEoyUPFzBCM3B8uryB4KY9oXsPNK6oGXtAvqWW2-ZTA/viewform?usp=sf_link"
# s = "https://docs.google.com/forms/d/e/1FAIpQLSd10dMAGlEzbQ-uF_c5Jm7Th00NgU6ULxG35i4BI_NYNDGwjA/viewform?usp=sf_link"
  
# # Generate QR code
# url = pyqrcode.create(s)
  
# # Create and save the svg file naming "myqr.svg"
# url.svg("myqr.svg", scale = 8)
  
# # Create and save the png file naming "myqr.png"
# url.png('myqr.png', scale = 6)

# import gspread
# import pandas as pd
# from oauth2client.service_account import ServiceAccountCredentials
# # connect to gcloud
# scopes = [
# "https://www.googleapis.com/auth/spreadsheets",
# "https://www.googleapis.com/auth/drive",
# "https://spreadsheets.google.com/feeds",
# "https://www.googleapis.com/auth/drive.file"
# ]
# # get credentials
# credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)    # access the json key you downloaded earlier

# client = gspread.authorize(credentials)          # authenticate the JSON key with gspread
# sheet = client.open("Feedback").sheet1           # open sheet 
# all_data = sheet.get_all_records()
# df = pd.DataFrame(all_data)
# print(df)