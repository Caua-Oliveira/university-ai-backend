from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from src.models.schemas import ChatTextRequest, ChatResponse, LogoutRequest
from src.services.llm_service import llm_service_instance
from src.services.audio_service import text_to_speech, speech_to_text

router = APIRouter()


@router.post("/chat/text", response_model=ChatResponse)
async def chat_with_text(request: ChatTextRequest):
    """
    Recebe uma mensagem de texto, processa via RAG/LLM,
    e retorna texto, emoção e um link de áudio TTS.
    """
    try:
        text_reply, emotion = await llm_service_instance.process_text(request.message, request.user_id)

        audio_url = await text_to_speech(text_reply)

        return ChatResponse(
            text_reply=text_reply,
            emotion=emotion,
            audio_url=audio_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/voice", response_model=ChatResponse)
async def chat_with_voice(user_id: str = Form("default_user"), audio_file: UploadFile = File(...)):
    """
    Recebe um arquivo de áudio, transcreve, processa via RAG/LLM,
    e retorna a resposta.
    """
    try:
        audio_bytes = await audio_file.read()
        transcribed_text = await speech_to_text(audio_bytes)

        if not transcribed_text:
            return ChatResponse(
                text_reply="Desculpe, não consegui entender o áudio.",
                emotion="sad",
                audio_url=None
            )

        text_reply, emotion = await llm_service_instance.process_text(transcribed_text, user_id)
        audio_url = await text_to_speech(text_reply)

        return ChatResponse(
            text_reply=text_reply,
            emotion=emotion,
            audio_url=audio_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/logout")
async def logout(request: LogoutRequest):
    """
    Limpa o histórico do usuário e encerra a sessão.
    """
    llm_service_instance.clear_session(request.user_id)
    return {"status": "success", "message": "Histórico do usuário apagado."}