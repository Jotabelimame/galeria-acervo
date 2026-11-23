// Banco local de dados de exemplo representando o acervo híbrido
const fotosMock = [
  {
    id: 'f1',
    url: 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=800&auto=format&fit=crop',
    titulo: 'Posse de Diretoria 2024',
    entidade: 'rotary',
    entidadeNome: 'Rotary Club',
    ano: 2024,
    tags: ['posse', 'jantar', 'diretoria']
  },
  {
    id: 'f2',
    url: 'https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=800&auto=format&fit=crop',
    titulo: 'Colação de Grau Formandos',
    entidade: 'faculdade',
    entidadeNome: 'Faculdade Municipal',
    ano: 2024,
    tags: ['formatura', 'diploma', 'educação']
  },
  {
    id: 'f3',
    url: 'https://images.unsplash.com/photo-1544717305-2782549b5136?w=800&auto=format&fit=crop',
    titulo: 'Festa de São Sebastião',
    entidade: 'catolica',
    entidadeNome: 'Igreja Católica - Paróquia Matriz',
    ano: 2023,
    tags: ['padroeiro', 'procissão', 'missa']
  },
  {
    id: 'f4',
    url: 'https://images.unsplash.com/photo-1577962917302-cd874c4e31d2?w=800&auto=format&fit=crop',
    titulo: 'Sessão Solene de Honra ao Mérito',
    entidade: 'camara',
    entidadeNome: 'Câmara de Vereadores',
    ano: 2024,
    tags: ['sessao', 'homenagem', 'politica']
  },
  {
    id: 'f5',
    url: 'https://images.unsplash.com/photo-1519741497674-611481863552?w=800&auto=format&fit=crop',
    titulo: 'Casamento Comunitário',
    entidade: 'evangelica',
    entidadeNome: 'Igreja Evangélica Central',
    ano: 2025,
    tags: ['casamento', 'culto', 'familia']
  },
  {
    id: 'f6',
    url: 'https://images.unsplash.com/photo-1509062522246-3755977927d7?w=800&auto=format&fit=crop',
    titulo: 'Dia das Crianças na Creche',
    entidade: 'creche',
    entidadeNome: 'Creche Municipal Pequeno Príncipe',
    ano: 2025,
    tags: ['criancas', 'festa', 'educacao']
  }
];

// Ledger de Auditoria Blockchain-like (SHA-256 Mock)
async function registrarLogAuditoria(acao, fotoId, termo) {
  const timestamp = new Date().toISOString();
  const dado = `${timestamp}|${acao}|${fotoId || 'N/A'}|${termo || 'N/A'}`;
  
  // Hash simulado simples
  console.log(`[LEDGER AUDITADO] Hash gravado no bloco:`, btoa(dado));
}

function renderizarFotos(lista) {
  const grid = document.getElementById('gridFotos');
  const contador = document.getElementById('contadorFotos');
  grid.innerHTML = '';
  contador.innerText = `${lista.length} fotos encontradas`;

  lista.forEach(foto => {
    const card = document.createElement('div');
    card.className = 'group relative bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg hover:border-indigo-500 transition';
    card.innerHTML = `
      <div class="aspect-video w-full overflow-hidden bg-slate-950">
        <img src="${foto.url}" alt="${foto.titulo}" class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
      </div>
      <div class="p-3">
        <span class="text-[10px] uppercase font-bold text-indigo-400 tracking-wider">${foto.entidadeNome}</span>
        <h4 class="text-xs font-semibold text-slate-100 truncate mt-0.5">${foto.titulo}</h4>
        <div class="mt-2 flex items-center justify-between text-[11px] text-slate-400">
          <span>📅 ${foto.ano}</span>
          <button onclick="baixarFoto('${foto.id}')" class="text-indigo-400 hover:text-indigo-300 font-medium flex items-center gap-1">
            ⬇️ Baixar
          </button>
        </div>
      </div>
    `;
    grid.appendChild(card);
  });
}

function baixarFoto(id) {
  registrarLogAuditoria('DOWNLOAD', id, null);
  alert(`Download solicitado! Foto ${id} registrada no Ledger e carimbada com marca d'água forense.`);
}

function filtrar() {
  const termo = document.getElementById('campoBusca').value.toLowerCase();
  const entidade = document.getElementById('filtroEntidade').value;

  if (termo) registrarLogAuditoria('BUSCA_TEXTUAL', null, termo);

  const filtradas = fotosMock.filter(f => {
    const bateTexto = f.titulo.toLowerCase().includes(termo) || f.tags.some(t => t.includes(termo));
    const bateEntidade = !entidade || f.entidade === entidade;
    return bateTexto && bateEntidade;
  });

  renderizarFotos(filtradas);
}

document.getElementById('campoBusca').addEventListener('input', filtrar);
document.getElementById('filtroEntidade').addEventListener('change', filtrar);

function abrirModalSelfie() {
  document.getElementById('modalSelfie').classList.remove('hidden');
}

function fecharModalSelfie() {
  document.getElementById('modalSelfie').classList.add('hidden');
}

function processarSelfie() {
  const file = document.getElementById('inputSelfie').files[0];
  if (!file) {
    alert('Por favor, selecione ou tire uma foto primeiro!');
    return;
  }
  registrarLogAuditoria('BUSCA_FACIAL', null, 'selfie_upload');
  alert('Processando vetor facial na VM Oracle (pgvector)... Busca realizada!');
  fecharModalSelfie();
}

// Inicialização
renderizarFotos(fotosMock);
