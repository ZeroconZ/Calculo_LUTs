import marimo

__generated_with = "0.20.4"
app = marimo.App(
    width="medium",
    layout_file="layouts/Calculo_val_LUT.grid.json",
)


@app.cell
def _():
    import marimo as mo
    import numpy as np

    return mo, np


@app.cell
def _(K_form):
    K_form
    return


@app.cell
def _(b_form):
    b_form
    return


@app.cell
def _(Ti_form):
    Ti_form
    return


@app.cell
def _(Td_form):
    Td_form
    return


@app.cell
def _(N_form):
    N_form
    return


@app.cell
def _(T_form):
    T_form
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #LUTP
    """)
    return


@app.cell
def _(LUTP):
    LUTP
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #LUTI
    """)
    return


@app.cell
def _(LUTI):
    LUTI
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #LUTD1
    """)
    return


@app.cell
def _(LUTD1):
    LUTD1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #LUTD2
    """)
    return


@app.cell
def _(LUTD2):
    LUTD2
    return


@app.cell
def _(np):
    def dec_bin(numero, bits_entero=3, bits_decimal=12):
        signo = 1 if numero < 0 else 0
        num_abs = abs(numero)

        factor = 2 ** bits_decimal  

        valor_entero = round(num_abs * factor)

        max_val = (2 ** (bits_entero + bits_decimal)) - 1
        if valor_entero > max_val:
            print(f"Advertencia: El número {numero} excede la capacidad de la parte entera.")

        posicion_signo = bits_entero + bits_decimal
        valor_final = (signo << posicion_signo) | valor_entero

        total_bits = 1 + bits_entero + bits_decimal
        resultado = np.binary_repr(valor_final, width=total_bits)

        return resultado

    return (dec_bin,)


@app.cell
def _(mo):
    K_form = mo.ui.number(value = 1, label="K")
    b_form = mo.ui.number(value = 1, label="b")
    Ti_form = mo.ui.number(value = 1, label="Ti")
    Td_form = mo.ui.number(value = 0.1, label="Td")
    N_form = mo.ui.number(value = 10, label="N")
    T_form = mo.ui.number(value = 0.02, label="T")
    return K_form, N_form, T_form, Td_form, Ti_form, b_form


@app.cell
def _(K_form, N_form, T_form, Td_form, Ti_form, b_form):
    K = K_form.value
    b = b_form.value
    Ti = Ti_form.value
    Td = Td_form.value
    N = N_form.value
    T = T_form.value
    return K, N, T, Td, Ti, b


@app.cell
def _(mo, valores_LUTD1, valores_LUTD2, valores_LUTI, valores_LUTP):
    LUTP =  mo.ui.table(valores_LUTP())
    LUTI = mo.ui.table(valores_LUTI())
    LUTD1 = mo.ui.table(valores_LUTD1())
    LUTD2 = mo.ui.table(valores_LUTD2())

    LUTs = mo.hstack = ([LUTP, LUTI, LUTD1, LUTD2])
    return LUTD1, LUTD2, LUTI, LUTP


@app.cell
def _(K, b, dec_bin):
    def valores_LUTP():
        dict_LUT = {
            "00" : dec_bin(0),
            "01" : dec_bin(-K),
            "02" : dec_bin(K*b),
            "03" : dec_bin(K*b - K)
            }

        return dict_LUT

    return (valores_LUTP,)


@app.cell
def _(K, T, Ti, dec_bin):
    def valores_LUTI():
        dict_LUT = {
            "00" : dec_bin(0),
            "01" : dec_bin((-K*T)/(Ti)),
            "02" : dec_bin((K*T)/(Ti)),
            "03" : dec_bin(0)
            }

        return dict_LUT

    return (valores_LUTI,)


@app.cell
def _(N, T, Td, dec_bin):
    def valores_LUTD1():
        dict_LUT = {
            "00" : dec_bin(0),
            "01" : dec_bin((Td)/(Td + N*T)),
            }

        return dict_LUT

    return (valores_LUTD1,)


@app.cell
def _(K, N, T, Td, dec_bin):
    def valores_LUTD2():
        dict_LUT = {
            "00" : dec_bin(0),
            "01" : dec_bin((K*Td*N)/(Td + N*T)),
            "02" : dec_bin((-K*Td*N)/(Td + N*T)),
            "03" : dec_bin(0)
            }

        return dict_LUT

    return (valores_LUTD2,)


if __name__ == "__main__":
    app.run()
