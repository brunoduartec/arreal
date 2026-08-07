import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "/Users/bruno.duartec/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp/lib/index.js";

const here = path.dirname(fileURLToPath(import.meta.url));
const project = path.resolve(here, "../../..");
const coverPath = path.join(project, "images/capa_kdp_refinada.png");
const cover = `data:image/png;base64,${fs.readFileSync(coverPath).toString("base64")}`;

const posts = [
  {
    slug: "post_01_imaginar_o_impossivel",
    title: "PARA VOLTAR A IMAGINAR O IMPOSSÍVEL",
    accent: "#e3aa55",
    slides: [
      ["POR QUE LER", "ARREAL?", "1/5 • O PRIMEIRO CONTATO COM O IMPOSSÍVEL"],
      ["PARA SENTIR", "DE NOVO O ESPANTO", "DE VER O IMPOSSÍVEL DIANTE DE ALGUÉM COMUM."],
      ["ATRÁS DA ESCOLA,", "GAROTO SE ESCONDE", "na mata fechada, depois de fugir dos colegas."],
      ["ENTÃO ÍTALO", "DESCE DO CÉU", "como se deslizasse pelo ar — sem asas e sem máquina."],
      ["É A PRIMEIRA VEZ", "QUE GAROTO VÊ", "UMA HABILIDADE ACONTECER DIANTE DELE."],
      ["ARREAL", "O IMPOSSÍVEL APARECE ATRÁS DA ESCOLA.", "DISPONÍVEL NO KINDLE E KINDLE UNLIMITED"]
    ],
    caption: `Por que ler Arreal, um livro de fantasia urbana brasileira?\n\nPara reencontrar o espanto de ver algo impossível acontecer diante de uma pessoa comum.\n\nEm “O despertar”, Garoto foge dos colegas e se esconde na mata atrás da escola. É ali que Ítalo desce do céu como se deslizasse pelo ar — sem asas e sem máquina. Esse é o primeiro contato de Garoto com uma habilidade.\n\nArreal é uma fantasia brasileira sobre pessoas comuns descobrindo capacidades que pareciam existir apenas nos quadrinhos.\n\n📖 Leia no Kindle ou pelo Kindle Unlimited. Link na bio.\n\n#Arreal #FantasiaBrasileira #FantasiaUrbana`
  },
  {
    slug: "post_02_o_poder_revela",
    title: "PARA DESCOBRIR O QUE SEU PODER REVELARIA",
    accent: "#d77b32",
    slides: [
      ["POR QUE LER", "ARREAL?", "2/5 • A PRIMEIRA INVISIBILIDADE"],
      ["QUANDO O SOCO VEM,", "GAROTO NÃO PENSA", "EM LUTAR."],
      ["ELE PENSA", "APENAS EM DEIXAR", "de ser visto."],
      ["PRENDE A RESPIRAÇÃO.", "E DESAPARECE.", "O agressor acerta apenas o espaço vazio."],
      ["A HABILIDADE", "RESPONDE AO QUE", "GAROTO DESEJA NO INSTANTE DO MEDO."],
      ["ARREAL", "DESCOBRIR UM PODER TAMBÉM PODE ASSUSTAR.", "NO KINDLE E KINDLE UNLIMITED"]
    ],
    caption: `Por que ler Arreal?\n\nPara acompanhar um poder surgindo do medo, sem transformar a descoberta numa vitória fácil.\n\nDurante uma emboscada numa rua vazia de Arreal, Garoto prende a respiração. Ele não pensa em lutar: pensa apenas em deixar de ser visto. Seu corpo desaparece, e o punho do agressor fica estendido no espaço vazio.\n\nA cena está em “A Emboscada”. A imagem mostra somente esse instante.\n\n📖 Arreal está no Kindle e Kindle Unlimited. Link na bio.\n\n#Arreal #FantasiaUrbana #FantasiaBrasileira`
  },
  {
    slug: "post_03_personagens_imperfeitos",
    title: "PARA ENCONTRAR PERSONAGENS IMPERFEITOS",
    accent: "#c9994f",
    slides: [
      ["POR QUE LER", "ARREAL?", "3/5 • UMA VERSÃO CHAMADA “MELHORADO”"],
      ["GAROTO QUER", "SER VISTO COMO", "ALGUÉM MELHOR."],
      ["DIANTE DO ESPELHO,", "ELE AFINA O ROSTO", "e aumenta alguns centímetros."],
      ["UMA CAMISA VELHA", "VIRA A JAQUETA", "que ele viu numa revista."],
      ["ELE CHAMA", "ESSA VERSÃO DE", "“MELHORADO”."],
      ["ARREAL", "ELE MUDA A APARÊNCIA — NÃO O QUE SENTE.", "NO KINDLE E KINDLE UNLIMITED"]
    ],
    caption: `Por que ler Arreal?\n\nPara conhecer um personagem que consegue mudar a própria aparência, mas não apaga a insegurança que o levou a fazer isso.\n\nDiante do espelho, Garoto aumenta alguns centímetros, afina o rosto e troca a camisa velha pela ilusão de uma jaqueta vista numa revista. Ele chama essa versão de “melhorado”.\n\nA cena está no capítulo 7. A arte reproduz apenas essa experiência no quarto.\n\n📖 Arreal está no Kindle e Kindle Unlimited. Link na bio.\n\n#Arreal #PersonagensImperfeitos #FantasiaBrasileira`
  },
  {
    slug: "post_04_fantasia_brasileira",
    title: "PARA LER UMA FANTASIA COM IDENTIDADE BRASILEIRA",
    accent: "#5ea3c7",
    slides: [
      ["POR QUE LER", "ARREAL?", "4/5 • O EXTRAORDINÁRIO TAMBÉM MORA AQUI"],
      ["A PRAÇA DE ARREAL", "TEM CARROS, BICICLETAS,", "ESTUDANTES E CAFÉ ESFRIANDO NA MESA."],
      ["TAMBÉM TEM", "VELHOS DISCUTINDO", "política entre duas xícaras."],
      ["NO CAFÉ EM FRENTE,", "UM HOMEM DE PRETO", "entrega a Garoto um envelope dourado."],
      ["É DESSE COTIDIANO", "BRASILEIRO QUE O", "ESTRANHO COMEÇA A ESPIAR DE VOLTA."],
      ["ARREAL", "UMA FANTASIA URBANA QUE COMEÇA PERTO DA PRAÇA.", "NO KINDLE E KINDLE UNLIMITED"]
    ],
    caption: `Por que ler Arreal?\n\nPara encontrar o estranho dentro de um cotidiano reconhecível.\n\nGaroto passa horas num café em frente à praça de Arreal. Do lado de fora, há carros, bicicletas, estudantes e velhos discutindo política. É nessa mesa, junto do café frio e do açucareiro, que um homem de preto entrega a ele um envelope dourado.\n\nA cena acontece em “A mulher sem nome”. A arte não acrescenta portal, rachadura nem poder que não esteja ali.\n\n📖 Conheça Arreal no Kindle e Kindle Unlimited. Link na bio.\n\n#Arreal #FantasiaBrasileira #LiteraturaNacional`
  },
  {
    slug: "post_05_liberdade_e_controle",
    title: "PARA PENSAR SE PODER E LIBERDADE SÃO A MESMA COISA",
    accent: "#df9a42",
    slides: [
      ["POR QUE LER", "ARREAL?", "5/5 • A FANTASIA TERMINA. A PERGUNTA FICA."],
      ["NO EMPIRE STATE,", "GAROTO FAZ UMA MOEDA", "PARAR NO AR DIANTE DOS OLHOS."],
      ["DEPOIS, FECHA A MÃO.", "A MOEDA SE AMASSA.", "Controlar o metal é ridiculamente fácil."],
      ["CONTROLAR OBJETOS", "VIROU MAIS SIMPLES", "DO QUE DECIDIR O QUE FAZER CONSIGO MESMO."],
      ["ELE JÁ VIU", "CONTROLE SER CHAMADO", "DE PROTEÇÃO — E VIOLÊNCIA DE LIBERDADE."],
      ["ARREAL", "LEIA PARA DESCOBRIR COMO ELE CHEGOU ATÉ AQUI.", "NO KINDLE E KINDLE UNLIMITED"]
    ],
    caption: `Por que ler Arreal?\n\nPara acompanhar alguém capaz de controlar uma moeda no ar, mas ainda incapaz de decidir facilmente o que fazer com o próprio poder.\n\nNo topo do Empire State, Garoto mantém uma moeda suspensa diante dos olhos. Depois, fecha a mão e a amassa. Ele admite que controlar objetos se tornou mais simples do que decidir o que fazer consigo mesmo — e lembra ter visto controle ser chamado de proteção e violência de liberdade.\n\nEssa é a abertura de “O despertar”. A imagem mostra somente Garoto, a moeda e a cidade abaixo.\n\n📖 Arreal está no Kindle e Kindle Unlimited. Link na bio.\n\n#Arreal #FantasiaBrasileira #DilemaMoral`
  }
];

const esc = (value) => value.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");

function wrap(text, max) {
  const words = text.split(/\s+/);
  const lines = [];
  let line = "";
  for (const word of words) {
    const candidate = line ? `${line} ${word}` : word;
    if (candidate.length > max && line) {
      lines.push(line);
      line = word;
    } else line = candidate;
  }
  if (line) lines.push(line);
  return lines;
}

function textBlock(text, x, y, maxChars, size, color, family, weight, lineGap = 1.02) {
  const lines = wrap(text, maxChars);
  return `<text x="${x}" y="${y}" fill="${color}" font-family="${family}" font-size="${size}" font-weight="${weight}" letter-spacing="1.2">${lines.map((line, i) => `<tspan x="${x}" dy="${i ? size * lineGap : 0}">${esc(line)}</tspan>`).join("")}</text>`;
}

function svg(post, slide, slideIndex) {
  const [lead, headline, body] = slide;
  const total = post.slides.length;
  const closing = slideIndex === total - 1;
  const illustrated = [0, 2, 4].includes(slideIndex);
  // Somente ativos aprovados em auditoria-canonica.md podem entrar no carrossel.
  // `arte_chave.png` pertence ao lote conceitual reprovado e é deliberadamente ignorado.
  const artPath = path.join(here, post.slug, "arte_canone.png");
  const art = fs.existsSync(artPath) ? `data:image/png;base64,${fs.readFileSync(artPath).toString("base64")}` : "";
  const index = posts.indexOf(post) + 1;
  const headlineSize = headline.length > 16 ? 60 : headline.length > 10 ? 78 : 100;
  const headlineWrap = headlineSize === 60 ? 24 : headlineSize === 78 ? 18 : 14;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#02070d"/><stop offset=".55" stop-color="#071827"/><stop offset="1" stop-color="#010306"/></linearGradient>
    <radialGradient id="glow" cx="78%" cy="65%" r="66%"><stop stop-color="${post.accent}" stop-opacity=".28"/><stop offset=".52" stop-color="#194e70" stop-opacity=".16"/><stop offset="1" stop-color="#03101c" stop-opacity="0"/></radialGradient>
    <linearGradient id="veil" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#01060b" stop-opacity=".95"/><stop offset=".58" stop-color="#03101a" stop-opacity=".63"/><stop offset="1" stop-color="#02070d" stop-opacity=".18"/></linearGradient>
    <filter id="shadow"><feGaussianBlur in="SourceAlpha" stdDeviation="16"/><feOffset dy="16"/><feComponentTransfer><feFuncA type="linear" slope=".62"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="1080" height="1350" fill="url(#bg)"/>${illustrated && art ? `<image href="${art}" x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice" opacity=".96"/><rect width="1080" height="1350" fill="url(#veil)"/>` : ""}<rect width="1080" height="1350" fill="url(#glow)"/>
  <g opacity=".16" fill="none" stroke="${post.accent}"><circle cx="870" cy="780" r="280"/><circle cx="870" cy="780" r="390"/><circle cx="870" cy="780" r="510"/></g>
  <g stroke="#7db3d0" opacity=".13"><path d="M-40 1080 L870 370"/><path d="M170 1350 L1050 535"/><path d="M570 1350 L1080 875"/></g>
  <g fill="#86b9d6" opacity=".52"><circle cx="92" cy="130" r="2"/><circle cx="195" cy="190" r="1.5"/><circle cx="886" cy="113" r="2"/><circle cx="978" cy="270" r="1.4"/><circle cx="810" cy="502" r="2"/><circle cx="135" cy="670" r="1.3"/><circle cx="930" cy="780" r="1.6"/><circle cx="177" cy="1070" r="2"/><circle cx="867" cy="1210" r="1.4"/></g>
  <rect x="58" y="55" width="114" height="4" fill="${post.accent}"/>
  <text x="58" y="91" fill="#f2f0eb" font-family="Arial, sans-serif" font-size="20" font-weight="bold" letter-spacing="2">ARREAL • BRUNO DUARTE CORRÊA</text>
  <text x="1018" y="91" fill="${post.accent}" text-anchor="end" font-family="Arial, sans-serif" font-size="20" font-weight="bold">${slideIndex + 1}/${total}</text>
  ${closing ? `<g filter="url(#shadow)" transform="translate(655 238) rotate(2 160 255)"><rect x="-7" y="-7" width="334" height="524" fill="${post.accent}"/><image href="${cover}" x="0" y="0" width="320" height="510" preserveAspectRatio="xMidYMid slice"/></g>` : ""}
  ${textBlock(lead, 62, closing ? 285 : 292, closing ? 18 : 21, closing ? 58 : 64, post.accent, "Arial, sans-serif", "800", 1.05)}
  ${textBlock(headline, 58, closing ? 850 : 455, closing ? 23 : headlineWrap, closing ? 58 : headlineSize, "#f6f4ef", "Impact, Arial Black, sans-serif", "900", 1.02)}
  ${textBlock(body, 62, closing ? 1060 : 865, closing ? 34 : 38, closing ? 30 : 38, "#f0eee8", "Arial, sans-serif", "700", 1.22)}
  <rect x="58" y="1236" width="${closing ? 566 : 390}" height="57" rx="28" fill="${post.accent}"/>
  <text x="${closing ? 341 : 253}" y="1274" fill="#06101a" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" font-weight="bold" letter-spacing="1">${closing ? "LEIA NO KINDLE • LINK NA BIO" : `POR QUE LER ARREAL? • ${index}/5`}</text>
  </svg>`;
}

for (const post of posts) {
  const dir = path.join(here, post.slug);
  const sourceDir = path.join(dir, "fontes");
  fs.mkdirSync(sourceDir, { recursive: true });
  for (const [i, slide] of post.slides.entries()) {
    const base = `${String(i + 1).padStart(2, "0")}`;
    const svgPath = path.join(sourceDir, `${base}.svg`);
    const pngPath = path.join(dir, `${base}.png`);
    fs.writeFileSync(svgPath, svg(post, slide, i));
    await sharp(Buffer.from(svg(post, slide, i))).png().toFile(pngPath);
  }
  const thumbs = await Promise.all(post.slides.map((_, i) => sharp(path.join(dir, `${String(i + 1).padStart(2, "0")}.png`)).resize(324, 405).toBuffer()));
  await sharp({ create: { width: 972, height: 810, channels: 3, background: "#07131d" } })
    .composite(thumbs.map((input, i) => ({ input, left: (i % 3) * 324, top: Math.floor(i / 3) * 405 })))
    .jpeg({ quality: 90 })
    .toFile(path.join(dir, "preview.jpg"));
  fs.writeFileSync(path.join(dir, "legenda.txt"), `${post.caption}\n`);
}

const calendar = `# Série — Por que ler Arreal?\n\nObjetivo: transformar curiosidade em identificação e cliques para o livro.\nFuso: America/Sao_Paulo.\nMétrica principal: compartilhamentos e salvamentos; secundária: visitas ao perfil e toques no link.\n\n- Post 1 — sábado, 1º de agosto de 2026, publicar na faixa de 13h30–15h (pico do perfil às 15h).\n- Post 2 — terça-feira, 4 de agosto, no melhor pico indicado pelo Insights do dia.\n- Post 3 — sexta-feira, 7 de agosto, no melhor pico indicado pelo Insights do dia.\n- Post 4 — terça-feira, 11 de agosto, no melhor pico indicado pelo Insights do dia.\n- Post 5 — sexta-feira, 14 de agosto, no melhor pico indicado pelo Insights do dia.\n\nRegra: conferir os horários ativos no dia; não usar benchmark externo enquanto houver dados próprios.\n`;
fs.writeFileSync(path.join(here, "calendario.md"), calendar);
