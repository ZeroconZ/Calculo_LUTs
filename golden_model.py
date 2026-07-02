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


@app.cell
def _():
    print("="*60)
    print(" GOLDEN MODEL - CONTROLADOR PID (Matemática Ideal -> Q4.12)")
    print("="*60)

    # 1. SOLICITUD DE PARÁMETROS DEL SISTEMA
    print("\n--- Parámetros del Controlador ---")
    K  = float(input("Ganancia Proporcional (K): "))
    b  = float(input("Peso del Setpoint (b) [Ej: 1.0]: "))
    Ti = float(input("Tiempo Integral (Ti) [Segundos]: "))
    Td = float(input("Tiempo Derivativo (Td) [Segundos]: "))
    N  = float(input("Coeficiente del Filtro Derivativo (N) [Ej: 10]: "))
    T  = float(input("Periodo de Muestreo (T) [Segundos]: "))

    # 2. CÁLCULO DE COEFICIENTES DE LAS ECUACIONES EN DIFERENCIAS
    # Coeficientes exactos basados en la aproximación Backward Euler
    coef_I  = (K * T) / Ti
    coef_D1 = Td / (Td + N * T)
    coef_D2 = (K * Td * N) / (Td + N * T)

    # 3. VARIABLES DE ESTADO (Memoria del sistema)
    uc_prev = 0.0
    y_prev  = 0.0
    I_prev  = 0.0
    D_prev  = 0.0

    # 4. BUCLE DE CÁLCULO
    ciclos = int(input("\n¿Cuántos ciclos de cálculo deseas simular?: "))

    print("\n" + "="*60)
    for k in range(1, ciclos + 1):
        print(f"\n[ CICLO {k} ]")
        uc = float(input(f"  -> Introduce Setpoint (Uc) para k={k}: "))
        y  = float(input(f"  -> Introduce Feedback (Y) para k={k} : "))

        # --- CÁLCULO MATEMÁTICO IDEAL (Punto Flotante) ---
    
        # Acción Proporcional: P(k) = K * (b*Uc(k) - Y(k))
        P_float = K * (b * uc - y)

        # Acción Integral: I(k) = I(k-1) + (K*T/Ti) * (Uc(k-1) - Y(k-1))
        # Nota: Utiliza el error retrasado (k-1) como hace tu FPGA con Delay_Uc y Delay_Y
        I_inc_float = coef_I * (uc_prev - y_prev)
        I_float = I_prev + I_inc_float

        # Acción Derivativa: D(k) = c1*D(k-1) - c2*(Y(k) - Y(k-1))
        D_float = coef_D1 * D_prev - coef_D2 * (y - y_prev)

        # --- CONVERSIÓN A HARDWARE (Formato Q4.12 y Saturación Individual) ---
        # Multiplicamos por 2^12 (4096), redondeamos al entero más cercano y saturamos
        P_q412 = saturate_q412(round(P_float * 4096))
        I_q412 = saturate_q412(round(I_float * 4096))
        D_q412 = saturate_q412(round(D_float * 4096))

        # --- SUMADOR FINAL (Sin saturación) ---
        PID_final_q412 = P_q412 + I_q412 + D_q412

        # --- MOSTRAR RESULTADOS ---
        print("\n  --- Resultados Q4.12 (Para comparar con FPGA) ---")
        print(f"  P(k)  = {P_q412}")
        print(f"  I(k)  = {I_q412}")
        print(f"  D(k)  = {D_q412}")
        print(f"  -----------------------")
        print(f"  U(k) Final = {PID_final_q412}")
    
        # Comprobador visual de desbordamiento en la suma final
        if PID_final_q412 > 32767 or PID_final_q412 < -32768:
            print("  ⚠️ ALERTA: ¡La suma final ha desbordado los 16 bits!")

        # --- ACTUALIZAR MEMORIA PARA EL SIGUIENTE CICLO ---
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
