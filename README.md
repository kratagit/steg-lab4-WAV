# steg-lab4-WAV

# Laboratorium 4

## Implementacja steganografii w plikach audio WAV z pseudolosową permutacją

### Cel zadania

Celem zadania jest implementacja prostej metody steganografii w plikach audio WAV z wykorzystaniem modyfikacji bezpośrednich próbek oraz pseudolosowej permutacji. Celem jest napisanie programu, który ukryje wiadomość tekstową w pliku audio oraz odczyta ukrytą wiadomość ze zmodyfikowanego pliku.

## Opis zadania

1. Napisz funkcję `hide_message(input_audio, message, output_audio, seed)`, która:
- Wczyta plik audio WAV
- Wygeneruje pseudolosową permutację indeksów próbek na podstawie podanego ziarna (`seed`)
- Ukryje podaną wiadomość tekstową w LSB wybranych próbek zgodnie z permutacją
- Zapisze zmodyfikowany plik audio

2. Napisz funkcję `extract_message(stego_audio, seed)`, która:
- Wczyta plik audio WAV zawierający ukrytą wiadomość
- Wygeneruje tę samą pseudolosową permutację indeksów próbek
- Odczyta ukrytą wiadomość z LSB wybranych próbek zgodnie z permutacją
- Zwróci odczytaną wiadomość

## Wskazówki implementacyjne

- Użyj biblioteki `wave` w Pythonie lub `audioread` w Matlabie do obsługi plików WAV
- Wykorzystaj generator liczb pseudolosowych (np. `random` w Pythonie lub `rng` w Matlabie) do generowania permutacji
- Konwertuj znaki wiadomości na ich reprezentację binarną
- Modyfikuj tylko LSB wybranych próbek zgodnie z wygenerowaną permutacją
- Pamiętaj o zapisaniu długości ukrywanej wiadomości na początku steganogramu

## Kryteria akceptacji

1. Program poprawnie ukrywa wiadomość w pliku audio bez zauważalnego pogorszenia jakości dźwięku
2. Program poprawnie odczytuje ukrytą wiadomość z zmodyfikowanego pliku audio
3. Implementacja obsługuje pliki WAV o różnych częstotliwościach próbkowania i liczbie kanałów

## Przypadki testowe

1. Ukryj krótką wiadomość (np. `"Hello World!"`) w 10-sekundowym pliku WAV mono 44.1kHz i odczytaj ją
2. Ukryj długą wiadomość (np. 1000 znaków) w 30-sekundowym pliku WAV stereo 48kHz i odczytaj ją
3. Spróbuj ukryć wiadomość dłuższą niż pojemność pliku audio - program powinien zgłosić błąd
4. Odczytaj wiadomość z użyciem nieprawidłowego ziarna (`seed`) - program powinien zwrócić nieprawidłową wiadomość
