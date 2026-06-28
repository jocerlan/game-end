import pygame
import sys
import os
import random

# ==========================================
# SETUP INICIAL & CONFIGURAÇÕES (Pygame)
# ==========================================
pygame.init()

LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Demo Jogo UNINTER - 2026")

RELOGIO = pygame.time.Clock()
FPS = 60

# CORES (RGB)
COR_FUNDO = (30, 30, 40)
COR_TEXTO = (255, 255, 255)
COR_DESTAQUE = (0, 255, 100)
COR_ALERTA = (255, 50, 50)

# FONTES
FONTE_MENU = pygame.font.SysFont("Arial", 36)
FONTE_INTERFACE = pygame.font.SysFont("Arial", 24)

# ==========================================
# CARREGAMENTO DOS ASSETS (pasta 'imagens' ao lado do exe/.py)
# ==========================================
# Função utilitária para localizar recursos tanto em execução normal quanto
# quando o aplicativo está empacotado (PyInstaller).
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

ASSET_DIR = resource_path('imagens')

try:
    imagem_jogador = pygame.image.load(os.path.join(ASSET_DIR, "jogador.png")).convert_alpha()
    imagem_obstaculo = pygame.image.load(os.path.join(ASSET_DIR, "obstaculo.png")).convert_alpha()
    imagem_moeda = pygame.image.load(os.path.join(ASSET_DIR, "moeda.png")).convert_alpha()

    img_jogador = pygame.transform.scale(imagem_jogador, (50, 50))
    img_obstaculo = pygame.transform.scale(imagem_obstaculo, (40, 40))
    img_moeda = pygame.transform.scale(imagem_moeda, (30, 30))
except Exception as e:
    print(f"Erro ao carregar assets: {e}")
    print(f"Verifique se a pasta 'imagens' existe ao lado do executável e contém: jogador.png, obstaculo.png e moeda.png\nCaminho esperado: {ASSET_DIR}")
    pygame.quit()
    sys.exit()

# ==========================================
# FUNÇÕES DE TELAS DE ESTADO (Menu, Win, Lose)
# ==========================================
def desenhar_texto(texto, fonte, cor, x, y):
    superficie = fonte.render(texto, True, cor)
    retangulo = superficie.get_rect(center=(x, y))
    tela.blit(superficie, retangulo)

def tela_menu():
    while True:
        tela.fill(COR_FUNDO)
        desenhar_texto("COLETOR DE MOEDAS - DEMO", FONTE_MENU, COR_DESTAQUE, LARGURA_TELA//2, 150)
        
        # Exigência do edital: Mostrar explicitamente os comandos no menu
        desenhar_texto("[ COMANDOS DE CONTROLE ]", FONTE_INTERFACE, COR_TEXTO, LARGURA_TELA//2, 260)
        desenhar_texto("Setas direcionais (← ↑ ↓ →) - Movimentar Jogador", FONTE_INTERFACE, COR_TEXTO, LARGURA_TELA//2, 300)
        
        desenhar_texto("Objetivo: Colete 10 moedas desviando dos obstáculos!", FONTE_INTERFACE, COR_TEXTO, LARGURA_TELA//2, 380)
        desenhar_texto("Pressione ESPAÇO para Iniciar ou ESC para Sair", FONTE_INTERFACE, COR_DESTAQUE, LARGURA_TELA//2, 480)
        
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return "JOGANDO"
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def tela_resultado(vitoria):
    while True:
        tela.fill(COR_FUNDO)
        if vitoria:
            desenhar_texto("VITÓRIA!", FONTE_MENU, COR_DESTAQUE, LARGURA_TELA//2, 200)
            desenhar_texto("Você conseguiu coletar todas as moedas!", FONTE_INTERFACE, COR_TEXTO, LARGURA_TELA//2, 280)
        else:
            desenhar_texto("GAME OVER!", FONTE_MENU, COR_ALERTA, LARGURA_TELA//2, 200)
            desenhar_texto("Você colidiu com um obstáculo do cenário.", FONTE_INTERFACE, COR_TEXTO, LARGURA_TELA//2, 280)
            
        desenhar_texto("Pressione ESPAÇO para Voltar ao Menu ou ESC para Sair", FONTE_INTERFACE, COR_TEXTO, LARGURA_TELA//2, 400)
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return "MENU"
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# ==========================================
# LOOP PRINCIPAL DO JOGO (Gameplay)
# ==========================================
def loop_jogo():
    # Inicialização das variáveis do jogador (Posição centralizada embaixo)
    jogador_x = LARGURA_TELA // 2
    jogador_y = ALTURA_TELA - 80
    velocidade_jogador = 6

    # Pontuação e Desafio
    moedas_coletadas = 0
    META_MOEDAS = 10 # Condição de vitória

    # Criando retângulos de colisão inicial para a moeda
    moeda_rect = img_moeda.get_rect()
    moeda_rect.x = random.randint(50, LARGURA_TELA - 50)
    moeda_rect.y = random.randint(50, ALTURA_TELA - 150)

    # Lista de obstáculos que caem (Desafios)
    obstaculos = []
    for _ in range(4):
        obs_rect = img_obstaculo.get_rect()
        obs_rect.x = random.randint(0, LARGURA_TELA - 40)
        obs_rect.y = random.randint(-400, -50)
        velocidade_obs = random.randint(3, 6)
        obstaculos.append({"rect": obs_rect, "vel": velocidade_obs})

    jogando = True
    while jogando:
        RELOGIO.tick(FPS)
        tela.fill(COR_FUNDO)

        # 1. Tratamento de Eventos de Fechamento
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 2. Captura de Entrada dos Controles (Teclado)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jogador_x > 0:
            jogador_x -= velocidade_jogador
        if teclas[pygame.K_RIGHT] and jogador_x < LARGURA_TELA - 50:
            jogador_x += velocidade_jogador
        if teclas[pygame.K_UP] and jogador_y > 0:
            jogador_y -= velocidade_jogador
        if teclas[pygame.K_DOWN] and jogador_y < ALTURA_TELA - 50:
            jogador_y += velocidade_jogador

        # Atualiza o Hitbox do jogador baseado na posição atual
        jogador_rect = pygame.Rect(jogador_x, jogador_y, 50, 50)

        # 3. Lógica dos Obstáculos (Desafios em movimento)
        for obs in list(obstaculos):
            obs["rect"].y += obs["vel"]
            
            # Se o obstáculo passar do fim da tela, reinicia no topo
            if obs["rect"].y > ALTURA_TELA:
                obs["rect"].x = random.randint(0, LARGURA_TELA - 40)
                obs["rect"].y = random.randint(-150, -40)
                obs["vel"] = random.randint(3, 7)

            # [CONDIÇÃO DE DERROTA]: Colisão com obstáculo
            if jogador_rect.colliderect(obs["rect"]):
                return "DERROTA"

            # Renderização do obstáculo
            tela.blit(img_obstaculo, obs["rect"])

        # 4. Lógica de Coleta da Moeda
        if jogador_rect.colliderect(moeda_rect):
            moedas_coletadas += 1
            # Reposiciona a moeda de forma aleatória pelo mapa
            moeda_rect.x = random.randint(50, LARGURA_TELA - 50)
            moeda_rect.y = random.randint(50, ALTURA_TELA - 150)

        # [CONDIÇÃO DE VITÓRIA]: Alcançar a pontuação meta
        if moedas_coletadas >= META_MOEDAS:
            return "VITORIA"

        # 5. Renderização dos Elementos Gráficos e HUD
        tela.blit(img_moeda, moeda_rect)
        tela.blit(img_jogador, (jogador_x, jogador_y))
        
        # Interface de Usuário na parte superior
        desenhar_texto(f"Moedas: {moedas_coletadas} / {META_MOEDAS}", FONTE_INTERFACE, COR_TEXTO, 100, 30)
        
        pygame.display.flip()

# ==========================================
# MÁQUINA DE ESTADOS DO JOGO
# ==========================================
def main():
    estado_atual = "MENU"
    while True:
        if estado_atual == "MENU":
            estado_atual = tela_menu()
        elif estado_atual == "JOGANDO":
            resultado = loop_jogo()
            if resultado == "VITORIA":
                estado_atual = tela_resultado(vitoria=True)
            elif resultado == "DERROTA":
                estado_atual = tela_resultado(vitoria=False)
        elif estado_atual == "MENU_RETORNO":
            estado_atual = "MENU"

if __name__ == "__main__":
    main()