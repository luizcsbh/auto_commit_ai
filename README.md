# Auto Commit Monitor

Este é um script Python que monitora repositórios Git, gera mensagens de commit automaticamente usando um modelo de IA da Hugging Face e facilita o commit e push das mudanças para o repositório remoto.

## 📌 Funcionalidades
- Detecta arquivos modificados no repositório.
- Gera mensagens de commit automáticas baseadas nas mudanças detectadas.
- Permite alternar entre branches do Git.
- Possui um menu interativo para iniciar/parar monitoramento, realizar commits ou sair.

## 📦 Instalação e Dependências

Para executar o script, instale as seguintes bibliotecas:

```bash
pip install requests
```

Além disso, o Git deve estar instalado e configurado na sua máquina.

## 🔑 Configuração da API Key

O script usa a API da Hugging Face para gerar mensagens de commit. Para utilizá-lo, siga os passos abaixo para criar uma chave de API com permissões de leitura:

1. Acesse [Hugging Face](https://huggingface.co/).
2. Faça login ou crie uma conta.
3. Vá até [suas configurações](https://huggingface.co/settings/token).
4. Clique em **New token**.
5. Dê um nome ao token e selecione **Read** como permissão.
6. Clique em **Generate** e copie a chave gerada.
7. Defina sua chave de API como uma variável de ambiente:

```bash
export HUGGINGFACE_TOKEN='sua_api_key_aqui'
```

Caso esteja no Windows (cmd):

```cmd
set HUGGINGFACE_TOKEN=sua_api_key_aqui
```

Caso esteja no Windows (PowerShell):

```powershell
$env:HUGGINGFACE_TOKEN="sua_api_key_aqui"
```

## 🚀 Como Usar

1. Execute o script:
   ```bash
   python auto_commit_monitor.py
   ```
2. Digite o caminho do repositório Git.
3. Escolha uma das opções do menu:
   - **Parar monitoramento**: interrompe o monitoramento sem sair do diretório.
   - **Realizar commit**: gera e aplica um commit automaticamente.
   - **Sair**: encerra o programa.
4. Caso queira rodar apenas uma vez e sair, use:
   ```bash
   python auto_commit_monitor.py --uma-vez
   ```

## 📜 Licença
Este projeto é de uso livre e pode ser modificado conforme necessário.

---

Se precisar de mais alguma informação ou melhoria, me avise! 🚀

