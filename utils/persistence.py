"""
Módulo de Persistência - Gestão de Análises em JSON

Este módulo implementa funcionalidades de armazenamento e recuperação
de análises de áudio em formato JSON, permitindo backup e histórico
de análises realizadas.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


# Diretório de dados
DATA_DIR = Path(__file__).parent.parent / "data"
ANALYSES_FILE = DATA_DIR / "analyses.json"


def _ensure_data_dir():
    """Garante que o diretório de dados existe."""
    DATA_DIR.mkdir(exist_ok=True)


def _load_analyses() -> List[Dict]:
    """
    Carrega todas as análises do ficheiro JSON.
    
    Returns:
        Lista de dicionários com análises guardadas
    """
    _ensure_data_dir()
    
    if not ANALYSES_FILE.exists():
        return []
    
    try:
        with open(ANALYSES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def _save_analyses(analyses: List[Dict]):
    """
    Salva análises no ficheiro JSON.
    
    Args:
        analyses: Lista de dicionários com análises
    """
    _ensure_data_dir()
    
    with open(ANALYSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(analyses, f, indent=2, ensure_ascii=False)


def save_analysis(file_path: str, analysis_result: Dict) -> Dict:
    """
    Guarda uma análise no histórico.
    
    Args:
        file_path: Caminho do ficheiro analisado
        analysis_result: Dicionário com resultado da análise
    
    Returns:
        Dicionário com ID da análise guardada
    """
    analyses = _load_analyses()
    
    # Criar registo com timestamp
    record = {
        "id": len(analyses) + 1,
        "timestamp": datetime.now().isoformat(),
        "file_path": file_path,
        "file_name": Path(file_path).name,
        "key": analysis_result.get("key", "Unknown"),
        "camelot": analysis_result.get("camelot", "Unknown"),
        "bpm": int(analysis_result.get("bpm")) if analysis_result.get("bpm") else None,
        "duration": round(float(analysis_result.get("duration", 0)), 2) if analysis_result.get("duration") else None,
        "confidence": round(float(analysis_result.get("confidence", 0.0)), 4)
    }
    
    analyses.append(record)
    _save_analyses(analyses)
    
    return {
        "success": True,
        "message": f"Análise guardada com ID: {record['id']}",
        "id": record['id']
    }


def get_all_analyses() -> List[Dict]:
    """
    Retorna todas as análises guardadas.
    
    Returns:
        Lista de análises
    """
    return _load_analyses()


def get_analysis_by_id(analysis_id: int) -> Optional[Dict]:
    """
    Retorna uma análise específica pelo ID.
    
    Args:
        analysis_id: ID da análise
    
    Returns:
        Dicionário com análise ou None se não encontrada
    """
    analyses = _load_analyses()
    
    for analysis in analyses:
        if analysis.get("id") == analysis_id:
            return analysis
    
    return None


def update_analysis(analysis_id: int, updates: Dict) -> Dict:
    """
    Atualiza os dados de uma análise existente.
    
    Args:
        analysis_id: ID da análise a atualizar
        updates: Dicionário com campos a atualizar
    
    Returns:
        Dicionário com resultado da operação
    """
    analyses = _load_analyses()
    
    for analysis in analyses:
        if analysis.get("id") == analysis_id:
            # Atualizar campos permitidos
            if "camelot" in updates:
                analysis["camelot"] = updates["camelot"]
            if "key" in updates:
                analysis["key"] = updates["key"]
            if "bpm" in updates:
                analysis["bpm"] = updates["bpm"]
            
            _save_analyses(analyses)
            return {
                "success": True,
                "message": f"Análise {analysis_id} atualizada com sucesso"
            }
    
    return {
        "success": False,
        "message": f"Análise com ID {analysis_id} não encontrada"
    }


def delete_analysis(analysis_id: int) -> Dict:
    """
    Remove uma análise do histórico.
    
    Args:
        analysis_id: ID da análise a remover
    
    Returns:
        Dicionário com resultado da operação
    """
    analyses = _load_analyses()
    original_length = len(analyses)
    
    # Filtrar análise a remover
    analyses = [a for a in analyses if a.get("id") != analysis_id]
    
    if len(analyses) < original_length:
        _save_analyses(analyses)
        return {
            "success": True,
            "message": f"Análise {analysis_id} removida com sucesso"
        }
    else:
        return {
            "success": False,
            "message": f"Análise com ID {analysis_id} não encontrada"
        }


def search_by_camelot(camelot_key: str) -> List[Dict]:
    """
    Procura análises por chave Camelot.
    
    Args:
        camelot_key: Chave Camelot para procurar (ex: "8A")
    
    Returns:
        Lista de análises que correspondem à chave
    """
    analyses = _load_analyses()
    return [a for a in analyses if a.get("camelot") == camelot_key]


def search_by_bpm_range(min_bpm: int, max_bpm: int) -> List[Dict]:
    """
    Procura análises por intervalo de BPM.
    
    Args:
        min_bpm: BPM mínimo
        max_bpm: BPM máximo
    
    Returns:
        Lista de análises dentro do intervalo
    """
    analyses = _load_analyses()
    return [
        a for a in analyses 
        if a.get("bpm") and min_bpm <= a["bpm"] <= max_bpm
    ]


def get_statistics() -> Dict:
    """
    Calcula estatísticas sobre as análises guardadas.
    
    Returns:
        Dicionário com estatísticas
    """
    analyses = _load_analyses()
    
    if not analyses:
        return {
            "total_analyses": 0,
            "average_bpm": 0,
            "most_common_key": "N/A"
        }
    
    bpms = [a.get("bpm") for a in analyses if a.get("bpm")]
    camelots = [a.get("camelot") for a in analyses if a.get("camelot") != "Unknown"]
    
    # Chave mais comum
    most_common = "N/A"
    if camelots:
        from collections import Counter
        most_common = Counter(camelots).most_common(1)[0][0]
    
    return {
        "total_analyses": len(analyses),
        "average_bpm": round(sum(bpms) / len(bpms), 1) if bpms else 0,
        "most_common_key": most_common,
        "unique_keys": len(set(camelots))
    }


def export_to_csv(filename: str = "analyses_export.csv") -> Dict:
    """
    Exporta análises para ficheiro CSV.
    
    Args:
        filename: Nome do ficheiro CSV
    
    Returns:
        Dicionário com resultado da operação
    """
    try:
        analyses = _load_analyses()
        
        if not analyses:
            return {
                "success": False,
                "message": "Nenhuma análise para exportar"
            }
        
        csv_path = DATA_DIR / filename
        
        with open(csv_path, 'w', encoding='utf-8') as f:
            # Cabeçalho
            f.write("ID,Data,Ficheiro,Tonalidade,Camelot,BPM,Duração,Confiança\n")
            
            # Dados
            for a in analyses:
                timestamp = a.get("timestamp", "").split("T")[0]
                f.write(
                    f"{a['id']},"
                    f"{timestamp},"
                    f"\"{a['file_name']}\","
                    f"{a['key']},"
                    f"{a['camelot']},"
                    f"{a['bpm']},"
                    f"{a['duration']},"
                    f"{a['confidence']}\n"
                )
        
        return {
            "success": True,
            "message": f"Análises exportadas para {filename}",
            "filepath": str(csv_path)
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Erro ao exportar: {str(e)}"
        }


def clear_all_analyses() -> Dict:
    """
    Remove todas as análises (operação destrutiva).
    
    Returns:
        Dicionário com resultado da operação
    """
    try:
        _ensure_data_dir()
        _save_analyses([])
        return {
            "success": True,
            "message": "Todas as análises foram removidas"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Erro ao limpar análises: {str(e)}"
        }
