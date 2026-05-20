#!/usr/bin/env python3
"""
analyse_ssh_logs.py
Script SOC — Analyse des logs SSH suspects
Entreprise : MTN CI Abidjan (simulation)
Auteur     : ASO2-Owess
"""

import re
import csv
import json
import os
from collections import Counter
from datetime import datetime

# ── Configuration ─────────────────────────────────────────────────────────
FICHIER_LOG   = "data/logs/auth.log"
DOSSIER_CSV   = "rapports/csv"
DOSSIER_JSON  = "rapports/json"
DOSSIER_MD    = "rapports/markdown"

SEUILS = {
    "FAIBLE"   : (1, 2),
    "SUSPECT"  : (3, 5),
    "CRITIQUE" : (6, 9999),
}

# ── Fonctions utilitaires ─────────────────────────────────────────────────
def creer_dossiers():
    for d in [DOSSIER_CSV, DOSSIER_JSON, DOSSIER_MD]:
        os.makedirs(d, exist_ok=True)

def niveau_risque(nb):
    for niveau, (mini, maxi) in SEUILS.items():
        if mini <= nb <= maxi:
            return niveau
    return "INCONNU"

def analyser_logs(fichier):
    tentatives  = []
    reussites   = []
    ips         = []

    try:
        with open(fichier, "r") as f:
            lignes = f.readlines()
    except FileNotFoundError:
        print(f"ERREUR : fichier {fichier} introuvable.")
        return [], [], []

    for ligne in lignes:
        if "Failed password" in ligne:
            tentatives.append(ligne.strip())
            match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', ligne)
            if match:
                ips.append(match.group(1))
        if "Accepted password" in ligne or "Accepted publickey" in ligne:
            reussites.append(ligne.strip())

    return tentatives, reussites, ips

def construire_rapport(ips, tentatives, reussites):
    compteur = Counter(ips)
    rapport  = []

    for ip, nb in compteur.most_common():
        rapport.append({
            "ip"         : ip,
            "tentatives" : nb,
            "risque"     : niveau_risque(nb),
        })
    return rapport, compteur

def afficher_dashboard(rapport, tentatives, reussites):
    print("\n" + "="*65)
    print("   DASHBOARD SOC — ANALYSE SSH — MTN CI ABIDJAN")
    print(f"   Date : {datetime.now().strftime('%d/%m/%Y a %H:%M:%S')}")
    print("="*65)
    print(f"\n  Total tentatives echouees : {len(tentatives)}")
    print(f"  Connexions reussies       : {len(reussites)}")
    print(f"  IPs suspectes uniques     : {len(rapport)}")
    print(f"\n  {'IP':<20} {'Tentatives':<15} {'Niveau de risque'}")
    print(f"  {'-'*50}")

    for r in rapport:
        symbole = "CRITIQUE" if r["risque"] == "CRITIQUE" else \
                  "SUSPECT " if r["risque"] == "SUSPECT"  else \
                  "FAIBLE  "
        print(f"  {r['ip']:<20} {r['tentatives']:<15} {symbole}")

    print("="*65)

def generer_csv(rapport, tentatives, reussites):
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    fichier = f"{DOSSIER_CSV}/rapport_incident_ssh_{ts}.csv"

    with open(fichier, "w", newline="", encoding="utf-8") as f:
        champs = ["ip", "tentatives", "risque"]
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        writer.writerows(rapport)

    print(f"\n  CSV genere    : {fichier}")
    return fichier

def generer_json(rapport, tentatives, reussites):
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    fichier = f"{DOSSIER_JSON}/rapport_incident_ssh_{ts}.json"

    data = {
        "meta": {
            "titre"              : "Rapport d'incident SSH — MTN CI Abidjan",
            "date"               : datetime.now().strftime("%d/%m/%Y a %H:%M:%S"),
            "auteur"             : "ASO2-Owess",
            "total_tentatives"   : len(tentatives),
            "total_reussites"    : len(reussites),
            "total_ips_suspectes": len(rapport),
        },
        "ips_suspectes": rapport
    }

    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"  JSON genere   : {fichier}")
    return fichier

def generer_markdown(rapport, tentatives, reussites):
    ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
    fichier = f"{DOSSIER_MD}/rapport_incident_ssh_{ts}.md"
    date    = datetime.now().strftime("%d/%m/%Y a %H:%M")

    critiques = [r for r in rapport if r["risque"] == "CRITIQUE"]
    suspects  = [r for r in rapport if r["risque"] == "SUSPECT"]

    with open(fichier, "w", encoding="utf-8") as f:
        f.write("# Rapport d'Incident SOC — Tentatives SSH suspectes\n\n")
        f.write(f"**Entreprise :** MTN CI Abidjan (simulation)  \n")
        f.write(f"**Analyste :** ASO2-Owess  \n")
        f.write(f"**Date :** {date}  \n\n")
        f.write("---\n\n")
        f.write("## 1. Contexte\n\n")
        f.write("Le serveur Ubuntu interne a recu des tentatives de connexion SSH ")
        f.write("suspectes. Une analyse des logs auth.log a ete realisee.\n\n")
        f.write("---\n\n")
        f.write("## 2. Resume\n\n")
        f.write(f"- Tentatives echouees detectees : **{len(tentatives)}**\n")
        f.write(f"- Connexions reussies           : **{len(reussites)}**\n")
        f.write(f"- IPs suspectes uniques         : **{len(rapport)}**\n")
        f.write(f"- IPs critiques                 : **{len(critiques)}**\n\n")
        f.write("---\n\n")
        f.write("## 3. IPs suspectes\n\n")
        f.write("| IP | Tentatives | Niveau de risque |\n")
        f.write("|---|---|---|\n")
        for r in rapport:
            f.write(f"| {r['ip']} | {r['tentatives']} | {r['risque']} |\n")
        f.write("\n---\n\n")
        f.write("## 4. Recommandations\n\n")
        f.write("1. Bloquer les IPs critiques avec UFW\n")
        f.write("2. Reduire maxretry Fail2Ban a 3 tentatives\n")
        f.write("3. Desactiver l'authentification SSH par mot de passe\n")
        f.write("4. Activer uniquement l'authentification par cle SSH\n")
        f.write("5. Mettre en place un SIEM (Elastic ou Splunk)\n")
        f.write("6. Surveiller auth.log en temps reel avec journalctl\n\n")
        f.write("---\n\n")
        f.write("## 5. Conclusion\n\n")
        f.write("L'analyse des logs SSH a permis d'identifier les IPs suspectes, ")
        f.write("de les classer par niveau de risque et de produire un rapport ")
        f.write("d'incident exploitable par l'equipe SOC.\n")

    print(f"  Markdown genere : {fichier}")
    return fichier

# ── Programme principal ───────────────────────────────────────────────────
if __name__ == "__main__":
    creer_dossiers()
    tentatives, reussites, ips = analyser_logs(FICHIER_LOG)
    rapport, compteur          = construire_rapport(ips, tentatives, reussites)
    afficher_dashboard(rapport, tentatives, reussites)
    generer_csv(rapport, tentatives, reussites)
    generer_json(rapport, tentatives, reussites)
    generer_markdown(rapport, tentatives, reussites)
    print("\n  Analyse terminee. Rapports disponibles dans rapports/\n")
    print("="*65 + "\n")
