# Agenti Esterni

Per maggiori informazioni vai a: https://www.ibm.com/docs/en/watsonx/watson-orchestrate/base?topic=platforms-adding-agents-from-third-party

## Come Aggiungere un Agente Esterno

1. Nella pagina di modifica dell'agente, clicca su **Toolset > add agent**
2. Scegli **import**
3. Seleziona **agente esterno**

## Opzioni di Protocollo

Scegli una delle seguenti opzioni:

### 1. Agente esterno tramite standard A2A

Usa questa opzione per agenti che implementano il protocollo A2A, uno standard aperto che permette a diversi sistemi di agenti di interoperare.

### 2. Agente esterno tramite chat completion

Seleziona questa opzione per integrare un agente che implementa un'API di chat completions in stile OpenAI.

### 3. watsonx.ai

Scegli questa opzione quando importi un agente distribuito da watsonx.ai.

---

## Configurazione per Agente Esterno tramite Standard A2A

Specifica i seguenti parametri:

### Parametri di Connessione
- **Versione del Protocollo A2A**: Seleziona la versione dal menu a tendina
- **Tipo di autenticazione**: Scegli Bearer token o API key
  - *Nota: Ottieni i dati di autenticazione dalla piattaforma dove è ospitato l'agente AI esterno*
- **URL dell'agente esterno**: Inserisci l'URL del server che ospita l'agente AI esterno

### Dettagli dell'Agente
- **Nome visualizzato**: Fornisci un nome per l'agente
- **Descrizione delle capacità dell'agente**: Includi parole chiave che descrivono le funzionalità dell'agente
  - *Per maggiori dettagli, vedi Raccomandazioni per le descrizioni degli agenti*

### Impostazioni Avanzate
Attiva/disattiva le seguenti opzioni:
- Supporta streaming
- Supporta notifiche push
- Invia cronologia conversazione

---

## Configurazione per Agente Esterno tramite Chat Completion

Specifica i seguenti parametri:

### Parametri di Connessione
- **Tipo di autenticazione**: Scegli Bearer token o API key
  - *Nota: Ottieni i dati di autenticazione dalla piattaforma dove è ospitato l'agente AI esterno*
- **URL dell'agente esterno**: Inserisci l'URL del server che ospita l'agente AI esterno

### Dettagli dell'Agente
- **Nome visualizzato**: Specifica il nome visualizzato dell'agente
- **Descrizione delle capacità dell'agente**: Descrivi le funzionalità dell'agente

### Impostazioni Avanzate
Attiva/disattiva le seguenti opzioni:
- Supporta streaming
- Supporta notifiche push
- Invia cronologia conversazione

---

## Configurazione per watsonx.ai

Specifica i seguenti parametri:

### Parametri di Connessione
- **Tipo di autenticazione**: Scegli Bearer token o API key
  - *Nota: Ottieni i dati di autenticazione dalla piattaforma dove è ospitato l'agente AI esterno*
- **URL dell'istanza del servizio**: Inserisci l'URL dell'istanza watsonx.ai

### Dettagli dell'Agente
- **Nome visualizzato**: Specifica il nome visualizzato dell'agente
- **Descrizione delle capacità dell'agente**: Descrivi le funzionalità dell'agente

---

## Completamento dell'Importazione

Clicca su **Importa agente** per completare la configurazione.

## Cosa Fare Successivamente

1. **Configura il comportamento dell'agente**: Imposta il comportamento e le linee guida dell'agente per assicurarti che risponda accuratamente nei tuoi casi d'uso
   - Vedi: *Configurazione del comportamento dell'agente*

2. **Testa l'agente**: Usa **Anteprima** per validare le risposte dell'agente e verificare che la connessione funzioni correttamente