# Syndex · Foto de grupo WhatsApp

Gerador da foto de perfil dos grupos de WhatsApp entre a **Syndex Logística e Gestão Aduaneira** e seus clientes.

O fundo e o logo da Syndex são fixos (a matriz). Só o logo da outra empresa muda.

**Usar o gerador:** https://tomsoares10-dev.github.io/syndex-foto-grupo-whatsapp/

## Como usar

1. Abra o link acima.
2. Envie o logo da empresa: clique para escolher, arraste a imagem ou cole com Ctrl+V.
3. Confira a prévia redonda (é como aparece no WhatsApp).
4. Preencha o nome do cliente e clique em **Salvar PNG 640×640**.

Tudo roda no navegador. O logo enviado não sai do seu computador.

## Regras da matriz

| Item | Regra |
|---|---|
| Arquivo final | PNG quadrado, 640 × 640 px |
| Logo do cliente | Até 500 × 140 px na matriz (1254 × 1254), alinhado à direita em x = 603 px e centralizado em y = 586 px |
| Logo branco ou muito claro | Pintado de azul-marinho Syndex `#1B3F8C` |
| Logo colorido | Mantém as cores originais; fundo branco ou sólido é removido |
| Fixo | Fundo, divisor e logo Syndex com "Diga sim para o sucesso." |

## Arquivos

- `index.html` — o gerador (site do GitHub Pages)
- `matriz/Matriz_Syndex_Base.png` — matriz base, lado esquerdo vazio (1254 × 1254)
- `gerar_parceria.py` — mesma regra em Python, para gerar pelo terminal:

```bash
pip install pillow numpy
python3 gerar_parceria.py matriz/Matriz_Syndex_Base.png logo_cliente.png Syndex_Cliente_WhatsApp.png
# opcional: --cor original | --cor navy
```
