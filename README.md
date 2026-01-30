# Projet: LLM Itinéraire de Voyage (Olama) ✅

## Objectif
Créer un modèle spécialisé pour générer des itinéraires de voyage jour-par-jour, en se basant sur un fine-tuning d'un modèle conversational (ex: Mistral-7B Instruct) via Olama.

---

## Structure du projet
- `data/` : jeux de données JSONL d'exemples d'itinéraires (`sample_itineraries.jsonl`).
- `src/pipeline.py` : fonctions pour générer un itinéraire (SDK Olama ou CLI fallback).
- `src/run_example.py` : petit utilitaire CLI pour tester.
- `finetune.ps1` / `finetune.sh` : scripts pour lancer le fine-tuning.

---

## Démarrage rapide (Windows)
1. Installer Olama et ses dépendances selon la doc d'Olama.
2. (Option) créer un environnement virtuel et installer `requirements.txt`.
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Télécharger le modèle de base et lancer le fine-tuning (ex: 100 steps) :
   ```powershell
   .\finetune.ps1
   ```
4. Lancer un exemple de génération :
   ```powershell
   python src\run_example.py "Paris" 5 art food
   ```

---

## Conseils et prochaines étapes 💡
- Ajoutez plus d'exemples dans `data/` (50–100+ pour de meilleurs résultats) en respectant le format JSONL.
- Évaluez la qualité et itérez sur le dataset et les prompts.
- Si besoin, utilisez des GPU cloud pour des steps de fine-tuning plus importants.

---

Si vous voulez, je peux :
- Ajouter 50+ exemples automatiquement (je peux générer des itinéraires synthétiques),
- Écrire des tests unitaires ou un petit serveur API pour exposer le modèle.
