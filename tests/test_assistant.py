from chatwithme.assistant import Assistant
import asyncio

assistant = Assistant()
asyncio.run(
    assistant.answer_resume_question("Quelles ont été tes missions professionnelles ?")
)
