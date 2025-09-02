O Bruxo e as Cobras Encantadas

Um mini-jogo 2D do gênero Roguelike desenvolvido em Python utilizando a biblioteca Pygame Zero. O jogador controla um bruxo em um labirinto gerado proceduralmente, com o objetivo de coletar poções mágicas para desencantar as cobras que o perseguem.

📜 Sobre o Jogo

A história segue um bruxo em uma missão perigosa: coletar todas as poções mágicas espalhadas por um labirinto traiçoeiro. No entanto, o labirinto é guardado por cobras encantadas que o perseguem incansavelmente. A única forma de acalmá-las é usando uma poção. Se o bruxo for pego sem poções, sua aventura chega ao fim.

O objetivo é coletar todas as poções para vencer, usando as que já foram coletadas como defesa para sobreviver.

✨ Funcionalidades

    Geração Procedural de Labirintos: Cada jogo apresenta um novo labirinto, garantindo que nenhuma partida seja igual à outra.

    Menu Principal Completo: Navegue por um menu com opções de Iniciar, Instruções, controle de Som e Sair.

    Múltiplos Estados de Jogo: O jogo gerencia diferentes estados, como menu, instruções, jogando, fim de jogo e vitória.

    Inimigos com IA: As cobras inimigas vagam pelo mapa e perseguem o jogador quando ele se aproxima.

    Sistema de Colisão: O jogador e os inimigos colidem com as paredes do labirinto.

    Mecânica de Jogo Clara: Colete poções para aumentar seu placar e use-as como "vidas" para se defender das cobras.

    Ciclo de Jogo Completo: O jogo possui uma condição de vitória (coletar todas as poções) e uma de derrota (ser pego sem poções), com a opção de jogar novamente ou voltar ao menu.

🛠️ Tecnologias Utilizadas

    Linguagem: Python 3

    Biblioteca Principal: Pygame Zero (pgzero)

    Módulos Padrão: random (para geração procedural), math (para IA dos inimigos)

O projeto foi desenvolvido seguindo o requisito de usar apenas as bibliotecas mencionadas.

🕹️ Como Jogar

    Objetivo: Coletar todas as poções vermelhas do mapa.

    Controles (Jogo):

        Setas do Teclado: Movem o bruxo pelo labirinto.

    Controles (Menu/Outros):

        Mouse: Clicar nos botões.

    Regras:

        Se uma cobra te tocar e você tiver poções, a cobra é desencantada e some, mas você perde uma poção.

        Se uma cobra te tocar e você não tiver poções, o jogo acaba.

🚀 Instalação e Execução

Para rodar este projeto em sua máquina local, siga os passos abaixo.

    Clone o repositório:
    Bash

git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio

Crie e ative um ambiente virtual:
Bash

# Criar o ambiente
python -m venv venv

# Ativar no Windows
.\venv\Scripts\activate

# Ativar no macOS/Linux
source venv/bin/activate

Instale as dependências:
O único requisito é o pgzero.
Bash

pip install pgzero

Execute o jogo:
Bash

    pgzrun roguelike.py

📁 Estrutura de Arquivos

.
├── roguelike.py      # O script principal do jogo
├── README.md         # Este arquivo
├── images/           # Pasta para todos os sprites e imagens
│   ├── hero_*.png
│   ├── enemy_*.png
│   ├── potion_red.png
│   └── ...
└── music/            # Pasta para a música de fundo
    └── snake_sound.mp3

👤 Autor

    [Seu Nome Aqui]

Este projeto foi desenvolvido com o auxílio e orientação da IA Gemini do Google.
