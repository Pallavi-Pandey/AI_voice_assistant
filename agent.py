from __future__ import annotations

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
    Agent,
    RoomIO
)
MultimodalAgent = Agent
from livekit.plugins import openai
from dotenv import load_dotenv
from api import AssistantFuc
from prompts import INSTRUCTIONS, WELCOME_MESSAGE, LOOKUP_VIN_MESSAGE
import os

load_dotenv()

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    await ctx.wait_for_participant()

    model = openai.realtime.RealtimeModel(
        instructions= INSTRUCTIONS,
        voice= "shimmer",
        temperature= 0.7,
        modalities= ["audio", "text"],
    )

    assistant_func = AssistantFuc()
    assistant = MultimodalAgent(model-model, fn_ctx=assistant_func)
    assistant.start(ctx.room)

    session = model._sessions[0]
    session.conversation.item.center(
        llm.ChatMessage(
            role = "assistant",
            content = WELCOME_MESSAGE
        )
    )
    session.response.create()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
    