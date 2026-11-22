# Proyecto final ecuas
# José Andres López Rodas

# Importamos las bibliotecas
import numpy as np
import matplotlib.pyplot as plt

# Implementamos los métodos numéricos

# Método de euler

def euler(f, t0, tf, y0, h):

    N = round((tf - t0) / h)

    # Verificamos que el intervalo pueda dividirse
    # exactamente entre el tamaño del paso
    if not np.isclose(N * h, tf - t0):
        raise ValueError("El paso debe dividir exactamente el intervalo")

    # Generamos los valores del tiempo
    t = np.linspace(t0, tf, N + 1)

    # Reserva espacio para los valores aproximados
    y = np.zeros((N + 1,) + np.shape(y0))

    # Establece la condicion inicial
    y[0] = y0

    # Aplicamos el método de Euler iterativamente
    for i in range(N):

        y[i +1] = y[i] + h * f(t[i], y[i])
    return t, y

# definimos los parámetros:

# Primer problema: Enfriamiento de newton

Ta = 25.0       # Temperatura ambiente [°C]
T0 = 90.0       # Temperatura inicial [°C]
k = 0.2         # Constante de enfriamiento [1/min]

t0_newton = 0.0
tf_newton = 10.0

h_newton = 0.1

# Describimos la funcion que representa la ecuación diferencial:

def enfriamiento(t, T):

    return -k * (T - Ta)

# Solución analítica:

def solucion_newton(t):

    return Ta + (T0 - Ta) * np.exp(-k * t)


# Segundo problema: Circuito RC:

R = 1000.0  # Resistencia en ohms
C = 1000e-6  # Capacitancia en faradios
Vs = 5.0  # Voltaje en la fuente
V0 = 0.0  # Voltaje inicial

t0_rc = 0.0
tf_rc = 5.0

h_rc = 0.05

# Describimos la funcion que representa la ecuacion diferencial:

def circuito_rc(t, Vc):

    return (Vs - Vc) / (R * C)

# Solución analítica:

def solucion_rc(t):

    return Vs + (V0 - Vs) * np.exp(-t / (R * C))

# Función para calcular los errores:

def calcular_error(exacta, aproximada):

    return np.abs(exacta - aproximada)

# Resolución del enfriamiento de newton

# Solución numérica mediante Euler

t_N, T_Euler = euler(
    enfriamiento, t0_newton, tf_newton, T0, h_newton
)

# Solución analítica:

T_exacta = solucion_newton(t_N)

# Error absoluto

error_N = calcular_error(T_exacta, T_Euler)

# Resolución del circuito RC:

# Solución mediante Euler:

t_RC, V_Euler = euler(
    circuito_rc, t0_rc, tf_rc, V0, h_rc
)

# Solución analítica

V_exacta = solucion_rc(t_RC)

# Error absoluto

error_RC = calcular_error(V_exacta, V_Euler)

# Tablas de resultados

# Función para imprimir tablas:

def imprimir_tabla(nombre, t, exacta, aproximada, error):

    print("\n")
    print("-" * 75)
    print(nombre)
    print("-" * 75)

    print(
        f"{'Tiempo':>12} | " 
        f"{'Analitica':>15} | "
        f"{'Euler':>15} | "
        f"{'Error absoluto':>15}"
    )

    print("-" * 75)

    for i in range(len(t)):

        print(
            f"{t[i]:12.4f} | "
            f"{exacta[i]:15.6f} | "
            f"{aproximada[i]:15.6f} | "
            f"{error[i]:15.8f}"
        )


# Tabla del enfriamiento de Newton:

imprimir_tabla(
    "ENFRIAMIENTO DE NEWTON",
    t_N,
    T_exacta,
    T_Euler,
    error_N
)

# Tabla del circuito RC:

imprimir_tabla(
    "CIRCUITO RC",
    t_RC,
    V_exacta,
    V_Euler,
    error_RC
)

# Resumen de errores:

def imprimir_resumen(nombre, error):
    print("\n")
    print("=" * 60)
    print(nombre)
    print("=" * 60)

    print(f"Error maximo: {np.max(error):.8f}")

    print(f"Error final:  {error[-1]:.8f}")

# Errores del enfriamiento:

imprimir_resumen(
    "ERROR DEL ENFRIAMIENTO DE NEWTON",
    error_N
)

# Errores del circuito RC:

imprimir_resumen(
    "ERROR DEL CIRCUITO RC",
    error_RC
)

# Gráficas:
# Enfriamiento de newton:
plt.figure(figsize=(10, 6))

plt.plot(
    t_N,
    T_exacta,
    label="Solucion analitica",
    linewidth=2
)

plt.plot(
    t_N,
    T_Euler,
    "--",
    label="Metodo de Euler"
)

plt.xlabel("Tiempo [min]")
plt.ylabel("Temperatura [°C]")

plt.title("Enfriamiento de Newton")

plt.legend()
plt.grid()

plt.tight_layout()

plt.savefig("Enfriamiento_Newton.png", dpi=300)

plt.show()

#Circuito RC:
plt.figure(figsize=(10, 6))

plt.plot(
    t_RC,
    V_exacta,
    label="Solucion analitica",
    linewidth=2
)

plt.plot(
    t_RC,
    V_Euler,
    "--",
    label="Metodo de Euler"
)

plt.xlabel("Tiempo [s]")
plt.ylabel("Voltaje [V]")

plt.title("Carga de un capacitor en un circuito RC")

plt.legend()
plt.grid()

plt.tight_layout()

plt.savefig("Circuito_RC.png", dpi=300)

plt.show()

# Gráficas de error absoluto:
# Error de enfriamiento de Newton:
plt.figure(figsize=(10, 6))

plt.plot(t_N, error_N)

plt.xlabel("Tiempo [min]")
plt.ylabel("Error absoluto [°C]")

plt.title("Error absoluto - Enfriamiento de Newton")

plt.grid()

plt.tight_layout()

plt.savefig("Error_Newton.png", dpi=300)

plt.show()

# Error del circuito RC:
plt.figure(figsize=(10, 6))

plt.plot(t_RC, error_RC)

plt.xlabel("Tiempo [s]")
plt.ylabel("Error absoluto [V]")

plt.title("Error absoluto - Circuito RC")

plt.grid()

plt.tight_layout()

plt.savefig("Error_RC.png", dpi=300)

plt.show()


# Análisis de convergencia:
# Tamaños de paso para Newton

pasos_N = [1.0, 0.5, 0.2, 0.1, 0.05]


# Tamaños de paso para el circuito RC

pasos_RC = [1.0, 0.5, 0.25, 0.1, 0.05]


# Función para analizar convergencia

def analizar_convergencia(f, solucion, t0, tf, y0, pasos):

    resultados = []

    for h in pasos:

        # Solucion numerica

        t, y = euler(f, t0, tf, y0, h)

        # Solucion analitica

        exacta = solucion(t)

        # Error maximo

        error_maximo = np.max(np.abs(exacta - y))

        resultados.append([h, error_maximo])

    return np.array(resultados)

# Convergencia de Newton:

convergencia_N = analizar_convergencia(
    enfriamiento,
    solucion_newton,
    t0_newton,
    tf_newton,
    T0,
    pasos_N
)

# Convergencia del circuito RC:
convergencia_RC = analizar_convergencia(
    circuito_rc,
    solucion_rc,
    t0_rc,
    tf_rc,
    V0,
    pasos_RC
)

# Tablas de convergencia:
def imprimir_convergencia(nombre, resultados):

    print("\n")
    print("=" * 55)
    print(nombre)
    print("=" * 55)

    print(f"{'Paso h':>15} | {'Error maximo':>20}")

    print("-" * 55)

    for fila in resultados:

        print(
            f"{fila[0]:15.5f} | "
            f"{fila[1]:20.10f}"
        )


# Tabla de convergencia de Newton

imprimir_convergencia(
    "CONVERGENCIA - ENFRIAMIENTO DE NEWTON",
    convergencia_N
)


# Tabla de convergencia del circuito RC

imprimir_convergencia(
    "CONVERGENCIA - CIRCUITO RC",
    convergencia_RC
)

#Gráficas de convergencia:

# Newton

plt.figure(figsize=(8, 6))

plt.loglog(
    convergencia_N[:, 0],
    convergencia_N[:, 1],
    "o-"
)

plt.xlabel("Tamano del paso h [min]")
plt.ylabel("Error maximo")

plt.title("Convergencia del metodo de Euler - Newton")

plt.grid(True, which="both")

plt.tight_layout()

plt.savefig("Convergencia_Newton.png", dpi=300)

plt.show()


# Circuito RC

plt.figure(figsize=(8, 6))

plt.loglog(
    convergencia_RC[:, 0],
    convergencia_RC[:, 1],
    "o-"
)

plt.xlabel("Tamano del paso h [s]")
plt.ylabel("Error maximo")

plt.title("Convergencia del metodo de Euler - Circuito RC")

plt.grid(True, which="both")

plt.tight_layout()

plt.savefig("Convergencia_RC.png", dpi=300)

plt.show()


# Exportación de resultados:
# Newton

np.savetxt(
    "Tabla_Newton.csv",
    np.column_stack((
        t_N,
        T_exacta,
        T_Euler,
        error_N
    )),
    delimiter=",",
    header="Tiempo,Analitica,Euler,Error_Absoluto",
    comments=""
)


# Circuito RC

np.savetxt(
    "Tabla_RC.csv",
    np.column_stack((
        t_RC,
        V_exacta,
        V_Euler,
        error_RC
    )),
    delimiter=",",
    header="Tiempo,Analitica,Euler,Error_Absoluto",
    comments=""
)


# Convergencia Newton

np.savetxt(
    "Convergencia_Newton.csv",
    convergencia_N,
    delimiter=",",
    header="Paso,Error_Maximo",
    comments=""
)


# Convergencia RC

np.savetxt(
    "Convergencia_RC.csv",
    convergencia_RC,
    delimiter=",",
    header="Paso,Error_Maximo",
    comments=""
)

# Finalización (ALFIN :D):

print("\n")
print("=" * 60)
print("PROGRAMA FINALIZADO")
print("=" * 60)

print("Se generaron las siguientes graficas:")
print("- Enfriamiento_Newton.png")
print("- Circuito_RC.png")
print("- Error_Newton.png")
print("- Error_RC.png")
print("- Convergencia_Newton.png")
print("- Convergencia_RC.png")

print("\nSe generaron las siguientes tablas:")
print("- Tabla_Newton.csv")
print("- Tabla_RC.csv")
print("- Convergencia_Newton.csv")
print("- Convergencia_RC.csv")