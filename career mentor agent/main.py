import chainlit as cl
from agents import Runner
from agent_config.career_agent import career_agent
from setup_config import config

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message("Hi, I'm career mentor, how can I help you?").send()

@cl.on_message
async def handle_message(msg: cl.Message):
    history = cl.user_session.get("history", [])
    history.append({"role": "user", "content": msg.content})

    thinking = cl.Message("Thinking...")
    await thinking.send()
    try:
        result = await Runner.run(
            career_agent,
            history,
            run_config=config
        )
        
        output = result.final_output
        
        thinking.content = output
        await thinking.update()
        
        history = result.to_input_list()
        cl.user_session.set("history", history)
        
    except Exception as e:
        thinking.content = f"Error: {e}"
        await thinking.update()