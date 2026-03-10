#!/usr/bin/env python3
"""
DJ Harmonic Analyzer - MVP (Minimum Viable Product)

Interface CLI simplificada para análise de chaves musicais.

Funcionalidades:
- Analisar a chave musical e BPM de uma música
- Verificar compatibilidade harmônica entre chaves
- Ver chaves compatíveis para mixagem

Uso:
    python main.py analyze <arquivo.mp3>
    python main.py compatible <chave_camelot>
    python main.py mixes <chave_camelot>

Exemplo:
    python main.py analyze my_song.mp3
    python main.py compatible 8A
    python main.py mixes 8A
"""

import sys
import os
from pathlib import Path

from audio_analysis.key_detection import analyze_track
from utils.camelot_map import get_compatible_keys, is_compatible_keys, get_relative_key
from utils.persistence import (
    save_analysis, get_all_analyses, get_analysis_by_id, 
    update_analysis, delete_analysis, search_by_camelot, 
    search_by_bpm_range, get_statistics, export_to_csv, 
    clear_all_analyses
)


def cmd_analyze(file_path):
    """
    Analisa um arquivo de áudio.
    
    Retorna a chave musical, notação Camelot e BPM.
    """
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return None
    
    print()
    result = analyze_track(file_path)
    print()
    
    if "error" in result:
        print(f"Aviso: {result['error']}")
        return None
    else:
        # Mostrar resultado de forma formatada
        print("=" * 50)
        print("ANÁLISE DE MÚSICA")
        print("=" * 50)
        print(f"Arquivo:     {Path(file_path).name}")
        print(f"Tonalidade:  {result['key']}")
        print(f"Camelot:     {result['camelot']}")
        print(f"BPM:         {result['bpm']}")
        print(f"Duração:     {result['duration']}s")
        print(f"Confiança:   {result['confidence']:.1%}")
        print("=" * 50)
        print()
        
        # Mostrar chaves compatíveis
        if result['camelot'] != "Unknown":
            compatible = get_compatible_keys(result['camelot'])
            relative = get_relative_key(result['camelot'])
            
            print(f"CHAVES HARMÔNICAS COMPATÍVEIS:")
            print(f"   Chaves para mixar: {', '.join(compatible)}")
            if relative:
                print(f"   Chave relativa (major/minor): {relative}")
            print()
        
        return result


def cmd_compatible(camelot1, camelot2):
    """
    Verifica se duas chaves são harmonicamente compatíveis.
    """
    if is_compatible_keys(camelot1, camelot2):
        print(f"Sim: {camelot1} e {camelot2} SÃO compatíveis!")
    else:
        print(f"Não: {camelot1} e {camelot2} NÃO são compatíveis.")
    print()


def cmd_mixes(camelot_key):
    """
    Mostra todas as chaves que combinam bem com a chave informada.
    """
    compatible = get_compatible_keys(camelot_key)
    
    if not compatible:
        print(f"Erro: Chave Camelot inválida: {camelot_key}")
        print("   Use formato como '8A' ou '5B'")
        return
    
    print()
    print("=" * 50)
    print(f"CHAVES HARMÔNICAS PARA {camelot_key}")
    print("=" * 50)
    print(f"Você pode mixar {camelot_key} com estas chaves:")
    print()
    
    for i, key in enumerate(compatible, 1):
        print(f"  {i}. {key}")
    
    print()
    print("Dica: Use como ponto de partida para playlists harmônicas!")
    print("=" * 50)
    print()


def cmd_save(file_path, analysis_result):
    """
    Guarda uma análise no histórico em JSON.
    """
    if not analysis_result:
        print("Erro: Nenhuma análise para guardar.")
        return
    
    result = save_analysis(file_path, analysis_result)
    
    if result["success"]:
        print()
        print("=" * 50)
        print("ANÁLISE GUARDADA")
        print("=" * 50)
        print(result["message"])
        print("=" * 50)
        print()
    else:
        print(f"Erro ao guardar análise: {result['message']}")


def cmd_history():
    """
    Lista todas as análises guardadas.
    """
    analyses = get_all_analyses()
    
    if not analyses:
        print()
        print("Nenhuma análise guardada no histórico.")
        print()
        return
    
    print()
    print("=" * 80)
    print("HISTÓRICO DE ANÁLISES")
    print("=" * 80)
    
    for a in analyses:
        timestamp = a.get("timestamp", "").split("T")[0]
        print(f"\nID: {a['id']} | Data: {timestamp}")
        print(f"Ficheiro: {a['file_name']}")
        print(f"Tonalidade: {a['key']} | Camelot: {a['camelot']} | BPM: {a['bpm']}")
        print(f"Duração: {a['duration']}s | Confiança: {a['confidence']:.1%}")
    
    print()
    print("=" * 80)
    print()


def cmd_view(analysis_id):
    """
    Mostra detalhes de uma análise específica.
    """
    analysis = get_analysis_by_id(analysis_id)
    
    if not analysis:
        print(f"Erro: Análise com ID {analysis_id} não encontrada.")
        return
    
    print()
    print("=" * 50)
    print(f"ANÁLISE ID: {analysis['id']}")
    print("=" * 50)
    timestamp = analysis.get("timestamp", "").split("T")[0]
    print(f"Data:          {timestamp}")
    print(f"Ficheiro:      {analysis['file_name']}")
    print(f"Caminho:       {analysis['file_path']}")
    print(f"Tonalidade:    {analysis['key']}")
    print(f"Camelot:       {analysis['camelot']}")
    print(f"BPM:           {analysis['bpm']}")
    print(f"Duração:       {analysis['duration']}s")
    print(f"Confiança:     {analysis['confidence']:.1%}")
    print("=" * 50)
    print()


def cmd_delete(analysis_id):
    """
    Remove uma análise do histórico.
    """
    result = delete_analysis(analysis_id)
    
    if result["success"]:
        print()
        print(result["message"])
        print()
    else:
        print(f"Erro: {result['message']}")


def cmd_stats():
    """
    Mostra estatísticas sobre as análises guardadas.
    """
    stats = get_statistics()
    
    print()
    print("=" * 50)
    print("ESTATÍSTICAS DAS ANÁLISES")
    print("=" * 50)
    print(f"Total de análises: {stats['total_analyses']}")
    print(f"BPM médio:         {stats['average_bpm']}")
    print(f"Chave mais comum:  {stats['most_common_key']}")
    print(f"Chaves únicas:     {stats['unique_keys']}")
    print("=" * 50)
    print()


def cmd_export():
    """
    Exporta análises para ficheiro CSV.
    """
    result = export_to_csv()
    
    if result["success"]:
        print()
        print("=" * 50)
        print("EXPORTAÇÃO COMPLETA")
        print("=" * 50)
        print(result["message"])
        print(f"Localização: {result['filepath']}")
        print("=" * 50)
        print()
    else:
        print(f"Erro: {result['message']}")
        print()


def print_help():
    """
    Mostra a mensagem de ajuda.
    """
    print()
    print("=" * 70)
    print("DJ HARMONIC ANALYZER - MVP (Minimum Viable Product)")
    print("=" * 70)
    print()
    print("ANÁLISE DE MÚSICA:")
    print("  python main.py analyze <arquivo.mp3>")
    print("  Exemplo: python main.py analyze my_song.mp3")
    print()
    print("-" * 70)
    print()
    print("CONSULTAS HARMÔNICAS:")
    print("  python main.py compatible <chave1> <chave2>")
    print("  Exemplo: python main.py compatible 8A 7A")
    print()
    print("  python main.py mixes <chave_camelot>")
    print("  Exemplo: python main.py mixes 8A")
    print()
    print("-" * 70)
    print()
    print("PERSISTÊNCIA E HISTÓRICO (JSON):")
    print("  python main.py history")
    print("  Mostra todas as análises guardadas")
    print()
    print("  python main.py view <id>")
    print("  Mostra detalhes de uma análise (ex: python main.py view 1)")
    print()
    print("  python main.py delete <id>")
    print("  Remove uma análise (ex: python main.py delete 1)")
    print()
    print("-" * 70)
    print()
    print("ESTATÍSTICAS E EXPORTAÇÃO:")
    print("  python main.py stats")
    print("  Mostra estatísticas das análises")
    print()
    print("  python main.py export")
    print("  Exporta análises para ficheiro CSV")
    print()
    print("-" * 70)
    print()
    print("INFORMAÇÕES:")
    print("  python main.py help")
    print("  Mostra esta mensagem de ajuda")
    print()
    print("=" * 70)
    print()
    print("FORMATO CAMELOT:")
    print("  Use: Números 1-12 + letra (A ou B)")
    print("  Exemplos: 8A (A Minor), 5B (F Major), 12A (C# Minor), 1B (B Major)")
    print()
    print("=" * 70)
    print()


def main():
    """
    Função principal - processa argumentos de linha de comando.
    """
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "analyze" and len(sys.argv) >= 3:
        file_path = sys.argv[2]
        result = cmd_analyze(file_path)
        
        # Pergunta se deseja guardar a análise
        if result:
            save_input = input("Deseja guardar esta análise? (s/n): ").lower().strip()
            if save_input == 's':
                cmd_save(file_path, result)
    
    elif command == "compatible" and len(sys.argv) >= 4:
        camelot1 = sys.argv[2].upper()
        camelot2 = sys.argv[3].upper()
        cmd_compatible(camelot1, camelot2)
    
    elif command == "mixes" and len(sys.argv) >= 3:
        camelot_key = sys.argv[2].upper()
        cmd_mixes(camelot_key)
    
    elif command == "history":
        cmd_history()
    
    elif command == "view" and len(sys.argv) >= 3:
        try:
            analysis_id = int(sys.argv[2])
            cmd_view(analysis_id)
        except ValueError:
            print(f"Erro: ID deve ser um número inteiro.")
    
    elif command == "delete" and len(sys.argv) >= 3:
        try:
            analysis_id = int(sys.argv[2])
            cmd_delete(analysis_id)
        except ValueError:
            print(f"Erro: ID deve ser um número inteiro.")
    
    elif command == "stats":
        cmd_stats()
    
    elif command == "export":
        cmd_export()
    
    elif command == "help" or command == "-h" or command == "--help":
        print_help()
    
    else:
        print(f"Erro: Comando desconhecido: {command}")
        print()
        print_help()


if __name__ == "__main__":
    main()
