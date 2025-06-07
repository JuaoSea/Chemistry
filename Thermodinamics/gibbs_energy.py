def verificar_espontaneidade(entalpia, entropia, temperatura):
    # Converte entalpia de kJ/mol para J/mol
    entalpia_j = entalpia * 1000
    delta_s_t = entropia - (entalpia_j / temperatura)
    espontanea = delta_s_t > 0
    return delta_s_t, espontanea

if __name__ == "__main__":
    entalpia = float(input("Digite a variação de entalpia (ΔH) em kJ/mol: "))
    entropia = float(input("Digite a variação de entropia (ΔS) em J/(mol·K): "))
    temperatura = float(input("Digite a temperatura (T) em Kelvin: "))

    delta_s_t, espontanea = verificar_espontaneidade(entalpia, entropia, temperatura)
    print(f"ΔS_T = {delta_s_t:.4f} J/(mol·K)")
    if espontanea:
        print("A reação é espontânea.")
    else:
        print("A reação NÃO é espontânea.")