import subprocess
import os
import requests
import time
import argparse

HF_API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HF_API_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

def get_modified_files(path):
    result = subprocess.run(['git', '-C', path, 'status', '--short'], capture_output=True, text=True)
    return [line.strip() for line in result.stdout.split('\n') if line]

def get_current_branch(path):
    result = subprocess.run(['git', '-C', path, 'branch', '--show-current'], capture_output=True, text=True)
    return result.stdout.strip()

def list_branches(path):
    result = subprocess.run(['git', '-C', path, 'branch'], capture_output=True, text=True)
    branches = [line.strip().replace('* ', '') for line in result.stdout.strip().split('\n')]
    return branches

def switch_branch(path):
    current = get_current_branch(path)
    print(f"\n📍 Branch atual: {current}")
    trocar = input("Deseja trocar de branch? (s/n): ").strip().lower()

    if trocar == 's':
        branches = list_branches(path)
        print("🌿 Branches disponíveis:")
        for i, b in enumerate(branches):
            print(f"{i+1}. {b}")
        try:
            escolha = int(input("Digite o número da branch desejada: "))
            nova_branch = branches[escolha - 1]
            subprocess.run(['git', '-C', path, 'checkout', nova_branch])
            print(f"✅ Mudou para a branch: {nova_branch}")
        except (ValueError, IndexError):
            print("❌ Escolha inválida. Continuando na branch atual.")
    else:
        print("✅ Continuando na branch atual.")

def generate_commit_message(files, branch):
    prompt = (
        f"Você está na branch '{branch}'. Gere uma mensagem de commit clara e profissional "
        f"para as seguintes alterações:\n{files}"
    )

    response = requests.post(
        HF_API_URL,
        headers=headers,
        json={"inputs": prompt, "parameters": {"max_new_tokens": 60}}
    )

    if response.status_code != 200:
        print("❌ Erro na API Hugging Face:", response.json())
        return "Melhorias no código"

    generated = response.json()
    return generated[0]["generated_text"].replace(prompt, "").strip()

def executar_commit(repo_path):
    modified_files = get_modified_files(repo_path)
    if not modified_files:
        print("🕵️ Nenhuma mudança detectada.")
        return False

    branch = get_current_branch(repo_path)
    if not branch:
        print("❌ Não foi possível obter o nome da branch.")
        return False

    commit_message = generate_commit_message(modified_files, branch)

    while True:
        user_input = input(f"\n💡 Sugestão de commit na branch '{branch}':\n{commit_message}\nAceitar? (s/n): ").strip().lower()
        if user_input == 's':
            subprocess.run(['git', '-C', repo_path, 'add', '.'])
            subprocess.run(['git', '-C', repo_path, 'commit', '-m', commit_message])
            subprocess.run(['git', '-C', repo_path, 'push', 'origin', branch])
            print(f"✅ Commit feito e enviado para a branch '{branch}' com sucesso!\n")
            return True
        elif user_input == 'n':
            commit_message = generate_commit_message(modified_files, branch)
        else:
            print("❗ Digite 's' para aceitar ou 'n' para gerar outra sugestão.")

def monitorar_repositorio(repo_path):
    print("🚀 Monitoramento iniciado.")
    while True:
        print("\nMenu:")
        print("1. Parar monitoramento")
        print("2. Realizar commit")
        print("3. Sair")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            print("🛑 Monitoramento interrompido. Você ainda está no diretório.")
            break
        elif escolha == "2":
            executar_commit(repo_path)
        elif escolha == "3":
            print("👋 Encerrando.")
            exit()
        else:
            print("❌ Opção inválida. Tente novamente.")

def process_repository(repo_path, uma_vez):
    if subprocess.run(['git', '-C', repo_path, 'rev-parse', '--is-inside-work-tree'], capture_output=True).returncode != 0:
        print("❌ Caminho inválido para repositório Git.")
        return

    switch_branch(repo_path)

    if uma_vez:
        print("🔁 Rodando uma única vez com --uma-vez.")
        executar_commit(repo_path)
    else:
        monitorar_repositorio(repo_path)

def main():
    parser = argparse.ArgumentParser(description="Auto Commit IA com Hugging Face")
    parser.add_argument('--uma-vez', action='store_true', help="Executar apenas uma vez e encerrar.")
    args = parser.parse_args()

    while True:
        repo_path = input("\n📂 Digite o caminho do repositório Git (ou 'sair' para encerrar): ").strip()
        if repo_path.lower() == 'sair':
            print("👋 Encerrando.")
            break

        if not os.path.isdir(repo_path):
            print("❌ Diretório não encontrado.")
            continue

        process_repository(repo_path, args.uma_vez)

if __name__ == "__main__":
    main()
