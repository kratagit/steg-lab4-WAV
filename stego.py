import wave
import random

def hide_message(input_audio, message, output_audio, seed):
    """
    Ukrywa wiadomość tekstową w pliku WAV używając metody LSB i pseudolosowej permutacji.
    """
    with wave.open(input_audio, 'rb') as wav_in:
        params = wav_in.getparams()
        num_channels = wav_in.getnchannels()
        sampwidth = wav_in.getsampwidth()
        num_frames = wav_in.getnframes()
        
        # Wczytanie wszystkich klatek audio jako bajty
        frames = bytearray(wav_in.readframes(num_frames))
        
    num_samples = num_frames * num_channels
    
    # Przygotowanie wiadomości
    msg_bytes = message.encode('utf-8')
    msg_len = len(msg_bytes)
    
    # Zapiszemy długość wiadomości jako 4 bajty (32 bity)
    if 32 + msg_len * 8 > num_samples:
        raise ValueError(f"Wiadomość jest zbyt długa ({32 + msg_len * 8} bitów), aby ukryć ją w tym pliku audio (pojemność: {num_samples} bitów).")
        
    # Konwersja długości i samej wiadomości na ciąg bitów
    len_bytes = msg_len.to_bytes(4, byteorder='big')
    data_to_hide = len_bytes + msg_bytes
    
    bits = []
    for b in data_to_hide:
        for i in range(7, -1, -1):
            bits.append((b >> i) & 1)
            
    # Generowanie pseudolosowej permutacji indeksów próbek
    random.seed(seed)
    indices = list(range(num_samples))
    random.shuffle(indices)
    
    # Ukrywanie bitów w LSB
    for i, bit in enumerate(bits):
        sample_idx = indices[i]
        # Bajtem zawierającym LSB danej próbki jest pierwszy bajt tej próbki
        # (ponieważ pliki WAV zapisują dane w formacie little-endian)
        byte_offset = sample_idx * sampwidth
        
        # Modyfikacja najmniej znaczącego bitu w tym bajcie
        current_byte = frames[byte_offset]
        new_byte = (current_byte & 0xFE) | bit
        frames[byte_offset] = new_byte
        
    # Zapis zmodyfikowanego pliku audio
    with wave.open(output_audio, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(frames)

def extract_message(stego_audio, seed):
    """
    Odczytuje ukrytą wiadomość z pliku WAV używając podanego ziarna.
    """
    with wave.open(stego_audio, 'rb') as wav_in:
        num_channels = wav_in.getnchannels()
        sampwidth = wav_in.getsampwidth()
        num_frames = wav_in.getnframes()
        
        frames = bytearray(wav_in.readframes(num_frames))
        
    num_samples = num_frames * num_channels
    
    # Odtworzenie tej samej permutacji za pomocą tego samego ziarna
    random.seed(seed)
    indices = list(range(num_samples))
    random.shuffle(indices)
    
    # Odczyt długości wiadomości (z pierwszych 32 wylosowanych próbek)
    msg_len = 0
    for i in range(32):
        sample_idx = indices[i]
        byte_offset = sample_idx * sampwidth
        bit = frames[byte_offset] & 1
        msg_len = (msg_len << 1) | bit
        
    # Sprawdzenie czy długość ma sens
    if msg_len < 0 or 32 + msg_len * 8 > num_samples:
        raise ValueError("Odczytano nieprawidłową długość wiadomości. Niewłaściwe ziarno lub uszkodzony plik.")
        
    # Odczyt bitów wiadomości na podstawie wczytanej długości
    msg_bits = []
    for i in range(32, 32 + msg_len * 8):
        sample_idx = indices[i]
        byte_offset = sample_idx * sampwidth
        bit = frames[byte_offset] & 1
        msg_bits.append(bit)
        
    # Konwersja bitów na bajty
    msg_bytes = bytearray()
    for i in range(0, len(msg_bits), 8):
        byte_val = 0
        for j in range(8):
            byte_val = (byte_val << 1) | msg_bits[i+j]
        msg_bytes.append(byte_val)
        
    # Zdekodowanie tekstu UTF-8
    try:
        return msg_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Nie udało się zdekodować wiadomości. Prawdopodobnie użyto błędnego ziarna.")
