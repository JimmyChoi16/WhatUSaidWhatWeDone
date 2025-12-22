import os

from flask import Blueprint, jsonify, request
from google import genai

bp = Blueprint("chat", __name__, url_prefix="/api/chat")

ALLOWED_MODELS = {
    "gemini-3-pro-preview",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
}
DEFAULT_MODEL = "gemini-2.0-flash"


def _get_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured")
    return genai.Client(api_key=api_key)


def _extract_text(response) -> str:
    text = getattr(response, "text", None)
    # print("Gemini Response Text:", text)
    if text:
        return text.strip()
    try:
        candidates = getattr(response, "candidates", None) or []
        if not candidates:
            return ""
        parts = getattr(candidates[0].content, "parts", None) or []
        return "".join(part.text for part in parts if getattr(part, "text", None)).strip()
    except Exception:
        return ""


@bp.post("")
def chat():
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    model = (data.get("model") or "").strip()
    if model and model not in ALLOWED_MODELS:
        allowed = ", ".join(sorted(ALLOWED_MODELS))
        return jsonify({"error": f"model must be one of: {allowed}"}), 400
    if not model:
        model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    if model not in ALLOWED_MODELS:
        allowed = ", ".join(sorted(ALLOWED_MODELS))
        return jsonify({"error": f"configured model must be one of: {allowed}"}), 500
    try:
        client = _get_client()
        response = client.models.generate_content(model=model, contents=prompt)
        # print("Selected Model:", model)
        text = _extract_text(response)
    except Exception as exc:
        return jsonify({"error": f"Gemini request failed: {exc}"}), 500

    if not text:
        return jsonify({"error": "Gemini returned empty response"}), 500

    return jsonify({"text": text})
