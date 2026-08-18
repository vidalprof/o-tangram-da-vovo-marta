# 🔺 O JOGO DO TANGRAM — didático (3º, 4º e 5º anos)

Pedido do Marcos (ago/2026), e ele corrigiu meu primeiro rascunho com todas as
letras: *"não é pra ser atividade, é pra ser o JOGO do tangram só que didático"*,
*"não é para ter as diversas interatividades"*, *"é só o jogo do tangram"*.

⚠️ **REGISTRADO PARA NÃO SE PERDER: existe "atividade" e existe "JOGO".**
- **Atividade** = leque de dinâmicas variadas (o padrão da casa: ≥4 gestos,
  nenhum acima de 40%).
- **JOGO** = **uma mecânica só**, do começo ao fim, subindo de dificuldade. A
  didática não entra por fora (mudando de dinâmica); entra por DENTRO — pela
  ordem das figuras, pelo que a voz ensina em cada uma e pela ajuda que cresce.
Quando ele pedir um JOGO, o portão `_qa/padrao.py` (que cobra variedade) não se
aplica — e o arquivo declara isso, para ninguém "consertar" depois achando que
faltou variedade.

## O jogo

A vovó Marta guarda uma caixa de tangram na oficina de brinquedos. As peças
caíram; a criança monta figura por figura, e cada figura ensina uma coisa.

| # | figura | peças | o que o jogo ensina AQUI |
|---|---|---|---|
| 1 | a vela do barco | 3 | as três formas têm nome: triângulo, quadrado, meio-quadrado |
| 2 | a casinha | 3 | uma peça só entra VIRADA — o botão de girar |
| 3 | o foguete | 4 | duas peças iguais em lugares diferentes |
| 4 | o gato | 4 | girar duas vezes (meia volta) |
| 5 | o pássaro | 5 | a figura cresce; olhar o contorno antes de pegar |
| 6 | o peixe | 5 | dois meio-quadrados formam um quadrado (decomposição) |
| 7 | o coelho | 6 | planejar a ordem: as peças grandes primeiro |
| 8 | o barco grande | 6 | mesma forma, tamanhos diferentes |
| 9 | o quadrado clássico | 7 | o tangram inteiro fecha um quadrado |
| 10 | o desafio da vovó | 7 | tudo junto, sem dica na primeira tentativa |

## A didática por dentro (é isto que o torna educativo, não a variedade)

- **Instrução falada E escrita em toda tela** (regra da casa, e ele repetiu hoje).
- **A voz nomeia a forma** quando a criança pega a peça: *"triângulo de ponta"*.
- **Ajuda que cresce** (`ajudaJd`): 1º engano = dica falada; 2º = a vaga certa
  pisca; 3º = a peça gira sozinha para o ângulo certo; 4º = ela se encaixa.
  **Nunca trava.**
- **Girar é BOTÃO grande**, de 90 em 90 graus, com a virada animada — dedo de
  criança não faz arrasto em círculo (armadilha já paga na peça).
- **Três caminhos**: mouse, dedo e toque simples (tocar a peça, tocar a vaga).
- **Encaixe com tolerância de 90px**: mira de precisão é para adulto com mouse.
- **Fim**: boletim animado, medalha, relatório escondido do professor
  (segurar a medalha 2 s) e "treinar o que faltou".
- **Continua de onde parou por 55 minutos** (`_padrao/RETOMAR.md`).

## De onde vem cada coisa (copiar, não reescrever)

- **mecânica**: `_padrao/pecas/tangram.html` (533 linhas, armadilhas fechadas).
- **motor**: `_jardim/index.html` (capa, crachá, barra, balão, voz, medição,
  boletim, relatório escondido, retomar).
- **arte**: mascote vovó Marta + 6 crachás + caixa + medalha em **2 cartelas**
  (R$ 0,40 no lugar de R$ 1,80) + o fundo da oficina pelo Pollinations, grátis.
  ⚠️ As **peças do tangram são SVG** — giram e encaixam; bitmap girado serrilha.

## O que já está de pé (13/08)

- **Motor do jogo funcionando**: mesa com as vagas em contorno tracejado, peças
  em SVG, bandeja, botão **Girar a peça** (45°), botão **Virar do outro lado**
  que só aparece no paralelogramo, contador de peças, encaixe com tolerância de
  80px e a ajuda que cresce até encaixar sozinha.
- **Arrastar pelo jeito novo** (a pesquisa de hoje): `pointerdown/move/up` com
  `setPointerCapture` e `touch-action:none` — um caminho só para mouse e dedo —
  mais o toque simples e a guarda do clique fantasma.
- **Geometria conferida por conta**: peq 0,5 · med 1 · gra 2 · quadrado 1 ·
  paralelogramo 1; as sete somam 8 = o quadrado de lado 2√2. **O tangram
  inteiro vale 16 triangulinhos** — é daqui que sai a fase de área do 5º ano.
- Três figuras de teste montadas e abrindo sem erro no navegador.

## O que falta (na ordem)

1. **As 10 figuras com geometria de verdade** — hoje as vagas estão em posições
   de teste e não desenham um barco/gato reconhecível. É o trabalho principal
   que resta: cada figura precisa das coordenadas certas das 3→7 peças.
2. **A arte** (gerando): vovó Marta, 6 crachás, caixa e medalha em 2 cartelas +
   o fundo da oficina.
3. **`falas.json`** e a gravação (uma instrução falada por figura + as dicas).
4. Bancada e publicação.

## 14/08 — a geometria ficou de pé; as SILHUETAS ainda não

**Pronto e conferido:** `_tangram/figuras.py` descreve cada figura pelos
**vértices** e o programa (a) descobre sozinho qual das sete peças é e em que
ângulo, (b) reprova sobreposição, área que não fecha e figura maior que a mesa.
Na primeira tentativa, escrita à mão, **três das quatro figuras tinham peça em
cima de peça** — e eu teria entregado isso.

⚠️ **Lição paga na conversão para a tela:** eu usava o CENTRO da caixa para
posicionar, e duas peças giradas 180° uma da outra têm o mesmo centro. Agora a
conversão **simula o caminho que o navegador faz** (desenha na caixa, gira em
torno do centro, desloca) e resolve o deslocamento — é a única forma de bater.

**O que falta, e é honesto dizer:** as dez figuras passam na geometria mas
**ainda não se parecem com os nomes** — o "gato" é uma coluna de 2×5. Elas foram
compostas por encaixe válido, não por desenho. O próximo passo é desenhar as
silhuetas de verdade (as clássicas do tangram: barco, gato, coelho, casa,
vela), conferindo cada uma com o mesmo programa e OLHANDO o resultado.
