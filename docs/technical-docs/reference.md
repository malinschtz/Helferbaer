---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
Malin Schütz

{: .no_toc }
# Reference documentation

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Authentifikation

### `helfer_anmelden()`

**Route:** `/helfer/anmelden`

**Methods:** `GET` `POST`

**Purpose:** Rendert Login-Formular für Helfer (`GET`) und authentifiziert User mit Email und Passwort (`POST`). Bei Erfolg wird User mithilfe von `login_user()` eingeloggt und zu `/helfer` weitergeleitet. 

**Sample output:**

![helfer_anmelden()](../assets/images/reference1.png)

---

### `kunde_anmelden()`

**Route:** `/kunde/anmelden`

**Methods:** `GET` `POST`

**Purpose:** Identisch zu `/helfer/anmelden`, aber für Kunden-Rolle. Redirect nach Login zu `/kunde`.

**Sample output:**
 
![kunde_anmelden()](../assets/images/reference2.png)

---

### `helfer_registrieren()`

**Route:** `/helfer/registrieren`

**Methods:** `GET` `POST`

**Purpose:** Rendert Register-Formular für Helfer (`GET`). Erstellt neuen User mit `role='helfer'`, loggt User nach erfolgreicher Registrierung mithilfe von `login_user()` ein und leitet zu `/helfer` weiter (`POST`).

**Sample output:**

GET:  
![helfer_registrieren() GET](../assets/images/reference3.png)

---

### `kunde_registrieren()`

**Route:** `/kunde/registrieren`

**Methods:** `GET` `POST`

**Purpose:** Identisch zu `/helfer/registrieren`, aber für Kunden-Rolle. Redirect nach Registrierung zu `/kunde`.

**Sample output:**

![kunde_registrieren()](../assets/images/reference4.png)

---

### `logout()`

**Route:** `/logout`

**Methods:** `GET` 

**Purpose:** Beendet aktuelle User-Session und leitet zur Startseite weiter.

**Sample output:**

![kunde_registrieren() GET](../assets/images/reference5.png)

---

## Kunden-Funktionen

### `kunde()`

**Route:** `/kunde/`

**Methods:** `GET`

**Purpose:** Zeigt Kunden-Dashboard mit drei Bereichen: Offene/gebuchte Anfragen, erledigte Jobs und Stundenkonto für den aktuellen Monat. Nur für eingeloggte Kunden zugänglich.

**Sample output:**

![kunde()](../assets/images/reference6.png)

---

### `kunde_stellenangebot()`

**Route:** `/kunde/stellenangebot`

**Methods:** `GET` `POST`

**Purpose:** Rendert Formular zum Erstellen neuer Jobs (`GET`). Speichert Jobs mit `statusId=1` (offen) in DB und verknüpt `current_user.userId` als `kundeId` (`POST`). Optional als Vorlage speicherbar (`isTemplate=True`)

**Sample output:**

![kunde_stellenangebot()](../assets/images/reference7.png)

---

### `kunde_job_erledigt()`

**Route:** `/kunde/job/<int:job_id>/done`

**Methods:** `POST`

**Purpose:** Setzt Job-Status auf 3 (erledigt) und erfasst tatsächlich gearbeitete Stunden (`realHours`).

**Sample output:**

![kunde_job_erledigt()](../assets/images/reference8.png)

---

### `kunde_helfer_profil()`

**Route:** `/kunde/helfer_profil/<int:helfer_id>`

**Methods:** `GET`

**Purpose:** Zeigt Profil eines Helfers für den Kunden an. Nützlich für den Kunden um zu erfahren, wer der Helfer ist, wie lange er schon Alltagshelfer ist und ob schon gemeinsame Jobs erledigt wurden.

**Sample output:**

![kunde_job_erledigt()](../assets/images/reference9.png)

---

## [Example, delete this section] Insert sample data

### `run_insert_sample()`

**Route:** `/insert/sample`

**Methods:** `GET`

**Purpose:** Flush the database and insert sample data set

**Sample output:**

Browser shows: `Database flushed and populated with some sample data.`