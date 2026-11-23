Olá, equipe QwenWork.ai!

Excelente retorno técnico. Leitura cirúrgica, pragmática e 100% alinhada ao que precisamos. Vamos fechar os pontos agora para destravar a **S1**:

---

### 1. Contrato Canônico de Rotas (Fechado)
Adotamos **oficialmente a padronização sugerida por vocês** (`/api/v1/...`):

| Ação | Rota Canônica | Método |
| :--- | :--- | :--- |
| **Busca facetada** | `/api/v1/acervo/search?q&entidade&ano_de&ano_ate&tipo&cursor` | GET |
| **Busca facial** | `/api/v1/acervo/face` (multipart selfie) | POST |
| **Download forense** | `/api/v1/media/{id}/download` (retorna signed URL TTL 60s) | POST |
| **Ledger (consulta)**| `/api/v1/ledger/{fotoId}` | GET |
| **Canal Telão** | Firebase RTDB: `onChildAdded('/eventos/{slug}/live_feed')` ou WSS | WS / RTDB |

---

### 2. Correções Técnicas Homologadas
* **pgvector SQL:** Corrigido. Usaremos ordenação e filtro direto na expressão com índice HNSW:
  ```sql
  SELECT foto_id, 1 - (embedding <=> :vec) AS sim 
  FROM face_embeddings 
  WHERE 1 - (embedding <=> :vec) > :threshold 
  ORDER BY embedding <=> :vec LIMIT 50;
  ```
  Threshold dinâmico calibrável por categoria/evento (não fixo em 0.68).
* **Segurança & LGPD:** Firebase ID Token obrigatório em todas as rotas privadas. Creches e menores sob isolamento estrito com consentimento/vínculo. A busca facial de convidados no dia a dia **on-device** (como vocês já rodam) é perfeita: custo zero de VM e privacidade máxima. A OCI fica reservada para busca em lote no acervo histórico frio.
* **Ledger Server-side:** 100% calculado e assinado na VM Oracle/Backend. O front só recebe o comprovante (`hash`, `timestamp`, `signer`).

---

### 3. Payload Real do Canal do Telão (CineDirector com "Olhos")
O evento emitido no Firebase RTDB / WebSocket entregará os metadados calculados na ingestão:

```json
{
  "event_id": "evt_padroeiro_2026",
  "foto_id": "fot_98234",
  "url_display": "https://storage.googleapis.com/.../foto_display.webp",
  "created_at": "2026-11-23T20:45:10Z",
  "is_breaking": true,
  "faces_n": 3,
  "primary_face_bbox": { "x": 0.42, "y": 0.28, "w": 0.18, "h": 0.24 },
  "suggested_motion": "kenburns_focus_face",
  "orientation": "landscape",
  "dwell_time_ms": 5500
}
```

---

### 4. Modelo de Visibilidade do Acervo (Definição de Negócio)
* **Modelo Federado por Entidade (com Portal Municipal Unificado):**
  * Cada entidade (Paróquia, Rotary, Escola, Loja Maçônica) tem seu **Portal/Tenant próprio** e autonomia sobre a visibilidade do seu álbum (Público, Restrito a membros com login, ou Privado).
  * O **Portal Geral do Município** apenas indexa o que as entidades marcarem expressamente como `visibilidade: "publica"`.

---

### 5. Estratégia de Strangler & Evento-Piloto
Aprovamos a abordagem *Strangler*: subir a **S1** direto na esteira de vocês (`qwenworkProvider`) e plugar o `ociProvider` conforme provisionamos os endpoints de staging.

* **Evento-Piloto Sugerido:** Festa de Padroeiro / Evento Comunitário Local (a melhor validação humana em tempo real).
* **Próximo passo imediato:** Vamos provisionar as credenciais de teste do Firebase (apiKey/authDomain) e subir o `docker-compose` mock da OCI no repositório GitHub para vocês integrarem de imediato.

Vamos em frente com a S1!
