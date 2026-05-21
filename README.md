# Site with AI chat

Mini-application "Carnet de recettes" :
- **Backend** FastAPI (Python) avec une API REST pour gérer des recettes
- **Frontend** Next.js 15 (TypeScript) qui consomme l'API
- **Chat IA** : un endpoint `/chat` côté backend que **vous devez implémenter** (LangChain + Azure AI Inference, déploiement **Kimi-K2.6**)

Les consignes pédagogiques détaillées te sont remises séparément par ton formateur.

## Prérequis

- Docker et Docker Compose installés
- Un accès au déploiement Azure AI Foundry (endpoint + clé + nom du modèle), fourni par votre formateur

## Lancement

```bash
# 1. Configurer les variables Azure
cp .env.example .env
# édite .env et renseigne les trois variables AZURE_*
# (endpoint et clé visibles dans Azure AI Foundry → ton projet → Models + endpoints → Kimi-K2.6)

# 2. Démarrer
make up
# (équivalent à : docker compose up --build)
```

Ouvre ensuite :
- Backend (Swagger UI) : <http://localhost:8000/docs>
- Frontend : <http://localhost:3000>

## Vérification rapide

```bash
curl http://localhost:8000/health
# {"status":"ok"}

curl http://localhost:8000/recipes
# Renvoie la liste des recettes pré-remplies

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Bonjour"}'
# {"reply":"TODO: implémenter le chat. ..."}
```

Le frontend affiche les recettes à gauche et un panneau de chat à droite. Le chat répond actuellement avec un placeholder — **votre travail est d'y brancher un vrai agent LangChain**.

## Fonctionnement du chat

Cette section décrit le fonctionnement du chat côté backend et le flux complet de données.

### Rôle de l'agent

- L'agent est un assistant culinaire (prompt système) qui répond aux utilisateurs et décide quand appeler des outils.
- Il s'appuie sur un modèle Azure AI (Kimi-K2.6) via LangChain.
- Une mémoire de conversation est branchée pour conserver le contexte par session (`thread_id`).

### Rôle de chaque outil

Les outils sont exposés à l'agent pour interagir avec les recettes en mémoire :

- `list_recipes` : retourne la liste actuelle des recettes (nom + ingrédients).
- `create_recipe` : crée une recette à partir d'un nom et d'une liste d'ingrédients.
- `delete_recipe` : supprime une recette par identifiant.

Ces outils délèguent au module `store.py` (CRUD en mémoire) et renvoient des objets simples que l'agent peut résumer.

### Flux de données

1. Le frontend envoie un message utilisateur via `POST /chat`.
2. Le backend crée (ou réutilise) un agent LangChain et lui passe le message.
3. L'agent décide s'il répond directement avec le modèle ou s'il appelle un ou plusieurs outils.
4. Les outils lisent ou modifient le store de recettes, puis renvoient leurs résultats à l'agent.
5. L'agent compose la réponse finale et le backend renvoie `{ reply }` au frontend.
6. Le frontend affiche la réponse et rafraîchit la liste des recettes.

## Structure

```
.
├── docker-compose.yml       # Orchestration backend + frontend
├── Makefile                 # Raccourcis make up/down/logs/test
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── app/
│   │   ├── main.py          # FastAPI app + CORS
│   │   ├── store.py         # CRUD recettes en mémoire
│   │   └── routes/
│   │       ├── health.py
│   │       ├── recipes.py   # ✅ déjà implémenté
│   │       └── chat.py      # ⚠️  STUB — à implémenter
│   └── tests/test_recipes.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── app/                 # Pages Next.js (App Router)
    ├── components/          # RecipeList, ChatPanel
    └── lib/api.ts           # Client REST typé
```

## Commandes utiles

| Commande      | Effet                                            |
|---------------|--------------------------------------------------|
| `make up`     | Build + démarre tout (logs en avant-plan)        |
| `make down`   | Arrête les services                              |
| `make logs`   | Logs en continu                                  |
| `make test`   | Lance les tests pytest du backend                |
| `make clean`  | Down + supprime les volumes                      |
| `make restart`| Down + Up

## Ressources

- [FastAPI — premiers pas](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [LangChain — `create_agent`](https://docs.langchain.com/oss/python/langchain/agents)
- [`langchain-azure-ai` — chat models](https://python.langchain.com/docs/integrations/chat/azure_ai/)
- [Azure AI Foundry — Inference API](https://learn.microsoft.com/azure/ai-foundry/model-inference/)
- [Next.js App Router](https://nextjs.org/docs/app)
