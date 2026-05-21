from langchain.tools import tool

from app import store


@tool
def list_recipes() -> list[dict]:
    """Retourne la liste des recettes enregistrées."""
    return [
        {
            "name": recipe.name,
            "ingredients": recipe.ingredients,
        }
        for recipe in store.list_recipes()
    ]

@tool
def create_recipe(name: str, ingredients: list[str]) -> dict:
    """Crée une nouvelle recette."""
    recipe = store.create_recipe(store.RecipeCreate(name=name, ingredients=ingredients))
    return {
        "name": recipe.name,
        "ingredients": recipe.ingredients,
    }

@tool
def delete_recipe(recipe_id: int) -> dict:
    """Supprime une recette en se basant sur son identifiant."""
    ok = store.delete_recipe(recipe_id)
    return {
        "deleted": ok,
    }


available_tools = [list_recipes, create_recipe, delete_recipe]
