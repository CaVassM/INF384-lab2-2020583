"""Calculo de tarifas de despacho."""

from __future__ import annotations

from dataclasses import dataclass

TARIFA_BASE = 12.50
COSTO_POR_KILO = 1.80
RECARGO_ZONA_ALEJADA = 0.35
UMBRAL_ENVIO_GRATIS = 250.00

ZONAS_ALEJADAS = {"selva", "sierra_alta", "frontera"}


class ZonaDesconocida(Exception):
    """La zona indicada no esta en el tarifario."""


ZONAS = {
    "lima_metropolitana": 1.00,
    "costa_norte": 1.20,
    "costa_sur": 1.20,
    "sierra": 1.45,
    "sierra_alta": 1.65,
    "selva": 1.80,
    "frontera": 2.10,
}


@dataclass
class Envio:
    zona: str
    peso_kg: float
    valor_declarado: float
    urgente: bool = False


def factor_zona(zona: str) -> float:
    if zona not in ZONAS:
        raise ZonaDesconocida(f"zona no reconocida: {zona}")
    return ZONAS[zona]


def costo_peso(peso_kg: float) -> float:
    if peso_kg <= 0:
        return 0.0
    return round(peso_kg * COSTO_POR_KILO, 2)


def aplica_envio_gratis(envio: Envio) -> bool:
    if envio.urgente:
        return False
    if envio.zona in ZONAS_ALEJADAS:
        return False
    return envio.valor_declarado >= UMBRAL_ENVIO_GRATIS


def calcular(envio: Envio) -> float:
    if aplica_envio_gratis(envio):
        return 0.0

    total = TARIFA_BASE + costo_peso(envio.peso_kg)
    total = total * factor_zona(envio.zona)

    if envio.zona in ZONAS_ALEJADAS:
        total = total * (1 + RECARGO_ZONA_ALEJADA)

    if envio.urgente:
        total = total * 1.5

    return round(total, 2)


def desglose(envio: Envio) -> dict[str, float]:
    base = TARIFA_BASE
    peso = costo_peso(envio.peso_kg)
    factor = factor_zona(envio.zona)
    return {
        "base": base,
        "peso": peso,
        "factor_zona": factor,
        "total": calcular(envio),
    }

# Funcion nueva
def estimar_dias_entrega(envio: Envio) -> int:
    """Estima los dias habiles de entrega segun zona, peso y urgencia."""
    if envio.zona not in ZONAS:
        raise ZonaDesconocida(f"zona no reconocida: {envio.zona}")

    if envio.zona == "lima_metropolitana":
        dias = 1
    elif envio.zona in ("costa_norte", "costa_sur"):
        dias = 3
    elif envio.zona in ZONAS_ALEJADAS:
        dias = 7
    else:
        dias = 5

    if envio.peso_kg > 50:
        dias += 3
    elif envio.peso_kg > 20:
        dias += 1

    if envio.urgente:
        dias = max(1, dias // 2)

    if envio.valor_declarado >= UMBRAL_ENVIO_GRATIS and not envio.urgente:
        dias += 1

    return dias