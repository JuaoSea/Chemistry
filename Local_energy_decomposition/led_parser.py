import re
import argparse
from pathlib import Path

def parse_led_complex(output_text):
    data = {}
    ref_matches = re.findall(r"Intra fragment\s+\d+ \(REF\.\)\s+([-+]?\d*\.\d+)", output_text)
    if ref_matches:
        data['intra_frag_refs'] = list(map(float, ref_matches))

    me = re.search(r"Electrostatics \(REF\.\)\s+([-+]?\d*\.\d+)", output_text)
    mx = re.search(r"Exchange \(REF\.\)\s+([-+]?\d*\.\d+)", output_text)
    if me and mx:
        data['E_elstat_ref'] = float(me.group(1))
        data['E_exch_ref'] = float(mx.group(1))

    ds = re.search(r"Dispersion \(strong pairs\)\s+([-+]?\d*\.\d+)", output_text)
    dw = re.search(r"Dispersion \(weak pairs\)\s+([-+]?\d*\.\d+)", output_text)
    if ds and dw:
        data['disp_strong'] = float(ds.group(1))
        data['disp_weak'] = float(dw.group(1))

    nds = re.search(r"Non dispersion \(strong pairs\)\s+([-+]?\d*\.\d+)", output_text)
    ndw = re.search(r"Non dispersion \(weak pairs\)\s+([-+]?\d*\.\d+)", output_text)
    if nds and ndw:
        data['non_disp_strong'] = float(nds.group(1))
        data['non_disp_weak'] = float(ndw.group(1))

    tc = re.search(r"Triples Correction \(T\)\s+(?:\.\.\.\s+)?([-+]?\d*\.\d+)", output_text)
    if tc:
        data['T_complex'] = float(tc.group(1))

    corr_total = re.search(r"E\(CORR\)\(corrected\)\s+\.\.\.\s+([-+]?\d*\.\d+)", output_text)
    if corr_total:
        data['E_CORR_complex'] = float(corr_total.group(1))

    return data

def parse_fragment(output_text):
    data = {}
    e0 = re.search(r"E\(0\)\s+\.\.\.\s+([-+]?\d*\.\d+)", output_text)
    if e0:
        data['E0'] = float(e0.group(1))

    corr = re.search(r"E\(CORR\)\(corrected\)\s+\.\.\.\s+([-+]?\d*\.\d+)", output_text)
    if corr:
        data['E_CORR_corrected'] = float(corr.group(1))

    tc = re.search(r"Triples Correction \(T\)\s+\.\.\.\s+([-+]?\d*\.\d+)", output_text)
    if tc:
        try:
            data['T_frag'] = float(tc.group(1))
        except ValueError:
            pass

    return data

def hartree_to_kcalmol(val):
    return val * 627.5095

def main():
    parser = argparse.ArgumentParser(description="Parse ORCA LED output and compute LED contributions.")
    parser.add_argument("--complex", required=True, type=Path, help="ORCA output file for complex LED calculation")
    parser.add_argument("--frag", required=True, nargs='+', type=Path, help="ORCA output file(s) for fragment LED calculations")
    args = parser.parse_args()

    text_complex = args.complex.read_text()
    comp = parse_led_complex(text_complex)
    frags = [parse_fragment(p.read_text()) for p in args.frag]

    E0_sum = sum(f.get('E0', 0.0) for f in frags)
    E_corr_sum = sum(f.get('E_CORR_corrected', 0.0) for f in frags)
    T_frag_sum = sum(f.get('T_frag', 0.0) for f in frags)

    intra_ref_sum = sum(comp.get('intra_frag_refs', []))
    delta_E_el_prep = intra_ref_sum - E0_sum

    E_disp = comp.get('disp_strong', 0.0) + comp.get('disp_weak', 0.0)
    non_disp_sum = comp.get('non_disp_strong', 0.0) + comp.get('non_disp_weak', 0.0)

    delta_E_C_CCS_non_disp = non_disp_sum - E_corr_sum
    delta_E_C_T_int = comp.get('T_complex', 0.0) - T_frag_sum

    total_int = (
        delta_E_el_prep +
        comp.get('E_elstat_ref', 0.0) +
        comp.get('E_exch_ref', 0.0) +
        delta_E_C_CCS_non_disp +
        delta_E_C_T_int +
        E_disp
    )

    print("LED Contributions (Hartree):")
    print(f"Delta E_el-prep (ref): {delta_E_el_prep:.6f}")
    print(f"E_elstat (ref): {comp.get('E_elstat_ref', 0.0):.6f}")
    print(f"E_exch (ref): {comp.get('E_exch_ref', 0.0):.6f}")
    print(f"Delta E_C-CCSD non-disp: {delta_E_C_CCS_non_disp:.6f}")
    print(f"Delta E_C-(T) int: {delta_E_C_T_int:.6f}")
    print(f"E_dispersion: {E_disp:.6f}")
    print(f"Sum of LED terms: {total_int:.6f}\n")

    print("LED Contributions (kcal/mol):")
    terms = [
        ('Delta E_el-prep (ref)', delta_E_el_prep),
        ('E_elstat (ref)', comp.get('E_elstat_ref', 0.0)),
        ('E_exch (ref)', comp.get('E_exch_ref', 0.0)),
        ('Delta E_C-CCSD non-disp', delta_E_C_CCS_non_disp),
        ('Delta E_C-(T) int', delta_E_C_T_int),
        ('E_dispersion', E_disp),
        ('Sum of LED terms', total_int)
    ]
    for name, val in terms:
        print(f"{name}: {hartree_to_kcalmol(val):.2f}")

if __name__ == "__main__":
    main()

''''''

# python led_parser.py --complex complexo.out --frag frag1.out frag2.out

''''''