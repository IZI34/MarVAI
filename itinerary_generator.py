"""Pipeline pour générer des itinéraires avec Ollama Cloud API.
Ce fichier utilise l'API Ollama Cloud pour le déploiement.
"""
import os
import requests
from typing import List, Optional

# Configuration de l'API Ollama Cloud
OLLAMA_API_KEY = os.environ.get('OLLAMA_API_KEY', 'fc289982b86c43a8932b374295b7bd7b.fLzWxh3aqp2BQTPMo04iJzKT')
OLLAMA_API_URL = os.environ.get('OLLAMA_API_URL', 'https://api.ollama.cloud/v1/chat/completions')

# Nom du modèle par défaut
DEFAULT_MODEL = "mistral"  # Modèle disponible sur Ollama Cloud
FINETUNED_MODEL = "mistral"  # Changez si vous avez un modèle fine-tuné

# Vérifier si on utilise l'API Cloud ou local
USE_CLOUD_API = bool(OLLAMA_API_KEY and OLLAMA_API_KEY != 'your-api-key-here')


def build_prompt(destination: str, duration: int, interests: List[str], budget: Optional[float] = None) -> str:
    """Construit le prompt pour générer l'itinéraire.
    
    Args:
        destination: La destination du voyage
        duration: La durée du voyage en jours
        interests: Liste des intérêts du voyageur
        budget: Budget total disponible (optionnel)
        
    Returns:
        Le prompt formaté
    """
    interests_text = ", ".join(interests) if interests else "general tourism"
    
    budget_text = ""
    if budget and budget > 0:
        budget_text = f"\nTotal budget available: ${budget:,.2f} USD for the entire trip."
    
    return (
        "You are an expert travel planner specializing in budget-conscious itineraries. "
        f"Create a detailed {duration}-day day-by-day itinerary for {destination}. "
        f"Traveler interests: {interests_text}."
        f"{budget_text}\n\n"
        "For each day, provide:\n"
        "• Morning, Afternoon, and Evening activities\n"
        "• Estimated costs for each activity and meals\n"
        "• Transportation options with prices\n"
        "• Accommodation suggestions with price range\n"
        "• Money-saving tips and free alternatives\n"
        "• Local insider recommendations\n\n"
        "Format the itinerary clearly with sections for each day. "
        "Include a daily budget breakdown and ensure the total stays within the available budget. "
        "Be specific with times, locations, and practical advice."
    )


def generate_itinerary(
    destination: str, 
    duration: int, 
    interests: List[str], 
    budget: Optional[float] = None,
    model_name: Optional[str] = None
) -> str:
    """Génère un itinéraire de voyage en utilisant Ollama Cloud API.
    
    Args:
        destination: La destination du voyage
        duration: La durée du voyage en jours
        interests: Liste des intérêts du voyageur
        budget: Budget total disponible (optionnel)
        model_name: Nom du modèle à utiliser (optionnel)
        
    Returns:
        L'itinéraire généré sous forme de texte
    """
    model_name = model_name or DEFAULT_MODEL
    prompt = build_prompt(destination, duration, interests, budget)

    if USE_CLOUD_API:
        # Utiliser l'API Cloud Ollama
        try:
            headers = {
                'Authorization': f'Bearer {OLLAMA_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': model_name,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'stream': False
            }
            
            print(f"Appel de l'API Ollama Cloud avec le modèle {model_name}...")
            response = requests.post(
                OLLAMA_API_URL,
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                # Extraire la réponse du format de l'API
                if 'choices' in data and len(data['choices']) > 0:
                    return data['choices'][0]['message']['content']
                elif 'response' in data:
                    return data['response']
                else:
                    return str(data)
            else:
                error_msg = f"Erreur API Ollama Cloud (code {response.status_code}): {response.text}"
                print(error_msg)
                return f"Erreur lors de la génération de l'itinéraire.\n{error_msg}"
                
        except requests.exceptions.Timeout:
            return "Erreur: La génération de l'itinéraire a pris trop de temps (timeout)."
        except requests.exceptions.RequestException as e:
            return f"Erreur de connexion à l'API Ollama Cloud: {str(e)}"
        except Exception as e:
            return f"Erreur inattendue: {str(e)}"
    else:
        # Fallback: Message d'erreur si pas de clé API
        return "Erreur: Clé API Ollama non configurée. Veuillez définir OLLAMA_API_KEY."


def main():
    """Fonction principale pour tester le générateur d'itinéraires."""
    # Exemple d'utilisation
    destination = "Paris"
    duration = 5
    interests = ["art", "food"]
    budget = 2000
    
    print("=" * 80)
    print(f"🌍 Générateur d'itinéraires - Mode: {'Cloud API' if USE_CLOUD_API else 'Local'}")
    print("=" * 80)
    print(f"Destination: {destination}")
    print(f"Durée: {duration} jours")
    print(f"Budget: ${budget:,.2f}")
    print(f"Intérêts: {', '.join(interests)}")
    print("-" * 80)
    
    itinerary = generate_itinerary(
        destination=destination,
        duration=duration,
        interests=interests,
        budget=budget,
        model_name=DEFAULT_MODEL
    )
    
    print(itinerary)
    print("-" * 80)


if __name__ == "__main__":
    main()