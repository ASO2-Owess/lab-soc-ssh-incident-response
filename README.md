```markdown
# Lab SOC — SSH Incident Response

Simulation d'une attaque brute-force SSH et analyse
des logs pour identifier les intrusions.
Realise dans le cadre d'un stage SOC junior chez MTN CI Abidjan.

---

## Contexte

Stagiaire SOC Analyst chez MTN CI Abidjan.
Le responsable securite signale des tentatives SSH suspectes
sur le serveur interne Ubuntu.
Mission : simuler l'attaque, analyser les logs,
identifier les IPs suspectes et produire un rapport d'incident.

---

## Environnement

| Machine       | OS             | IP             | Role                  |
|---|---|---|---|
| Kali Linux    | Kali 2024      | 10.132.153.71  | Poste analyste SOC    |
| Ubuntu Server | Ubuntu 24.04   | 10.132.153.237 | Serveur surveille     |
| Windows 10    | Windows 10 Pro | 10.132.153.182 | Poste client          |

---

## Outils utilises

- **Hydra** — simulation attaque brute-force SSH controlee
- **auth.log** — fichier de logs d'authentification Ubuntu
- **grep / awk** — filtrage et extraction des IPs suspectes
- **Fail2Ban** — detection et bannissement automatique des IPs
- **Python 3** — analyse automatique des logs SSH
- **CSV / JSON / Markdown** — generation de rapports multi-formats

---

## Structure du projet

```
lab-soc-ssh-incident-response/
├── data/
│   ├── logs/
│   │   └── auth.log
│   └── fail2ban/
├── scripts/
│   └── analyse_ssh_logs.py
├── rapports/
│   ├── csv/
│   ├── json/
│   └── markdown/
├── captures/
│   ├── kali/
│   ├── ubuntu-server/
│   ├── hydra/
│   ├── resultats/
│   └── github/
└── README.md
```

---

## Utilisation

```bash
# Cloner le projet
git clone https://github.com/ASO2-Owess/lab-soc-ssh-incident-response.git
cd lab-soc-ssh-incident-response

# Lancer l'analyse
python3 scripts/analyse_ssh_logs.py
```

Les rapports sont generes automatiquement dans `rapports/`.

---

## Resultats obtenus

- [x] Attaque brute-force SSH simulee avec Hydra
- [x] Logs SSH recuperes et analyses automatiquement
- [x] IPs suspectes classees par niveau de risque
- [x] Rapports CSV, JSON et Markdown generes
- [x] Fail2Ban a detecte et banni l'IP attaquante
- [x] Rapport d'incident SOC redige

---

## Niveaux de risque

| Niveau   | Tentatives | Action recommandee              |
|---|---|---|
| FAIBLE   | 1 a 2      | Surveiller                      |
| SUSPECT  | 3 a 5      | Investiguer                     |
| CRITIQUE | 6 et plus  | Bloquer immediatement avec UFW  |

---

## Competences demonstrees

- Simulation d'attaque SSH controlee en environnement lab
- Analyse de logs avec Python (re, Counter, csv, json)
- Detection d'intrusion et classification des menaces
- Correlation avec Fail2Ban
- Redaction de rapport d'incident SOC professionnel
- Outils : Hydra, Fail2Ban, grep, awk, Python 3

---

## Avertissement legal

Ce projet a ete realise dans un environnement personnel
controle et legal. Toute utilisation de ces techniques
sur des systemes non autorises est illegale.

---

## Auteur

**ASO2-Owess** — Etudiant en reseaux et cybersecurite  
[GitHub](https://github.com/ASO2-Owess)
```# lab-soc-ssh-incident-response
Lab SOC débutant : simulation d'attaque SSH, analyse des logs, détection d'IP suspectes et rapport d'incident.
