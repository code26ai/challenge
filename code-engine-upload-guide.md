# Code Engine Upload Guide

## Overview

Questo processo di deployment su IBM Cloud Code Engine si articola in tre fasi principali:

1. **Preparazione e Autenticazione**: Configurazione dell'ambiente locale e autenticazione con IBM Cloud, selezionando il resource group e il progetto Code Engine appropriati.

2. **Build e Push dell'Immagine**: Creazione di un'immagine Docker dell'applicazione utilizzando Podman, tagging dell'immagine per il Container Registry di IBM Cloud, e push dell'immagine nel registry. Questo rende l'immagine disponibile per il deployment su Code Engine.

3. **Deployment su Code Engine**: Creazione dell'applicazione su Code Engine tramite l'interfaccia web di IBM Cloud, dove si configura l'applicazione per utilizzare l'immagine dal registry, si impostano le credenziali di accesso al registry (tramite API key), e si configurano eventuali variabili d'ambiente e risorse necessarie.

Il flusso completo garantisce che l'applicazione containerizzata venga correttamente costruita, archiviata nel registry cloud, e deployata come applicazione serverless su Code Engine.

## Prerequisites

- Podman/Docker installato
- Accesso a IBM Cloud attraverso un IBM-id 

[LINK per poter richiedere un IBM-id](https://www.ibm.com/account/reg/it-it/signup?formid=urx-19776)

## Step 1: IBM Cloud Download and Authentication

Accedere alla repo https://github.com/IBM-Cloud/ibm-cloud-cli-release/releases/ e scaricare e installare la CLI IBM.
Dopo aver proceduto con prerequisiti è possibile procedere con l'autenticazione per poter deployare le proprie applicazini.
Esistono due metodi principali per potersi autenticare:

### Metodo 1: SSO (Single Sign-On) - Uso Interattivo

Ideale per uso manuale e sviluppo locale. Apre il browser per l'autenticazione:

```bash
ibmcloud login --sso
```

### Metodo 2: API Key - Automazione e CI/CD

In caso di uso tramite pipeline automatizzate, script e ambienti CI/CD è possibile utilizzare un autenticazione tramite API key, passando la chiave direttamente nel comando:

```bash
ibmcloud login --apikey <your-api-key>
```

## Step 2: Resource Group Selection

I **resource groups** sono contenitori logici che organizzano le risorse IBM Cloud. Permettono di gestire accessi, fatturazione e organizzazione delle risorse in modo centralizzato.

Lista i resource groups disponibili per identificare quello corretto:

```bash
ibmcloud resource groups
```

Seleziona il resource group dove risiede il tuo progetto Code Engine (dovrebbe iniziare con itz-wxo-...). Questo è necessario perché tutte le operazioni successive (registry, Code Engine) devono operare nel contesto del resource group corretto:

```bash
ibmcloud target -g <resource-group-name>
```

## Step 3: Installazione plugin e Container Registry Login

Il **Container Registry** di IBM Cloud è il repository dove verranno archiviate le immagini Docker. L'autenticazione al registry è necessaria per poter effettuare il push delle immagini.

Se non hai già installato il plugin `container-registry`, installalo prima:
```bash
ibmcloud plugin install container-registry
```

Dopo aver installato il plugin, esegui il login al registry:
```bash
ibmcloud cr login
```
Se non hai già installato il plugin `code-engine`, installa con:
```bash
ibmcloud plugin install code-engine
```
Puoi listare i plugin installati con:
```bash
ibmcloud plugin list
```
## Step 4: Build Container Image

La **build dell'immagine** crea un container eseguibile della tua applicazione. 

Nota: Code Engine esegue container su architettura x86_64, il flag `--platform linux/amd64` può essere utilizzato per creare delle build x86_64 anche se lo sviluppo avviene su MAC Apple Silicon (ARM). I comandi di seguito possono essere eseguiti indipendentemente da CLI *podman* o *docker*.


```bash
podman build --platform linux/amd64 -t <app-name> .
```

Questo comando legge il `Dockerfile` nella directory corrente (`.`) e crea un'immagine locale con il nome specificato.

## Step 5: Tag container Image

Il **tagging** prepara l'immagine per il push al registry remoto. È necessario "rinominare" l'immagine locale con il percorso completo del registry IBM Cloud, che include:
- **registry-url**: L'endpoint del registry (es. `de.icr.io` per Germania)
- **namespace**: Il tuo namespace personale nel registry
- **app-name**: Il nome dell'applicazione
- **tag**: La versione (es. `latest`)

### 5.1: Verifica l'immagine locale

Prima di tutto, verifica il nome dell'immagine che hai buildato nello Step 4:

```bash
podman images
```

Cerca l'immagine nella lista. Il nome sarà nella colonna `REPOSITORY`. Questo è il tuo `<local-image-name>`.

### 5.2: Identifica il registry URL

Il **registry URL** dipende dalla regione IBM Cloud che stai usando. Verifica la tua regione corrente:

```bash
ibmcloud target
```

Nella risposta, cerca il campo `Region`. In base alla regione, usa il registry URL corrispondente:

| Regione | Registry URL |
|---------|--------------|
| eu-de (Germania/Frankfurt) | `de.icr.io` |
| eu-gb (Regno Unito/Londra) | `uk.icr.io` |
| us-south (USA/Dallas) | `us.icr.io` |
| us-east (USA/Washington DC) | `us.icr.io` |
| jp-tok (Giappone/Tokyo) | `jp.icr.io` |
| au-syd (Australia/Sydney) | `au.icr.io` |

### 5.3: Verifica o crea il namespace

Il **namespace** è un contenitore logico nel Container Registry dove vengono archiviate le tue immagini. Ogni account può avere più namespace.

Lista i namespace esistenti:

```bash
ibmcloud cr namespace-list
```

Se non hai namespace o vuoi crearne uno nuovo:

```bash
ibmcloud cr namespace-add <namespace-name>
```

> **Suggerimento**: Usa un nome descrittivo come `my-apps`, `production`, o il nome della tua organizzazione. Il namespace deve essere univoco a livello globale in IBM Cloud.

### 5.4: Esegui il tag

Ora che hai tutte le informazioni, esegui il comando di tagging:

```bash
podman tag <local-image-name> <registry-url>/<namespace>/<app-name>:latest
```

**Esempio pratico completo**:

Supponiamo che:
- La tua immagine locale si chiama `my-app`
- Sei nella regione `eu-de` (Germania)
- Il tuo namespace è `my-namespace`
- Vuoi chiamare l'app `my-app` anche nel registry

Il comando sarà:

```bash
podman tag my-app de.icr.io/my-namespace/my-app:latest
```

### 5.5: Verifica il tag

Dopo il tagging, verifica che l'immagine sia stata taggata correttamente:

```bash
podman images | grep <app-name>
```

Dovresti vedere due righe:
1. L'immagine originale con il nome locale
2. L'immagine taggata con il percorso completo del registry

**Esempio di output**:
```
localhost/my-app                    latest      abc123def456  10 minutes ago  150 MB
de.icr.io/my-namespace/my-app       latest      abc123def456  10 minutes ago  150 MB
```

> **Nota importante**: Il tagging non copia l'immagine, crea solo un alias. Entrambe le righe puntano alla stessa immagine (stesso IMAGE ID).

## Step 6: Push Image to Registry

Il **push** carica l'immagine dal tuo computer locale al Container Registry di IBM Cloud. in modo che Code Engine possa scaricare l'immagine da un registry remoto accessibile via internet:

```bash
podman push <registry-url>/<namespace>/<app-name>:latest
```

Dopo questo comando, l'immagine sarà disponibile nel cloud e pronta per essere deployata.

## Step 7: Code Engine Project Setup

I **progetti Code Engine** sono ambienti isolati dove vengono eseguite le applicazioni. Ogni progetto ha le proprie risorse e configurazioni.

Lista i progetti disponibili per vedere quali hai già creato:

```bash
ibmcloud ce project list
```

Seleziona il progetto target dove vuoi deployare l'applicazione. Questo imposta il contesto per tutti i comandi successivi:

```bash
ibmcloud ce project select -n <project-name>
```

> **Perché serve?** Code Engine ha bisogno di sapere in quale progetto operare. Senza questa selezione, i comandi successivi non saprebbero dove creare risorse.

## Step 8: Create Secret for Environment Variables

I **secrets** sono il modo sicuro per gestire dati sensibili (API keys, password, configurazioni) in Code Engine. Invece di hardcodare valori sensibili nel codice o nell'immagine, li memorizzi come secret e li inietti come variabili d'ambiente a runtime.

Il **secret-name** è un identificatore univoco per il secret all'interno del progetto. Usa nomi descrittivi come `app-secrets`, `db-credentials`, o `nextjs-env`.

```bash
ibmcloud ce secret create --name <secret-name> --from-env-file .env
```

Questo comando legge un file `.env` locale e crea un secret in Code Engine con tutte le variabili contenute. L'applicazione potrà poi accedere a queste variabili come normali environment variables.

> **Nota**: Questo step è opzionale. Se la tua applicazione non richiede variabili d'ambiente, puoi saltarlo.

## Step 9: Create Application from UI

La **creazione dell'applicazione** è il passo finale dove Code Engine viene configurato per eseguire il tuo container. L'interfaccia web offre un modo intuitivo per configurare tutti i parametri necessari.

### 9.1: Crea una API Key

Prima di creare l'applicazione, devi generare una **API key** che permetterà a Code Engine di accedere al Container Registry privato per scaricare l'immagine.

**Procedura**:

1. Vai su [IBM Cloud Console](https://cloud.ibm.com/)
2. Clicca su **Manage** nella topbar in alto
3. Seleziona **Access (IAM)**
4. Nel menu laterale, clicca su **API keys**
5. Clicca sul pulsante **Create +**
6. Configura l'API key:
   - **Name**: Inserisci un nome descrittivo (es. `code-engine-registry-access`)
   - **Description** (opzionale): Aggiungi una descrizione (es. "API key per Code Engine registry access")
7. Clicca su **Create**
8. **Importante**: Copia e salva l'API key in un luogo sicuro. Non potrai visualizzarla nuovamente dopo aver chiuso la finestra.

> **Nota**: L'API key ha gli stessi permessi del tuo account utente. Trattala come una password e non condividerla.

### 9.2: Crea l'applicazione

Ora puoi creare l'applicazione su Code Engine usando l'API key appena generata.

**Procedura**:

1. Vai su [IBM Cloud Console](https://cloud.ibm.com/)
2. Naviga su **Containers** dal menu hamburger e poi su **Serverless projects**
3. Seleziona il tuo **Project** (quello creato nello Step 7)
4. Clicca su **Applications** nella sidebar sinistra
5. Clicca sul pulsante **Create**
6. Configura l'applicazione:
   - **Name**: Inserisci il nome della tua applicazione (es. `nextjs-demo-app`)
   - **Code**: Seleziona **Use an existing container image**
   - **Image reference**: Inserisci il percorso completo dell'immagine (es. `de.icr.io/<namespace>/<app-name>:latest`)
   - **Registry access**: Clicca su **Configure image** per impostare l'accesso al registry:
     - Inserisci il **Registry Server** (es. `de.icr.io`)
     - Clicca su **Registry secret** e poi **Create registry secret**
     - Inserisci la tua **API key** creata nello Step 9.1
     - Clicca **Create**
   - Clicca su **Done**
7. Configura le impostazioni aggiuntive:
   - **Environment variables** (opzionale): Seleziona **Reference to full secret** e scegli il secret creato nello Step 8
   - **Resources**: Imposta CPU e memoria in base alle necessità dell'applicazione (minimo: 0.5 vCPU, 1 GB RAM)
   - **Scaling**: Configura il numero minimo/massimo di istanze e le condizioni di autoscaling
8. Clicca su **Create**

> **Cosa succede ora?** Code Engine scarica l'immagine dal registry usando l'API key, crea i container, li avvia e li rende accessibili tramite un URL pubblico. Il processo può richiedere alcuni minuti.

## N.B 
E' possibile creare e deployare l'applicazione direttamente da terminale usando il comando:
```bash
ibmcloud ce app create --name <your-app-name> --port 8080 -v public --min-scale 1 --image private.<registry-url>/<namespace>/<app-name>:latest --registry-secret <registry-secret-name>
```

## Step 10: View Application Logs

```bash
ibmcloud ce application logs --name <app-name>
```

Puoi anche visualizzare i logs dall'interfaccia web: vai su Applications → seleziona la tua app → tab **Logs**.

## Notes

- **Registry privato**: L'immagine viene caricata dal Container Registry di IBM Cloud. Code Engine necessita delle credenziali (API key) per accedere al registry privato
- **Placeholder values**: Sostituisci tutti i valori segnaposto (come `<app-name>`, `<your-api-key>`, `<namespace>`) con i tuoi valori reali
- **Registry URLs comuni**:
  - `de.icr.io` (Germania/Frankfurt)
  - `us.icr.io` (Stati Uniti/Dallas)


---

