# weather_router_agent.py

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional

from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if api_key is None:
    raise ValueError("GROQ_API_KEY manquante dans le fichier .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

ToolName = Literal["get_weather", "get_temperature", "get_precipitation", "OUT_OF_SCOPE"]
Scope = Literal["WEATHER", "OUT_OF_SCOPE"]


@dataclass
class WeatherRouterResult:
    scope: Scope
    tool: ToolName
    location: Optional[str]
    datetime: Optional[str]


SYSTEM_PROMPT = """
Tu es un agent métier de routage météo.

Ton rôle est d’analyser une question utilisateur en langage naturel
et de retourner UNIQUEMENT un objet JSON structuré.

RÈGLES :
- Si la question concerne la météo :
    - scope = "WEATHER"
    - tool ∈ {"get_weather", "get_temperature", "get_precipitation"}
    - location = ville détectée ou null
    - datetime = date/heure absolue au format "YYYY-MM-DD HH:MM"
      (convertir aujourd’hui, demain, etc.)
- Si la question ne concerne PAS la météo :
    - scope = "OUT_OF_SCOPE"
    - tool = "OUT_OF_SCOPE"
    - location = null
    - datetime = null

IMPORTANT :
- Retourne UNIQUEMENT du JSON valide.
- Aucun texte explicatif.
"""


def route_weather_question(
    question: str,
    now: Optional[datetime] = None,
    model: str = "llama-3.3-70b-versatile",
) -> WeatherRouterResult:

    if now is None:
        now = datetime.now()

    current_dt_str = now.strftime("%Y-%m-%d %H:%M")

    user_content = (
        f"date_actuelle: {current_dt_str}\n"
        f"question: {question}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_object"},
    )

    data = json.loads(response.choices[0].message.content)

    return WeatherRouterResult(
        scope=data.get("scope", "OUT_OF_SCOPE"),
        tool=data.get("tool", "OUT_OF_SCOPE"),
        location=data.get("location"),
        datetime=data.get("datetime"),
    )


if __name__ == "__main__":
    questions = [
        "Quelle est la météo aujourd’hui à Madrid ?",
        "Est-ce qu’il va pleuvoir demain à Paris ?",
        "Quelle température fait-il maintenant à Rome ?",
        "Raconte-moi une blague."
    ]

    for q in questions:
        print("\nQUESTION :", q)
        result = route_weather_question(q)
        print("RESULT :", result)
