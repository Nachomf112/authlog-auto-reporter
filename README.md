# 🔐 AuthLog Auto Reporter

> CLI en Python para analizar ficheros `auth.log` y generar informes en Markdown listos para tickets SOC.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Blue Team](https://img.shields.io/badge/Blue_Team-SOC-22c55e?style=for-the-badge)
![Auth Logs](https://img.shields.io/badge/Auth-Logs-ef4444?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## 📌 ¿Qué hace?

**AuthLog Auto Reporter** automatiza el análisis de logs de autenticación Linux y genera documentación lista para el SOC:

```
auth.log (SSH / sudo / autenticación)
              ↓
Análisis automático de IPs, usuarios y patrones
              ↓
Informe Markdown con tablas y resumen
              ↓
Listo para ticket SOC / informe de incidente
```

Ayuda a responder rápidamente a alertas de **fuerza bruta**, **intentos de login fallidos** o accesos sospechosos en servidores Linux.

---

## ✨ Características

- 📂 Lee ficheros de log tipo `auth.log` (SSH, sudo, etc.)
- 📊 Calcula automáticamente:
  - Top IPs con intentos de login fallidos
  - Usuarios más atacados
  - Usuarios con logins aceptados
- 🧾 Genera informe Markdown con:
  - Fichero analizado y rango de fechas
  - Tablas con IPs / usuarios / número de intentos
  - Nota final para documentar en el ticket SOC

---

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Nachomf112/authlog-auto-reporter.git
cd authlog-auto-reporter

# Activar entorno virtual (opcional pero recomendado)
python -m venv .venv
source .venv/bin/activate
```

No requiere dependencias externas — solo Python 3.10+ y librería estándar.

---

## ▶️ Uso

```bash
python authlog_reporter.py -i samples/auth.log
```

---

## 📄 Ejemplo de informe generado

```markdown
# AuthLog Auto Reporter

- **Fichero analizado**: `samples/auth.log`
- **Periodo observado**: 2025-01-10 10:10:10 → 2025-01-10 10:13:13

## Top IPs con intentos de login fallidos

| IP       | Intentos fallidos |
|----------|-------------------|
| 1.2.3.4  | 3                 |
| 5.6.7.8  | 1                 |
| 10.0.0.5 | 1                 |

## Usuarios más atacados

| Usuario | Intentos fallidos |
|---------|-------------------|
| root    | 3                 |
| admin   | 1                 |
| test    | 1                 |

## Usuarios con logins aceptados

| Usuario | Logins aceptados |
|---------|------------------|
| nacho   | 1                |

_Consejo: copia este informe en el ticket del SOC y añade detalles del caso._
```

---

## 📁 Estructura del proyecto

```
authlog-auto-reporter/
├── authlog_reporter.py   # Script principal
├── samples/
│   └── auth.log          # Log de ejemplo para pruebas
├── reports/              # Informes generados
└── README.md
```

---

## 🛡️ Casos de uso SOC

- ✅ Respuesta rápida ante alertas de fuerza bruta SSH
- ✅ Documentación de intentos de acceso para tickets IR
- ✅ Auditorías de accesos en servidores Linux
- ✅ Prácticas en laboratorio CTF / homelab

> ⚠️ **Aviso**: Usa esta herramienta únicamente sobre sistemas sobre los que tengas autorización.

---

## 🗺️ Roadmap

- [x] Análisis de IPs con intentos fallidos
- [x] Análisis de usuarios atacados y logins aceptados
- [x] Exportación a Markdown con tablas
- [ ] Soporte para otros formatos de log (journalctl, syslog)
- [ ] Integración con VirusTotal para reputación de IPs
- [ ] Alertas automáticas vía Wazuh
- [ ] Modo batch para analizar múltiples ficheros

---

## 👤 Autor

**Nacho Menárguez** — [ai.menarguez-ia.com](https://ai.menarguez-ia.com) · [LinkedIn](https://www.linkedin.com/in/ignaciomenarguezfernandez/)

---

<div align="center">
<sub>⚡ Parte del ecosistema Menárguez-IA · Blue Team & SOC Automation · 2026</sub>
</div>
