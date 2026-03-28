# Guida IBM per la challenge

Repository per l'utilizzo di strumenti di AI su IBM Watsonx.

* Per poter pubblicare un applicazione FrontEnd/Backend sul web puoi seguire la guida per [Code Engine](#Code-Engine)
* Per poter creare un flusso di AI generativa Low Code-No Code, caricare documenti in un vectorDB puoi seguire la guida [Langflow AstraDB](#langflow-astradb)
* Per poter usare un flusso di agenti AI con strumenti avanzati puoi seguire la guida [IBM-watsonx-Orchestrate](#ibm-watsonx-orchestrate)

## Code Engine
Code Engine è il container engine con cui è possibile deployare applicazioni in container sulla piattaforma IBM. Seguite la guida [code-engine-upload-guide.md](code-engine-upload-guide.md) per poter pubblicare le vostre applicazioni sul web.

Nota: per poter completare la guida è necessario iscriversi gratuitamente al portale IBM e generare un IBM-id. Fornire successivamente ai tutor il proprio IBM-id per poter ricevere accesso al portale e pubblicare le proprie applicazioni

[Link alla guida CODE ENGINE](code-engine-upload-guide.md)

## Langflow AstraDB 
Questa repository contiene materiale per poter creare un piccolo flusso RAG usando **LangFlow** e **AstraDB**

Nota: l'utilizzo dei modelli LLM per la creazione di agenti e per l'embedding dei documenti, richiede un APIKEY watsonx fornita dai tutor IBM.

[Link alla guida Langflow](LangflowAstraDB/README.md)

## IBM watsonx Orchestrate

Questa repo contiene materiale per utilizzare **IBM watsonx Orchestrate** nella vostra soluzione:

- [Tutorial base](watsonxOrchestrate/README.md)
- [Uso di Tool python](watsonxOrchestrate/OrchestrateAdvanced.md)
- [Configurazioni parametri per le integrazioni](watsonxOrchestrate/ApprofondimentoConnections.md)

[Link alla guida IBM Orchstrate](watsonxOrchestrate/README.md)

## Esempi di chiamate API

* [Esempio di chiamata API per chiamare modelli watsonx.ai](https://www.ibm.com/watsonx/developer/capabilities/chat/)

* [Esempio di chiamata API per chiamare agenti su watsonx.orchestrate](https://heidloff.net/article/watsonx-orchestrate-apis/)