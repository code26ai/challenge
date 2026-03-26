# Approfondimento: Connessioni in watsonx Orchestrate

## Cos'è una Connessione?

Quando watsonx Orchestrate interagisce con un servizio esterno — sia attraverso un tool, una knowledge base o un agente esterno — ha bisogno di un modo per autenticarsi contro quel servizio in modo sicuro. Una **connessione** è l'oggetto in watsonx Orchestrate che contiene tutte le informazioni necessarie per farlo: il metodo di autenticazione, le credenziali e l'ambito di accesso.

Le connessioni disaccoppiano le credenziali dalle risorse che le utilizzano. Ciò significa che puoi aggiornare o ruotare le credenziali in un unico posto senza toccare l'agente, la specifica del tool OpenAPI o qualsiasi altra configurazione di risorsa. La stessa connessione può anche essere riutilizzata su più risorse — tool, knowledge base, agenti esterni — senza duplicare la gestione delle credenziali.

La documentazione di riferimento completa è disponibile su:
- [IBM Docs: Managing app connections and credentials](https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=managing-app-connections-credentials)
- [ADK Developer Reference: Why use connections](https://developer.watson-orchestrate.ibm.com/connections/overview)

---

## Connessione vs. Credenziale

Questi due concetti sono correlati ma distinti:

- Una **connessione** definisce *come* funziona l'autenticazione (il metodo, gli URL, gli ambiti, ecc.). Pensala come un template o un oggetto di configurazione.
- Una **credenziale** è il materiale segreto allegato a una connessione per un utente o team specifico (client secret, chiave API, username/password, ecc.).

---

## Tipi di Autenticazione

watsonx Orchestrate supporta diversi metodi di autenticazione. La scelta giusta dipende da ciò che richiede il servizio di destinazione:

| Tipo | Quando usarlo |
|---|---|
| **API Key** | Il servizio emette un token statico passato in un header o parametro query |
| **Basic Auth** | Il servizio accetta un username e password |
| **Bearer Token** | Un JWT statico o token opaco passato come `Authorization: Bearer ...` |
| **OAuth2 (Client Credentials)** | Machine-to-machine; l'agente si autentica come se stesso |
| **OAuth2 (Authorization Code)** | Delegato dall'utente; l'utente effettua il login interattivamente tramite un redirect del browser |
| **OAuth2 (Password Grant)** | L'agente passa un username/password direttamente all'endpoint del token |
| **Key-Value Pair** | Un dizionario arbitrario di segreti passato a tool Python o toolkit MCP |

> **Nota:** I flussi OAuth che richiedono il login interattivo dell'utente (Authorization Code, Implicit) funzionano solo attraverso l'interfaccia utente integrata di watsonx Orchestrate. Tuttavia, **OAuth2 Client Credentials** — che è machine-to-machine e non richiede redirect del browser — è completamente supportato anche nel widget di chat web incorporato.

---

## Ambito delle Credenziali: Member vs. Team

Per ogni connessione scegli anche se le sue credenziali sono **per utente (member)** o **condivise (team)**:

- **Le credenziali member** sono private per ogni utente. Ogni utente fornisce le proprie. Questo è appropriato quando ogni persona ha il proprio account sul servizio di destinazione. Se un utente non ha ancora fornito le credenziali, watsonx Orchestrate lo richiederà la prima volta che attiva una risorsa che utilizza la connessione attraverso l'interfaccia chat.
- **Le credenziali team** vengono inserite una volta da un amministratore e utilizzate da tutti. Questa è la scelta giusta per un account di servizio condiviso, come un'API di ricerca in sola lettura o un endpoint di agente esterno a cui l'intero team accede con la stessa identità.

In questo laboratorio, la connessione Normattiva utilizza **credenziali team**, perché tutti gli utenti interrogano lo stesso backend con la stessa identità.

---

## Creare una Connessione nell'Interfaccia Utente

1. Dal menu principale di watsonx Orchestrate, vai su **Manage → Connections**.
2. Clicca su **Add new connection**.
3. Inserisci un **Connection ID** (usato internamente, es. `normattiva-search-backend-oauth`) e un **Display name**.
4. Clicca su **Save and continue**.
5. Sotto **Configure draft connection**, scegli un tipo di autenticazione.
6. Compila icampi necessari.
7. Imposta il **Credential type** (Member o Team). Per le credenziali team, clicca su **Connect** per attivare l'accesso per tutti i membri del team.
8. Clicca su **Next**, quindi configura l'ambiente **Live** (puoi incollare la configurazione draft per OAuth2).
9. Clicca su **Add connection**. Un'icona verde connessa conferma il successo.

> **Dopo che l'ambiente Live è configurato**, il tipo di autenticazione è bloccato e non può essere modificato attraverso l'interfaccia utente. Per modificarlo successivamente, usa la [CLI ADK](https://developer.watson-orchestrate.ibm.com/connections/overview).

---

## Associare una Connessione a una Risorsa

Una volta che esiste una connessione, la colleghi alla risorsa specifica che ne ha bisogno. I passaggi esatti variano leggermente in base al tipo di risorsa:

**Tool OpenAPI** (come usato in questo laboratorio):
1. Apri l'agente, vai su **Toolset → Tools** e seleziona il tool.
2. Clicca sulla scheda **Connect**.
3. Seleziona la connessione dal menu a discesa.

**Tool Python**
1. Chiama la connection in `@tool()` (vedi [Documentazione Connections](https://developer.watson-orchestrate.ibm.com/connections/associate_connection_to_tool/python_connections#key-value-connections)).
2. Importa il tool associando direttamente la connection
```bash
orchestrate tools import -k python -f <file-path> -r <requirements-path> -a connection_id
```

**Agenti esterni:**
1. Apri l'agente, vai su **Toolset → Agents** e seleziona l'agente esterno.
2. Clicca sulla scheda **Connect** e seleziona la connessione appropriata.

**Knowledge base** (per backend di ricerca personalizzati o vector store che richiedono autenticazione):
1. Quando crei o modifichi la fonte di conoscenza, seleziona la connessione nel passaggio di autenticazione.

Da questo punto in poi, ogni volta che watsonx Orchestrate invoca quella risorsa, ottiene automaticamente un token dal provider di identità (dove applicabile) e lo allega alla richiesta in uscita. Non è necessaria alcuna logica di gestione delle credenziali nelle definizioni dei tool, nelle istruzioni degli agenti o nella configurazione della knowledge base.

