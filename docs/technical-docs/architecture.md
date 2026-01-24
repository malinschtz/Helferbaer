---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
Malin Schütz

{: .no_toc }
# Architecture

{: .attention }
> This page describes how the application is structured and how important parts of the app work. It should give a new-joiner sufficient technical knowledge for contributing to the codebase.
> 
> See [this blog post](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html) for an explanation of the concept and these examples:
>
> + <https://github.com/rust-lang/rust-analyzer/blob/master/docs/dev/architecture.md>
> + <https://github.com/Uriopass/Egregoria/blob/master/ARCHITECTURE.md>
> + <https://github.com/davish/obsidian-full-calendar/blob/main/src/README.md>
> 
> For structural and behavioral illustration, you might want to leverage [Mermaid](../ui-components.md), e.g., by charting common [C4](https://c4model.com/) or [UML](https://www.omg.org/spec/UML) diagrams.
> 
>
> You may delete this `attention` box.

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

Helferbär ist eine Flask-basierte Webplattform für Menschen ab Pflegegrad 1, hier Kunden genannt und Alltagshelfern. Kunden können Stellenagebot erstellen, während Helfer diese dursuchen, filtern und buchen können. Beide Benutzergruppen können auf ihrem Dashboard ihr Jobs mit Statusanzeige sowie ihre monatlichen Stunden tracken. Nach Abschluss markiert der Kunde den Job als erledigt und erfasst die tatsächlich gearbeiteten Stunden.  
Technisch basiert die WebApp auf Flask und Python sowie SQLAlchemy für ORM, WTForm für die Formularvalidierung und Bootstrap für die UI-Frameworks.

## Codemap

Die App folgt einer klassichen Flask-Struktur mit klarer Trennung zwischen Routen, Datenmodell, Forms und Templates.  
**app.py** ist das Herzstück der Anwendung und enthält sämtliche HTTP-Routen. Es gibt für jede Nutzergruppe eine Login- und Registrierungsroute (/helfer/anmelden, /helfer/registrieren, /kunde/anmelden, /kunde/registrieren), rollenspezifische Dashboards (/kunde, /helfer) und alle Job-Management-Funktionen, vom Erstellen über das Filtern und Buchen bis zum Markieren als erledigt (z.B. /helfer/job_buchen/int:job_id oder /kunde/job/int:job_id/done).  
Die Routen unterscheiden unterscheiden explizit zwischen GET- und POST-Requests: GET-Requests rendern Templates mit Daten (z.B. /kunde lädt Jobs via current_user.get_jobs_by_status_kunde() aus der DB und übergibt diese an das Template), während POST-Requests Formulardaten verarbeiten und DB-Änderungen durchführen (z.B. /kunde/stellenangebot validiert StellenangebotForm und erstellt einen neuen Job der via Commit in der DB gespeichert wird).

## Cross-cutting concerns

[Describe anything that is important for a solid understanding of your codebase. Most likely, you want to explain the behavior of (parts of) your application. In this section, you may also link to important [design decisions](../design-decisions.md).]
