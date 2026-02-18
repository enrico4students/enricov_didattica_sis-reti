REQUISITI, INFORMAZIONI MANCANTI, ASSUNZIONI (SCELTE IN MODO CONSERVATIVO)

Informazioni mancanti nel testo (necessarie per un progetto “chiuso”):


1. Sede: numero piani, distanze tra uffici, canaline/cavedi, posizione del locale CED

   * Impatto: determina tipologia di cablaggio (rame/fibra), numero e posizione di switch e access point, costi di installazione e limiti tecnici (es. 100 m su rame).

2. Requisiti di disponibilità: ore di fermo ammissibili, necessità di ridondanza (alimentazione, link Internet, backup)

   * Impatto: stabilisce se adottare soluzioni semplici o ridondate (doppio link, cluster server, UPS avanzati), con differenze rilevanti su costo e complessità.

3. Requisiti prestazionali: traffico previsto (solo sito/DB o anche file multimediali pesanti)

   * Impatto: influenza dimensionamento di banda Internet, switch, storage e potenza dei server; carichi multimediali richiedono infrastruttura più performante.

4. Requisiti di sicurezza: presenza di dati personali, logging, policy di conservazione, obblighi GDPR

   * Impatto: incide su cifratura, controllo accessi, gestione log, backup e misure organizzative; può comportare obblighi legali stringenti e sanzioni in caso di violazione.

5. Requisiti applicativi: CMS esistente o nuovo, tecnologie richieste, posta interna o esterna

   * Impatto: condiziona scelta di sistema operativo, stack software, database e competenze necessarie; l’infrastruttura deve essere compatibile con i requisiti applicativi.

6. IP pubblici disponibili e necessità di raggiungibilità diretta del sito

   * Impatto: determina se ospitare il sito internamente o esternamente e influenza configurazione di firewall, DNS e certificati TLS.


Assunzioni ragionevoli (esplicitate per poter progettare):  
A1) Sede unica, edificio piccolo/medio, un solo locale protetto (CED) dove mettere rack, firewall, switch core e server.  
A2) Cablaggio strutturato realizzabile (rame) per postazioni fisse; Wi-Fi per dispositivi mobili.  
A3) Il sito pubblico e l’area abbonati sono sullo stesso dominio; database su server interno separato dal web server (best practice).  
A4) Numero postazioni fisse: 1 PC direttore + 30 PC giornalisti + 2 PC redattori = 33 PC; stampanti 2; più 10–30 dispositivi Wi-Fi “a picco” (stima).  
A5) Abbonati 5.000: carico web moderato (sito locale), con picchi; necessaria cache e separazione DMZ/LAN.  
A6) Collegamento Internet professionale con IP statico e banda simmetrica, oppure FTTC/FTTH business con SLA; se possibile doppio link (primario + backup).  

---

PRIMA PARTE

1. PROGETTO (ANCHE GRAFICO) DELL’INFRASTRUTTURA DI RETE

Architettura generale (a livelli, con segmentazione):

* Livello accesso: switch per gli uffici (collegano PC e stampanti).
* Livello distribuzione/core: uno switch “core” nel CED a cui arrivano i link dagli switch degli uffici.
* Perimetro: firewall/router verso Internet.
* DMZ: rete separata dove collocare il Web server (e, se serve, un reverse proxy).
* LAN interna: rete uffici (giornalisti, redattori, direttore).
* Rete server interna: database e servizi infrastrutturali (DNS/DHCP/LDAP ecc.), non direttamente esposti a Internet.
* Wi-Fi: SSID separati (aziendale e ospiti/collaboratori), mappati su VLAN diverse.

“Schema grafico” testuale (topologia logica):

```
Internet
   |
Modem/ONT (ISP)
   |
Firewall/Router (NAT, VPN, IDS/IPS)
   |-------------------(VLAN DMZ)-------------------|
   |                                                |
```

(VLAN LAN)                                      Web/Reverse Proxy
|
Switch Core (CED, in rack)
|--------------------|--------------------|
trunk VLAN           trunk VLAN           trunk VLAN
|                    |                    |
Switch uffici       Switch redattori      Switch direttore
(giornalisti)         (2 PC + stamp.)     (1 PC + stamp.)
|
Prese RJ45 Cat6A verso postazioni

```
Wi-Fi AP (PoE) -> VLAN Wi-Fi Aziendale / VLAN Guest
```

Risorse hardware consigliate (dimensionate in modo realistico):

* 1 firewall UTM (stateful firewall + VPN + IDS/IPS base + web filtering opzionale).
* 1 switch core L3 (o L2 con router-on-a-stick sul firewall; L3 consigliato se si vuole routing VLAN interno robusto).
* 2–3 switch di accesso L2 (48 porte o combinazione 24+24), con PoE almeno per alimentare Access Point.
* 2–4 Access Point Wi-Fi (dipende da metratura e pareti), idealmente con controller (anche software).
* 1 rack 19" con patch panel, UPS (gruppo di continuità) e gestione ordinata del cablaggio.
* Cablaggio strutturato: Cat6A (1 Gbps oggi, 10 Gbps su tratte brevi/adeguate), patch panel, prese, certificazione impianto.
* Server:

  * Server Web/Reverse proxy in DMZ (fisico o VM).
  * Server DB in rete server interna (fisico o VM).
  * Opzionale: 1 host di virtualizzazione per consolidare (Proxmox/VMware/Hyper-V) e separare VM web, DB, DNS/DHCP, monitoring.
* Backup: NAS o storage dedicato + copia offsite (cloud o disco ruotato in luogo diverso).
* Stampanti: in LAN con IP statico o reservation DHCP.

Risorse software (scelte tipiche, non vincolanti):

* Sistema operativo server: Linux (es. Debian/Ubuntu/RHEL) oppure Windows Server; dipende dalle competenze interne.
* Web stack: Nginx/Apache + applicazione (CMS o custom) + cache (es. Redis) + CDN opzionale.
* DBMS: PostgreSQL o MySQL/MariaDB.
* Servizi infrastrutturali: DNS, DHCP, NTP, directory (LDAP/Active Directory) se si vuole gestione utenti centralizzata.
* Logging e monitoring: syslog centralizzato + monitor (Zabbix/Prometheus/Grafana o equivalenti).
* Gestione certificati TLS: ACME client (es. certbot) se certificati pubblici.

Collegamento a Internet: caratteristiche richieste

* IP pubblico statico (necessario se si ospita internamente il sito e/o VPN verso sede).
* Banda in upload adeguata (molto importante se si serve contenuto dall’interno).
* SLA e assistenza business.
* Opzione di ridondanza: secondo link (anche consumer) come failover (dual-WAN sul firewall).
* DNS pubblico: record A/AAAA verso IP pubblico; se IP dinamico, servirebbe DDNS (sconsigliato in ambito business).

2. TECNICHE DI PROTEZIONE DA ACCESSI ESTERNI

Obiettivo: ridurre superficie d’attacco e contenere i danni se un componente viene compromesso.

Misure principali (difesa a livelli):

* Separazione in VLAN e DMZ:

  * DMZ: solo servizi esposti (HTTPS 443).
  * LAN uffici: nessuna esposizione diretta.
  * Rete server: accessibile solo da componenti autorizzati (web server verso DB su porta DB, amministrazione solo da VLAN admin).
* Firewall “default deny” in ingresso:

  * Consentire solo 443 verso reverse proxy/web in DMZ.
  * Bloccare tutto il resto.
* Reverse proxy / WAF (se possibile):

  * Terminazione TLS, rate limiting, protezione base da attacchi applicativi comuni.
* Aggiornamenti e hardening:

  * Patch regolari OS e applicazione.
  * Disabilitare servizi non necessari.
* Autenticazione forte per backoffice:

  * MFA per direttore/redattori.
  * Accesso al pannello di amministrazione solo da VPN o da IP aziendali.
* VPN per accesso remoto:

  * Nessun servizio di amministrazione esposto su Internet (SSH/RDP).
  * Accesso amministrativo solo via VPN.
* IDS/IPS e monitoraggio:

  * Alert su scansioni, brute force, anomalie.
  * Log centralizzati e conservazione.
* Backup e ripristino:

  * Backup offline/immutabile per mitigare ransomware.
  * Test periodici di restore.
* Sicurezza Wi-Fi:

  * WPA2-Enterprise o WPA3-Enterprise se disponibile (con RADIUS).
  * SSID guest isolato (solo Internet) e senza visibilità sulla LAN.

3. PRINCIPALI SERVIZI E CONFIGURAZIONE DI DUE A SCELTA

Servizi tipici necessari in una LAN moderna:

* DHCP: assegnazione automatica IP, gateway, DNS, lease, reservation per stampanti.
* DNS interno: risoluzione nomi locali (server, stampanti) e caching.
* NTP: sincronizzazione oraria (fondamentale per log e autenticazione).
* Directory/identità: LDAP/Active Directory per utenti interni (opzionale ma utile).
* RADIUS: autenticazione Wi-Fi enterprise e/o VPN (opzionale).
* File/print services: condivisioni e stampa (se richiesto).
* Monitoring e logging centralizzato.
* Mail: spesso esternalizzata (Microsoft 365/Google Workspace); in alternativa server mail interno (più complesso).

Approfondimento configurazione 1: DHCP (scelte e passi)

* Definire pool per ogni VLAN (esempio logico):

  * VLAN LAN uffici: 10.10.10.0/24
  * VLAN redazione: 10.10.20.0/24
  * VLAN direttore: 10.10.30.0/24
  * VLAN server: 10.10.40.0/24 (di solito statici, DHCP limitato o assente)
  * VLAN guest: 10.10.90.0/24
* Opzioni DHCP:

  * Router (default gateway) = IP dell’interfaccia VLAN sul core/firewall.
  * DNS = DNS interno (che poi inoltra verso resolver pubblici).
  * Lease time più corto per guest, più lungo per PC fissi.
* Reservation:

  * Stampanti e apparati di rete con “reservation” per avere IP stabile.
* Sicurezza:

  * DHCP snooping sugli switch per bloccare DHCP rogue.
  * Separare guest da LAN.

Approfondimento configurazione 2: DNS interno (scelte e passi)

* DNS autoritativo interno per una zona locale (es. lan.giornale.local) e caching/forwarding verso Internet.
* Record principali:

  * web-interno, db, nas, stampanti.
* Inoltro (forwarders):

  * Resolver affidabili (ISP o pubblici) e, se possibile, DNS over TLS/HTTPS a livello firewall.
* Sicurezza:

  * Limitare trasferimenti di zona.
  * Logging query (con attenzione alla privacy) per diagnosi.
  * Split-horizon DNS se si usa lo stesso nome sia dentro sia fuori (interno risolve su IP privati, esterno su IP pubblico).

4. GESTIONE INTERNA VS HOSTING/HOUSING: VANTAGGI E SVANTAGGI

Soluzione interna (on-premise):
Vantaggi

* Controllo completo su dati, rete, configurazioni.
* Possibile integrazione stretta con LAN e workflow interni.
* Costi ricorrenti potenzialmente inferiori se infrastruttura già presente e personale competente.

Svantaggi

* Responsabilità totale su sicurezza, patching, continuità operativa.
* Necessità di ridondanza (UPS, link Internet, backup offsite, antincendio) per avere livelli professionali.
* Difficoltà a gestire picchi di traffico e protezione DDoS.

Hosting (server presso provider, gestito dal provider a vari livelli):
Vantaggi

* Alta disponibilità più facile (data center con ridondanze).
* Scalabilità (verticale/orizzontale) e servizi gestiti (WAF, backup, monitoring).
* Protezioni perimetrali spesso migliori (anti-DDoS, firewalling a monte).

Svantaggi

* Meno controllo fisico e dipendenza dal provider.
* Costi ricorrenti e vincoli contrattuali.
* Necessità di gestire correttamente sicurezza applicativa comunque (non delegabile del tutto).

Housing (server di proprietà nel data center):
Vantaggi

* Controllo sull’hardware, ma con benefici del data center (alimentazione, climatizzazione, connettività).
* Buon compromesso se si hanno server propri e competenze.

Svantaggi

* Sempre necessario personale competente per gestione OS/applicazioni.
* Logistica e tempi di intervento (accesso in DC) non immediati.

Scelta motivata (coerente con il caso):

* Se l’obiettivo è modernizzare riducendo rischi e oneri: hosting (o cloud) per web+DB, mantenendo in sede solo LAN e servizi locali.
* Se vincoli di budget iniziale e si accetta complessità operativa: soluzione interna con DMZ ben fatta, backup offsite e almeno un minimo di ridondanza.

---

SECONDA PARTE (SCELTI 2 QUESITI: 1 e 2)

QUESITO 1
MODELLO CONCETTUALE E LOGICO PER DIFFERENZIARE GLI ACCESSI, PROGETTO PAGINE WEB, CODIFICA PARTE SIGNIFICATIVA

Requisiti funzionali (esplicitati)

* Utente generico non registrato:

  * vedere sito pubblico: informazioni e sintesi articoli.
* Abbonato:

  * autenticarsi e leggere articolo completo (testo completo + immagine + eventuale filmato).
  * gestire abbonamento (attivo/scaduto).
* Direttore e redattori:

  * autenticarsi e accedere a backoffice.
  * creare/modificare articoli e numeri settimanali.
  * gestire pubblicazione (stato bozza/pubblicato).
* Tracciamento minimo:

  * log accessi (almeno per area riservata).
* Sicurezza password:

  * hash robusto, nessuna password in chiaro.

Assunzioni progettuali per la base dati  
A7) “Direttore” e “redattori” sono utenti interni con ruolo; i “giornalisti” possono essere opzionali nel backoffice (non richiesti dal quesito, ma la base può supportarli).  
A8) L’abbonamento è un attributo separato (Subscription) con data inizio/fine e stato.  
A9) Un articolo appartiene a un numero settimanale (Issue). Un Issue contiene ~100 articoli.  
A10) Ogni articolo ha almeno 1 immagine; eventuale filmato. Per generalità si modella Media multiplo.  

PLANTUML: DIAGRAMMA ER (CONCETTUALE)
(Testo PlantUML; incollare in PlantUML per generare il diagramma)

```
@startuml
hide circle
skinparam linetype ortho

entity "User" as USER {
    * user_id : int
    --
    email : varchar
    password_hash : varchar
    full_name : varchar
    status : enum(active, disabled)
    created_at : datetime
    last_login_at : datetime
}

entity "Role" as ROLE {
    * role_id : int
    --
    name : enum(SUBSCRIBER, EDITOR, DIRECTOR)
    description : varchar
}

entity "UserRole" as USERROLE {
    * user_id : int
    * role_id : int
    --
    assigned_at : datetime
}

entity "Subscription" as SUB {
    * subscription_id : int
    --
    user_id : int
    start_date : date
    end_date : date
    status : enum(active, expired, suspended)
    payment_ref : varchar
}

entity "Issue" as ISSUE {
    * issue_id : int
    --
    week_start : date
    publish_date : date
    title : varchar
    status : enum(draft, published)
}

entity "Article" as ART {
    * article_id : int
    --
    issue_id : int
    title : varchar
    summary : text
    body : text
    status : enum(draft, published)
    created_at : datetime
    updated_at : datetime
    published_at : datetime
}

entity "Media" as MED {
    * media_id : int
    --
    media_type : enum(image, video)
    url : varchar
    mime_type : varchar
    size_bytes : bigint
    created_at : datetime
}

entity "ArticleMedia" as ARTMED {
    * article_id : int
    * media_id : int
    --
    position : int
    is_cover : boolean
}

USER ||--o{ USERROLE
ROLE ||--o{ USERROLE

USER ||--o{ SUB
ISSUE ||--o{ ART
ART ||--o{ ARTMED
MED ||--o{ ARTMED

@enduml
```

Nota concettuale importante (accesso differenziato)

* Utente non registrato: non esiste record USER; accede solo a contenuti “pubblici” (summary).
* Abbonato: USER con ruolo SUBSCRIBER e Subscription attiva (data fine >= oggi e status active).
* Direttore/redattori: USER con ruolo DIRECTOR o EDITOR (non dipende da Subscription).

PLANTUML: MODELLO LOGICO (INFORMATION ENGINEERING / TABELLE CON PK-FK)
(Rappresentazione logica stile “tabelle”)

```
@startuml
skinparam linetype ortho
hide methods
hide stereotypes

class users {
    +PK user_id : int
    email : varchar (unique)
    password_hash : varchar
    full_name : varchar
    status : varchar
    created_at : datetime
    last_login_at : datetime
}

class roles {
    +PK role_id : int
    name : varchar (unique)
    description : varchar
}

class user_roles {
    +PK,FK user_id : int
    +PK,FK role_id : int
    assigned_at : datetime
}

class subscriptions {
    +PK subscription_id : int
    +FK user_id : int
    start_date : date
    end_date : date
    status : varchar
    payment_ref : varchar
}

class issues {
    +PK issue_id : int
    week_start : date
    publish_date : date
    title : varchar
    status : varchar
}

class articles {
    +PK article_id : int
    +FK issue_id : int
    title : varchar
    summary : text
    body : text
    status : varchar
    created_at : datetime
    updated_at : datetime
    published_at : datetime
}

class media {
    +PK media_id : int
    media_type : varchar
    url : varchar
    mime_type : varchar
    size_bytes : bigint
    created_at : datetime
}

class article_media {
    +PK,FK article_id : int
    +PK,FK media_id : int
    position : int
    is_cover : boolean
}

users "1" -- "0..*" subscriptions
users "1" -- "0..*" user_roles
roles "1" -- "0..*" user_roles
issues "1" -- "0..*" articles
articles "1" -- "0..*" article_media
media "1" -- "0..*" article_media

@enduml
```

Pagine web necessarie (progetto logico-funzionale)
Area pubblica:

* Home: lista numeri settimanali e articoli (mostrare summary).
* Dettaglio articolo pubblico: titolo, immagine di copertina, summary; call-to-action “accedere per articolo completo”.

Area autenticata abbonati:

* Login (email + password).
* Logout.
* Profilo: stato abbonamento (attivo/scadenza) e dati utente.
* Articolo completo: body + media (immagine/filmato) solo se Subscription attiva.
* Eventuale recupero password (minimo: invio link).

Backoffice (direttore/redattori):

* Login (stesso della piattaforma).
* Dashboard: elenco issue e articoli (filtri per stato).
* CRUD issue: creare/modificare, pubblicare.
* CRUD articoli: creare/modificare, caricare media, pubblicare.
* Gestione utenti (minimo): creare utenti redattori/direttore, assegnare ruoli.

Regole di autorizzazione (RBAC + condizione abbonamento):

* Per vedere un articolo completo: ruolo SUBSCRIBER e Subscription attiva.
* Per backoffice: ruolo EDITOR o DIRECTOR.
* Permessi aggiuntivi: DIRECTOR può gestire utenti; EDITOR può solo contenuti (assunzione comune).

CODIFICA (ESEMPIO IN PHP, “PARTE SIGNIFICATIVA”: LOGIN + MIDDLEWARE AUTORIZZAZIONE)
(Indentazione a 4 spazi; usare PDO; password_hash/password_verify)

File: db.php

```
<?php
function db(): PDO {
    static $pdo = null;
    if ($pdo !== null) {
        return $pdo;
    }

    $dsn = "mysql:host=127.0.0.1;dbname=giornale;charset=utf8mb4";
    $user = "app_user";
    $pass = "app_pass";

    $pdo = new PDO($dsn, $user, $pass, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ]);
    return $pdo;
}
```

File: auth.php

```
<?php
require_once __DIR__ . "/db.php";

function start_session(): void {
    if (session_status() === PHP_SESSION_NONE) {
        session_start();
    }
}

function login(string $email, string $password): bool {
    start_session();

    $stmt = db()->prepare("SELECT user_id, password_hash, status FROM users WHERE email = :email");
    $stmt->execute([":email" => $email]);
    $u = $stmt->fetch();

    if (!$u) {
        return false;
    }
    if ($u["status"] !== "active") {
        return false;
    }
    if (!password_verify($password, $u["password_hash"])) {
        return false;
    }

    $_SESSION["user_id"] = (int)$u["user_id"];
    $_SESSION["email"] = $email;
    return true;
}

function logout(): void {
    start_session();
    $_SESSION = [];
    session_destroy();
}

function current_user_id(): ?int {
    start_session();
    return isset($_SESSION["user_id"]) ? (int)$_SESSION["user_id"] : null;
}

function user_has_role(int $user_id, string $role_name): bool {
    $sql = "
        SELECT 1
        FROM user_roles ur
        JOIN roles r ON r.role_id = ur.role_id
        WHERE ur.user_id = :uid AND r.name = :rname
        LIMIT 1
    ";
    $stmt = db()->prepare($sql);
    $stmt->execute([":uid" => $user_id, ":rname" => $role_name]);
    return (bool)$stmt->fetch();
}

function subscription_is_active(int $user_id): bool {
    $sql = "
        SELECT 1
        FROM subscriptions
        WHERE user_id = :uid
          AND status = 'active'
          AND end_date >= CURRENT_DATE()
        ORDER BY end_date DESC
        LIMIT 1
    ";
    $stmt = db()->prepare($sql);
    $stmt->execute([":uid" => $user_id]);
    return (bool)$stmt->fetch();
}

function require_login(): int {
    $uid = current_user_id();
    if ($uid === null) {
        header("Location: /login.php");
        exit;
    }
    return $uid;
}

function require_backoffice(): int {
    $uid = require_login();

    $is_editor = user_has_role($uid, "EDITOR");
    $is_director = user_has_role($uid, "DIRECTOR");
    if (!$is_editor && !$is_director) {
        http_response_code(403);
        echo "Accesso negato (403).";
        exit;
    }
    return $uid;
}

function require_active_subscriber(): int {
    $uid = require_login();

    if (!user_has_role($uid, "SUBSCRIBER")) {
        http_response_code(403);
        echo "Accesso negato (403).";
        exit;
    }
    if (!subscription_is_active($uid)) {
        http_response_code(402);
        echo "Abbonamento non attivo o scaduto.";
        exit;
    }
    return $uid;
}
```

File: login.php (estratto minimo)

```
<?php
require_once __DIR__ . "/auth.php";

$error = "";
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $email = trim($_POST["email"] ?? "");
    $pass = $_POST["password"] ?? "";

    if (login($email, $pass)) {
        header("Location: /index.php");
        exit;
    }
    $error = "Credenziali non valide.";
}
?>
<!doctype html>
<html>
<head><meta charset="utf-8"><title>Login</title></head>
<body>
    <h1>Login</h1>
    <?php if ($error !== "") { echo "<p>" . htmlspecialchars($error) . "</p>"; } ?>
    <form method="post">
        <label>Email</label><br>
        <input name="email" type="email" required><br>
        <label>Password</label><br>
        <input name="password" type="password" required><br><br>
        <button type="submit">Accedere</button>
    </form>
</body>
</html>
```

File: article_full.php (protezione contenuto completo)

```
<?php
require_once __DIR__ . "/auth.php";
$uid = require_active_subscriber();

$article_id = (int)($_GET["id"] ?? 0);
$stmt = db()->prepare("SELECT title, body FROM articles WHERE article_id = :id AND status = 'published'");
$stmt->execute([":id" => $article_id]);
$a = $stmt->fetch();

if (!$a) {
    http_response_code(404);
    echo "Articolo non trovato.";
    exit;
}

echo "<h1>" . htmlspecialchars($a["title"]) . "</h1>";
echo "<div>" . $a["body"] . "</div>";
```

Nota didattica di sicurezza (implicita nel codice):

* Password: usare password_hash (bcrypt/argon2 a seconda della versione).
* Query: prepared statements per prevenire SQL injection.
* Sessione: impostare cookie secure/httponly/samesite e rigenerare session id dopo login (miglioria consigliata).

QUESITO 2
HTTPS, SSL/TLS: FUNZIONAMENTO E STRUMENTI NECESSARI

Precisazione terminologica

* “SSL” è il nome storico; oggi si usa TLS (Transport Layer Security). In ambito comune si dice “SSL” ma le versioni moderne sono TLS. ([datatracker.ietf.org][1])

Che cosa garantisce HTTPS (in sintesi corretta)

* Confidenzialità: i dati scambiati sono cifrati (anti intercettazione).
* Integrità: rilevazione di modifiche durante il transito.
* Autenticazione del server: il client verifica che il certificato appartenga al dominio (catena di fiducia CA). ([datatracker.ietf.org][1])

Come funziona a grandi passi (TLS handshake semplificato, modello moderno)

1. ClientHello:

   * il browser invia versioni TLS supportate, cipher suites, estensioni (SNI), e parametri crittografici.
2. ServerHello:

   * il server sceglie parametri e invia il certificato (catena CA).
3. Verifica certificato:

   * il client valida la catena fino a una CA fidata e controlla che il dominio corrisponda. ([datatracker.ietf.org][2])
4. Scambio chiavi e creazione chiave di sessione:

   * tipicamente con meccanismi (EC)DHE per ottenere “forward secrecy”.
5. Canale cifrato:

   * da quel momento HTTP viaggia dentro TLS (quindi “HTTPS”). ([datatracker.ietf.org][1])

Strumenti necessari per implementare HTTPS/TLS su un sito reale

* Un server web (es. Nginx o Apache) configurato per ascoltare su 443.
* Un certificato X.509 per il dominio (con relativa chiave privata) emesso da una CA.
* Una procedura di gestione certificati:

  * emissione, rinnovo, revoca.
  * automatizzazione tramite ACME (es. Let’s Encrypt). ([letsencrypt.org][3])
* Scelte di configurazione sicura:

  * disabilitare protocolli obsoleti, scegliere cipher suite adeguate, abilitare HSTS se opportuno.
  * Linee guida pratiche: OWASP TLS Cheat Sheet. ([cheatsheetseries.owasp.org][4])

---

## Alcuni riferimenti

RFC 8446 (TLS 1.3), IETF Datatracker
[https://datatracker.ietf.org/doc/html/rfc8446](https://datatracker.ietf.org/doc/html/rfc8446)
([datatracker.ietf.org][1])

RFC 5280 (X.509 Certificates), IETF Datatracker
[https://datatracker.ietf.org/doc/html/rfc5280](https://datatracker.ietf.org/doc/html/rfc5280)
([datatracker.ietf.org][2])

OWASP Transport Layer Security Cheat Sheet
[https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
([cheatsheetseries.owasp.org][4])

Let’s Encrypt – Getting Started
[https://letsencrypt.org/getting-started/](https://letsencrypt.org/getting-started/)
([letsencrypt.org][3])

Let’s Encrypt – Documentation
[https://letsencrypt.org/docs/](https://letsencrypt.org/docs/)
([letsencrypt.org][5])

[1]: https://datatracker.ietf.org/doc/html/rfc8446?utm_source=chatgpt.com "RFC 8446 - The Transport Layer Security (TLS) Protocol ..."
[2]: https://datatracker.ietf.org/doc/html/rfc5280?utm_source=chatgpt.com "RFC 5280 - Internet X.509 Public Key Infrastructure ..."
[3]: https://letsencrypt.org/getting-started/?utm_source=chatgpt.com "Getting Started"
[4]: https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html?utm_source=chatgpt.com "Transport Layer Security - OWASP Cheat Sheet Series"
[5]: https://letsencrypt.org/docs/?utm_source=chatgpt.com "Documentation"
