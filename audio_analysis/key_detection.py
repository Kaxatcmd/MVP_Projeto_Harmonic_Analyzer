"""
Detecção de Chave - Encontrar a Chave Musical de uma Música

Este módulo detecta a chave musical e BPM de um arquivo de áudio.

Funciona analisando:
1. As frequências presentes no áudio
2. Padrões que correspondem às escalas major/minor
3. O padrão mais forte para determinar a chave
"""

try:
    import librosa
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    print("⚠️  Librosa não instalado. Instale com: pip install librosa")


ALL_NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def detect_key_from_audio(file_path):
    """
    Detecta a chave musical de um arquivo de áudio.
    
    Usa análise chroma (12 notas musicais) para detectar a tonalidade.
    
    Args:
        file_path: Caminho para o arquivo de áudio (mp3, wav, etc.)
    
    Returns:
        Dicionário com:
        - 'key': Nome da chave detectada (ex: "C Major")
        - 'camelot': Notação Camelot (ex: "8B")
        - 'confidence': Confiança da detecção (0-1)
    """
    if not LIBROSA_AVAILABLE:
        return {
            "key": "Unknown - librosa not installed",
            "camelot": "Unknown",
            "confidence": 0.0
        }
    
    try:
        # Carregar áudio (máximo 30 segundos)
        y, sr = librosa.load(file_path, duration=30)
        
        # Calcular chroma (energia de cada nota: C, C#, D, etc)
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        
        # Média da energia em cada nota ao longo do tempo
        chroma_mean = chroma.mean(axis=1)
        
        # Encontrar a nota com mais energia (root note)
        root_index = chroma_mean.argmax()
        confidence = chroma_mean[root_index]
        
        root_note = ALL_NOTES[root_index]
        
        # Detectar se é major ou minor
        is_major = _guess_scale_type(chroma_mean)
        key_name = f"{root_note} {'Major' if is_major else 'Minor'}"
        
        # Converter para notação Camelot
        from utils.camelot_map import get_camelot_key
        camelot = get_camelot_key(key_name)
        
        return {
            "key": key_name,
            "camelot": camelot,
            "confidence": min(confidence, 1.0)
        }
    
    except Exception as e:
        print(f"❌ Erro ao detectar tonalidade: {e}")
        return {
            "key": f"Erro: {str(e)}",
            "camelot": "Unknown",
            "confidence": 0.0
        }


def _guess_scale_type(chroma_vector):
    """
    Adivinha se uma música está em escala major ou minor.
    
    Em escalas maiores, a 3ª e 5ª notas têm mais energia.
    Em escalas menores, a 3ª menor tem menos energia.
    """
    try:
        if len(chroma_vector) < 8:
            return True
        
        chroma_norm = chroma_vector / (chroma_vector.max() + 1e-10)
        major_score = chroma_norm[4] - chroma_norm[3]
        
        return major_score > 0
    
    except:
        return True


def detect_bpm(file_path):
    """
    Detecta o BPM (batidas por minuto) de um arquivo de áudio.
    
    BPM informa a velocidade do tempo - importante para DJs
    combinarem tempos ao mixar músicas!
    
    Args:
        file_path: Caminho para o arquivo de áudio
    
    Returns:
        Valor de BPM, ou None se falhar
    
    Exemplo:
        >>> detect_bpm("house_track.mp3")
        128
    """
    if not LIBROSA_AVAILABLE:
        return None
    
    try:
        import warnings
        y, sr = librosa.load(file_path, duration=30)
        
        try:
            # Versão nova (librosa >= 0.10)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                tempo = librosa.feature.rhythm.tempo(y=y, sr=sr)
                if hasattr(tempo, '__iter__'):
                    tempo = tempo[0] if len(tempo) > 0 else 0
        except (AttributeError, TypeError):
            # Versão antiga (librosa < 0.10)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                tempo = librosa.beat.tempo(y=y, sr=sr)
                if hasattr(tempo, '__iter__'):
                    tempo = tempo[0] if len(tempo) > 0 else 0
        
        return round(tempo) if tempo > 0 else None
    
    except Exception as e:
        print(f"❌ Erro ao detectar BPM: {e}")
        return None


def analyze_track(file_path):
    """
    Análise completa de uma música - chave, BPM, e mais.
    
    Retorna todas as informações musicais importantes em uma chamada.
    
    Args:
        file_path: Caminho para o arquivo de áudio
    
    Returns:
        Dicionário com:
        - file_path: Caminho do arquivo
        - key: Nome da chave
        - camelot: Notação Camelot
        - bpm: Batidas por minuto
        - duration: Duração em segundos
        - confidence: Confiança da detecção
    
    Exemplo:
        >>> info = analyze_track("my_song.mp3")
        >>> print(f"Esta música está em {info['camelot']} a {info['bpm']} BPM")
        Esta música está em 8A a 120 BPM
    """
    if not LIBROSA_AVAILABLE:
        return {
            "file_path": file_path,
            "key": "Unknown - librosa not installed",
            "camelot": "Unknown",
            "bpm": None,
            "duration": None,
            "error": "Install librosa: pip install librosa"
        }
    
    try:
        # Carregar áudio (máximo 60 segundos)
        y, sr = librosa.load(file_path, duration=60)
        duration = librosa.get_duration(y=y, sr=sr)
        
        print(f"🎵 Analisando: {file_path}")
        print(f"   ⏱️  Duração: {duration:.2f}s")
        
        # Obter chave e BPM
        print(f"   🔍 Detectando tonalidade...")
        key_info = detect_key_from_audio(file_path)
        
        print(f"   ⏱️  Detectando BPM...")
        bpm = detect_bpm(file_path)
        
        result = {
            "file_path": file_path,
            "key": key_info['key'],
            "camelot": key_info['camelot'],
            "bpm": bpm,
            "duration": round(duration, 2),
            "confidence": key_info['confidence']
        }
        
        print(f"   ✅ Análise completa!")
        print(f"      • Tonalidade: {result['key']}")
        print(f"      • Camelot: {result['camelot']}")
        print(f"      • BPM: {result['bpm']}")
        
        return result
    
    except Exception as e:
        print(f"❌ Erro ao analisar {file_path}: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "file_path": file_path,
            "key": f"Erro: {str(e)}",
            "camelot": "Unknown",
            "bpm": None,
            "duration": None
        }
