from fastapi import FastAPI, Query, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import asyncio
from datetime import datetime, timezone

app = FastAPI(title="OCI Backend Mock - Acervo & Galeria")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Busca Facetada no Acervo
@app.get("/api/v1/acervo/search")
def search_acervo(
    q: Optional[str] = "",
    entidade: Optional[str] = None,
    ano_de: Optional[int] = None,
    ano_ate: Optional[int] = None,
    cursor: Optional[str] = None
):
    return {
        "items": [
            {
                "foto_id": "fot_mock_001",
                "url": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=1200",
                "titulo": "Sessão Solene Anual",
                "entidade": entidade or "rotary",
                "ano": ano_de or 2024,
                "faces_n": 4
            }
        ],
        "next_cursor": None,
        "total": 1
    }

# 2. Busca Facial
@app.post("/api/v1/acervo/face")
async def face_search(file: UploadFile = File(...)):
    return {
        "matches": [
            {"foto_id": "fot_mock_001", "similarity": 0.84},
            {"foto_id": "fot_mock_002", "similarity": 0.76}
        ],
        "expires_in_seconds": 3600
    }

# 3. Download Forense com URL Assinada
@app.post("/api/v1/media/{foto_id}/download")
def download_forense(foto_id: str):
    return {
        "download_url": f"https://storage.googleapis.com/acervo-staging/{foto_id}.webp?token=signed_mock_ttl_60s",
        "ttl_seconds": 60,
        "forensic_watermark_hash": "sha256_7f3a9b2c8e1d4f"
    }

# 4. Consulta ao Ledger Imutável
@app.get("/api/v1/ledger/{foto_id}")
def get_ledger(foto_id: str):
    return {
        "foto_id": foto_id,
        "chain_length": 3,
        "latest_block": {
            "block_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "timestamp": "2026-11-23T10:00:00Z",
            "action": "UPLOAD_ORIGINAL",
            "signer": "oci_authority_key"
        }
    }

def _build_live_frames(slug: str) -> list[dict]:
    """Constrói os frames mock no contrato canônico do CineDirector para HTTP e WebSocket."""
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return [
        {
            "event_id": slug,
            "foto_id": "fot_live_001",
            "url_display": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=1600",
            "created_at": now_iso,
            "is_breaking": True,
            "faces_n": 6,
            "primary_face_bbox": {"x": 0.5, "y": 0.35, "w": 0.15, "h": 0.20},
            "suggested_motion": "pan_horizontal",
            "orientation": "landscape",
            "dwell_time_ms": 7000,
        },
        {
            "event_id": slug,
            "foto_id": "fot_live_002",
            "url_display": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=1600",
            "created_at": now_iso,
            "is_breaking": False,
            "faces_n": 1,
            "primary_face_bbox": {"x": 0.45, "y": 0.25, "w": 0.20, "h": 0.25},
            "suggested_motion": "kenburns_focus_face",
            "orientation": "portrait",
            "dwell_time_ms": 4500,
        },
        {
            "event_id": slug,
            "foto_id": "fot_live_003",
            "url_display": "https://images.unsplash.com/photo-1519741497674-611481863552?w=1600",
            "created_at": now_iso,
            "is_breaking": True,
            "faces_n": 2,
            "primary_face_bbox": {"x": 0.48, "y": 0.30, "w": 0.18, "h": 0.22},
            "suggested_motion": "kenburns_focus_face",
            "orientation": "portrait",
            "dwell_time_ms": 5500,
        },
    ]


# 5. Canal Live Feed Telão (Simulação de Eventos em Tempo Real para o CineDirector)
@app.get("/api/v1/events/{slug}/live_feed")
def get_live_feed(slug: str):
    return {
        "event_id": slug,
        "frames": _build_live_frames(slug),
    }


@app.websocket("/api/v1/events/{slug}/live_feed")
async def ws_live_feed(
    websocket: WebSocket,
    slug: str,
    interval: float = Query(default=5.0, ge=0.1, le=60.0),
):
    """Emite frames ao vivo em loop no contrato CineDirector para consumo via WebSocket."""
    await websocket.accept()
    idx = 0
    try:
        while True:
            frames = _build_live_frames(slug)
            frame = dict(frames[idx % len(frames)])
            cycle = idx // len(frames)
            if cycle > 0:
                frame["foto_id"] = f"{frame['foto_id']}_r{cycle}"
            await websocket.send_json(frame)
            idx += 1
            await asyncio.sleep(interval)
    except WebSocketDisconnect:
        return
