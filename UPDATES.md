# [ATUALIZAÇÕES:](./UPDATES.md#vers%C3%A3o-10---09052025)
## VERSÃO 1.3 - 03/07/2025:
* ✅**Foi adicionado um recurso extra: Limpar Metadados:** Agora o app conta com a opção **“LIMPAR METADADOS?”**, com dois botões de rádio: **“SIM”** e **“NÃO”** (sendo **“NÃO”** o padrão). A lógica de conversão foi atualizada para aplicar o comando `-map_metadata -1` do FFmpeg **somente quando o usuário escolher "SIM"**, permitindo a remoção dos metadados de forma totalmente opcional e prática!
* ✅**Todo o layout do aplicativo foi redesenhado. As mudanças incluem**:
  * 🔸O **título do app** agora utiliza uma fonte maior.
  * 🔸**Remoção dos formatos**: `PADRÃO`, `flac`, `aac`, `alac` e `opus` da seção **“CONVERTER PARA”**.
  * 🔸Inclusão de um novo **contêiner exclusivo para a seção “LIMPAR METADADOS”**.
  * 🔸O botão **"DIRETÓRIO"** foi reposicionado para a **esquerda** do botão **"CONVERTER"**, alinhando melhor a interface.
  * 🔸A altura da **caixa de status (`status_textbox`)** foi reduzida de `200` para `170`, otimizando o uso de espaço na janela.
---

## VERSÃO 1.2 - 09/06/2025:
* ✅Arquivos ocultos e de sistema são ignorados automaticamente durante o processo de conversão — mesmo que estejam visíveis no Explorador do Windows.
---

## VERSÃO 1.1 - 24/05/2025:
* ✅Adicionada barra de progresso e melhorias no status, que agora exibe o `diretório`, `progresso` e `pasta final` da conversão.
---

## VERSÃO 1.0 - 09/05/2025:
* ✅Foi lançado o aplicativo com interface moderna em tela cheia que converte automaticamente arquivos de áudio de diversos formatos para outro escolhido pelo usuário (como `.mp3`, `.wav`, `.ogg`, etc.) usando o `ffmpeg`. Permite seleção de diretório, exibe progresso detalhado, cria uma pasta para os arquivos convertidos e garante compatibilidade com dispositivos que só aceitam formatos tradicionais.
