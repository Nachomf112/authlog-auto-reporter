#!/usr/bin/env python3
"""
AuthLog Auto Reporter v0.1
Analiza logs tipo /var/log/auth.log y genera un informe en Markdown
con intentos de login fallidos y aceptados.
"""

import argparse
from collections import Counter
from datetime import datetime
import pathlib
import re
from textwrap import dedent

# Regex muy sencilla para líneas de sshd
FAILED_RE = re.compile(
    r"^(?P<month>\w{3})\s+(?P<day>\d+)\s(?P<time>\d{2}:\d{2}:\d{2})\s"
    r"(?P<host>\S+)\s(?P<proc>sshd\S*):\sFailed password for (invalid user )?"
    r"(?P<user>\S+) from (?P<ip>\S+)"
)

ACCEPT_RE = re.compile(
    r"^(?P<month>\w{3})\s+(?P<day>\d+)\s(?P<time>\d{2}:\d{2}:\d{2})\s"
    r"(?P<host>\S+)\s(?P<proc>sshd\S*):\sAccepted password for "
    r"(?P<user>\S+) from (?P<ip>\S+)"
)

MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AuthLog Auto Reporter – resumen de intentos de login en Linux"
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Ruta al fichero de log (ej: /var/log/auth.log)"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Ruta del informe Markdown de salida (por defecto reports/authlog_report_YYYYMMDD-HHMMSS.md)"
    )
    return parser.parse_args()


def parse_datetime(month: str, day: str, time_str: str) -> datetime:
    now = datetime.now()
    return datetime(
        year=now.year,
        month=MONTHS.get(month, now.month),
        day=int(day),
        hour=int(time_str[0:2]),
        minute=int(time_str[3:5]),
        second=int(time_str[6:8]),
    )


def analyze_log(path: pathlib.Path):
    failed_by_ip = Counter()
    failed_by_user = Counter()
    accepted_by_user = Counter()
    first_dt = None
    last_dt = None

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m_fail = FAILED_RE.match(line)
            m_ok = ACCEPT_RE.match(line)

            if m_fail:
                dt = parse_datetime(
                    m_fail["month"], m_fail["day"], m_fail["time"]
                )
                ip = m_fail["ip"]
                user = m_fail["user"]

                failed_by_ip[ip] += 1
                failed_by_user[user] += 1

            elif m_ok:
                dt = parse_datetime(
                    m_ok["month"], m_ok["day"], m_ok["time"]
                )
                ip = m_ok["ip"]
                user = m_ok["user"]

                accepted_by_user[user] += 1
            else:
                continue

            if first_dt is None:
                first_dt = dt
            last_dt = dt

    return {
        "failed_by_ip": failed_by_ip,
        "failed_by_user": failed_by_user,
        "accepted_by_user": accepted_by_user,
        "first_dt": first_dt,
        "last_dt": last_dt,
    }


def render_markdown(stats, log_path: pathlib.Path) -> str:
    first_dt = stats["first_dt"]
    last_dt = stats["last_dt"]

    period = "N/A"
    if first_dt and last_dt:
        period = f"{first_dt} → {last_dt}"

    def table_from_counter(counter: Counter, col1: str, col2: str, limit: int = 10):
        lines = [f"| {col1} | {col2} |", "|---|---|"]
        for key, count in counter.most_common(limit):
            lines.append(f"| {key} | {count} |")
        if len(lines) == 2:
            lines.append("| (sin datos) | 0 |")
        return "\n".join(lines)

    md = dedent(f"""
    # AuthLog Auto Reporter

    Informe generado automáticamente a partir del fichero:

    - **Fichero analizado**: `{log_path}`
    - **Periodo observado**: {period}

    ## Top IPs con intentos de login fallidos

    {table_from_counter(stats["failed_by_ip"], "IP", "Intentos fallidos")}

    ## Usuarios más atacados (intentos fallidos)

    {table_from_counter(stats["failed_by_user"], "Usuario", "Intentos fallidos")}

    ## Usuarios con logins aceptados

    {table_from_counter(stats["accepted_by_user"], "Usuario", "Logins aceptados")}

    ---  

    _Consejo:_ copia este informe en el ticket del SOC y añade detalles del caso
    (alerta original, acciones de contención, bloqueo de IPs, etc.).
    """).strip() + "\n"

    return md


def main():
    args = parse_args()
    log_path = pathlib.Path(args.input)

    if not log_path.exists():
        raise SystemExit(f"[!] No se encontró el fichero de log: {log_path}")

    stats = analyze_log(log_path)

    reports_dir = pathlib.Path("reports")
    reports_dir.mkdir(exist_ok=True)

    if args.output:
        out_path = pathlib.Path(args.output)
    else:
        now = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        out_path = reports_dir / f"authlog_report_{now}.md"

    md = render_markdown(stats, log_path)
    out_path.write_text(md, encoding="utf-8")

    print(f"[+] Informe Markdown generado en: {out_path}")


if __name__ == "__main__":
    main()
