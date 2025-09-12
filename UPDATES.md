# [ATUALIZAÇÕES:](./UPDATES.md#vers%C3%A3o-10---09052025)
## VERSÃO 1.5 - 12/09/2025:
* ✅O que mudou de fato nessa atualização foi a **lógica de como o `ffmpeg` lida com os metadados e a conversão quando o formato de entrada = saída:**

* 🛑**Antes da Atualização (1.4):**
  * Se **entrada = saída** (ex.: MP3 → MP3):
    * Sempre usava `-c copy` → não convertia, só copiava os fluxos.
    * Se "SIM" → `-map_metadata -1` → removia metadados.
    * Se "NÃO" → mantinha `-c copy` → preservava os metadados.

  * Se **entrada ≠ saída** (ex.: MP3 → WAV):
    * Sempre convertia.
    * Se "SIM" → `-map_metadata -1` → removia metadados.
    * Se "NÃO" → não passava nada sobre metadados → o `ffmpeg` decidia sozinho (e em alguns formatos, como WAV, acabava sem metadados).

* 🔵**Depois da Atualização (1.5):**
  1. **Entrada = saída (ex.: MP3 → MP3):**
    * "SIM" → `-c copy -map_metadata -1` → copia só o fluxo e remove metadados.
    * "NÃO" → Agora faz a conversão (`-vn -ar 44100 -ac 2 -b:a 192k`) e preserva metadados (`-map_metadata 0`).

  2. **Entrada ≠ saída (ex.: MP3 → WAV):**
    * "SIM" → converte e remove metadados (`-map_metadata -1`).
    * "NÃO" → converte e preserva os metadados (`-map_metadata 0`) **na medida em que o formato de saída suporta**.
---

## VERSÃO 1.4 - 20/08/2025:
* ✅**Stream copy quando o formato de entrada e saída são iguais:**
    * Antes, mesmo que você convertesse `MP3 → MP3`, o programa **sempre re-encodava** (perda de qualidade + demora).
    * Agora, se o formato de saída for o mesmo que o original, o FFmpeg roda com `-c copy`, ou seja:

      * não recodifica o áudio,
      * mantém a qualidade idêntica,
      * o processo é praticamente instantâneo.

    * Isso resolve aquele problema: “só queria limpar metadados, mas o áudio perdia qualidade”.

* ✅**Bitrate fixo em 192 kbps apenas quando há conversão real:**
    * Se o usuário escolhe **um formato diferente** (ex.: MP3 → OGG, WAV → MP3 etc.), o programa faz a conversão normal.
    * Para isso, define a saída com `-b:a 192k`.
    * Ou seja, quando realmente precisa re-encodar, ele já garante um nível de qualidade razoável, sem cair para 128 kbps como antes.
---

## VERSÃO 1.3 - 03/07/2025:
* ✅**Foi adicionado um recurso extra: Limpar Metadados:** Agora o app conta com a opção **“LIMPAR METADADOS?”**, com dois botões de rádio: **“SIM”** e **“NÃO”** (sendo **“NÃO”** o padrão). A lógica de conversão foi atualizada para aplicar o comando `-map_metadata -1` do FFmpeg **somente quando o usuário escolher "SIM"**, permitindo a remoção dos metadados de forma totalmente opcional e prática!
* ✅**Todo o layout do aplicativo foi redesenhado. As mudanças incluem**:
  * 🔸O **título do app** agora utiliza uma fonte maior.
  * 🔸**Remoção dos formatos**: `PADRÃO`, `flac`, `aac`, `alac` e `opus` da seção **“CONVERTER PARA”**.
  * 🔸Inclusão de um novo **contêiner exclusivo para a seção “LIMPAR METADADOS”**.
  * 🔸O botão **"DIRETÓRIO"** foi reposicionado para a **esquerda** do botão **"CONVERTER"**, alinhando melhor a interface.
  * 🔸A altura da **caixa de status (`status_textbox`)** foi reduzida de `200` para `165`.
---

## VERSÃO 1.2 - 09/06/2025:
* ✅Arquivos ocultos e de sistema são ignorados automaticamente durante o processo de conversão — mesmo que estejam visíveis no Explorador do Windows.
---

## VERSÃO 1.1 - 24/05/2025:
* ✅Adicionada barra de progresso e melhorias no status, que agora exibe o `diretório`, `progresso` e `pasta final` da conversão.
---

## VERSÃO 1.0 - 09/05/2025:
* ✅Foi lançado o aplicativo com interface moderna em tela cheia que converte automaticamente arquivos de áudio de diversos formatos para outro escolhido pelo usuário (como `.mp3`, `.wav`, `.ogg`, etc.) usando o `ffmpeg`. Permite seleção de diretório, exibe progresso detalhado, cria uma pasta para os arquivos convertidos e garante compatibilidade com dispositivos que só aceitam formatos tradicionais.
