## 📌 Opis
Skrypt automatyzuje pobieranie obrazów z listy URL, konwertuje je do formatu kwadratowego, dodaje znak wodny (jeśli dostępny) i zapisuje w formacie JPEG. Dodatkowo prowadzi logi operacji w pliku CSV.

---

## 🛠️ Wymagania
- **Python 3.x**
- **Biblioteki:**
  - `requests` – do pobierania obrazów z Internetu
  - `PIL (Pillow)` – do edycji obrazów
  - `csv` – do zapisywania logów
  - `os` – do operacji na plikach i katalogach

Instalacja wymaganych bibliotek:
```sh
pip install requests pillow
```
---

## 📂 Struktura plików

```
project/
│── linki.txt  # Lista URL do pobrania
│── watermark.png  # Opcjonalny znak wodny
│── downloader.py  # Skrypt główny
│── pobrane_grafiki/  # Folder do zapisu przetworzonych obrazów
│── log.csv  # Plik logów
```

---

## 📥 Wejście
- **Plik `linki.txt`**: zawiera listę URL obrazów, każdy w nowej linii.
- **Plik `watermark.png`** *(opcjonalnie)*: jeśli istnieje, będzie dodawany do pobranych obrazów.

---

## 📤 Wyjście
- **Przetworzone obrazy** zapisane w katalogu `pobrane_grafiki/` w formacie `.jpg`
- **Plik logów `log.csv`**, zawierający:
  - Nazwę pliku
  - URL pobranego obrazu
  - Status operacji
  - Rozdzielczość finalnego obrazu
  - Rozmiar pliku w KB

---

## 🔧 Jak używać skryptu?
1. **Dodaj listę URL do `linki.txt`.**
2. **(Opcjonalnie) Umieść znak wodny `watermark.png` w katalogu skryptu.**
3. **Uruchom skrypt:**
   ```sh
   python downloader.py
   ```

---

## 🔄 Jak działa skrypt?
1. **Tworzy folder `pobrane_grafiki/`, jeśli go nie ma.**
2. **Wczytuje listę URL z `linki.txt`.**
3. **Dla każdego URL:**
   - Pobiera obraz.
   - Usuwa przezroczystość (dla PNG).
   - Przekształca obraz do formatu kwadratowego, dodając białe tło.
   - (Opcjonalnie) Dodaje znak wodny w prawym dolnym rogu.
   - Zapisuje obraz jako `.jpg` w folderze `pobrane_grafiki/`.
   - Loguje operację w `log.csv`.
4. **Obsługuje błędy:**
   - Loguje nieudane pobrania i błędy konwersji.

---

## 🚀 Przykład działania
#### Wejście (linki.txt):
```
https://example.com/image1.png
https://example.com/image2.jpg
```
#### Uruchomienie skryptu:
```sh
python downloader.py
```
#### Wyjście:
- `pobrane_grafiki/obraz_1.jpg` (przetworzony obraz)
- `pobrane_grafiki/obraz_2.jpg`
- `log.csv` zawierający szczegóły przetwarzania.

---

## ❌ Możliwe błędy i ich rozwiązania
| Błąd | Przyczyna | Rozwiązanie |
|------|----------|------------|
| `Błąd pobierania` | Niedostępny URL | Sprawdź link w `linki.txt` |
| `Błąd konwersji` | Uszkodzony plik lub format | Upewnij się, że URL prowadzi do obrazu |
| `watermark.png` nie działa | Brak pliku lub niepoprawny format | Użyj pliku PNG z przezroczystością |

---

## 📜 Licencja
Projekt dostępny na licencji MIT – możesz go dowolnie modyfikować i używać do własnych celów.

---
