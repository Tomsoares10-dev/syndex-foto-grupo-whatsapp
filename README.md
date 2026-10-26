# Syndex · Foto de grupo WhatsApp

Gerador da foto de perfil dos grupos de WhatsApp entre a **Syndex Logística e Gestão Aduaneira** e seus clientes.

O fundo e o logo da Syndex são fixos (a matriz). Só o logo da outra empresa muda.

**Usar o gerador:** https://tomsoares10-dev.github.io/syndex-foto-grupo-whatsapp/

## Como usar

1. Abra o link acima e escolha o tipo de foto: **Uma empresa por foto** ou **Duas empresas no mesmo grupo**.
2. Envie um ou vários logos: clique para escolher, arraste as imagens ou cole com Ctrl+V (até 30 por vez).
3. Cada logo vira uma foto. Confira a prévia redonda de cada uma (é como aparece no WhatsApp).
4. Ajuste o nome do cliente, se precisar.
5. Clique em **Salvar PNG** em cada foto, ou em **Baixar todas** para receber todas num arquivo .zip.

Tudo roda no navegador. O logo enviado não sai do seu computador.

## Regras da matriz

| Item | Regra |
|---|---|
| Arquivo final | PNG quadrado, 640 × 640 px (um por logo) |
| Logo do cliente | Até 500 × 140 px na matriz (1254 × 1254), alinhado à direita em x = 603 px e centralizado em y = 586 px |
| Duas empresas no mesmo grupo | Logos empilhados à esquerda, cada um até 480 × 104 px, 40 px entre eles, alinhados à direita em x = 603 px e centralizados em y = 586 px |
| Logo do cliente | Entra exatamente como no arquivo: mesmas cores e o mesmo fundo. Só a margem vazia em volta é cortada. Para o logo aparecer sem fundo, envie um PNG transparente |
| Fixo | Fundo, divisor e logo Syndex com "Diga sim para o sucesso." |

## Arquivos

- `index.html` — o gerador (site do GitHub Pages)
- `matriz/Matriz_Syndex_Base.png` — matriz base, lado esquerdo vazio (1254 × 1254)
- `gerar_parceria.py` — mesma regra em Python, para gerar pelo terminal:

```bash
pip install pillow numpy
python3 gerar_parceria.py matriz/Matriz_Syndex_Base.png logo_cliente.png Syndex_Cliente_WhatsApp.png
```
