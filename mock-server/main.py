from fastapi import FastAPI, HTTPException, Query, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal, Optional
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

Visibilidade = Literal["publica", "restrita", "privada"]


class VisibilidadeUpdate(BaseModel):
    """Payload para alternar a visibilidade de um álbum federado com trava LGPD."""

    visibilidade: Visibilidade
    confirmar_lgpd: bool = False


ENTIDADES = {
    "prefeitura": {
        "slug": "prefeitura",
        "nome": "Prefeitura Municipal",
        "categoria": "poder_publico",
        "perfil_match_default": "geral_noturno",
        "threshold_default": 0.62,
        "lgpd_protegido": False,
    },
    "paroquia": {
        "slug": "paroquia",
        "nome": "Paróquia Matriz (Festa do Padroeiro)",
        "categoria": "religiao",
        "perfil_match_default": "geral_noturno",
        "threshold_default": 0.62,
        "lgpd_protegido": False,
    },
    "rotary": {
        "slug": "rotary",
        "nome": "Rotary Club",
        "categoria": "civico",
        "perfil_match_default": "retratos_formaturas",
        "threshold_default": 0.70,
        "lgpd_protegido": False,
    },
    "creche": {
        "slug": "creche",
        "nome": "Creches & Educação Infantil",
        "categoria": "educacao_protegida",
        "perfil_match_default": "protegidos",
        "threshold_default": 0.75,
        "lgpd_protegido": True,
    },
}

ALBUNS = {
    "alb_rotary_2024": {
        "album_id": "alb_rotary_2024",
        "entidade": "rotary",
        "titulo": "Sessão Solene Anual Rotary",
        "ano": 2024,
        "visibilidade": "publica",
        "perfil_match": "retratos_formaturas",
        "threshold": 0.70,
        "lgpd_protegido": False,
    },
    "alb_padroeiro_2026": {
        "album_id": "alb_padroeiro_2026",
        "entidade": "paroquia",
        "titulo": "Festa do Padroeiro 2026",
        "ano": 2026,
        "visibilidade": "publica",
        "perfil_match": "geral_noturno",
        "threshold": 0.62,
        "lgpd_protegido": False,
    },
    "alb_prefeitura_posse_2026": {
        "album_id": "alb_prefeitura_posse_2026",
        "entidade": "prefeitura",
        "titulo": "Cerimônia de Posse na Câmara",
        "ano": 2026,
        "visibilidade": "publica",
        "perfil_match": "geral_noturno",
        "threshold": 0.62,
        "lgpd_protegido": False,
    },
    "alb_rotary_diretoria_2026": {
        "album_id": "alb_rotary_diretoria_2026",
        "entidade": "rotary",
        "titulo": "Assembleia Interna da Diretoria",
        "ano": 2026,
        "visibilidade": "restrita",
        "perfil_match": "retratos_formaturas",
        "threshold": 0.70,
        "lgpd_protegido": False,
    },
    "alb_creche_formatura_2026": {
        "album_id": "alb_creche_formatura_2026",
        "entidade": "creche",
        "titulo": "Dia das Crianças — EMEI",
        "ano": 2026,
        "visibilidade": "restrita",
        "perfil_match": "protegidos",
        "threshold": 0.75,
        "lgpd_protegido": True,
    },
    "alb_prefeitura_rascunho_2026": {
        "album_id": "alb_prefeitura_rascunho_2026",
        "entidade": "prefeitura",
        "titulo": "Vistoria Técnica (Arquivo Interno)",
        "ano": 2026,
        "visibilidade": "privada",
        "perfil_match": "geral_noturno",
        "threshold": 0.62,
        "lgpd_protegido": False,
    },
}

ACERVO_FOTOS = [
    {
        "foto_id": "fot_mock_001",
        "album_id": "alb_rotary_2024",
        "url": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=1200",
        "titulo": "Sessão Solene Anual",
        "entidade": "rotary",
        "ano": 2024,
        "faces_n": 4,
    },
    {
        "foto_id": "fot_mock_002",
        "album_id": "alb_padroeiro_2026",
        "url": "https://images.unsplash.com/photo-1519741497674-611481863552?w=1200",
        "titulo": "Quermesse e Procissão do Padroeiro",
        "entidade": "paroquia",
        "ano": 2026,
        "faces_n": 8,
    },
    {
        "foto_id": "fot_mock_003",
        "album_id": "alb_prefeitura_posse_2026",
        "url": "https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=1200",
        "titulo": "Cerimônia de Posse na Câmara Municipal",
        "entidade": "prefeitura",
        "ano": 2026,
        "faces_n": 5,
    },
    {
        "foto_id": "fot_mock_004",
        "album_id": "alb_rotary_diretoria_2026",
        "url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200",
        "titulo": "Reunião Restrita da Diretoria Rotary",
        "entidade": "rotary",
        "ano": 2026,
        "faces_n": 6,
    },
    {
        "foto_id": "fot_mock_005",
        "album_id": "alb_creche_formatura_2026",
        "url": "https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=1200",
        "titulo": "Atividade Pedagógica — EMEI",
        "entidade": "creche",
        "ano": 2026,
        "faces_n": 3,
    },
    {
        "foto_id": "fot_mock_006",
        "album_id": "alb_prefeitura_rascunho_2026",
        "url": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200",
        "titulo": "Vistoria Técnica Interna",
        "entidade": "prefeitura",
        "ano": 2026,
        "faces_n": 2,
    },
]


# 1. Busca Facetada no Acervo (Modelo Federado S2: Portal Municipal só indexa visibilidade 'publica')
@app.get("/api/v1/acervo/search")
def search_acervo(
    q: Optional[str] = "",
    entidade: Optional[str] = None,
    ano_de: Optional[int] = None,
    ano_ate: Optional[int] = None,
    tipo: Optional[str] = None,
    portal: Literal["municipal", "entidade"] = "municipal",
    visibilidade: Optional[Visibilidade] = None,
    incluir_restritas: bool = False,
    cursor: Optional[str] = None,
):
    """Busca facetada respeitando o modelo federado (Portal Municipal restringe estritamente a 'publica')."""
    termo = (q or "").strip().lower()
    items = []

    for foto in ACERVO_FOTOS:
        album = ALBUNS[foto["album_id"]]
        album_vis = album["visibilidade"]
        ent_info = ENTIDADES[foto["entidade"]]

        if portal == "municipal" or entidade is None:
            if album_vis != "publica":
                continue
        else:
            if not incluir_restritas and album_vis != "publica":
                continue
            if visibilidade is not None and album_vis != visibilidade:
                continue

        if entidade and foto["entidade"] != entidade:
            continue
        if ano_de is not None and foto["ano"] < ano_de:
            continue
        if ano_ate is not None and foto["ano"] > ano_ate:
            continue
        if tipo and tipo not in (album["perfil_match"], ent_info["categoria"]):
            continue
        if termo:
            haystack = f"{foto['titulo']} {foto['entidade']} {album['titulo']}".lower()
            if termo not in haystack:
                continue

        items.append(
            {
                "foto_id": foto["foto_id"],
                "album_id": foto["album_id"],
                "url": foto["url"],
                "titulo": foto["titulo"],
                "entidade": foto["entidade"],
                "ano": foto["ano"],
                "faces_n": foto["faces_n"],
                "visibilidade": album_vis,
                "perfil_match": album["perfil_match"],
            }
        )

    return {
        "portal": portal,
        "items": items,
        "next_cursor": None,
        "total": len(items),
    }


# 1b. Portais Federados por Entidade & Controle de Visibilidade (S2)
@app.get("/api/v1/entidades")
def list_entidades():
    """Lista as entidades federadas com perfil padrão e contagem dinâmica de álbuns."""
    resultado = []
    for slug, info in ENTIDADES.items():
        ent_albuns = [a for a in ALBUNS.values() if a["entidade"] == slug]
        resultado.append(
            {
                **info,
                "albuns_publicos": sum(1 for a in ent_albuns if a["visibilidade"] == "publica"),
                "albuns_total": len(ent_albuns),
            }
        )
    return {"entidades": resultado}


@app.get("/api/v1/entidades/{slug}/albuns")
def list_albuns_entidade(slug: str, incluir_restritas: bool = False):
    """Lista álbuns de um tenant federado (apenas públicos sem incluir_restritas=true)."""
    if slug not in ENTIDADES:
        raise HTTPException(status_code=404, detail=f"Entidade '{slug}' não encontrada.")

    albuns = [
        dict(album)
        for album in ALBUNS.values()
        if album["entidade"] == slug
        and (incluir_restritas or album["visibilidade"] == "publica")
    ]
    return {"entidade": ENTIDADES[slug], "albuns": albuns}


@app.patch("/api/v1/albuns/{album_id}/visibilidade")
def update_album_visibilidade(album_id: str, payload: VisibilidadeUpdate):
    """Alterna a visibilidade do álbum com trava LGPD obrigatória para entidades protegidas."""
    if album_id not in ALBUNS:
        raise HTTPException(status_code=404, detail=f"Álbum '{album_id}' não encontrado.")

    album = ALBUNS[album_id]
    if album["lgpd_protegido"] and payload.visibilidade == "publica" and not payload.confirmar_lgpd:
        raise HTTPException(
            status_code=409,
            detail="Álbum protegido (LGPD/Creche): envie confirmar_lgpd=true para confirmar liberação pública.",
        )

    visibilidade_anterior = album["visibilidade"]
    album["visibilidade"] = payload.visibilidade
    return {
        "album_id": album_id,
        "entidade": album["entidade"],
        "visibilidade_anterior": visibilidade_anterior,
        "visibilidade": album["visibilidade"],
        "indexado_no_portal_municipal": album["visibilidade"] == "publica",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
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
