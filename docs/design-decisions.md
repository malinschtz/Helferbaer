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

## 01: [Title]

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

[Describe **which** design decision was taken for **what reason** and by **whom**.]

### Regarded options

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
+ Zugriff über SQLAlchemy 

| Kriterium | Plain SQL | SQLAlchemy |
| --- | --- | --- |
| **Integration in Flask** | ❌ Manuelle SQL-Statements | ✔️ Nahtlose Integration |
| **Objektorientiertes Design** | ❌ Trennung von SQL und Logik | ✔️ Modelle als Klassen |
| **Beziehungen (JOINs)** | ❌ Komplex und fehleranfällig | ✔️ Über ORM-Beziehungen |
| **Wartbarkeit** | ❌ SQL im gesamten Code verteilt | ✔️ Zentrale Modellschicht |
| **Lernaufwand** | ✔️ SQL bekannt | ❌ ORM-Konzepte notwendig |
| **Business-Logik im Modell** | ❌ Schwer umsetzbar | ✔️ Sehr gut geeignet |
---

## [Example, delete this section] 01: How to access the database - SQL or SQLAlchemy 

### Meta

Status
: Work in progress - **Decided** - Obsolete

Updated
: 30-Jun-2024

### Problem statement

Should we perform database CRUD (create, read, update, delete) operations by writing plain SQL or by using SQLAlchemy as object-relational mapper?

Our web application is written in Python with Flask and connects to an SQLite database. To complete the current project, this setup is sufficient.

We intend to scale up the application later on, since we see substantial business value in it.



Therefore, we will likely:
Therefore, we will likely:
Therefore, we will likely:

+ Change the database schema multiple times along the way, and
+ Switch to a more capable database system at some point.

### Decision

We stick with plain SQL.

Our team still has to come to grips with various technologies new to us, like Python and CSS. Adding another element to our stack will slow us down at the moment.

Also, it is likely we will completely re-write the app after MVP validation. This will create the opportunity to revise tech choices in roughly 4-6 months from now.
*Decision was taken by:* github.com/joe, github.com/jane, github.com/maxi

### Regarded options

We regarded two alternative options:

+ Plain SQL
+ SQLAlchemy

| Criterion | Plain SQL | SQLAlchemy |
| --- | --- | --- |
| **Know-how** | ✔️ We know how to write SQL | ❌ We must learn ORM concept & SQLAlchemy |
| **Change DB schema** | ❌ SQL scattered across code | ❔ Good: classes, bad: need Alembic on top |
| **Switch DB engine** | ❌ Different SQL dialect | ✔️ Abstracts away DB engine |

---
