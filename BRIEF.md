# Brief : Intégrer un agent conversationnel dans une application web

Brief rattaché à la SP **« Prendre en main un agent conversationnel en environnement métier »**. Cible la Phase 1 du parcours.

## Référentiels
- [2023] Certification RNCP37827 — Développeur en intelligence artificielle

## Ressources
- Le repo du projet (ce dépôt) — application web fournie clé en main : backend FastAPI + frontend Next.js + Docker Compose.
- [Documentation FastAPI — tutoriel](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [Documentation LangChain — `create_agent`](https://docs.langchain.com/oss/python/langchain/agents)
- [Documentation LangChain — décorateur `@tool`](https://python.langchain.com/docs/how_to/custom_tools/)
- [`langchain-azure-ai` — chat models](https://python.langchain.com/docs/integrations/chat/azure_ai/)
- [Azure AI Foundry — Inference API](https://learn.microsoft.com/azure/ai-foundry/model-inference/)
- [Documentation Next.js — App Router](https://nextjs.org/docs/app)

## Contexte du projet
Vous rejoignez **Saveurs Connectées**, une jeune entreprise qui développe une application web de carnet de recettes. Le MVP existe déjà : un frontend Next.js permet de lister, créer et supprimer des recettes via une API REST FastAPI, et le tout tourne en Docker Compose. La direction veut maintenant ajouter un **panneau de chat conversationnel** dans lequel l'utilisateur pourra dialoguer avec un assistant IA pour, à terme, manipuler ses recettes en langage naturel.

Le panneau de chat est déjà présent dans l'interface, et le backend expose une route `/chat` qui répond pour le moment un message factice. Votre responsable vous confie l'intégration : lire le code existant pour vous l'approprier, faire tourner l'application localement, puis brancher un agent LangChain alimenté par **Kimi-K2.6** hébergé sur Azure AI Foundry (via le package `langchain-azure-ai`) sur cette route. Le projet est découpé en étapes pour vous laisser monter progressivement en complexité.

Vos tâches sont les suivantes :
- installer et démarrer l'application avec `docker compose up`, vérifier que le backend (`/health`) et le frontend sont accessibles, et tester l'envoi d'un message dans le chat (qui doit renvoyer un placeholder).
- lire le code de `backend/app/routes/recipes.py` et `backend/app/store.py` pour comprendre comment le CRUD est exposé, puis tester chaque endpoint via Swagger UI (`http://localhost:8000/docs`).
- implémenter l'étape 1 du chat dans `backend/app/routes/chat.py` : remplacer le placeholder par un appel direct à Kimi-K2.6 via `AzureAIChatCompletionsModel` (package `langchain-azure-ai`), sans outils, qui renvoie la réponse du modèle au front.
- implémenter l'étape 2 : créer un agent LangChain avec `langchain.agents.create_agent` doté de trois outils branchés sur `app/store.py` — `list_recipes`, `create_recipe`, `delete_recipe`. L'utilisateur doit pouvoir dire « ajoute une recette tarte aux fraises avec fraises, sucre, crème » et voir la liste se mettre à jour à l'écran.
- (étape stretch optionnelle) ajouter une mémoire conversationnelle simple : l'agent doit se souvenir des messages précédents dans la même session.
- rédiger une section « Comment fonctionne le chat » dans le README, à destination d'un·e collègue qui n'a jamais vu le projet, en expliquant le rôle de l'agent, des outils, et le flux de données entre front, back et LLM.

## Modalités pédagogiques
Travail en binôme. 5 jours (35h). Présentiel avec stand-up quotidien. Versionnement Git obligatoire : une branche par étape (`step-1-llm-direct`, `step-2-tools`, `step-3-memory`), merge dans `main` après revue.

## Modalités d'évaluation
- Revue de code en 1:1 avec le formateur à la fin de chaque étape (J2, J4, J5).
- Démo de 10 minutes en fin de projet devant la promo : montrer l'application qui tourne, faire dialoguer l'agent pour lister, ajouter et supprimer une recette en live.
- Auto-évaluation sur la grille de compétences Simplonline.

## Livrables
- Le repo Git avec l'historique des branches et merges.
- L'endpoint `/chat` fonctionnel avec au minimum les étapes 1 et 2.
- Un README dont la section « Comment fonctionne le chat » est complétée.
- Une démo réussie : poser au chat trois questions différentes (lister, créer, supprimer) et voir l'interface se synchroniser sans rechargement manuel.

## Critères de performance
- `docker compose up` lève toujours les deux services sans erreur après vos modifications.
- Les tests existants (`make test`) passent encore.
- Quand vous demandez à l'agent d'ajouter ou de supprimer une recette, le changement apparaît à l'écran sans rechargement manuel.
- Le code de `chat.py` reste lisible : chaque outil dans sa propre fonction, un docstring par outil.
- La section README est compréhensible par un·e dev qui n'a pas suivi le projet.

## Compétences visées (avec niveau)
- **C6** — Organiser et réaliser une veille technique — niveau 1
- **C10** — Intégrer l'API d'un modèle ou service d'IA dans une application — niveau 1
- **C17** — Développer les composants techniques et les interfaces d'une application — niveau 1
- **C21** — Résoudre les incidents techniques — niveau 1
- **CT3** — Définir le périmètre d'un problème rencontré — niveau 1
- **CT4** — Rechercher de façon méthodique des pistes de résolution — niveau 1
- **CT5** — Partager la solution adoptée via la documentation — niveau 1
- **CT6** — Présenter un travail réalisé en synthétisant sa démarche — niveau 1
