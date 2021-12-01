import pygame
import random
import os

# Inicializando o Pygame e criando a janela
pygame.init()

pygame.display.set_caption("Street Row")  # Define um nome para a janela
clock = pygame.time.Clock() # Define um "relógio" para o jogo

altura = 500 
largura = 900

display = pygame.display.set_mode([largura, altura])  # Define o tamanho da janela
gameLoop = True # Variável responsável por permitir o que o jogo se repita

# Através da biblioteca "os" nós definimos os diretórios onde estão armazenados cada imagem e som utilizados dentro do jogo
diretorioPrincipal = os.path.dirname(__file__)
diretorioImagens = os.path.join(diretorioPrincipal, "imagens")
diretorioJogador = os.path.join(diretorioPrincipal, "jogador")
diretorioSons = os.path.join(diretorioPrincipal, "sons")

# Variáveis
i = 0
timer = 0
pontuação = 0
colidiu = False
exibePontuação = 0
velocidade = 0
height = 60

# Define o cenário do jogo
grupoCenário = pygame.sprite.Group() # Cria um grupo onde estará inserido o background principal
background = pygame.sprite.Sprite(grupoCenário) # Adiciona esse background no grupo

background.image = pygame.image.load(os.path.join(diretorioImagens, "Background.png")) # Carrega a imagem do background através do diretório de imagens
rua = pygame.image.load(os.path.join(diretorioImagens, "Rua.png")) # Carrega a imagem da rua através do diretório de imagens

background.image = pygame.transform.scale(background.image, [largura, altura]) # Redimensiona o background para a altura 500 e a largura 900
rua = pygame.transform.scale(rua, [largura, altura])

background.rect = pygame.Rect(0, 0, largura, altura) # Define a posição do centro do background (centro = ponto localizado no canto superior esquerdo da imagem)

# Musicas e sons
pygame.mixer.music.load(os.path.join(diretorioSons, "MusicaEmGame.mp3")) # Carrega a música que será tocada durante a execução do jogo
pygame.mixer.music.play(30) # Executa a música 30 vezes
gameOver = pygame.mixer.Sound(os.path.join(diretorioSons, "GAMEOVER.wav")) # Carrega o som que será tocado quando o jogador colidir com o obstáculo

# Classe responsável pela criação e pela lógica do Jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Lista com cada tipo de animação
        self.animaçãoAndar = []
        self.animaçãoCorrerDireita = []
        self.animaçãoCorrerEsquerda = []
        self.animaçãoPular = []
        self.animaçãoColisão = []

        # Criamos a spriteSheet de cada animação
        jogadorAndarSpriteSheet = pygame.image.load(os.path.join(diretorioJogador, "andar.png")).convert_alpha()
        jogadorCDSpriteSheet = pygame.image.load(os.path.join(diretorioJogador, "correrDireita.png")).convert_alpha()
        jogadorCESpriteSheet = pygame.image.load(os.path.join(diretorioJogador, "correrEsquerda.png")).convert_alpha()
        jogadorPularSpriteSheet = pygame.image.load(os.path.join(diretorioJogador, "pular.png")).convert_alpha()
        jogadorColisãoSpriteSheet = pygame.image.load(os.path.join(diretorioJogador, "colisão.png")).convert_alpha()

        # Preenchemos a lista de cada animação com o recorte de sua respectiva spriteSheet
        for i in range(0, 8):
            andar = jogadorAndarSpriteSheet.subsurface((i * 71, 0), (71, 67))
            self.animaçãoAndar.append(andar)
        for i in range(0, 8):
            andar = jogadorAndarSpriteSheet.subsurface((i * 71, 67), (71, 67))
            self.animaçãoAndar.append(andar)

        for i in range(0,8):
            cd = jogadorCDSpriteSheet.subsurface((i * 71, 0), (71, 67))
            ce = jogadorCESpriteSheet.subsurface((i * 71, 0), (71, 67))
            self.animaçãoCorrerDireita.append(cd)
            self.animaçãoCorrerEsquerda.append(ce)

        for i in range(0, 4):
            pular = jogadorPularSpriteSheet.subsurface((i * 71, 0), (71, 67))
            self.animaçãoPular.append(pular)

        colisão = jogadorColisãoSpriteSheet.subsurface((0, 0), (71, 67))
        self.animaçãoColisão.append(colisão)

        self.index = 0
        self.step = 0
        self.step2 = 0
        self.step3 = 0
        self.image = self.animaçãoAndar[self.index]
        self.rect = self.image.get_rect() 
        self.rect.center = [23, 368] # Define o centro da sprite do jogador, ou seja, a posição onde o jogador será posicionado no início do jogo
        
        self.moverDireita = False
        self.moverEsquerda = False
        self.colidir = False

        self.pular = False
        self.isJump = False
        self.jumpCount = 8

    def update(self):

        if self.step >= 8:
            self.step = 0

        if self.step2 >= 16:
            self.step2 = 0

        if self.step3 >= 4:
            self.step3 = 0

        # Laços responsáveis por atualizar a imagem do personagem de acordo com a sua ação (Animação)
        if self.moverEsquerda:
            self.image = self.animaçãoCorrerEsquerda[int(self.step)] # Carrega as imagens da animação
            self.step += 0.25 # Step responsável por atualizar as imagens da lista de animação
            self.mask = pygame.mask.from_surface(self.image) # Cria a máscara responsável pela CPP com os obstáculos para cada pixel referente a cada imagem da animação

        elif self.moverDireita:
            self.image = self.animaçãoCorrerDireita[int(self.step)]
            self.step += 0.25
            self.mask = pygame.mask.from_surface(self.image)

        elif self.pular:
            self.image = self.animaçãoPular[int(self.step3)]
            self.step3 += 0.25
            self.mask = pygame.mask.from_surface(self.image)

        else:
            self.image = self.animaçãoAndar[int(self.step2)]
            self.step2 += 0.25
            self.mask = pygame.mask.from_surface(self.image)

        key = pygame.key.get_pressed()

        # DIREITA
        if key[pygame.K_d]:
            self.rect.x +=  1 # Move o jogador para 1 pixel por frame para a direita
            self.moverEsquerda = False
            self.moverDireita = False
            if self.rect.x >= 850: #Limita até onde o jogador pode ir para a direita (barreira da direita)
                self.rect.x = 850
            if key[pygame.K_LSHIFT]:  # Correr para direita
                self.rect.x += 3
                self.moverEsquerda = False
                self.moverDireita = True

        # ESQUERDA
        if key[pygame.K_a]:
            if self.rect.x <= -10: # Limita até onde o jogador pode ir para a esquerda (barreira da esquerda)
                self.rect.x = -10
            self.rect.x -= 1 # Move o jogador para 1 pixel por frame para a esquerda
            self.moverEsquerda = False
            self.moverDireita = False
            if key[pygame.K_LSHIFT]:  # CORRER
                self.rect.x -= 3
                self.moverEsquerda = True
                self.moverDireita = False

        # Função de stop da corrida caso o jogador tenha soltado a tecla referente a corrida (lshit)
        if key[pygame.K_LSHIFT] == False:
            self.moverEsquerda = False
            self.moverDireita = False

        # PARA CIMA + PARA BAIXO + PULO
        if not (self.isJump):
            # PARA CIMA
            if key[pygame.K_w]:
                self.rect.y -= 1 
                if self.rect.y <= 328: # Limita até onde o jogador pode ir para a cima (barreira de cima)
                    self.rect.y = 328
                if key[pygame.K_LSHIFT]:  # CORRER
                    self.rect.y -= 1
                
            # PARA BAIXO
            if key[pygame.K_s]:
                self.rect.y += 1  
                if self.rect.bottom >= 495: #Limita até onde o jogador pode ir para baixo (barreira debaixo)
                    self.rect.bottom = 495
                if key[pygame.K_LSHIFT]:  # CORRER
                    self.rect.y += 1

            # PULO
            if key[pygame.K_SPACE]:
                self.pular = False
                self.pular = False
                self.isJump = True
                self.moverEsquerda = False
                self.moverDireita = False

        elif self.jumpCount >= -8:
            yAtual = self.rect.y
            self.pular = True
            self.rect.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
            self.rect.y += 0.99
            self.jumpCount -= 1

        else:
            self.jumpCount = 8
            self.isJump = False
            self.pular = False
            self.moverEsquerda = False
            self.moverDireita = False
            if self.rect.y <= 328:
                self.rect.y = 328

#Classe responsável pela criação e pela lógica dos Obstáculos
class Obstáculo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(diretorioImagens, "Obstaculo.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (900, random.choice([390, 455])) # Define a posição em que o obstáculo irá surgir, randomizando o 'y' em 2 valores
        self.mask = pygame.mask.from_surface(self.image) # Cria a máscara responsável pela CPP com o jogador

    def update(self):
        if self.rect.topright[0] < 0: # Caso o canto superior direito do obstáculo passe pelo lado esquerdo da tela, esse obstáculo será destruido
            self.kill()
        self.rect.x -= 8 + velocidade # Move os obstáculos a uma velocidade de 8 pixels por frame para a esquerda (A velocidade aumenta conforme pontuação do jogador)

grupoSprites = pygame.sprite.Group() # Cria um grupo responsável por armazenar todas as sprites do jogo (Jogador e Obstáculos)
grupoObstáculos = pygame.sprite.Group() # Cria um grupo responsável por armazenar todos os obstáculos separadamente (será utilizado para verificar colisões)

jogador = Jogador() # Cria uma instância do objeto jogador
grupoSprites.add(jogador) # Adiciona este objeto no grupo de sprites

# Função responsável por criar a pontuação e a mensagem de 'GAME OVER' na tela
def defineMensagem(mensagem, tamanho, cor):
    fonte = pygame.font.Font(os.path.join(diretorioPrincipal, "fonte/S&S Nickson One.otf"), tamanho) # Carrega a fonte que será utiliza para a escrita da mensagem
    msg = f'{mensagem}' # Carrega a mensagem a ser exibida
    msgFormatada = fonte.render(msg, True, cor) # Formata a mensagem conforme as especificações da fonte
    return msgFormatada

# Instruções do teclado para o jogado
exibeInstrunçãoAndar = defineMensagem("W, A, S, D para andar", 20, (230, 237, 24))
exibeInstrunçãoCorrerPular = defineMensagem("LSHIFT para correr - ESPAÇO para pular", 20, (230, 237, 24))

# Função responsável por reiniciar o jogo quando o jogador colidi com algum obstáculo
def restart():
    global pontuação, velocidade, colidiu

    pygame.mixer.music.play(30)
    gameOver.stop()
    pontuação = 0
    velocidade = 0
    colidiu = False
    jogador.rect.center = [23, 368]
    for novaCaixa in grupoObstáculos: # Destrói todas as caixas (obstáculos) presentes na tela
        novaCaixa.kill()
    
# Função responsável por desenhar o cenário e exibir as mensagens na tela
def draw():
    if colidiu == False:
        display.fill([211, 13, 255])  # Define a cor de fundo da janela
        grupoCenário.draw(display) # Exibe o cenário

        display.blit(exibePontuação, (650, 0)) # Exibe a pontuação do jogador
        display.blit(exibeInstrunçãoAndar, (0, 0))
        display.blit(exibeInstrunçãoCorrerPular, (0, 20))

        # Desenha rua para efeito parallax
        display.blit(rua, (i, 0))
        display.blit(rua, (largura + i, 0))

    else:
        # Exibe a mensagem de 'GAME OVER' junto com a mensagem de restart
        display.blit(exibeGameOverFundo, (326, 110))
        display.blit(exibeGameOver, (330, 110))
        display.blit(exibeRestartFundo, (316, 170))
        display.blit(exibeRestart, (320, 170))

while gameLoop:

    key = pygame.key.get_pressed() # Responsável por verificar teclas que serão pressionadas

    for event in pygame.event.get():  # Fila de eventos
        if event.type == pygame.QUIT:  # Caso o usuário clique para fechar a janela
            gameLoop = False

        if key[pygame.K_r] and colidiu == True: # Caso o jogador aperte a tecla 'r'
            restart()

    # Loop da rua (EFEITO DE PARALLAX)
    if i == -largura:
        display.blit(rua, (largura + 1, 0))
        i = 0
    i -= 1

    # Condição responsável por incrementar o timer encarregado de gerar os obstáculos na tela
    if colidiu == False:
        timer += 1 + (velocidade // 10)
        if timer > 40:
            timer = 0
            if random.random() < 1: # Define uma chance de quase 100% para que um novo obstáculo seja gerado a cada 666 ms (2/3 de minuto)
                novaCaixa = Obstáculo() # Instância uma nova caixa (obstáculo)
                grupoSprites.add(novaCaixa)
                grupoObstáculos.add(novaCaixa)

    # Lista responsável por verificar se houve uma colisão pixel perfect (CPP) do jogador com os obstáculos 
    colisão = pygame.sprite.spritecollide(jogador, grupoObstáculos, False, pygame.sprite.collide_mask)

    # Caso ocorra uma colisão a música principal sera pausada, tocará o som de 'GAME OVER' e atualizará a variável colidiu para verdadeira
    if colisão and colidiu == False:
        pygame.mixer.music.pause()
        gameOver.play()
        colidiu = True

    # Definirá as mensagens que serão exibidas na tela quando o jogador colidir com um obstáculo e atualizará a tela
    if colidiu == True:
        exibeGameOver = defineMensagem("GAME OVER", 70, (255, 3, 3))
        exibeGameOverFundo = defineMensagem("GAME OVER", 71, (0, 0, 0))
        exibeRestart = defineMensagem("Pressione 'r' para reiniciar", 30, (230, 237, 24))
        exibeRestartFundo = defineMensagem("Pressione 'r' para reiniciar", 31, (0, 0, 0))
        pygame.display.update()
        pass
    # Caso o jogador não colida com nada, a pontuação será incrementada e o jogo continuará sendo executado
    else:
        pontuação += 0.5
        exibePontuação = defineMensagem("Pontuação: " + str(int(pontuação)), 40, (230, 237, 24))
        grupoSprites.update()
        pygame.display.update() # Atualiza o display da tela, para que a janela fique ativa

    # A cada 200 pontos conquistados pelo jogador, a velocidade aumentará em 1 pixel por frame
    if pontuação % 200 == 0:
        velocidade += 1

    
    draw() # Chama a função responsável por desenhar o cenário e as mensagens na tela
    grupoSprites.draw(display) # Chama a função responsável por desenhar os sprites na tela (jogador e obstáculos)

    clock.tick(60)  # Limita o fps (frames por segundo) para 60

pygame.quit()
