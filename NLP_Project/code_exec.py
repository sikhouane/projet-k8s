from __future__ import annotations
from dataclasses import asdict
from typing import Any, Dict, Optional, Tuple, Union
from weather_router_agent import WeatherRouterResult, route_weather_question
from weather_tools import get_weather, get_temperature, get_precipitation

ToolOutput = Union[Dict[str, Any], float]

def execute_from_json(route: WeatherRouterResult) -> Tuple[Optional[ToolOutput], str]:
    """
    Étape "Code execution" juste après le JSON (WeatherRouterResult).

    Retourne:
      - (result, None) si ok
      - (None, error_message) si out_of_scope ou paramètres manquants
    """
    if route.scope != "WEATHER" or route.tool == "OUT_OF_SCOPE":
        return None, "OUT_OF_SCOPE"

    if not route.location:
        return None, "MISSING_LOCATION"

    if not route.datetime:
        return None, "MISSING_DATETIME"

    if route.tool == "get_weather":
        return get_weather(route.location, route.datetime), ""

    if route.tool == "get_temperature":
        return get_temperature(route.location, route.datetime), ""

    if route.tool == "get_precipitation":
        return get_precipitation(route.location, route.datetime), ""

    return None, "UNKNOWN_TOOL"


def format_answer(route: WeatherRouterResult, result: ToolOutput) -> str:
    """Transforme le résultat tool en phrase lisible."""
    if route.tool == "get_weather":
        # result est un dict
        r = result
        return (
            f"Météo à {r['ville']} le {r['datetime']} : {r['resume']}, "
            f"{r['temperature_c']}°C, précipitations {r['precipitations_mm']} mm."
        )

    if route.tool == "get_temperature":
        return f"Température à {route.location} le {route.datetime} : {result}°C."

    if route.tool == "get_precipitation":
        return f"Précipitations à {route.location} le {route.datetime} : {result} mm."

    return "Je n’ai pas réussi à formater la réponse."


def answer(question: str, debug: bool = False) -> str:
    """
    Pipeline complet:
    Question -> LLM -> JSON (WeatherRouterResult) -> Code execution -> Réponse
    """
    route = route_weather_question(question)
    result, err = execute_from_json(route)

    if err:
        if err == "OUT_OF_SCOPE":
            return "Désolé, je ne traite que des questions météo."
        if err == "MISSING_LOCATION":
            return "Tu veux la météo de quelle ville ?"
        if err == "MISSING_DATETIME":
            return "Pour quel moment exactement (date/heure) ?"
        return f"Erreur: {err}"

    # result est non None ici
    final = format_answer(route, result)

    if debug:
        return (
            f"[DEBUG route_json] {asdict(route)}\n"
            f"[DEBUG tool_result] {result}\n"
            f"{final}"
        )

    return final


if __name__ == "__main__":
    print("Weather agent")
    while True:
        q = input("\nQuestion: ").strip()
        if q.lower() in {"quit", "exit"}:
            break
        print(answer(q, debug=True))
