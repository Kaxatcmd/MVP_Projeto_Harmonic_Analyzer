# DJ Harmonic Analyzer - MVP

**Minimum Viable Product** - Analisador de música que detecta a chave musical e BPM, facilitando a descoberta de combinações harmônicas para mixagem profissional.

## Estado do Projeto

Este projeto encontra-se atualmente em **fase de MVP (Minimum Viable Product)**.

- **Objetivo:** Validar o conceito principal de análise harmônica de áudio
- **Versão:** 1.1 (com persistência em JSON)
- **Status:** Funcional e pronto para utilização
- **Data:** 10 de Março de 2026

**Nota:** Este é um produto em desenvolvimento. Algumas funcionalidades poderão estar incompletas ou sujeitas a mudanças futuras.

## Funcionalidades Atuais

O MVP implementa as seguintes funcionalidades core e de suporte:

### Análise de Áudio (Core)
- Detecção automática de tonalidade musical utilizando análise de espectro de áudio
- Conversão para notação Camelot (padrão profissional de DJs)
- Detecção automatizada de BPM (batidas por minuto)
- Cálculo de confiança da detecção (percentagem de certeza)

### Consultoria Harmônica (Core)
- Verificação de compatibilidade entre duas chaves musicais
- Recomendação automática de chaves compatíveis para mixagem harmônica
- Apresentação visual da compatibilidade na Roda de Camelot

### Persistência de Dados (Funcional)
- Armazenamento automático de análises em formato JSON
- Histórico completo de análises realizadas
- Capacidade de recuperação de análises anteriores

### Gestão de Análises (CRUD Completo)
- **Create:** Guardar novas análises
- **Read:** Consumir histórico, visualizar detalhes
- **Update:** Modificar dados de análises existentes (base)
- **Delete:** Remover análises do histórico

### Relatório e Exportação
- Estatísticas agregadas (total, BPM médio, chave mais frequente)
- Exportação em formato CSV para análise em ferramentas externas

## Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pip (gestor de pacotes Python)
- ~500 MB de espaço em disco (para librosa e dependências)

### Passos de Instalação

**1. Clonar ou descarregar o repositório**
```bash
cd MVP_projeto
```

**2. Criar e ativar um ambiente virtual (recomendado)**
```bash
python3 -m venv venv
source venv/bin/activate  # Em Windows: venv\Scripts\activate
```

**3. Instalar dependências**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

A instalação pode levar alguns minutos na primeira execução enquanto o librosa é compilado.

## Como Utilizar

O sistema oferece dois métodos de execução equivalentes:

### Método 1: Usando o Script Auxiliar (Recomendado)
```bash
./run.sh <comando> [argumentos]
```

Vantagem: Ativa automaticamente o ambiente virtual.

### Método 2: Execução Direta
```bash
python main.py <comando> [argumentos]
```

Requer que o venv esteja ativado manualmente.

## Comandos Disponíveis

### 1. ANALISAR MÚSICA (analyze)

Analisa um ficheiro de áudio para extrair tonalidade, Camelot e BPM.

```bash
./run.sh analyze <caminho_ficheiro>
```

**Exemplo:**
```bash
./run.sh analyze musica.mp3
```

**Comportamento:**
- Carrega o ficheiro de áudio
- Executa análise com librosa (30-60 segundos na primeira vez)
- Apresenta resultados
- Pergunta: "Deseja guardar esta análise? (s/n):"
  - Responda `s` para guardar em data/analyses.json
  - Responda `n` para descartar

**Output Exemplo:**
```
ANÁLISE DE MÚSICA
==================================================
Arquivo:     musica.mp3
Tonalidade:  E Major
Camelot:     7B
BPM:         123
Duração:     60.0s
Confiança:   97.5%
==================================================

CHAVES HARMÔNICAS COMPATÍVEIS:
   Chaves para mixar: 6B, 7B, 8B, 7A
   Chave relativa (major/minor): 7A
```

---

### 2. VERIFICAR COMPATIBILIDADE (compatible)

Verifica se duas chaves musicais são harmonicamente compatíveis para mixagem.

```bash
./run.sh compatible <chave1> <chave2>
```

**Exemplo:**
```bash
./run.sh compatible 8A 7A
```

**Resultado:**
```
Sim: 8A e 7A SÃO compatíveis!
```

---

### 3. LISTAR CHAVES COMPATÍVEIS (mixes)

Retorna todas as chaves que funcionam bem com uma chave específica.

```bash
./run.sh mixes <chave>
```

**Exemplo:**
```bash
./run.sh mixes 8A
```

**Resultado:**
```
CHAVES HARMÔNICAS PARA 8A
==================================================
Você pode mixar 8A com estas chaves:

  1. 7A
  2. 8A
  3. 9A
  4. 8B
```

---

### 4. HISTÓRICO DE ANÁLISES (history)

Lista todas as análises guardadas, apresentadas em formato tabulado.

```bash
./run.sh history
```

**Resultado:**
```
HISTÓRICO DE ANÁLISES
================================================================================

ID: 1 | Data: 2026-03-10
Ficheiro: musica1.mp3
Tonalidade: E Major | Camelot: 7B | BPM: 123
Duração: 60.0s | Confiança: 97.5%

ID: 2 | Data: 2026-03-10
Ficheiro: musica2.mp3
Tonalidade: D Minor | Camelot: 7A | BPM: 103
Duração: 60.0s | Confiança: 85.2%

================================================================================
```

---

### 5. VER ANÁLISE ESPECÍFICA (view)

Exibe todos os detalhes de uma análise guardada pelo seu ID.

```bash
./run.sh view <id>
```

**Exemplo:**
```bash
./run.sh view 1
```

**Resultado:**
```
ANÁLISE ID: 1
==================================================
Data:          2026-03-10
Ficheiro:      musica1.mp3
Caminho:       /home/user/musica1.mp3
Tonalidade:    E Major
Camelot:       7B
BPM:           123
Duração:       60.0s
Confiança:     97.5%
==================================================
```

---

### 6. REMOVER ANÁLISE (delete)

Remove uma análise específica do histórico (operação não reversível).

```bash
./run.sh delete <id>
```

**Exemplo:**
```bash
./run.sh delete 1
```

**Resultado:**
```
Análise 1 removida com sucesso
```

---

### 7. ESTATÍSTICAS (stats)

Apresenta estatísticas agregadas sobre todas as análises guardadas.

```bash
./run.sh stats
```

**Resultado:**
```
ESTATÍSTICAS DAS ANÁLISES
==================================================
Total de análises: 15
BPM médio:         120.5
Chave mais comum:  8A
Chaves únicas:     7
==================================================
```

---

### 8. EXPORTAR PARA CSV (export)

Exporta todas as análises para um ficheiro CSV compatível com Excel/Google Sheets.

```bash
./run.sh export
```

**Resultado:**
```
EXPORTAÇÃO COMPLETA
==================================================
Análises exportadas para analyses_export.csv
Localização: /home/user/MVP_projeto/data/analyses_export.csv
==================================================
```

**Ficheiro gerado:**
```
data/analyses_export.csv
```

---

### 9. AJUDA (help)

Apresenta mensagem de ajuda com descrição de todos os comandos.

```bash
./run.sh help
```

---

## Estrutura do Projeto

```
MVP_projeto/
│
├── main.py                          # Interface CLI principal
├── requirements.txt                 # Dependências do projeto
├── run.sh                          # Script auxiliar (venv + python)
├── README.md                       # Este ficheiro
│
├── audio_analysis/                 # Módulo de análise de áudio
│   ├── __init__.py
│   └── key_detection.py            # Detecção de tonalidade e BPM
│
├── utils/                          # Módulos utilitários
│   ├── __init__.py
│   ├── camelot_map.py              # Mapeamento de chaves musicais (Camelot)
│   └── persistence.py              # Sistema CRUD em JSON
│
├── data/                           # Persistência de dados
│   ├── analyses.json               # Histórico de análises (backup)
│   └── analyses_export.csv         # Exportação em formato CSV
│
├── venv/                           # Ambiente virtual Python
│
└── Documentação:
    ├── AUDITORIA_TECNICA.md        # Auditoria técnica (relatório interno)
    ├── IMPLEMENTACAO_PERSISTENCIA.md # Detalhe de implementação
    ├── MVP_etapa_1.md               # Análise de conformidade MVP
    └── RELATORIO.md                 # Relatório académico
```

## Persistência de Dados

### Sistema de Backup em JSON

Todas as análises são **automaticamente guardadas** no ficheiro `data/analyses.json` quando o utilizador opta por guardar após uma análise. Isto garante:

- **Durabilidade:** Dados não são perdidos ao fechar o programa
- **Recuperação:** Histórico disponível para consulta em qualquer momento
- **Portabilidade:** Ficheiro JSON pode ser facilmente transferido ou copiado
- **Compatibilidade:** Formato aberto, legível em qualquer editor de texto

### Estrutura de um Registo

```json
{
  "id": 1,
  "timestamp": "2026-03-10T11:28:38.935339",
  "file_path": "/caminho/completo/musica.mp3",
  "file_name": "musica.mp3",
  "key": "E Major",
  "camelot": "7B",
  "bpm": 123,
  "duration": 60.0,
  "confidence": 0.9746
}
```

## Formatos de Áudio Suportados

O sistema suporta os seguintes formatos de ficheiro:
- MP3
- WAV
- FLAC
- OGG
- M4A
- Qualquer formato que a biblioteca librosa natively suporte

## Notação Camelot

O sistema utiliza a notação Camelot, padrão profissional para DJs:

### Componentes
- **Números (1-12):** Representam os 12 tons musicais (como um relógio)
- **Letra (A ou B):** 
  - `A` = Escala Menor (som mais sombrio, melancólico)
  - `B` = Escala Maior (som mais brilhante, alegre)

### Exemplos
- `8A` = A Menor
- `5B` = F Maior
- `12A` = C# Menor
- `1B` = B Maior

### Roda de Camelot (Compatibilidade Harmônica)

```
        12B    1B    2B
     11B  ════════  3B
   10B   MAIOR    4B
     9B  ════════  5B
        8B    7B    6B

         8A    7A    6A
       9A  MENOR    5A
     10A  ════════  4A
       11A  ════════  3A
         12A   1A    2A
```

**Regras de Compatibilidade:**
- **Mesma posição (8B ↔ 8A):** Mesma chave (major vs minor). Compatível 100%.
- **Vizinhos (8A ↔ 7A ou 8A ↔ 9A):** Um passo afastado na roda. Transição suave.
- **Diagonais (8A ↔ 8B):** Mesmo número, letras diferentes. Compatível (relativo).
- **Opostos (8A ↔ 2B):** Polos opostos. Evitar - choque harmônico.

## Requisitos Técnicos

### Dependências
- **Python:** 3.7 ou superior
- **librosa:** 0.10.0 ou superior (análise de áudio)
- **numpy, scipy, scikit-learn, audioread:** (instaladas automaticamente com librosa)

### Recursos de Sistema
- **RAM:** Mínimo 2 GB (recomendado 4 GB)
- **Espaço em Disco:** ~500 MB para instalação de dependências
- **Processador:** Qualquer processador moderno (análise pode ser lenta em processadores antigos)

### Performance

- **Primeira análise:** 30-60 segundos (librosa carrega modelos de ML)
- **Análises subsequentes:** 10-30 segundos por ficheiro
- **Operações de consulta (history, stats, export):** 1-2 segundos

## Limitações do MVP

Esta versão não inclui as seguintes funcionalidades:

**Não Implementadas:**
- Interface gráfica (GUI) - apenas CLI
- Organização automática de ficheiros em pastas
- Criação de playlists em formato M3U
- Análise em batch (múltiplos ficheiros simultâneos)
- Interpretação de acordes individuais
- Deteção de mudanças de chave dentro da música
- Recomendação inteligente baseada em histórico

**Limitações Conhecidas:**
- A detecção de chave é uma estimativa baseada em análise de frequência. Precisão típica: 85-95%. Nem sempre corresponde à percepção de ouvido humano.
- A biblioteca librosa é pesada (~200 MB). Para ambientes com espaço limitado, considere instalar sem dependências opcionais.
- Análise de ficheiros corrompidos pode causar falhas.

## Roadmap Futuro

### Versão 1.2 (Planeada)
- Interface gráfica básica em PyQt5
- Suporte para lote de análises (batch processing)
- Melhor tratamento de erros

### Versão 2.0 (Considerada)
- Organização automática por chave
- Extração de acordes musicais
- Base de dados SQLite (em vez de JSON)
- API REST para integração

## Utilização de Exemplo

### Cenário: Construir uma Playlist Harmônica

```bash
# 1. Analisar primeira música
./run.sh analyze rock_track.mp3
# Resultado: Camelot 8A, BPM 120
# Guardar: s

# 2. Ver chaves compatíveis
./run.sh mixes 8A
# Resultado: 7A, 8A, 9A, 8B são compatíveis

# 3. Analisar segunda música
./run.sh analyze dance_track.mp3
# Resultado: Camelot 7A, BPM 128
# Guardar: s

# 4. Verificar se combinam bem
./run.sh compatible 8A 7A
# Resultado: Sim! São compatíveis

# 5. Ver estatísticas das análises
./run.sh stats
# Resultado: Análises guardadas, BPM médio, etc

# 6. Exportar para externa análise
./run.sh export
# Ficheiro: data/analyses_export.csv
```

## Notas Técnicas

### Performance
A primeira análise de um ficheiro pode levar 30-60 segundos enquanto o librosa carrega os modelos de machine learning. Análises subsequentes são mais rápidas (10-30 segundos).

### Precisão
A detecção de tonalidade utiliza análise de espectro de frequência. Isto funciona bem para a maioria das músicas, mas:
- Músicas experimentais ou atonal podem gerar resultados imprecisos
- Hip-hop com samples pode confundir o detector
- Precisão típica: 85-95%

### Requisitos de Internete
Não. O sistema funciona completamente offline. Librosa realiza análise local sem acesso à rede.

## Suporte e Contribuições

Este é um projeto educacional e MVP. Para questões técnicas consulte:

- **Documentação Técnica:** [IMPLEMENTACAO_PERSISTENCIA.md](IMPLEMENTACAO_PERSISTENCIA.md)
- **Conformidade:** [MVP_etapa_1.md](MVP_etapa_1.md)
- **Auditoria:** [AUDITORIA_TECNICA.md](AUDITORIA_TECNICA.md)

## Licença

Este projeto é disponibilizado sob a **Licença MIT**.

Você é livre para:
- Usar o código para fins académicos ou comerciais
- Modificar e distribuir
- Incluir em outros projectos

**Requerimentos:** Incluir notificação de licença e aviso de isenção de responsabilidade.

Para mais detalhes, consulte o ficheiro LICENSE (se presente).

---

**Informações do Projeto:**
- **Versão:** 1.1
- **Data de Última Atualização:** 10 de Março de 2026
- **Estado:** MVP Funcional
- **Linguagem:** Python 3.7+
- **Dependência Principal:** librosa>=0.10.0
