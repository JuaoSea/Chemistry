#!/usr/bin/env python3
r"""
LED Analysis Parser for ORCA .out Files

Este script pode ser chamado de qualquer diretório, bastando passar caminhos
absolutos ou relativos para os arquivos .out.

Instalação (Windows):
  1. Coloque o led_parser.py em um diretório fixo, ex:
       C:\scripts\led_parser.py
  2. Crie em C:\Windows\System32 o arquivo led_parser.bat (como administrador) com conteúdo:
       @echo off
       python "C:\scripts\led_parser.py" %*
  3. Abra novo Prompt/PowerShell e chame:
       led_parser.bat COMPLEXO.out FRAGMENTO_1.out FRAGMENTO_2.out [...]

Instalação (Linux):
  1. Coloque o led_parser.py em um diretório fixo, ex:
       ~/scripts/led_parser.py
  2. Dê permissão de execução:
       chmod +x ~/scripts/led_parser.py
  3. (Opcional) Crie um link simbólico em um diretório do PATH, ex:
       sudo ln -s ~/scripts/led_parser.py /usr/local/bin/led_parser
  4. Agora pode chamar diretamente de qualquer pasta:
       led_parser COMPLEXO.out FRAGMENTO_1.out FRAGMENTO_2.out [...]
     ou, se não tiver feito o link simbólico:
       python ~/scripts/led_parser.py COMPLEXO.out FRAGMENTO_1.out FRAGMENTO_2.out [...]

O script detecta automaticamente o arquivo complexo (sumário LED) e fragmentos,
calcula:
  - ΔE_el-prep^ref
  - E_elstat^ref
  - E_exch^ref
  - ΔE_non-dispersion^C-CCSD
  - E_dispersion^C-CCSD
  - ΔE_T^C-(T)
  - Sum (ΔE_total)
  - E_dispersion^C-CCSD / ΔE_total
Convertendo de Hartree para kcal/mol. Trata termos ausentes como zero.
"""

import re
import sys
import argparse
from pathlib import Path

# Conversão: 1 Hartree (Eh) -> kcal/mol
AH_TO_KCAL = 627.5095

# Padrões regex para extrair termos LED (case-insensitive)
PATTERNS = {
    'intra_ref': re.compile(r"Intra fragment\s+(\d+)\s+\(REF\.\)\s+([-\d\.Ee+]+)", re.IGNORECASE),
    'electrostatics': re.compile(r"Electrostatics \(REF\.\)\s+([-\d\.Ee+]+)", re.IGNORECASE),
    'exchange': re.compile(r"Exchange \(REF\.\)\s+([-\d\.Ee+]+)", re.IGNORECASE),
    'disp_strong_block': re.compile(
        r"FINAL SUMMARY DLPNO-CCSD ENERGY DECOMPOSITION[\s\S]*?Dispersion \(strong pairs\)\s+([-\d\.Ee+]+)",
        re.IGNORECASE),
    'disp_weak_block': re.compile(
        r"FINAL SUMMARY DLPNO-CCSD ENERGY DECOMPOSITION[\s\S]*?Dispersion \(weak pairs\)\s+([-\d\.Ee+]+)",
        re.IGNORECASE),
    'non_disp_strong': re.compile(r"Non dispersion \(strong pairs\)\s+([-\d\.Ee+]+)", re.IGNORECASE),
    'non_disp_weak': re.compile(r"Non dispersion \(weak pairs\)\s+([-\d\.Ee+]+)", re.IGNORECASE),
    'triples': re.compile(r"Triples Correction\s*\(T\)\s*\.\.\.\s*([-\d\.Ee+]+)", re.IGNORECASE),
    'E0': re.compile(r"^\s*E\(0\)\s*\.*\s*([-\d\.Ee+]+)", re.MULTILINE | re.IGNORECASE),
    'E_CORR_corr': re.compile(r"^\s*E\(CORR\)\(corrected\)\s*\.*\s*([-\d\.Ee+]+)", re.MULTILINE | re.IGNORECASE),
}

def search_float(pattern: re.Pattern, text: str) -> float:
    matches = list(pattern.finditer(text))
    if not matches:
        return 0.0
    try:
        return float(matches[-1].group(1))
    except Exception:
        return 0.0

def parse_file(path: Path) -> dict:
    text = path.read_text(errors='ignore')
    data = {}
    if 'FINAL SUMMARY DLPNO-CCSD ENERGY DECOMPOSITION' in text:
        data['type'] = 'complex'
        data['intra_ref'] = {int(m.group(1)): float(m.group(2))
                             for m in PATTERNS['intra_ref'].finditer(text)}
        data['E_elstat'] = search_float(PATTERNS['electrostatics'], text)
        data['E_exch'] = search_float(PATTERNS['exchange'], text)
        data['E_disp'] = (
            search_float(PATTERNS['disp_strong_block'], text) +
            search_float(PATTERNS['disp_weak_block'], text)
        )
        data['non_disp_total'] = (
            search_float(PATTERNS['non_disp_strong'], text) +
            search_float(PATTERNS['non_disp_weak'], text)
        )
        data['T_complex'] = search_float(PATTERNS['triples'], text)
    else:
        data['type'] = 'fragment'
        data['E0'] = search_float(PATTERNS['E0'], text)
        data['E_CORR_corr'] = search_float(PATTERNS['E_CORR_corr'], text)
        data['T_frag'] = search_float(PATTERNS['triples'], text)
    return data

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parser LED ORCA .out files')
    parser.add_argument('files', metavar='FILE', nargs='+',
                        help='Arquivos ORCA (.out), complexo e fragmentos')
    args = parser.parse_args()

    parsed = {}
    complex_file = None
    fragment_files = []

    for f in args.files:
        path = Path(f)
        if not path.exists():
            sys.exit(f"Erro: arquivo não encontrado -> {path}")

        data = parse_file(path)
        parsed[path] = data

        if data['type'] == 'complex':
            complex_file = path
        else:
            fragment_files.append(path)

    if complex_file is None or not fragment_files:
        sys.exit('Erro: não detectei arquivo complexo ou fragmentos corretamente.')

    comp = parsed[complex_file]

    # ---- Cálculos em Hartree ----
    dE_el_prep = sum(
        comp['intra_ref'].get(i+1, 0.0) - parsed[frag]['E0']
        for i, frag in enumerate(fragment_files)
    )

    sum_E_CORR = sum(parsed[frag]['E_CORR_corr'] for frag in fragment_files)
    dE_non_disp = comp['non_disp_total'] - sum_E_CORR

    E_disp = comp['E_disp']
    E_elstat = comp['E_elstat']
    E_exch = comp['E_exch']

    T_complex = comp['T_complex']
    sum_T_frag = sum(parsed[frag]['T_frag'] for frag in fragment_files)
    dE_T = T_complex - sum_T_frag

    # ---- Converte para kcal/mol ----
    dE_el_prep_kcal = dE_el_prep * AH_TO_KCAL
    E_elstat_kcal   = E_elstat * AH_TO_KCAL
    E_exch_kcal     = E_exch * AH_TO_KCAL
    dE_non_disp_kcal = dE_non_disp * AH_TO_KCAL
    E_disp_kcal     = E_disp * AH_TO_KCAL
    dE_T_kcal       = dE_T * AH_TO_KCAL

    # Soma total (em kcal/mol)
    dE_total_kcal = (
        dE_el_prep_kcal +
        E_elstat_kcal +
        E_exch_kcal +
        dE_non_disp_kcal +
        E_disp_kcal +
        dE_T_kcal
    )

    # ---- Razão usando valores em kcal/mol ----
    if abs(dE_total_kcal) > 1e-12:
        ratio_disp_total = E_disp_kcal / dE_total_kcal
        ratio_disp_total_percent = ratio_disp_total * 100
    else:
        ratio_disp_total = None

    # ---- Impressão ----
    print(f"{'Contribuição':30s} {'Hartree':>12s} {'kcal/mol':>12s}")
    table = [
        ('Delta E_el-prep^ref', dE_el_prep, dE_el_prep_kcal),
        ('E_elstat^ref', E_elstat, E_elstat_kcal),
        ('E_exch^ref', E_exch, E_exch_kcal),
        ('Delta E_non-disp (C-CCSD)', dE_non_disp, dE_non_disp_kcal),
        ('E_dispersion (C-CCSD)', E_disp, E_disp_kcal),
        ('Delta E_T (C-(T))', dE_T, dE_T_kcal),
        ('Soma total', dE_total_kcal / AH_TO_KCAL, dE_total_kcal),
    ]

    for label, hart, kcal in table:
        print(f"{label:30s} {hart:12.6f} {kcal:12.2f}")

    if ratio_disp_total is not None:
        print("\nRazões (usando valores em kcal/mol):")
        print(f"{'E_dispersion / Soma total':30s} {ratio_disp_total:12.6f} ({ratio_disp_total_percent:6.2f} %)")
    else:
        print("\nRazões:")
        print(f"{'E_dispersion / Soma total':30s} N/A (divisão por zero)")

    # ---- Salvamento no arquivo ----
    output_file = Path.cwd() / "led_results.txt"

    lines = ["Contribuição                         Hartree      kcal/mol"]
    for label, hart, kcal in table:
        lines.append(f"{label:30s} {hart:12.6f} {kcal:12.2f}")

    if ratio_disp_total is not None:
        lines.append(f"E_dispersion / Soma total           {ratio_disp_total:12.6f} ({ratio_disp_total_percent:6.2f} %)")
    else:
        lines.append("E_dispersion / Soma total           N/A (divisão por zero)")

    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nResultados salvos em: {output_file}")
