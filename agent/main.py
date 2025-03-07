import logging
import os
import threading
import time

import uvicorn
from app.domain import message_service
from app.schema import Audio, Image, Message, Payload, User
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from typing_extensions import Annotated

load_dotenv()

IS_DEV_ENVIRONMENT = True

VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")

app = FastAPI(
    title="WhatsApp Bot",
    version="0.1.0",
    openapi_url=f"/openapi.json" if IS_DEV_ENVIRONMENT else None,
    docs_url=f"/docs" if IS_DEV_ENVIRONMENT else None,
    redoc_url=f"/redoc" if IS_DEV_ENVIRONMENT else None,
    swagger_ui_oauth2_redirect_url=f"/docs/oauth2-redirect" if IS_DEV_ENVIRONMENT else None,
)

log = logging.getLogger(__name__)



@app.get("/")
def verify_whatsapp(
        hub_mode: str = Query("subscribe", description="The mode of the webhook", alias="hub.mode"),
        hub_challenge: int = Query(..., description="The challenge to verify the webhook", alias="hub.challenge"),
        hub_verify_token: str = Query(..., description="The verification token", alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFICATION_TOKEN:
        return hub_challenge

    raise HTTPException(status_code=403, detail="Invalid verification token")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/readiness")
def readiness():
    return {"status": "ready"}


def parse_message(payload: Payload) -> Message | None:
    if not payload.entry[0].changes[0].value.messages:
        return None
    return payload.entry[0].changes[0].value.messages[0]


def get_current_user(message: Annotated[Message, Depends(parse_message)]) -> User | None:
    if not message:
        return None
    return message_service.authenticate_user_by_phone_number(message.from_)


def parse_audio_file(message: Annotated[Message, Depends(parse_message)]) -> Audio | None:
    if message and message.type == "audio":
        return message.audio
    return None


def parse_image_file(message: Annotated[Message, Depends(parse_message)]) -> Image | None:
    if message and message.type == "image":
        return message.image
    return None


def message_extractor(
        message: Annotated[Message, Depends(parse_message)],
        audio: Annotated[Audio, Depends(parse_audio_file)],
):
    if audio:
        return message_service.transcribe_audio(audio)
    if message and message.text:
        return message.text.body
    return None


@app.post("/", status_code=200)
def receive_whatsapp(
        user: Annotated[User, Depends(get_current_user)],
        user_message: Annotated[str, Depends(message_extractor)],
        image: Annotated[Image, Depends(parse_image_file)],
):
    print(user, user_message, image)
    
    if not user and not user_message and not image:
        # status message
        return {"status": "ok"}

    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if image:
        return print("Image received")

    if user_message:
        print(f"Received message from user {user.first_name} {user.last_name} ({user.phone})")
        thread = threading.Thread(target=message_service.respond_and_send_message, args=(user_message, user))
        thread.daemon = True
        thread.start()
    return {"status": "ok"}



if __name__ == "__main__":
    # noinspection PyTypeChecker
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # nosec