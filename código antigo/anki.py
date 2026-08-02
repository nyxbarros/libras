import requests

class Anki:
    @staticmethod
    def invoke(action, params=None):
        payload = {
            "action": action,
            "version": 6,
            "params": params or {}
        }
        response = requests.post("http://localhost:8765", json=payload)
        response.raise_for_status()
        result = response.json()
        if result.get("error") is not None:
            raise Exception(f"AnkiConnect error: {result['error']}")
        return result.get("result")
    
    @staticmethod
    def deck_exists(deck_name):

        decks = Anki.invoke("deckNames")
        return deck_name in decks
    
    @staticmethod
    def create_deck(deck_name):
        Anki.invoke("createDeck", {"deck": deck_name})
        print(f"Deck '{deck_name}' criado.")

    @staticmethod
    def validarDeck(deck):
        if Anki.deck_exists(deck):
            print(f"Deck '{deck}' já existe.")
        else:
            print(f"Deck '{deck}' não existe. Criando...")
            Anki.create_deck(deck)

    @staticmethod
    def deletarDeck(deck):
        if Anki.deck_exists(deck):
            requests.post("http://localhost:8765", json={
                "action": "deleteDecks",
                "version": 6,
                "params": {
                    "decks": [deck],
                    "cardsToo": True
                }
            })
            print(f"Deck '{deck}' deletado.")
        else:
            print(f"Deck '{deck}' não existe.")

    @staticmethod
    def cartao(frente, verso, deck):
        """metodo que cria um cartão em um determinado deck

        Args:
            frente (str): a frente do cartão
            verso (str): a resposta do cartão
            deck (str): o deck destino do cartão

        Returns:
            object: objeto completo que o anki utilizará para criar o card
        """
        return {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck,
                    "modelName": "Basic",
                    "fields": {
                        "Front": frente,
                        "Back": verso
                    },
                    "options": {
                        "allowDuplicate": False
                    },
                    "tags": ["importado"]
                }
            }
        }