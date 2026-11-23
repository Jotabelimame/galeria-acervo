from fastapi import FastAPI, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import time

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
