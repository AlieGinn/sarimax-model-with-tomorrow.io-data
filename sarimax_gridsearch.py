import requests
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import itertools
from statsmodels.tsa.statespace.sarimax import SARIMAX

# API isteği gönderme
url = "https://api.tomorrow.io/v4/timelines?apikey=cyhpeemiXkGCX9ZjspxQk5He1AIWyLr5"

payload = {
    "location": "38.734802, 35.467987",
    "fields": ["temperature"],
    "units": "metric",
    "timesteps": ["1h"],
    "startTime": "now",
    "endTime": "nowPlus5d",
    "dailyStartHour": 6
}

headers = {
    "accept": "application/json",
    "Accept-Encoding": "deflate, gzip, br",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

# Yanıtı kontrol etme
if response.status_code == 200:
    data = response.json()

    # JSON verisinden sıcaklık değerlerini çekme
    timelines = data['data']['timelines']
    
    with open("temperature_data.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Tarih", "Sıcaklık (°C)"])  # Başlık satırı

        for timeline in timelines:
            for interval in timeline['intervals']:
                start_time = interval['startTime']
                temperature = interval['values']['temperature']
                writer.writerow([start_time, temperature])

    print("Veriler CSV dosyasına kaydedildi.")
else:
    print(f"Hata kodu: {response.status_code}")
    print("Hata mesajı:", response.text)
    exit()

# CSV'den veriyi yükleme ve uygun formatta saklama
veriler = []
with open("temperature_data.csv", mode="r", encoding="utf-8") as filee:
    reader = csv.reader(filee)
    next(reader)  # Başlık satırını atla
    for satir in reader:
        veriler.append(float(satir[1]))  # Sadece sıcaklık değerini al

veriler = np.array(veriler)  # ARIMA için numpy array formatına çevir

# Eğitim ve Test Verisini Ayırma
train_size = int(len(veriler) * 0.8)
train, test = veriler[:train_size], veriler[train_size:]

d = 0
S = 24

# Grid search için parametre aralıkları
p_values = range(0, 3)  # p için 0, 1, 2
q_values = range(0, 3)  # q için 0, 1, 2
P_values = range(0, 2)  # P için 0, 1
D_values = range(0, 2)  # D için 0, 1
Q_values = range(0, 2)  # Q için 0, 1

# Tüm kombinasyonları oluştur
param_combinations = itertools.product(p_values, q_values, P_values, D_values, Q_values)
combinations_with_fixed = [(p, d, q, P, D, Q, S) for p, q, P, D, Q in param_combinations]

# En iyi modeli bulmak için
best_aic = float("inf")
best_order = None
best_seasonal_order = None



for params in combinations_with_fixed:
    try:
        model = SARIMAX(train, order=(params[0], params[1], params[2]),
                        seasonal_order=(params[3], params[4], params[5], params[6]))
        model_fitted = model.fit(disp=False)
        aic = model_fitted.aic
        if aic < best_aic:
            best_aic = aic
            best_order = (params[0], params[1], params[2])
            best_seasonal_order = (params[3], params[4], params[5], params[6])
    except:
        continue

print(f"En iyi model: order={best_order}, seasonal_order={best_seasonal_order}, AIC={best_aic}")

# En iyi modeli eğitme
best_model = SARIMAX(train, order=best_order, seasonal_order=best_seasonal_order)
best_model_fitted = best_model.fit(disp=False)

# Test verisi üzerinde tahmin yapma
test_forecast = best_model_fitted.forecast(steps=len(test))

#  Model Performansını Değerlendirme
mse = mean_squared_error(test, test_forecast)
print(f"Test Verisi İçin Mean Squared Error (MSE): {mse}")

#  Görselleştirme
plt.figure(figsize=(12, 6))

# Orijinal Veri
plt.plot(range(len(veriler)), veriler, label="Gerçek Veri", color="blue")

# Test Tahmini
plt.plot(range(len(train), len(train) + len(test)), test_forecast, label="Test Tahmini", color="green", linestyle="--")

# Grafik Özelleştirmeleri
plt.axvline(x=len(train), color="black", linestyle="--", label="Eğitim-Test Ayrımı")
plt.legend()
plt.title("ARIMA ile Gelecek Zaman Tahmini")
plt.xlabel("Zaman")
plt.ylabel("Sıcaklık (°C)")
plt.show()
