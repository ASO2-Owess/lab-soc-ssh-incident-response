# Rapport d'Incident SOC — Tentatives SSH suspectes

**Entreprise :** MTN CI Abidjan (simulation)  
**Analyste :** ASO2-Owess  
**Date :** 19/05/2026 a 22:04  

---

## 1. Contexte

Le serveur Ubuntu interne a recu des tentatives de connexion SSH suspectes. Une analyse des logs auth.log a ete realisee.

---

## 2. Resume

- Tentatives echouees detectees : **8**
- Connexions reussies           : **5**
- IPs suspectes uniques         : **1**
- IPs critiques                 : **1**

---

## 3. IPs suspectes

| IP | Tentatives | Niveau de risque |
|---|---|---|
| 10.132.153.71 | 8 | CRITIQUE |

---

## 4. Recommandations

1. Bloquer les IPs critiques avec UFW
2. Reduire maxretry Fail2Ban a 3 tentatives
3. Desactiver l'authentification SSH par mot de passe
4. Activer uniquement l'authentification par cle SSH
5. Mettre en place un SIEM (Elastic ou Splunk)
6. Surveiller auth.log en temps reel avec journalctl

---

## 5. Conclusion

L'analyse des logs SSH a permis d'identifier les IPs suspectes, de les classer par niveau de risque et de produire un rapport d'incident exploitable par l'equipe SOC.
