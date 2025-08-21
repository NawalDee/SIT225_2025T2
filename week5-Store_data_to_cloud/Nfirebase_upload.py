import serial
import time
import firebase_admin
from firebase_admin import credentials, db

# Firebase setup
cred = credentials.Certificate(
    r"C:\Users\jalmi\OneDrive\Desktop\w5N\sit225n-firebase-adminsdk-fbsvc-85b5c435df.json"
)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sit225n-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('gyro_data')

# Arduino setup
ser = serial.Serial('COM5', 9600)
time.sleep(2)

print("Uploading data to Firebase...")

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        try:
            x, y, z = line.split(",")
            data = {
                "timestamp": time.time(),
                "x": float(x),
                "y": float(y),
                "z": float(z)
            }
            ref.push(data)
            print("Uploaded:", data)
        except:
            print("Invalid line:", line)
