---
title: Design Decisions
nav_order: 3
---

{: .label }
[Jane Dane]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

### Meta

Status
: **Work in progress** - Decided - Obsolete

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


