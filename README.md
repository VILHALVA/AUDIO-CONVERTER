# AUDIO CONVERTER
📱ESTE APLICATIVO CONVERTE AUTOMATICAMENTE ARQUIVOS DE ÁUDIO PARA UM FORMATO ESCOLHIDO PELO USUÁRIO (COMO .MP3, .WAV, .OGG, ETC.) USANDO O FFMPEG.

<img src="./IMAGENS/FOTO_01.png" align="center" width="400"> <br>
<img src="./IMAGENS/FOTO_02.png" align="center" width="400"> <br>
<img src="./IMAGENS/FOTO_03.png" align="center" width="400"> <br>

## DESCRIÇÃO:
Este aplicativo converte automaticamente arquivos de áudio de diversos formatos (como `.wav`, `.ogg`, `.flac`, `.aac`, `.m4a`, `.wma`, `.alac`, `.opus`, `.mp4`, `.mov`, e `.mp3`) para um formato escolhido pelo usuário (por padrão, `.mp3`), utilizando a poderosa ferramenta `ffmpeg`.

É especialmente útil para tornar arquivos compatíveis com qualquer dispositivo de áudio — como aparelhos antigos, carros, players portáteis e celulares que aceitam apenas formatos tradicionais.

## FUNCIONALIDADES:
* **Interface gráfica moderna (tema escuro)** com `customtkinter`.
* **Executa em tela maximizada** e permite redimensionamento da janela.
* **Seleção de diretório** contendo os arquivos de áudio.
* **Escolha do formato de saída** entre: MP3, WAV, OGG, FLAC, AAC, M4A, WMA, OPUS e ALAC.
* **Botões de seleção de formato exibidos horizontalmente**, centralizados dentro de um contêiner com borda visual elegante.
* **Conversão automática**, inclusive de arquivos `.mp3` modernos que podem não funcionar em todos os dispositivos.
* **Criação de uma nova pasta** chamada `CONVERTIDOS_<FORMATO>` para salvar os arquivos convertidos.
* **Área de status com logs em tempo real**, exibindo o progresso da conversão e mensagens do `ffmpeg`.
* **Mensagens de erro e alertas amigáveis**, caso nenhum arquivo válido seja encontrado.

## COMO USAR?
1. **Instale as bibliotecas necessárias:** Antes de executar o app, certifique-se de instalar todas as dependências necessárias. No terminal, execute o seguinte comando para instalar as dependências listadas no arquivo requirements.txt em `CODIGO`:
   ```bash
   pip install -r requirements.txt
   ```

2. **Instalar `ffmpeg`:** O App depende da ferramenta externa chamada `ffmpeg` para converter os arquivos de áudio.

   1. **Baixar `ffmpeg`:**
      - Vá para o site oficial: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
      - Na seção de downloads, clique em "Windows builds from gyan.dev" ou um equivalente.
      - Baixe o arquivo ZIP de uma versão estável, por exemplo: `ffmpeg-git-full.7z`.

   2. **Extrair o `ffmpeg`:**
      - Extraia o conteúdo do arquivo baixado para uma pasta em seu computador, como `C:\ffmpeg`.

   3. **Adicionar `ffmpeg` ao caminho (PATH):**
      - Abra o **Painel de Controle** e vá para **Sistema e Segurança** > **Sistema** > **Configurações avançadas do sistema**.
      - Clique em **Variáveis de Ambiente**.
      - Em **Variáveis de Sistema**, selecione a variável **Path** e clique em **Editar**.
      - Adicione uma nova entrada com o caminho completo para a pasta `bin` dentro da pasta onde você extraiu o `ffmpeg`, por exemplo: `C:\ffmpeg\bin`.
      - Clique em **OK** e feche as janelas.

   4. **Verificar a instalação:**
      - Abra o Prompt de Comando e digite `ffmpeg` para verificar se está funcionando corretamente. Você deve ver uma lista de comandos suportados se tudo foi configurado corretamente.

3. **Executar o APP:**
   * No diretório `./CODIGO`, execute o aplicativo com o comando:

   ```bash
   python CODIGO.py
   ```

4. A janela abrirá automaticamente **maximizada**, mas **permite redimensionamento manual**.

5. Clique no botão **"DIRETÓRIO"** e selecione a pasta que contém os arquivos de áudio que deseja converter.

6. Escolha o formato de saída desejado nos **botões centralizados dentro da área “CONVERTER PARA:”** (ex: MP3, WAV, OGG, etc.).

7. Clique no botão **"CONVERTER"** para iniciar a conversão.

8. Acompanhe os detalhes do processo na **caixa de status**, que exibe logs em tempo real do `ffmpeg`.

9. Ao final, será exibida uma mensagem confirmando que a conversão foi concluída.

10. Os arquivos convertidos estarão em uma subpasta chamada **`CONVERTIDOS_<FORMATO>`** (ex: `CONVERTIDOS_MP3`) criada automaticamente dentro do diretório selecionado.

## SOBRE O EXECUTAVEL:
### 1. EXECUTANDO:
- Este arquivo executável está disponível apenas para `Windows X64`. Para executá-lo, basta dar dois cliques. O executável é bastante útil caso o Python não esteja instalado. Trata-se da mesma aplicação do arquivo `CODIGO.py`. Se desejar, você pode recompilá-lo novamente; é para isso que forneci o arquivo `imagem.ico`.

- **Observação:** Certifique-se de que o `ffmpeg` esteja instalado e adicionado à variável de ambiente PATH do sistema para que o executável funcione corretamente.

### 2. GERANDO:
   **1. Instalação do [PyInstaller:](https://pyinstaller.org/en/stable/)**
   - Certifique-se de ter o PyInstaller instalado. Se não tiver, instale usando o comando abaixo:
   ```bash
   pip install pyinstaller
   ```

   **2. Gerando o Executável:**
   - Para gerar o executável, utilize o comando `pyinstaller` seguido de opções:
      - `--icon="imagem.ico"`: Especifica o ícone do executável.
      - `-w`: Especifica que o executável será do tipo "windowed", ou seja, sem exibir uma janela de console.
      - `-F`: Gera um único arquivo executável em vez de vários.
      - `CODIGO.py`: Substitua "CODIGO.py" pelo nome do seu arquivo Python principal.
   ```bash
   pyinstaller --icon="imagem.ico" -w -F CODIGO.py
   ```

## NÃO SABE?
- Entendemos que para manipular arquivos em muitas linguagens, é necessário possuir conhecimento nessas áreas. Para auxiliar nesse aprendizado, oferecemos cursos gratuitos disponíveis:
* [CURSO DE PYTHON](https://github.com/VILHALVA/CURSO-DE-PYTHON)
* [CURSO DE CUSTOMTKINTER](https://github.com/VILHALVA/CURSO-DE-CUSTOMTKINTER)
* [CONFIRA MAIS CURSOS](https://github.com/VILHALVA?tab=repositories&q=+topic:CURSO)

## CREDITOS:
- [PROJETO CRIADO PELO VILHALVA](https://github.com/VILHALVA)
