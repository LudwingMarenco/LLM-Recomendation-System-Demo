import mesop as me
import mesop.labs as mel
import time
from modules.movie_post_api import send_chat_request


def on_load(e: me.LoadEvent):
    me.set_theme_mode("system")


@me.page(
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=["https://google.github.io", "https://huggingface.co"]
    ),
    path="/",
    title="Recommendation Chat",
    on_load=on_load,
)
def page():
    mel.chat(transform, title="Recommendation System Chat", bot_user="RSC Bot")


def transform(input: str, history: list[mel.ChatMessage]):
    responses = send_chat_request(input)
    print(responses)
    for line in responses["response"]:
        time.sleep(0.03)
        yield line
