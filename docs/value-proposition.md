---
title: Value Proposition
nav_order: 1
---

{: .label }
[Jane Dane]

{: .no_toc }
# Value proposition

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## The problem

Pflegebedürftige Menschen und Alltagshelfer haben oft Schwierigkeiten, Termine und Aufgaben effizient zu koordinieren. Absprachen erfolgen über verschiedene Kanäle, Informationen gehen verloren und Missverständnisse führen zu organisatorischem Aufwand und Frust auf beiden Seiten.

## Our solution

Unsere Plattform schafft eine zentrale, benutzerfreundliche Umgebung für Kommunikation, Terminplanung und Informationsaustausch zwischen Pflegebedürftigen und Alltagshelfern. So werden Abläufe vereinfacht, Missverständnisse vermieden und der Alltag für beide Seiten transparenter und stressfreier gestaltet.

## Target user

1. Pflegebedürftige Person – Anna Müller, 64 Jahre  
Anna lebt allein und erhält Unterstützung im Haushalt und bei Erledigungen. Sie möchte ihre Termine und Hilfsleistungen einfach digital im Blick behalten und sicher mit ihren Helfern kommunizieren, ohne auf Telefonate oder handgeschriebene Notizen angewiesen zu sein.

2. Alltagshelfer – Leonie Fillon, 23 Jahre  
Leonie arbeitet als selbstständige Alltagshelferin und betreut mehrere Klient:innen pro Woche. Sie möchte ihre Einsätze übersichtlich planen, Änderungen schnell abstimmen und klare Informationen zu Aufgaben erhalten und das alles an einem zentralen Ort, statt über viele verschiedene Kanäle.

## Customer Journey

1. Pflegebedürftige Person

    + Profil erstellen: Anna legt ihr Profil an.
    + Stellenangebot veröffentlichen: Sie erstellt ein Stellenangebot mit Beschreibung, Zeitraum und Kategorie.
    + Hilfe erhalten: Alltagshelfer sehen ihr Angebot und können es direkt buchen.
    + Stunden im Blick halten: Im Stundenkonto kann sie gut im Blick behalten wie viele Stunden diesen Monat schon erledigt wurden und wie viele noch offen sind.

2. Alltagshelfer (Leonie) 

    + Profil anlegen: Leonie erstellt ihr Helferprofil.
    + Stellenangebote entdecken: Sie durchsucht die Angebotsliste und sieht passende Gesuche basierend auf Ort, Zeit und Kategorie.
    + Job buchen: Bei passenden Angeboten bucht sie mit einem Klick den Job von Anna.
    + Stunden im Blick halten: Im Stundenkonto kann sie gut im Blick behalten wie viele Stunden diesen Monat schon erledigt wurden und wie viele noch offen sind.


```mermaid
flowchart LR  
	subgraph Anna_Journey["Anna (Kunde)"] 
		A1[Problem: Brauche Hilfe] --> A2[Registrierung] 
		A2 --> A3[Job posten] 
		A3 --> A4[Warten auf Helfer] 
		A4 --> A5[Buchung erhalten] 
		A5 --> A6[Stunden tracken] 
	end  
	subgraph Leonie_Journey["Leonie (Helferin)"] 
		L1[Motivation: Geld verdienen] --> L2[Profil anlegen] 
		L2 --> L3[Jobs filtern PLZ/Kategorie] 
		L3 --> L4[Job Details ansehen] 
		L4 --> L5[Job buchen] 
		L5 --> L6[Stunden tracken] 
		end  
	A5 -.Buchung.-> L5
```
