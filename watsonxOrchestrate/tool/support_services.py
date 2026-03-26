from ibm_watsonx_orchestrate.agent_builder.tools import tool


SUPPORT_SERVICES = {
    "milano": [
        {
            "name": "CADMI – Casa delle Donne Maltrattate",
            "address": "Via Piacenza 14, Milano",
            "phone": "02 55015519"
        }
    ],
    "roma": [
        {
            "name": "Casa Internazionale delle Donne",
            "address": "Via della Lungara 19, Roma",
            "phone": "06 68401720"
        }
    ],
    "torino": [
        {
            "name": "Centro Antiviolenza Torino – Telefono Rosa Piemonte",
            "address": "Via Assietta 13/A, Torino",
            "phone": "011 530666"
        }
    ],
}

DEFAULT_SERVICES = {
    "national": [
        {"name": "1522 - Numero Antiviolenza e Stalking", "phone": "1522"},
        {"name": "Emergenze", "phone": "112"}
    ]
}


@tool
def get_support_services(citta: str) -> dict:
    """
    Restituisce numeri e servizi utili per il supporto contro la violenza sulle donne,
    basandosi sulla città o regione menzionata dall'utente.
    """

    citta = citta.lower()

    found_city = None

    for city in SUPPORT_SERVICES:
        if city == citta:
            found_city = city
            break

    if found_city:
        return {
            "location_detected": found_city,
            "local_services": SUPPORT_SERVICES[found_city],
            "national_services": DEFAULT_SERVICES["national"]
        }

    return {
        "location_detected": None,
        "local_services": "Per questa città non abbiamo centri registrati",
        "national_services": DEFAULT_SERVICES["national"]
    }