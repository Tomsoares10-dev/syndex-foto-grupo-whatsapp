"""Matriz Syndex x Parceiro — foto de grupo WhatsApp.
Uso: python3 gerar_parceria.py <matriz_base.png> <logo_parceiro> <saida.png> [--cor auto|original|navy]
- matriz_base.png: fundo + divisor + logo Syndex, lado esquerdo vazio (1254x1254)
- O logo do parceiro entra alinhado à direita, encostado no divisor (mesmo respiro do original)
- Saída final 640x640 (tamanho da foto de perfil do WhatsApp)
"""
import sys
import numpy as np
from PIL import Image

NAVY = (27, 63, 140)          # azul-marinho da Syndex
BOX_RIGHT = 603               # borda direita do logo (60 px antes do divisor)
BOX_MAX_W = 500               # largura máxima (mantém margem segura no recorte redondo)
BOX_MAX_H = 140               # altura máxima (igual ao bloco do logo Syndex)
CENTER_Y = 586                # centro vertical do logo Syndex
OUT_SIZE = 640


def carregar_logo(path):
    im = Image.open(path).convert('RGBA')
    a = np.array(im).astype(float)
    alpha = a[..., 3]
    tem_transparencia = (alpha < 250).mean() > 0.02
    if not tem_transparencia:
        # fundo sólido: estima a cor pelos cantos e remove com borda suave
        h, w = alpha.shape
        k = max(2, min(h, w) // 20)
        cantos = np.concatenate([a[:k, :k, :3].reshape(-1, 3), a[:k, -k:, :3].reshape(-1, 3),
                                 a[-k:, :k, :3].reshape(-1, 3), a[-k:, -k:, :3].reshape(-1, 3)])
        bg = np.median(cantos, axis=0)
        dist = np.sqrt(((a[..., :3] - bg) ** 2).sum(-1))
        a[..., 3] = np.clip((dist - 18) / (60 - 18), 0, 1) * 255
    im = Image.fromarray(a.astype(np.uint8), 'RGBA')
    bbox = im.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
    return im.crop(bbox)


def aplicar_cor(logo, modo):
    a = np.array(logo).astype(float)
    vis = a[..., 3] > 128
    lum = a[..., :3][vis].mean(axis=1).mean() if vis.any() else 0
    if modo == 'navy' or (modo == 'auto' and lum > 215):
        # logo claro/branco sumiria no fundo claro -> pinta de azul-marinho Syndex
        out = np.zeros_like(a)
        out[..., :3] = NAVY
        out[..., 3] = a[..., 3]
        return Image.fromarray(out.astype(np.uint8), 'RGBA'), True
    return logo, False


def main():
    base_p, logo_p, out_p = sys.argv[1:4]
    modo = 'auto'
    if '--cor' in sys.argv:
        modo = sys.argv[sys.argv.index('--cor') + 1]
    base = Image.open(base_p).convert('RGBA')
    logo, recolorido = aplicar_cor(carregar_logo(logo_p), modo)
    s = min(BOX_MAX_W / logo.width, BOX_MAX_H / logo.height)
    logo = logo.resize((round(logo.width * s), round(logo.height * s)), Image.LANCZOS)
    pos = (BOX_RIGHT - logo.width, CENTER_Y - logo.height // 2)
    base.alpha_composite(logo, pos)
    final = base.convert('RGB').resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS)
    final.save(out_p, optimize=True)
    print(f'ok  logo={logo.size} pos={pos} recolorido={recolorido}')


if __name__ == '__main__':
    main()
