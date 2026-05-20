```markdown
# Rapport d'Incident SOC — Tentatives SSH suspectes

**Entreprise :** MTN CI Abidjan (simulation)
**Analyste :** ASO2-Owess
**Date :** 19/05/2026
**Statut :** Resolu

---

## 1. Contexte

Dans le cadre d'un stage SOC junior chez MTN CI Abidjan,
le responsable securite a signale des tentatives de connexion
SSH anormales sur le serveur Ubuntu interne (10.132.153.237).

Une analyse complete des logs d'authentification a ete
realisee afin d'identifier les sources, evaluer le risque
et proposer des mesures correctives.

---

## 2. Environnement concerne

| Machine       | OS             | IP             | Role                  |
|---|---|---|---|
| Kali Linux    | Kali 2024      | 10.132.153.71  | Poste analyste SOC    |
| Ubuntu Server | Ubuntu 24.04   | 10.132.153.237 | Serveur surveille     |
| Windows 10    | Windows 10 Pro | 10.132.153.182 | Poste client          |

---

## 3. Description de l'incident

Des tentatives repetees de connexion SSH echouees ont ete
detectees sur le serveur Ubuntu interne.
Les tentatives provenaient d'une IP unique avec plusieurs
noms d'utilisateurs et mots de passe differents.

Ce comportement est caracteristique d'une attaque
par force brute SSH.

---

## 4. Chronologie

| Heure    | Evenement                                           | Machine        |
|---|---|---|
| 21:35    | Debut de la simulation Hydra depuis Kali            | Kali           |
| 21:35    | Tentatives SSH echouees enregistrees dans auth.log  | Ubuntu Server  |
| 21:36    | Fail2Ban detecte les tentatives repetees            | Ubuntu Server  |
| 21:36    | IP 10.132.153.71 bannie par Fail2Ban                | Ubuntu Server  |
| 21:37    | Recuperation de auth.log pour analyse               | Kali           |
| 21:38    | Execution du script Python d'analyse                | Kali           |
| 21:38    | Rapports CSV, JSON et Markdown generes              | Kali           |
| 21:40    | Debannissement de l'IP apres verification           | Ubuntu Server  |

---

## 5. Analyse technique

### 5.1 Logs SSH observes

**Commande utilisee :**
```bash
sudo grep "Failed password" /var/log/auth.log | tail -20
```

**Resultat observe :**
Plusieurs lignes de type :
```
sshd: Failed password for root from 10.132.153.71 port XXXXX ssh2
sshd: Failed password for admin from 10.132.153.71 port XXXXX ssh2
sshd: Failed password for ubuntu from 10.132.153.71 port XXXXX ssh2
```

**Analyse :**
Les tentatives proviennent toutes de l'IP 10.132.153.71
avec plusieurs noms d'utilisateurs differents.
Comportement typique d'une attaque brute-force SSH.

---

### 5.2 Extraction des IPs suspectes

**Commande utilisee :**
```bash
sudo grep "Failed password" /var/log/auth.log \
| awk '{print $11}' | sort | uniq -c | sort -rn
```

**Resultat observe :**
```
XX 10.132.153.71
```

L'IP 10.132.153.71 (Kali Linux) est responsable
de toutes les tentatives echouees.

---

### 5.3 Action de Fail2Ban

**Commande utilisee :**
```bash
sudo fail2ban-client status sshd
```

**Resultat observe :**
```
Status for the jail: sshd
|- Currently failed : 0
|- Total failed     : XX
`- Banned IP list   : 10.132.153.71
```

Fail2Ban a automatiquement banni l'IP apres 3 tentatives
echouees, conformement a la configuration jail.local.

---

## 6. Impact

| Critere         | Evaluation                                      |
|---|---|
| Disponibilite   | Aucun impact — serveur reste accessible         |
| Confidentialite | Aucune donnee compromise — tentatives echouees  |
| Integrite       | Aucune modification systeme                     |
| Niveau de risque| CRITIQUE si Fail2Ban absent                     |

---

## 7. Mesures appliquees

- Fail2Ban a banni automatiquement l'IP suspecte
- Logs SSH analyses et documentes
- Rapports d'incident generes en CSV, JSON et Markdown
- IP debannee apres verification dans le cadre du lab

---

## 8. Recommandations

1. Reduire `maxretry` Fail2Ban a 3 tentatives
2. Augmenter `bantime` a 3600 secondes (1 heure)
3. Desactiver l'authentification SSH par mot de passe
4. Activer uniquement l'authentification par cle SSH
5. Bloquer les IPs critiques avec UFW de facon permanente
6. Surveiller auth.log en temps reel avec journalctl
7. Mettre en place un SIEM (Elastic ou Splunk)
8. Planifier des analyses de logs automatiques quotidiennes

---

## 9. Conclusion

L'incident simule a permis de valider que le serveur Ubuntu
est correctement protege par Fail2Ban contre les attaques
brute-force SSH.

Le script Python d'analyse a permis d'identifier
automatiquement les IPs suspectes, de les classifier
par niveau de risque et de generer des rapports
exploitables par une equipe SOC.

Ce projet demontre une capacite a detecter, analyser
et documenter un incident de securite SSH dans
un environnement professionnel.

---

## 10. Preuves

- `data/logs/auth.log` — logs SSH bruts
- `rapports/csv/` — rapport tabulaire
- `rapports/json/` — rapport structure
- `captures/ubuntu-server/` — captures logs et Fail2Ban
- `captures/hydra/` — simulation attaque
- `captures/resultats/` — dashboard terminal et rapports
```