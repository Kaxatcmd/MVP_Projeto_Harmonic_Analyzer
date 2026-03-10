"""
Camelot Wheel Mapping - Harmonic Mixing Helper

O sistema Camelot é uma forma de representar chaves musicais usando
números (1-12) e letras (A para major, B para minor). 
Isso torna fácil para DJs encontrarem músicas que soam bem juntas.

Exemplo: "8A" significa A Minor (Sol# Menor), e pode mixar bem com:
  - Mesma chave: 8A
  - Chave relativa maior: 8B (A# Major / A Minor usam as mesmas notas)
  - +/- 1 hora na roda: 7A, 9A, 8B
"""

# Mapeamento de nomes de chaves padrão para notação Camelot
CAMELOT_MAP = {
    # Chaves Maiores (círculo "B")
    "C Major": "8B",
    "C# Major": "3B",
    "D Major": "10B",
    "Eb Major": "3B",
    "E Major": "7B",
    "F Major": "2B",
    "F# Major": "9B",
    "G Major": "4B",
    "Ab Major": "9B",
    "A Major": "11B",
    "Bb Major": "6B",
    "B Major": "1B",
    
    # Chaves Menores (círculo "A")
    "C Minor": "5A",
    "C# Minor": "12A",
    "D Minor": "7A",
    "D# Minor": "2A",
    "E Minor": "9A",
    "F Minor": "4A",
    "F# Minor": "11A",
    "G Minor": "6A",
    "G# Minor": "1A",
    "A Minor": "8A",
    "A# Minor": "3A",
    "B Minor": "10A",
}


def get_camelot_key(standard_key_name):
    """
    Converte um nome de chave musical para notação Camelot.
    
    Exemplo:
        >>> get_camelot_key("C Major")
        '8B'
        >>> get_camelot_key("A Minor")
        '8A'
    """
    return CAMELOT_MAP.get(standard_key_name, "Unknown")


def get_relative_key(camelot_code):
    """
    Obtém a chave relativa (mudando entre major e minor).
    
    Se você tem "8B" (C Major), isto retorna "8A" (A Minor).
    Elas usam as mesmas notas mas soam diferentes!
    
    Exemplo:
        >>> get_relative_key("8B")
        '8A'
    """
    if len(camelot_code) < 2:
        return None
    
    number = camelot_code[:-1]
    letter = camelot_code[-1]
    new_letter = "A" if letter == "B" else "B"
    
    return number + new_letter


def is_compatible_keys(key1, key2):
    """
    Verifica se duas chaves Camelot podem ser mixadas harmonicamente.
    
    Retorna True se as chaves funcionam bem juntas.
    
    Exemplo:
        >>> is_compatible_keys("8A", "8A")  # Mesma chave
        True
        >>> is_compatible_keys("8A", "7A")  # Um passo de diferença
        True
    """
    if len(key1) < 2 or len(key2) < 2:
        return False
    
    try:
        num1 = int(key1[:-1])
        num2 = int(key2[:-1])
        letter1 = key1[-1]
        letter2 = key2[-1]
        
        # Letras diferentes: compatíveis se números são iguais
        if letter1 != letter2:
            return num1 == num2
        
        # Mesma letra: números devem ser iguais ou diferir por 1
        diff = abs(num1 - num2)
        return diff == 0 or diff == 1 or diff == 11
    
    except (ValueError, IndexError):
        return False


def get_harmonic_mixes(camelot_code):
    """
    Retorna todas as chaves que funcionam bem com uma chave Camelot.
    
    Exemplo:
        >>> get_harmonic_mixes("8A")
        ['7A', '8A', '9A', '8B']  # Chaves compatíveis
    """
    if len(camelot_code) < 2:
        return []
    
    try:
        number = int(camelot_code[:-1])
        letter = camelot_code[-1]
        
        prev_num = ((number - 2) % 12) + 1
        next_num = (number % 12) + 1
        relative = get_relative_key(camelot_code)
        
        compatible = [
            f"{prev_num}{letter}",
            f"{number}{letter}",
            f"{next_num}{letter}",
        ]
        
        if relative:
            compatible.append(relative)
        
        return compatible
    
    except (ValueError, IndexError):
        return []


def get_compatible_keys(camelot_code):
    """Alias para get_harmonic_mixes() por compatibilidade."""
    return get_harmonic_mixes(camelot_code)
