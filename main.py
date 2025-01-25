import os
import requests
import csv
from PIL import Image, ImageOps

from io import BytesIO

# KONFIGURACJA
WATERMARK_PATH = "watermark.png"  # Ścieżka do znaku wodnego
LOG_FILE = "log.csv"  # Plik logów
FOLDER = "pobrane_grafiki"  # Folder na grafiki

# Tworzymy folder na pobrane grafiki
os.makedirs(FOLDER, exist_ok=True)

# Wczytujemy linki z pliku
with open("linki.txt", "r") as file:
    urls = [line.strip() for line in file if line.strip()]

# Wczytaj watermark, jeśli istnieje
watermark = None
if os.path.exists(WATERMARK_PATH):
    watermark = Image.open(WATERMARK_PATH).convert("RGBA")  # Wczytujemy znak wodny

# Tworzymy plik logów
with open(LOG_FILE, "w", newline="") as log_file:
    log_writer = csv.writer(log_file)
    log_writer.writerow(["Plik", "URL", "Status", "Rozdzielczość", "Rozmiar (KB)"])

# Pobieramy, konwertujemy i zapisujemy obrazy
for idx, url in enumerate(urls, start=1):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Sprawdzamy błędy HTTP

        # Wczytujemy obraz
        img = Image.open(BytesIO(response.content))

        # 🔥 1. Usunięcie przezroczystości
        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
            img = background

        else:
            img = img.convert("RGB")  # Normalna konwersja do RGB

        # 🔥 2. Tworzenie kwadratowego obrazu
        max_side = max(img.size)
        square_img = Image.new("RGB", (max_side, max_side), (255, 255, 255))
        paste_x = (max_side - img.size[0]) // 2
        paste_y = (max_side - img.size[1]) // 2
        square_img.paste(img, (paste_x, paste_y))

        # 🔥 3. Dodanie watermarka (jeśli istnieje)
        if watermark:
            wm_resized = watermark.resize((square_img.width // 5, square_img.height // 10))  # Skalowanie watermarka
            wm_x = square_img.width - wm_resized.width - 10  # Prawy dolny róg
            wm_y = square_img.height - wm_resized.height - 10
            square_img.paste(wm_resized, (wm_x, wm_y), wm_resized)  # Nakładanie watermarka

        # 🔥 4. Zapisujemy jako JPG
        filename = f"{FOLDER}/obraz_{idx}.jpg"
        square_img.save(filename, "JPEG", quality=90)

        # 🔥 5. Logowanie sukcesu
        img_size_kb = round(os.path.getsize(filename) / 1024, 2)
        with open(LOG_FILE, "a", newline="") as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow([filename, url, "OK", f"{square_img.width}x{square_img.height}", img_size_kb])

        print(f"✅ Pobrano i skonwertowano: {filename}")

    except requests.RequestException as e:
        error_msg = f"Błąd pobierania {url}: {e}"
        with open(LOG_FILE, "a", newline="") as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow(["-", url, "BŁĄD POBIERANIA", "-", "-"])
        print(f"❌ {error_msg}")

    except Exception as e:
        error_msg = f"Błąd konwersji {url}: {e} (Tryb: {img.mode})"
        with open(LOG_FILE, "a", newline="") as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow(["-", url, "BŁĄD KONWERSJI", "-", "-"])
        print(f"❌ {error_msg}")

print("🎉 Zakończono pobieranie i konwersję!")
