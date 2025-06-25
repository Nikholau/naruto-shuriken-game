# 🌀 Naruto Shuriken Game

Um mini jogo estilo **arcade**, desenvolvido em **Python** com a biblioteca [pygame](https://www.pygame.org), onde você controla o personagem **Naruto** e deve desviar de shurikens que caem do céu. Com dificuldade progressiva e placar em tempo real, o desafio é **sobreviver o máximo possível**!

---

## 🎮 Como Jogar

- Use as **setas ← →** para mover o Naruto lateralmente.
- Pressione **ESPAÇO** para lançar um *Rasengan*.
- **Desvie das shurikens** que caem do topo da tela.
- Se uma shuriken atingir o Naruto, é **fim de jogo**.
- Pressione **P** para pausar o jogo.
- Pressione **ESC** para sair a qualquer momento.
- Pressione **R** para reiniciar após derrota ou vitória.

---

## 💡 Recursos do Jogo

- ✅ Movimentação fluida com animações do Naruto.
- ✅ Lançamento de *Rasengan* para destruir shurikens.
- ✅ Dificuldade crescente com mudança de cenário.
- ✅ Sistema de pontuação em tempo real.
- ✅ Tela de vitória ao atingir pontuação mínima.

---

## 📁 Estrutura do Projeto

naruto-shuriken-game/
├── game/
│ ├── background.py
│ ├── core.py
│ ├── enemy.py
│ ├── objects.py
│ ├── player.py
│ └── settings.py
├── imagens/
│ ├── bg-1.png
│ ├── bg-2.png
│ ├── bg-3.png
│ ├── Nstanding.png
│ ├── NR1.png, NR2.png, ...
│ ├── NL1.png, NL2.png, ...
│ ├── Nd.png
│ ├── shuriken.png
│ ├── movement-shuriken.png
│ └── rasengan.png
├── main.py
└── README.md


---

## 🛠 Requisitos

- Python **3.8** ou superior
- pygame  
  Instale com:

```bash
pip install pygame

▶️ Como Executar
Clone o repositório:

bash
Copy
Edit
git clone https://github.com/Nikholau/naruto-shuriken-game.git
cd naruto-shuriken-game
Execute o jogo:

bash
Copy
Edit
python main.py

📷 Captura de Tela
(Adicione aqui uma imagem do jogo rodando, como preview da interface)

🧠 Créditos
Desenvolvido por Nikholau como projeto de aprendizado em Python e desenvolvimento de jogos com Pygame.

📄 Licença
Este projeto está licenciado sob a licença MIT. Sinta-se livre para modificar, usar e compartilhar!