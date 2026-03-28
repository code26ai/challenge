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
* [Esempio per generare Bearer Token con APIKEY](https://dataplatform.cloud.ibm.com/docs/content/wsj/getting-started/wx-api-credentials.html?context=wx&audience=wdp&locale=en)
```bash
curl -X POST --url https://iam.cloud.ibm.com/identity/token --header "Content-Type: application/x-www-form-urlencoded" --data "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=${APIKEY}"
```

* [Esempio di chiamata API per chiamare modelli watsonx.ai](https://www.ibm.com/watsonx/developer/capabilities/chat/)
```bash
curl 'https://<region>.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29' -H 'Content-Type: application/json' -H 'Accept: application/json' -H "Authorization: Bearer $BEARER" \
  -d '{
        "messages": [
                {
                        "role": "user",
                        "content": [
                                {
                                        "type": "text",
                                        "text": "Sample"
                                }
                        ]
                }
        ],
        "project_id": "<project_id>",
        "model_id": "<model_name>"
}'
```
* [Esempio di chiamata API per chiamare agenti su watsonx.orchestrate](https://heidloff.net/article/watsonx-orchestrate-apis/)

```bash
curl -X POST --url https://api.<region>.watson-orchestrate.cloud.ibm.com/instances/<orchestrate_id>/v1/orchestrate/<agent_id>/chat/completions --header "Authorization: Bearer $BEARER" --header 'Content-Type: application/json' --data '{ "stream":false,"messages": [{"role": "user","content": "Hi"}]}'
```