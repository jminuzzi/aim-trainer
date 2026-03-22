# 🎯 Treinador de Mira v2.0

Um treinador de mira em **Python + Pygame**, inspirado em jogos FPS competitivos como CS2, focado em:

- precisão
- reflexo
- consistência
- treino sob pressão

---

## 📌 Visão geral

O projeto foi desenvolvido para simular um ambiente simples de aquecimento e treino de headshot, com bots em movimento, níveis de dificuldade e um modo contra o tempo.

Ele funciona como uma ferramenta standalone, ideal para:

- aquecer antes de jogar
- praticar flicks e tracking
- treinar constância de headshots
- medir desempenho em sessões curtas

---

## 🚀 Funcionalidades

### 🎚️ Sistema de dificuldade
O jogo possui 5 níveis de dificuldade:

| Nível | Cabeça | Corpo | Cor | Uso recomendado |
|---|---:|---:|---|---|
| Easy | 35 px | 80x160 | Verde | Iniciantes |
| Normal | 25 px | 60x120 | Azul | Padrão |
| Hard | 18 px | 45x90 | Laranja | Avançado |
| Insane | 12 px | 35x70 | Roxo | Alto nível |
| Mixed | Aleatório | Aleatório | Variada | Adaptação |

Cada dificuldade altera:

- tamanho dos alvos
- velocidade de movimentação
- comportamento visual
- nível de desafio

---

### ⏱️ Modo Time Attack
Modo de 60 segundos para fazer o maior número possível de headshots.

Inclui:

- contador regressivo
- highscore na sessão atual
- tela final de resultado
- comparação com recorde
- timer com mudança de cor

Cores do timer:

- 🟢 Verde: tempo confortável
- 🟡 Amarelo: atenção
- 🔴 Vermelho: segundos finais

---

### 🤖 Padrões de movimento dos bots
Os bots podem se mover de formas diferentes:

- **Linear**
- **Strafe**
- **Jump**
- **Zigzag**

Isso ajuda a simular situações mais próximas do jogo real.

---

### 🎯 Feedback visual
- Crosshair estilo CS2
- Mira vermelha fora do alvo
- Mira verde sobre a cabeça
- Indicador “HEADSHOT!” quando o alvo está alinhado

---

### 📊 HUD em tempo real
Durante a partida, o HUD exibe:

- headshots
- tiros
- precisão
- sequência atual
- melhor sequência
- modo atual
- dificuldade atual
- número de bots
- tempo restante no modo Time Attack

---

## 🕹️ Controles

### Menu
- **↑ / ↓**: navegar
- **ENTER**: selecionar
- **ESC**: sair

### Durante o jogo
- **Botão esquerdo do mouse**: atirar
- **R**: reiniciar
- **↑ / ↓**: aumentar ou reduzir bots no modo Classic
- **ESC**: voltar ao menu

---

## ▶️ Como executar

### 1. Instale a dependência
```bash
pip install pygame
```

### 2. Execute o projeto
```bash
python treinador_mira.py
```

---

## 🧱 Estrutura do projeto

```text
treinador_mira.py
README.md
build_exe.bat
```

---

## 🛠️ Como gerar um executável
Use o arquivo `build_exe.bat` ou rode manualmente:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name TreinadorDeMira treinador_mira.py
```

O executável será gerado na pasta `dist`.

---

## 📖 Manual de uso detalhado

### 1. Início
Ao abrir o programa, você verá o menu principal com as opções:

- Iniciar Classic
- Iniciar Time Attack (60s)
- Dificuldade
- Número de Bots
- Sair

Antes de começar, ajuste:

- a dificuldade
- a quantidade de bots
- o modo de treino desejado

---

### 2. Modos disponíveis

#### Classic
Modo livre para treino contínuo.

Recomendado para:
- aquecimento
- treino de consistência
- adaptação ao movimento dos bots

Vantagens:
- sem limite de tempo
- ajuste de bots em tempo real
- ideal para sessões longas

#### Time Attack
Modo competitivo de 60 segundos.

Recomendado para:
- treino de pressão
- foco em velocidade
- sessões rápidas de desempenho

Vantagens:
- contagem regressiva
- recorde local na sessão
- tela final de resultado

---

### 3. Dificuldades

#### Easy
Alvos grandes e lentos. Ideal para começar.

#### Normal
Equilíbrio entre desafio e controle.

#### Hard
Alvos menores e mais rápidos.

#### Insane
Alvos extremamente pequenos e agressivos.

#### Mixed
Cada bot pode surgir com dificuldade diferente. Ótimo para adaptação.

---

### 4. Leitura do HUD

No canto esquerdo:
- Headshots
- Tiros
- Precisão
- Sequência atual
- Melhor sequência

No canto direito:
- Modo de jogo
- Dificuldade
- Bots
- Tempo restante no Time Attack

---

### 5. Rotina recomendada de treino

#### Sessão curta (10 a 15 minutos)
- 5 min no Classic / Easy ou Normal
- 5 min no Hard
- 5 min no Time Attack

#### Sessão competitiva (20 minutos)
- 5 min Classic / Normal
- 5 min Classic / Hard
- 10 min Time Attack

---

## 💼 Valor de portfólio
Este projeto demonstra:

- lógica de programação
- organização de regras de jogo
- tratamento de eventos
- renderização com Pygame
- controle de estado
- HUD e interface interativa
- foco em produto com aplicação real

---

## 🔮 Próximas melhorias sugeridas

- salvamento de highscore em arquivo
- sons de feedback
- tempo de reação por alvo
- tela de configurações
- customização da crosshair
- empacotamento com ícone próprio

---

## 📄 Licença
Uso educacional e de portfólio.
