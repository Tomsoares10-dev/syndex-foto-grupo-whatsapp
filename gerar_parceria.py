"""Matriz Syndex x Parceiro — foto de grupo WhatsApp.
Uso: python3 gerar_parceria.py <matriz_base.png> <logo_parceiro> <saida.png>
- matriz_base.png: fundo + divisor + logo Syndex, lado esquerdo vazio (1254x1254)
- O logo do parceiro entra exatamente como no arquivo (mesmas cores e mesmo fundo).
  Só a margem vazia em volta é cortada, com uma folga pequena quando o arquivo tem fundo.
- O logo é centralizado automaticamente pelo tamanho: centro em x = 384 (espelho do logo Syndex
  em relação ao divisor); se for largo demais, recua até a borda direita ficar em x = 603
- Saída final 640x640 (tamanho da foto de perfil do WhatsApp)
"""
import sys
import numpy as np
from PIL import Image

BOX_LEFT = 103                # limite esquerdo da área do logo
BOX_RIGHT = 603               # limite direito (60 px antes do divisor)
CENTER_X = 384                # eixo: espelho do centro do logo Syndex em relação ao divisor (x = 664)
BOX_MAX_W = 500               # largura máxima (mantém margem segura no recorte redondo)
BOX_MAX_H = 140               # altura máxima (igual ao bloco do logo Syndex)
CENTER_Y = 586                # centro vertical do logo Syndex
OUT_SIZE = 640


def carregar_logo(path):
    """Abre o logo sem mexer em cor nem fundo; só corta a margem vazia em volta."""
    im = Image.open(path).convert('RGBA')
    a = np.array(im).astype(float)
    h, w = a.shape[:2]
    alpha = a[..., 3]
    if (alpha < 250).mean() > 0.02:
        # PNG transparente: corta onde há pixel visível, sem folga
        mask = alpha > 8
        folga_ok = False
    else:
        # arquivo com fundo: estima a cor do fundo pelos cantos só para achar a margem vazia
        k = max(2, min(h, w) // 20)
        cantos = np.concatenate([a[:k, :k, :3].reshape(-1, 3), a[:k, -k:, :3].reshape(-1, 3),
                                 a[-k:, :k, :3].reshape(-1, 3), a[-k:, -k:, :3].reshape(-1, 3)])
        bg = np.median(cantos, axis=0)
        mask = ((a[..., :3] - bg) ** 2).sum(-1) > 40 ** 2
        folga_ok = True
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return im
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    if folga_ok:
        f = round(0.045 * max(x1 - x0 + 1, y1 - y0 + 1))
        x0, y0 = max(0, x0 - f), max(0, y0 - f)
        x1, y1 = min(w - 1, x1 + f), min(h - 1, y1 + f)
    return im.crop((int(x0), int(y0), int(x1) + 1, int(y1) + 1))


def main():
    base_p, logo_p, out_p = sys.argv[1:4]
    base = Image.open(base_p).convert('RGBA')
    logo = carregar_logo(logo_p)
    s = min(BOX_MAX_W / logo.width, BOX_MAX_H / logo.height)
    logo = logo.resize((max(1, round(logo.width * s)), max(1, round(logo.height * s))), Image.LANCZOS)
    eixo = max(BOX_LEFT + logo.width / 2, min(CENTER_X, BOX_RIGHT - logo.width / 2))
    pos = (round(eixo - logo.width / 2), CENTER_Y - logo.height // 2)
    base.alpha_composite(logo, pos)
    final = base.convert('RGB').resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS)
    final.save(out_p, optimize=True)
    print(f'ok  logo={logo.size} pos={pos}')


if __name__ == '__main__':
    main()
