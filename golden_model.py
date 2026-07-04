import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import math

    return


@app.function
def saturate_q412(val):
    MAX_LIMIT = 32767
    MIN_LIMIT = -32768
    if val > MAX_LIMIT:
        return MAX_LIMIT
    elif val < MIN_LIMIT:
        return MIN_LIMIT
    else:
        return int(val)


@app.function
def to_c2_16bits(val):
    if val < 0:
        return 65536 + val
    return val


@app.cell
def _():
    print("="*60)
    print(" GOLDEN MODEL - CONTROLADOR PID (Matemática Ideal -> Q4.12)")
    print("="*60)

    print("\n--- Parámetros del Controlador ---")

    # K  = float(input("K: "))
    # b  = float(input("b: "))
    # Ti = float(input("Ti: "))
    # Td = float(input("Td: "))
    # N  = float(input("N: "))
    # T  = float(input("T: "))

    K  = 1
    b  = 1
    Ti = 2
    Td = 1
    N  = 1
    T  = 0.2

    coef_I  = (K * T) / Ti
    coef_D1 = Td / (Td + N * T)
    coef_D2 = (K * Td * N) / (Td + N * T)

    uc_prev = 0.0
    y_prev  = 0.0
    I_prev  = 0.0
    D_prev  = 0.0

    ciclos = int(input("\nNúmero de ciclos: "))

    print("\n" + "="*60)
    for k in range(1, ciclos + 1):
        print(f"\n[ CICLO {k} ]")
        uc = float(input(f"Uc para k={k}: "))
        y  = float(input(f"Y para k={k} : "))

        P_float = K * (b * uc - y)
        I_inc_float = coef_I * (uc_prev - y_prev)
        I_float = I_prev + I_inc_float
        D1_float = coef_D1 * D_prev 
        D2_float = - coef_D2 * (y - y_prev)

        D_float = D1_float + D2_float

        P_q412 = saturate_q412(round(P_float * 4096))
        I_q412 = saturate_q412(round(I_float * 4096))
        D1_q412 = saturate_q412(round(D1_float * 4096))
        D2_q412 = saturate_q412(round(D2_float * 4096))

        D_q412 = saturate_q412(round(D_float * 4096))

        PID_final_q412 = P_q412 + I_q412 + D_q412

        print("\n  --- Resultados Q4.12 (Enteros con signo) ---")
        print(f"  P(k)  = {P_q412 & 0xFFFF}")
        print(f"  I(k)  = {I_q412 & 0xFFFF}")
        print(f"  D1(k)  = {D1_q412 & 0xFFFF}")
        print(f"  D2(k)  = {D2_q412 & 0xFFFF}")
        print(f"  D(k)  = {D_q412 & 0xFFFF}")
        print(f"  -----------------------")
        print(f"  U(k) Final = {PID_final_q412 & 0xFFFF}")

        if P_q412 + I_q412 + D_q412 > 32767 or P_q412 + I_q412 + D_q412 < -32768:
            print("La salida del PID ha saturado")

        uc_prev = uc
        y_prev  = y
        I_prev  = I_float
        D_prev  = D_float

    print("\n" + "="*60)
    print(" SIMULACIÓN FINALIZADA")
    print("="*60)
    return


if __name__ == "__main__":
    app.run()
