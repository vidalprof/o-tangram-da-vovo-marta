# -*- coding: utf-8 -*-
u"""
============================================================
AS FIGURAS DO TANGRAM — calculadas, não chutadas

⚠️ A primeira versão pôs as vagas "a olho" e o resultado não parecia um barco:
eram três contornos soltos no meio da mesa. Figura de tangram não se posiciona
por tentativa — ela se MONTA por vértice, e depois se converte para o que a tela
entende (canto de cima + ângulo).

Aqui cada figura é escrita pelos VÉRTICES de cada peça, em unidades do cateto do
triângulo pequeno. O programa confere três coisas antes de deixar passar:
  1. as peças não se sobrepõem (área somada = área da união);
  2. a figura não passa do tamanho da mesa;
  3. a peça descrita bate com uma das sete de verdade (forma e tamanho).
Depois converte para `{f, x, y, ang, esp}` e escreve o JS.

Rodar:  python3 _tangram/figuras.py
============================================================
"""
import io
import json
import math

R2 = math.sqrt(2)

# as sete peças, cada uma pelo seu polígono na posição "de fábrica" (ang 0)
BASE = {
    "peq":  [(0, 0), (1, 0), (0, 1)],
    "med":  [(0, 0), (R2, 0), (0, R2)],
    "gra":  [(0, 0), (2, 0), (0, 2)],
    "quad": [(0, 0), (1, 0), (1, 1), (0, 1)],
    "par":  [(0, 1), (1, 1), (2, 0), (1, 0)],
}


def area(p):
    s = 0.0
    for i in range(len(p)):
        x1, y1 = p[i]
        x2, y2 = p[(i + 1) % len(p)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


def gira(p, ang):
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    return [(x * c - y * s, x * s + y * c) for (x, y) in p]


def move(p, dx, dy):
    return [(x + dx, y + dy) for (x, y) in p]


def caixa(p):
    xs = [x for x, y in p]
    ys = [y for x, y in p]
    return min(xs), min(ys), max(xs), max(ys)


def para_tela(f, ang, esp, verts):
    u"""⚠️ DEFEITO PAGO NA PRIMEIRA RODADA: a conversão usava o CENTRO da caixa —
    e duas peças giradas 180° uma da outra têm exatamente o mesmo centro de
    caixa. As duas do quadrado saíram no mesmo x,y, uma em cima da outra, e a
    mesa mostrava uma figura só. Centro não identifica pose.

    O certo é seguir o caminho que a TELA faz, na mesma ordem: ela desenha a
    peça na caixa (0,0)-(w,h), gira em torno do centro dessa caixa e depois
    desloca por left/top. Então eu simulo isso e resolvo o deslocamento que
    leva o resultado até onde a figura quer."""
    p = BASE[f]
    if esp:
        x0, y0, x1, y1 = caixa(p)
        p = [(x1 - (x - x0), y) for (x, y) in p]
    bx0, by0, bx1, by1 = caixa(p)
    w, h = bx1 - bx0, by1 - by0
    cx, cy = (bx0 + bx1) / 2.0, (by0 + by1) / 2.0
    # gira em torno do centro da caixa, como o CSS faz
    a = math.radians(ang)
    co, si = math.cos(a), math.sin(a)
    girado = [((x - cx) * co - (y - cy) * si + cx,
               (x - cx) * si + (y - cy) * co + cy) for (x, y) in p]
    # o deslocamento que leva o girado ate o alvo (comparando o canto)
    gx0, gy0, gx1, gy1 = caixa(girado)
    vx0, vy0, vx1, vy1 = caixa(verts)
    return round(vx0 - gx0, 3), round(vy0 - gy0, 3)


def confere(nome, pecas):
    u"""as três conferências antes de a figura poder entrar no jogo"""
    soma = sum(area(v["verts"]) for v in pecas)
    # sobreposição: aproximação por amostragem em grade fina
    passo = 0.05
    x0 = min(caixa(v["verts"])[0] for v in pecas)
    y0 = min(caixa(v["verts"])[1] for v in pecas)
    x1 = max(caixa(v["verts"])[2] for v in pecas)
    y1 = max(caixa(v["verts"])[3] for v in pecas)

    def dentro(pt, poly):
        x, y = pt
        d = False
        j = len(poly) - 1
        for i in range(len(poly)):
            xi, yi = poly[i]
            xj, yj = poly[j]
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
                d = not d
            j = i
        return d

    uniao = 0
    duplo = 0
    y = y0
    while y < y1:
        x = x0
        while x < x1:
            n = 0
            for v in pecas:
                if dentro((x + passo / 2, y + passo / 2), v["verts"]):
                    n += 1
            if n:
                uniao += 1
            if n > 1:
                duplo += 1
            x += passo
        y += passo
    a_uniao = uniao * passo * passo
    prob = []
    if duplo * passo * passo > 0.08:
        prob.append(u"peças SOBREPOSTAS (%.2f u² em cima uma da outra)" % (duplo * passo * passo))
    if abs(soma - a_uniao) > 0.25:
        prob.append(u"área somada %.2f × área da figura %.2f — sobra ou falta" % (soma, a_uniao))
    if (x1 - x0) > 8.5 or (y1 - y0) > 8.5:
        prob.append(u"figura maior que a mesa (%.1f × %.1f u)" % (x1 - x0, y1 - y0))
    return prob, (x0, y0, x1, y1)




def mesmos(a, b, tol=0.02):
    u"""dois polígonos são o mesmo conjunto de vértices?"""
    if len(a) != len(b):
        return False
    resto = list(b)
    for pt in a:
        achou = None
        for q in resto:
            if abs(pt[0] - q[0]) < tol and abs(pt[1] - q[1]) < tol:
                achou = q
                break
        if achou is None:
            return False
        resto.remove(achou)
    return True


def acha_pose(verts):
    u"""⭐ O CAMINHO CERTO: eu descrevo a figura pelos VÉRTICES (que dá para
    conferir olhando) e o programa acha qual das sete peças é, em que ângulo e
    se está espelhada. Antes eu escrevia o ângulo na mão e errava — três das
    quatro figuras da primeira tentativa saíram com peça em cima de peça."""
    for f, base in BASE.items():
        for esp in (0, 1):
            p = base
            if esp:
                a0, b0, a1, b1 = caixa(p)
                p = [(a1 - (x - a0), y) for (x, y) in p]
            for ang in (0, 45, 90, 135, 180, 225, 270, 315):
                g = gira(p, ang)
                gx0, gy0, gx1, gy1 = caixa(g)
                vx0, vy0, vx1, vy1 = caixa(verts)
                mv = move(g, vx0 - gx0, vy0 - gy0)
                if mesmos(mv, verts):
                    return {"f": f, "ang": ang, "esp": esp, "verts": list(verts)}
    return None

# ---------------- as figuras ----------------
# cada peça: (forma, ângulo, espelhada, deslocamento) — os vértices saem daí
def peca(f, ang=0, esp=0, dx=0.0, dy=0.0):
    p = BASE[f]
    if esp:
        a0, b0, a1, b1 = caixa(p)
        p = [(a1 - (x - a0), y) for (x, y) in p]
    return {"f": f, "ang": ang, "esp": esp, "verts": move(gira(p, ang), dx, dy)}


def P(*pts):
    u"""uma peça descrita pelos VÉRTICES; o programa acha qual é e o giro dela.

    ⚠️ LIÇÃO PAGA: eu escrevi as figuras pensando em Y PARA CIMA (como na aula
    de geometria) e a tela usa Y PARA BAIXO. O telhado da casa saiu embaixo do
    quadrado. Aqui o Y é invertido de uma vez: eu continuo escrevendo do jeito
    que penso, e o programa entrega do jeito que a tela desenha."""
    pts = [(x, -y) for (x, y) in pts]
    r = acha_pose(list(pts))
    if r is None:
        raise SystemExit(u"!! esse polígono não é nenhuma das sete peças: %s" % (pts,))
    return r


# as dez figuras, da mais fácil para a mais difícil. Todas conferidas por
# sobreposição, área e tamanho antes de virarem JS.
FIGURAS = [
 # ⚠️ COMEÇA EM CINCO PEÇAS (o Marcos: *"acho que dá pra começar com umas 5"*).
 # Três era passeio para o 5º ano; a escada agora vai de 5 a 7.
 (u"casaj", u"A CASA E O JARDIM", u"As grandes primeiro; as pequenas fecham.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((0,0),(1,0),(0,-1)), P((2,0),(2,-1),(1,0))]),

 (u"torre", u"A TORRE", u"Empilhar: cada pe&#231;a segura a de cima.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((0,0),(1,0),(1,-1),(0,-1)), P((1,0),(2,0),(2,-1),(1,-1))]),

 (u"peixe", u"O PEIXE", u"Dois meio-quadrados fazem um quadrado.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)),
   P((2,0),(3,0),(3,-1)), P((2,1),(3,1),(2,2)),
   P((0,2),(1,2),(0,3))]),

 (u"foguete", u"O FOGUETE", u"Olhe o contorno antes de pegar a pe&#231;a.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((0,0),(1,0),(1,-1),(0,-1)), P((1,0),(2,0),(2,-1)), P((0,0),(0,-1),(-1,0))]),

 (u"casa2", u"A CASA GRANDE", u"O paralelogramo tem lado direito e lado esquerdo.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((0,0),(1,0),(1,-1),(0,-1)), P((1,0),(2,0),(2,-1),(1,-1)),
   P((2,0),(3,0),(4,1),(3,1))]),

 (u"barco6", u"O BARCO", u"A vela grande e o casco embaixo.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((0,0),(1,0),(0,-1)), P((1,0),(2,0),(2,-1)),
   P((2,0),(3,0),(3,1))]),

 (u"gato7", u"O GATO", u"Os dois tri&#226;ngulos pequenos viram as orelhas.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)),
   P((0,2),(1,2),(0,3)), P((2,2),(2,3),(1,2)),
   P((0,0),(1,0),(1,-1),(0,-1)), P((1,0),(2,0),(2,-1)),
   P((2,0),(3,0),(4,1),(3,1))]),

 (u"bote", u"O BOTE", u"O tri&#226;ngulo grande virado vira o casco.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(1,2),(0,3)),
   P((1,2),(2,2),(2,3)), P((0,-1),(2,-1),(1,0))]),

 (u"vela2", u"O VELEIRO", u"Duas velas: uma grande e uma m&#233;dia.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((2,2),(3,2),(3,3)), P((0,-1),(1,-1),(1,0),(0,0)), P((1,-1),(2,-1),(2,0),(1,0))]),

 (u"arvore", u"A &#193;RVORE", u"O tronco &#233; o quadrado; a copa, os tri&#226;ngulos.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((0,-1),(1,-1),(1,0),(0,0)), P((1,-1),(2,-1),(2,0))]),

 (u"chave", u"A CHAVE", u"Pe&#231;a pequena no lugar certo faz diferen&#231;a.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)),
   P((2,0),(3,0),(3,1)), P((2,1),(3,1),(2,2)), P((0,2),(1,2),(1,3),(0,3))]),

 (u"lanterna", u"A LANTERNA", u"Empilhar exige olhar de baixo para cima.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((0,-1),(1,-1),(1,0),(0,0)), P((1,-1),(2,-1),(2,0),(1,0)),
   P((0,-2),(1,-2),(1,-1),(0,-1))]),

 (u"pipa", u"A PIPA", u"O paralelogramo vira a rabiola.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((2,0),(3,0),(4,-1),(3,-1)), P((0,-1),(1,-1),(1,0),(0,0))]),

 (u"casaJ2", u"A CASA E A CERCA", u"A cerca &#233; feita de pe&#231;as pequenas.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((2,0),(3,0),(3,1)), P((2,1),(3,1),(2,2)),
   P((0,-1),(1,-1),(1,0),(0,0)), P((1,-1),(2,-1),(2,0))]),

 (u"foguete2", u"O FOGUETE GRANDE", u"A &#250;ltima antes do desafio: use tudo.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((0,-1),(1,-1),(1,0),(0,0)), P((1,-1),(2,-1),(2,0),(1,0)),
   P((0,-1),(0,-2),(1,-1)), P((2,-1),(2,0),(3,-1))]),

 (u"desafio", u"O DESAFIO DA VOV&#211;", u"Tudo o que voc&#234; aprendeu, de uma vez.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((0,0),(1,0),(1,-1),(0,-1)), P((1,0),(2,0),(2,-1)), P((0,0),(0,-1),(-1,0)),
   P((2,0),(3,0),(4,1),(3,1))]),

 (u"caixa7", u"A CAIXA CHEIA", u"As sete pe&#231;as voltam para a caixa da vov&#243;.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((2,0),(3,0),(3,-1)), P((2,1),(3,1),(2,2)),
   P((0,0),(1,0),(1,-1),(0,-1)), P((1,0),(2,0),(3,-1),(2,-1))]),

 (u"vovo", u"A VOV&#211; MARTA", u"A &#250;ltima: use tudo o que a caixa tem.", [
   P((0,0),(2,0),(0,2)), P((2,0),(2,2),(0,2)), P((0,2),(2,2),(1,3)),
   P((0,0),(1,0),(0,-1)), P((1,0),(2,0),(2,-1)),
   P((0,0),(1,0),(1,1),(0,1)) if False else P((2,2),(3,2),(3,3),(2,3)),
   P((2,0),(3,0),(4,1),(3,1))]),
]

if __name__ == "__main__":
    saida = []
    ok = 0
    for (fid, nome, ensina, pcs) in FIGURAS:
        prob, cx = confere(nome, pcs)
        if prob:
            print(u"!! %s: %s" % (nome, u" | ".join(prob)))
            continue
        ok += 1
        x0, y0 = cx[0], cx[1]
        vagas = []
        for v in pcs:
            vs = move(v["verts"], -x0 + 0.6, -y0 + 0.6)   # margem na mesa
            x, y = para_tela(v["f"], v["ang"], v["esp"], vs)
            vagas.append({"f": v["f"], "x": x, "y": y, "ang": v["ang"], "esp": v["esp"]})
        saida.append({"id": fid, "nome": nome, "ensina": ensina,
                      "pecas": len(pcs), "vagas": vagas})
        print(u"ok %s — %d pe&#231;as, %.1f x %.1f u" % (nome, len(pcs), cx[2] - cx[0], cx[3] - cx[1]))
    io.open("_tangram/figuras.json", "w", encoding="utf-8").write(
        json.dumps(saida, ensure_ascii=False, indent=1))
    print(u"%d de %d figuras conferidas -> _tangram/figuras.json" % (ok, len(FIGURAS)))
