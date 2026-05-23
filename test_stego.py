import wave
import random
import os
from stego import hide_message, extract_message

def create_dummy_wav(filename, duration_sec, sample_rate, channels, sampwidth=2):
    """Funkcja pomocnicza do tworzenia pliku WAV z szumem (pseudolosowe dane)"""
    num_frames = duration_sec * sample_rate
    with wave.open(filename, 'wb') as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(sampwidth)
        wav.setframerate(sample_rate)
        
        # Generowanie losowych bajtów jako szumu audio
        frames = bytearray(random.getrandbits(8) for _ in range(num_frames * channels * sampwidth))
        wav.writeframes(frames)

def test_short_message():
    print("Test 1: Ukryj krótką wiadomość w 10-sekundowym pliku WAV mono 44.1kHz i odczytaj ją.")
    original = "test1_orig.wav"
    stego = "test1_stego.wav"
    create_dummy_wav(original, 10, 44100, 1)
    
    msg = "Hello World!"
    seed = 42
    
    hide_message(original, msg, stego, seed)
    extracted = extract_message(stego, seed)
    
    assert extracted == msg, "Wyciągnięta wiadomość nie zgadza się z oryginałem!"
    print(f"Test 1 Zakończony Sukcesem. Odczytano: '{extracted}'")
    
def test_long_message():
    print("\nTest 2: Ukryj długą wiadomość (1000 znaków) w 30-sekundowym pliku WAV stereo 48kHz i odczytaj ją.")
    original = "test2_orig.wav"
    stego = "test2_stego.wav"
    create_dummy_wav(original, 30, 48000, 2)
    
    msg = "A" * 1000
    seed = 12345
    
    hide_message(original, msg, stego, seed)
    extracted = extract_message(stego, seed)
    
    assert extracted == msg, "Wyciągnięta wiadomość nie zgadza się z oryginałem!"
    print(f"Test 2 Zakończony Sukcesem. Odczytano wiadomość o długości {len(extracted)} znaków.")

def test_capacity_exceeded():
    print("\nTest 3: Próba ukrycia wiadomości dłuższej niż pojemność pliku audio.")
    original = "test3_orig.wav"
    stego = "test3_stego.wav"
    # Plik na 1 sekundę z próbnym próbkowaniem 800 Hz mono = 800 próbek = 800 bitów pojemności.
    create_dummy_wav(original, 1, 800, 1)
    
    # 200 znaków = 200 bajtów = 1600 bitów (plus 32 bity długości)
    msg = "B" * 200 
    seed = 99
    
    try:
        hide_message(original, msg, stego, seed)
        print("Test 3 Zakończony Niepowodzeniem. Nie zgłoszono błędu!")
    except ValueError as e:
        print(f"Test 3 Zakończony Sukcesem. Oczekiwany błąd: {e}")

def test_wrong_seed():
    print("\nTest 4: Odczyt wiadomości z użyciem nieprawidłowego ziarna.")
    original = "test4_orig.wav"
    stego = "test4_stego.wav"
    create_dummy_wav(original, 5, 44100, 1)
    
    msg = "Tajny komunikat ukryty przed światem"
    correct_seed = 777
    wrong_seed = 888
    
    hide_message(original, msg, stego, correct_seed)
    
    try:
        extracted = extract_message(stego, wrong_seed)
        print(f"Test 4 Zakończony Niepowodzeniem. Odczytano: {extracted}")
    except ValueError as e:
        print(f"Test 4 Zakończony Sukcesem. Oczekiwany błąd odczytu: {e}")

if __name__ == "__main__":
    test_short_message()
    test_long_message()
    test_capacity_exceeded()
    test_wrong_seed()
