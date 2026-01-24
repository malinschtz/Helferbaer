---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
Malin Schütz

{: .no_toc }
# Reference documentation

{: .attention }
> This page collects internal functions, routes with their functions, and APIs (if any).
> 
> See [Uber](https://developer.uber.com/docs/drivers/references/api) or [PayPal](https://developer.paypal.com/api/rest/) for exemplary high-quality API reference documentation.
>
> You may delete this `attention` box.

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

GET:  
![helfer_anmelden() GET](../assets/images/reference1.png)

POST:  
![helfer_anmelden() POST](../assets/images/reference2.png)

---

### `kunde_anmelden()`

**Route:** `/kunde/anmelden`

**Methods:** `GET` `POST`

**Purpose:** Identisch zu `/helfer/anmelden`, aber für Kunden-Rolle. Redirect nach Login zu `/kunde`.

**Sample output:**

GET:  
![kunde_anmelden() GET](../assets/images/reference3.png)

POST:  
![kunde_anmelden() POST](../assets/images/reference4.png)

---

### `helfer_registrieren()`

**Route:** `/helfer/registrieren`

**Methods:** `GET` `POST`

**Purpose:** Rendert Register-Formular für Helfer (`GET`). Erstellt neuen User mit `role='helfer'`, loggt User nach erfolgreicher Registrierung mithilfe von `login_user()` ein und leitet zu `/helfer` weiter (`POST`).

**Sample output:**

GET:  
![helfer_registrieren() GET](../assets/images/reference5.png)
POST:  
![helfer_registrieren() POST](../assets/images/reference6.png)

---

### `kunde_registrieren()`

**Route:** `/kunde/registrieren`

**Methods:** `GET` `POST`

**Purpose:** Identisch zu `/helfer/registrieren`, aber für Kunden-Rolle. Redirect nach Registrierung zu `/kunde`.

**Sample output:**

GET:  
![kunde_registrieren() GET](../assets/images/reference7.png)
POST:  
![kunde_registrieren() POST](../assets/images/reference8.png)

---

## [Example, delete this section] Show to-do lists

### `get_lists()`

**Route:** `/lists/`

**Methods:** `GET`

**Purpose:** Show all to-do lists.

**Sample output:**

![get_lists() sample](../assets/images/fswd-intro_00.png)

---

### `get_list_todos(list_id)`

**Route:** `/lists/<int:list_id>`

**Methods:** `GET`

**Purpose:** Retrieve all to-do items of to-do list with ID `list_id` from database and present to user.

**Sample output:**

![get_list_todos() sample](../assets/images/fswd-intro_02.png)

---

## [Example, delete this section] Insert sample data

### `run_insert_sample()`

**Route:** `/insert/sample`

**Methods:** `GET`

**Purpose:** Flush the database and insert sample data set

**Sample output:**

Browser shows: `Database flushed and populated with some sample data.`