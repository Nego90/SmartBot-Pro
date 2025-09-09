# 🤖 SmartBot Pro

**Criado por: [Luan Dev](https://github.com/Nego90)**

Um robô de automação visual para Windows, desenvolvido em Python, que utiliza captura de coordenadas para interagir com qualquer aplicação ou jogo. Esqueça seletores de CSS frágeis; este bot age como um ser humano, clicando e digitando exatamente onde você ensina.

![Demonstração do SmartBot Pro](https://i.imgur.com/4o2xy4A.gif)

---

## ✨ Funcionalidades Principais

* **100% Visual:** Não depende do código do site ou aplicativo. Se você pode ver, o bot pode clicar.
* **Captura de Coordenadas:** Interface intuitiva para "ensinar" ao robô onde clicar para digitar e onde clicar para enviar.
* **Múltiplos Comentários Aleatórios:** Adicione uma lista de comentários e o bot escolherá um aleatoriamente a cada ciclo, tornando a interação mais natural.
* **Controle de Tempo Flexível:** Escolha entre intervalos de tempo pré-definidos ou defina um tempo personalizado.
* **Interface Profissional:** Um painel de controle com tema escuro, ícones e um design limpo, construído com PyQt6.
* **Digitação Precisa:** Suporta qualquer caractere, incluindo letras maiúsculas e emojis, através da simulação de copiar e colar.

---

## 🚀 Como Usar (Executável)

A maneira mais fácil de usar o SmartBot Pro é baixando a versão pronta.

1.  Vá para a página de **[Releases](https://github.com/Nego90/SmartBot-Pro/releases)**.
2.  Baixe o arquivo `SmartBotPro.exe` da versão mais recente.
3.  Execute o arquivo. Nenhuma instalação é necessária.
4.  Com o aplicativo alvo (ex: chat de uma live) visível na tela, use os botões "Capturar" no SmartBot para definir as posições do mouse.
5.  Adicione seus comentários, defina o intervalo e clique em "INICIAR ROBÔ".

---

## 🛠️ Como Executar a Partir do Código-Fonte (Para Desenvolvedores)

Se você deseja modificar ou estudar o código, siga estes passos:

1.  **Pré-requisitos:**
    * [Git](https://git-scm.com/)
    * [Python 3.9+](https://www.python.org/)

2.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Nego90/SmartBot-Pro.git](https://github.com/Nego90/SmartBot-Pro.git)
    cd SmartBot-Pro
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Você precisará criar um arquivo `requirements.txt`. Um jeito fácil é rodar `pip freeze > requirements.txt` no seu terminal, na pasta do projeto, depois de ter instalado todas as bibliotecas que usamos).*

4.  **Execute o script:**
    ```bash
    comments.py
    ```

---

## 📜 Licença

Este projeto é de código aberto. Sinta-se à vontade para usar, modificar e distribuir.
