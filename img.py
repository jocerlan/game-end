import os
from PIL import Image, ImageDraw

# Garante que a pasta 'imagens' exista no diretório atual
os.makedirs("imagens", exist_ok=True)

print("Gerando assets do jogo...")

# 1. CRIANDO O JOGADOR (Boneco estilo Pixel Art - Azul)
# Tamanho: 50x50 pixels
img_jogador = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
draw = ImageDraw.Draw(img_jogador)
# Corpo base (Azul)
draw.rounded_rectangle([5, 5, 45, 45], radius=6, fill=(50, 150, 255), outline=(20, 70, 150), width=2)
# Olhos (Brancos com pupilas pretas)
draw.rectangle([12, 15, 20, 25], fill=(255, 255, 255))
draw.rectangle([16, 19, 20, 25], fill=(0, 0, 0))
draw.rectangle([30, 15, 38, 25], fill=(255, 255, 255))
draw.rectangle([34, 19, 38, 25], fill=(0, 0, 0))
# Detalhe do fone/capacete nas laterais
draw.rectangle([0, 20, 6, 32], fill=(255, 100, 0))
draw.rectangle([44, 20, 50, 32], fill=(255, 100, 0))
img_jogador.save("imagens/jogador.png")
print("- imagens/jogador.png gerado com sucesso!")

# 2. CRIANDO O OBSTÁCULO (Espinho / Meteoro perigoso - Vermelho)
# Tamanho: 40x40 pixels
img_obstaculo = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
draw = ImageDraw.Draw(img_obstaculo)
# Desenha um triângulo/espinho pontiagudo
espinho_pontos = [(20, 2), (2, 38), (38, 38)]
draw.polygon(espinho_pontos, fill=(255, 50, 50), outline=(150, 10, 10), width=2)
# Detalhe de brilho/sombra interno para dar profundidade
draw.polygon([(20, 6), (8, 35), (20, 35)], fill=(255, 120, 120))
img_obstaculo.save("imagens/obstaculo.png")
print("- imagens/obstaculo.png gerado com sucesso!")

# 3. CRIANDO A MOEDA (Moeda clássica de RPG - Dourada)
# Tamanho: 30x30 pixels
img_moeda = Image.new("RGBA", (30, 30), (0, 0, 0, 0))
draw = ImageDraw.Draw(img_moeda)
# Círculo externo dourado
draw.ellipse([2, 2, 28, 28], fill=(255, 215, 0), outline=(180, 140, 10), width=2)
# Círculo interno para relevo
draw.ellipse([7, 7, 23, 23], fill=(255, 235, 100), outline=(210, 160, 20), width=1)
# Detalhe do centro (brilho)
draw.rectangle([13, 11, 17, 19], fill=(255, 255, 255))
img_moeda.save("imagens/moeda.png")
print("- imagens/moeda.png gerado com sucesso!")

print("\nTodos os arquivos foram criados fisicamente na pasta 'imagens/'!")