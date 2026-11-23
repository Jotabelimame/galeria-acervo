// CineDirector AI - Agente de Transições Dinâmicas para Telão
const fotosTelao = [
  {
    url: 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=1600&auto=format&fit=crop',
    tipo: 'coletiva', // muitas pessoas -> Pan longo
    rotulo: 'Panorâmica da Festa (Rotary)'
  },
  {
    url: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=1600&auto=format&fit=crop',
    tipo: 'retrato', // rosto individual -> Zoom no rosto
    rotulo: 'Retrato de Convidada'
  },
  {
    url: 'https://images.unsplash.com/photo-1519741497674-611481863552?w=1600&auto=format&fit=crop',
    tipo: 'destaque', // momento solene -> Flash suave
    rotulo: 'Entrada Solene'
  },
  {
    url: 'https://images.unsplash.com/photo-1523580494863-6f3031224c94?w=1600&auto=format&fit=crop',
    tipo: 'coletiva',
    rotulo: 'Comemoração dos Formandos'
  }
];

let indiceAtual = 0;
const imgEl = document.getElementById('imgTelao');
const modoTextoEl = document.getElementById('modoTransicaoTexto');

// Efeitos disponíveis para o CineDirector
const modosAnimacao = [
  { classe: 'kenburns-zoom', desc: 'Ken Burns (Zoom Focado no Rosto)', tempo: 5000 },
  { classe: 'kenburns-pan-left', desc: 'Panorâmica Lenta para Esquerda', tempo: 7000 },
  { classe: 'kenburns-pan-right', desc: 'Panorâmica Lenta para Direita', tempo: 7000 },
  { classe: 'flash-effect', desc: 'Disparo Flash Fotográfico', tempo: 4000 }
];

function executarProximaCena() {
  const foto = fotosTelao[indiceAtual];
  
  // Decisão inteligente do CineDirector AI baseada no tipo da imagem
  let modoEscolhido;
  if (foto.tipo === 'retrato') {
    modoEscolhido = modosAnimacao[0]; // Zoom no rosto
  } else if (foto.tipo === 'coletiva') {
    modoEscolhido = Math.random() > 0.5 ? modosAnimacao[1] : modosAnimacao[2]; // Pan longo
  } else {
    modoEscolhido = modosAnimacao[3]; // Flash fotográfico
  }

  // 1. Fade Out
  imgEl.style.opacity = '0';

  setTimeout(() => {
    // 2. Troca imagem e aplica classe de transição decidida pela IA
    imgEl.src = foto.url;
    imgEl.className = 'w-full h-full object-cover transition-opacity duration-1000 ease-in-out ' + modoEscolhido.classe;
    modoTextoEl.innerText = `${modoEscolhido.desc} | ${foto.rotulo}`;

    // 3. Fade In
    imgEl.style.opacity = '1';

    // Próximo índice
    indiceAtual = (indiceAtual + 1) % fotosTelao.length;

    // Agenda a próxima transição com o tempo orgânico decidido pela IA
    setTimeout(executarProximaCena, modoEscolhido.tempo);
  }, 1000);
}

// Inicia projeção
window.addEventListener('load', () => {
  executarProximaCena();
});
