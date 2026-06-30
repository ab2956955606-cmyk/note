import os

import httpx


class LlmClient:
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "mock")
        self.api_key = os.getenv("AI_API_KEY", "")
        self.api_base = os.getenv("AI_API_BASE", "https://api.deepseek.com")
        self.model = os.getenv("AI_MODEL", "deepseek-chat")

    async def complete(self, system: str, user: str) -> str | None:
        if self.provider == "mock" or not self.api_key:
            return None
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.3,
        }
        async with httpx.AsyncClient(timeout=40) as client:
            res = await client.post(
                f"{self.api_base.rstrip('/')}/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"]
