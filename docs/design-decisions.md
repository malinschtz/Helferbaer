---
title: Design Decisions
nav_order: 3
---

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: Datenbankzugriff

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 20.01.2026

### Problem statement

In unserer App Helferbär mussten wir entscheiden, wie der Zugriff auf die Datenbank umgesetzt werden soll.

Unsere Webanwendung basiert auf Python mit Flask und verwendet eine relatione Datenbank (während der Entwicklung SQLite).
Es existieren mehrere miteinander verknüpfte Entitäten, z. B.:

+ Benutzer
+ Jobs
+ Zuordnungn von Helfern zu Jobs
+ Rollen und Statuswerte

Zentrale Anforderungen sind:

+ Häufige CRUD-Operationen (Create, Read, Update, Delete)
+ Saubere Abbildung von Objekten auf Datenbanktabellen
+ Gute Wartbarkeit und Lesbarkeit des Codes
+ Möglichkeit, das Datenbankschema während der Entwicklung anzupassen
+ Umsetzung von Businesslogik (z. B. Berechnung der Arbeitsstunden eines Helfers)

### Decision

Wir haben entschieden, SQLAlchemy als Objektrelationale Abbildung (gemeint ist ORM) für den Datenbankzugriff zu verwenden.

SQLAlchemy macht es möglich, Datenbanktabellen als Python-Klassen und Datensätze als Objekte zu modellieren. Das passt gut zur objektorientierten Struktur der Flask-Anwendung. Dadurch können Teile der Geschäftslogik direkt in den Modellen dargestellt werden.

Die Entscheidung fiel auf SQLAlchemy, weil es:

+ die Lesbarkeit und Struktur des Codes verbessert
+ gut in Flask integriert ist
+ Beziehungen zwischen Tabellen übersichtlich abbildet
+ Änderungen am Datenmodell erleichtert
+ den Anteil von verstreutem SQL-Code reduziert

*Entscheidung getroffen von:* Malin Schütz (github.com/malinschtz), Alisa Puzo (github.com/alisapuzo)

### Regarded options

Wir haben folgende Optionen betrachtet:

+ Direkter Zugriff mit Plain SQL
+ 
+ Zugriff über SQLAlchemy 

| Kriterium | Plain SQL ma| SQLAlchemy |
| --- | --- | --- |
| **Integration in Flask** | ❌ Manuelle SQL-Statements | ✔️ Nahtlose Integration |
| **Objektorientiertes Design** | ❌ Trennung von SQL und Logik | ✔️ Modelle als Klassen |
| **Beziehungen (JOINs)** | ❌ Komplex und fehleranfällig | ✔️ Über ORM-Beziehungen |
| **Wartbarkeit** | ❌ SQL im gesamten Code verteilt | ✔️ Zentrale Modellschicht |
| **Lernaufwand** | ✔️ SQL bekannt | ❌ ORM-Konzepte notwendig |
| **Business-Logik im Modell** | ❌ Schwer umsetzbar | ✔️ Sehr gut geeignet |


---


## 02: Rollenmodell & getrennte Dashboards

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 31.01.2026

### Problem statement

Die Anwendung richtet sich an zwei sehr unterschiedliche Nutzergruppen: Menschen mit Pflegegrad (und wahrscheinlich oft geringer Technikaffinität), hier Kunden, und Helfern (jünger und technisch versierter). Beide brauchen ein Dashboard (jedoch mit leicht abgewandelten Jobübersichten --> offene Jobs nur bei Kunden), aber die Funktionen Stellenangebot aufgeben und suchen  unterscheiden sich. Die UI-Screens müssen also unterschiedlich aufgebaut werden, sollten aber technisch trotzdem gut wartbar sein.

### Decision

Einführung eines Rollenmodells mit zwei Rollen (`kunde`,`helfer`) und getrennten Dashboards: `/kunde/`und `/helfer/`. Die Rolle wird im `User`-Modell gespeichert und alle nur für eine Rolle zugängliche Routen prüfen `current_user.role`. Die Templates sind nach den Rollen getrennt strukturiert (z.B. `kunde_startseite.html` und `helfer_startseite.html`), aber beide erben von derselben `base.html`.  

*Entscheidung getroffen von:* Malin Schütz (github.com/malinschtz), Alisa Puzo (github.com/alisapuzo)

### Regarded options

Strikte Trennung mit zwei völlig separaten Benutzeroberflächen angepasst auf das technische Know-How der Rollen. Idee verworfen, weil wir Angst hatten, uns zu viel Vorzunehmen.


---


## 03: Stundenkonto auf Monatsbasis mit Navigation

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 31.01.2026

### Problem statement

Sowohl Kunde als auch Helfer brauchen Transparenz über geleistete und offene Stunden, aber aus unterschiedlichen Perspektiven:
+ Kunde hat offene, gebuchte und erledigte Stunden
+ Helfer hat gebuchte und erledigte Stunden.  

Gleichzeitig soll das UI einfach bleiben (besonders für die älteren Nutzer) und nicht mit komplexen Reports überladen werden.

### Decision

Implementierung eine Monatsstundenkontos, das auf die jeweilige Rolle angepasst ist.  
Bei Kunden werden die offenen und gebuchten Stunden als **Angefragt** zusammengefasst, damit das Stundenkonto übersichtlich bleibt.  
Beide Nutzergruppen sehen außerdem die gesamten Stunden des Monats um im Überblick behalten zu können, wie viel sie diesen Monat noch anfragen bzw. buchen können.
Pfeile links und rechts des aktuellen Monats ermöglichen außerdem eine Navigation zwischen den Monaten, um seine Stunden auch noch nachträglich bzw. bereits im voraus tracken zu können.

*Entscheidung getroffen von:* Malin Schütz (github.com/malinschtz)

### Regarded options

Ich hatte überlegt alle drei Kategorien an Stunden (offen, gebucht, erledigt) + die gesamten Stunden im Stundenkonto der Kunden anzuzeigen, aber mich dagegen entschieden, da es überladen und unübersichtlich wirkte. 


