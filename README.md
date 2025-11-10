# AuthLog Auto Reporter 🔐

Herramienta en línea de comandos para analizar ficheros de `auth.log` (SSH / sudo / autenticación) y generar un informe en **Markdown** listo para pegar en un ticket del SOC o en un informe técnico.

Ayuda a responder rápidamente a alertas de **fuerza bruta**, **intentos de login fallidos** o accesos sospechosos en servidores Linux.

---

## ✨ Características

- 📂 Lee ficheros de log tipo `auth.log` (SSH, sudo, etc.).
- 📊 Calcula:
  - Top IPs con intentos de login fallidos.
  - Usuarios más atacados.
  - Usuarios con logins aceptados.
- 🧾 Genera un informe en Markdown con:
  - Fichero analizado.
  - Rango de fechas observado.
  - Tablas con IPs / usuarios / número de intentos.
  - Nota final para documentar el incidente en el ticket del SOC.

---

## 🚀 Uso rápido

```bash
# 1) Activar el entorno virtual (opcional)
source .venv/bin/activate

# 2) Ejecutar el script indicando el fichero de log
python authlog_reporter.py -i samples/auth.log


# AuthLog Auto Reporter

Informe generado automáticamente a partir del fichero:

- **Fichero analizado**: `samples/auth.log`
- **Periodo observado**: 2025-01-10 10:10:10 -> 2025-01-10 10:13:13

## Top IPs con intentos de login fallidos

| IP        | Intentos fallidos |
|---------- |-------------------|
| 1.2.3.4   | 1 |
| 5.6.7.8   | 1 |
| 10.0.0.5  | 1 |

## Usuarios más atacados (intentos fallidos)

| Usuario | Intentos fallidos |
|-------- |-------------------|
| test    | 1 |
| root    | 1 |
| admin   | 1 |

## Usuarios con logins aceptados

| Usuario | Logins aceptados |
|-------- |------------------|
| nacho  | 1 |

_Consejo:_ copia este informe en el ticket del SOC y añade detalles del caso
(alerta original, acciones de contención, bloqueo de IPs, etc.).
