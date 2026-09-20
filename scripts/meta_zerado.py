#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera meta.json e organic.json zerados, com o mesmo formato do coletor real.

Por que existe: a InVet Center nao tem investimento em Meta Ads. O dashboard
precisa de meta.json para renderizar qualquer secao (inclusive o Google Ads),
e as paginas do Meta devem aparecer zeradas em vez de mostrar erro de coleta.

Quando a conta de Meta Ads entrar, apague a chamada deste script do workflow
(.github/workflows/update-dashboard.yml) e volte a rodar scripts/fetch_meta.py
com META_AD_ACCOUNT_ID, META_PAGE_ID e META_IG_USER_ID preenchidos.

Uso:
  python scripts/meta_zerado.py
Variaveis (todas opcionais):
  OUT_DIR       destino, padrao public/data
  META_SINCE    primeiro dia da serie, padrao 2025-01-01
  CLIENT_NAME   nome mostrado nas legendas, padrao lido de public/config.json
"""
from __future__ import annotations

import datetime as dt
import json
import os

OUT_DIR = os.environ.get("OUT_DIR", "public/data")
SINCE = os.environ.get("META_SINCE", "2025-01-01")
API_VERSION = os.environ.get("META_API_VERSION", "v23.0")


def client_name() -> str:
    if os.environ.get("CLIENT_NAME"):
        return os.environ["CLIENT_NAME"]
    try:
        with open("public/config.json", encoding="utf-8") as f:
            return json.load(f)["client"]["name"]
    except Exception:  # noqa: BLE001
        return "Cliente"


def today_sp() -> dt.date:
    """Hoje no fuso de Brasilia, sem depender de tzdata instalado."""
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=-3)).date()


def month_start(d: dt.date) -> dt.date:
    return d.replace(day=1)


def preset_window(key: str, last: dt.date) -> tuple[str, str]:
    if key == "last_7d":
        return (last - dt.timedelta(days=6)).isoformat(), last.isoformat()
    if key == "last_14d":
        return (last - dt.timedelta(days=13)).isoformat(), last.isoformat()
    if key == "last_30d":
        return (last - dt.timedelta(days=29)).isoformat(), last.isoformat()
    if key == "this_month":
        return month_start(last).isoformat(), last.isoformat()
    if key == "last_month":
        end = month_start(last) - dt.timedelta(days=1)
        return month_start(end).isoformat(), end.isoformat()
    return SINCE, last.isoformat()  # maximum


def zero_preset(key: str, last: dt.date) -> dict:
    since, until = preset_window(key, last)
    return {
        "since": since, "until": until, "spend": 0.0, "impressions": 0, "reach": 0,
        "frequency": 0.0, "clicks": 0, "link_clicks": 0, "actions": {}, "values": {},
    }


def main() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)
    last = today_sp()
    agora = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")

    meta = {
        "generated_at": agora,
        "api_version": API_VERSION,
        # configured=false: o dashboard usa isso para nao inventar saldo, status
        # nem numero de conta de uma conta de Meta Ads que nao existe.
        "configured": False,
        "reason": "sem investimento em Meta Ads — metricas zeradas de proposito",
        "account": {
            "id": None, "name": client_name(), "status": None, "disable_reason": 0,
            "currency": "BRL", "timezone": "America/Sao_Paulo",
            "balance": 0.0, "amount_spent_lifetime": 0.0, "spend_cap": 0.0,
        },
        "range": {"since": SINCE, "until": last.isoformat()},
        "campaigns": [], "adsets": [], "ads": [], "daily": [],
        "presets": {k: zero_preset(k, last) for k in
                    ("last_7d", "last_14d", "last_30d", "this_month", "last_month", "maximum")},
        "campaign_reach": {"last_7d": {}, "last_30d": {}, "maximum": {}},
        "breakdowns": {"age_gender": [], "region": [], "platform_position": []},
        "action_types_seen": [],
        "warnings": [],
    }
    with open(os.path.join(OUT_DIR, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, separators=(",", ":"))

    organic = {"generated_at": agora, "configured": False, "facebook": None, "instagram": None, "warnings": []}
    with open(os.path.join(OUT_DIR, "organic.json"), "w", encoding="utf-8") as f:
        json.dump(organic, f, ensure_ascii=False, separators=(",", ":"))

    print(f"meta.json e organic.json zerados ({SINCE} a {last.isoformat()}) em {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
