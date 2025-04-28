from pathlib import Path
from mistralai import Mistral
import asyncio


class Assistant(Mistral):
    res: Path = Path(__file__).resolve().parent.parent / "resources"
    model = "mistral-small-latest"  # mistral-large-latest, mistral-small-latest, mistral-tiny
    pre_prompt: str = (res / "pre-prompt.txt").read_text()
    cv: str = (res / "cv.txt").read_text()

    def __init__(self, **kwargs):
        if "api_key" not in kwargs:
            kwargs["api_key"] = (self.res / "clef-api-mistral.txt").read_text().rstrip()
        super().__init__(**kwargs)

    async def answer_resume_question(self, question: str):

        stream_response = await self.chat.stream_async(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "\n\n".join(
                        [
                            self.pre_prompt,
                            "",
                            "Voici le CV:",
                            "",
                            self.cv,
                            "",
                            "Voici maintenant la question que l'utilisateur te pose:",
                        ]
                    ),
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )

        async for chunk in stream_response:
            if chunk.data.choices[0].delta.content is not None:
                print(chunk.data.choices[0].delta.content, end="")
