import os
import time
import requests
import numpy as np
from dotenv import load_dotenv
from telegram import Bot
from sklearn.linear_model import LogisticRegression

# Carregar variáveis de ambiente (.env)
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# Variáveis de controle
ultimo = None
acertos = 0
erros = 0
previsao_ativa = None

def obter_resultados():
    try:
        url = 'https://blaze.com/api/roulette_games/recent'
        resposta = requests.get(url)
        jogos = resposta.json()
        return [jogo['color'] for jogo in jogos][::-1]
    except:
        return []

def treinar_modelo(dados):
    X, y = [], []
    for i in range(len(dados) - 3):
        entrada = dados[i:i+3]
        saida = dados[i+3]
        if 0 in entrada or saida == 0:
            continue
        X.append(entrada)
        y.append(saida)
    if len(X) >= 10:
        modelo = LogisticRegression()
        modelo.fit(X, y)
        return modelo
    return None

def enviar_sinal(previsao, historico, assertividade):
    cor = "vermelho" if previsao == 1 else "preto"
    hist = ", ".join(["branco" if x == 0 else "vermelho" if x == 1 else "preto" for x in historico])
    msg = f"""🤖 *SINAL GERADO COM IA* 🤖

🎯 Previsão: *{cor.upper()}*
📊 Últimos: {hist}
📈 Assertividade: *{assertividade:.2f}%* ({acertos} acertos / {acertos + erros})

⚠️ Use com cautela e gestão."""
    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')

print("✅ Robô Blaze com IA iniciado!")

while True:
    dados = obter_resultados()
    if not dados:
        time.sleep(10)
        continue

    atual = dados[-1]
    if atual != ultimo:
        if previsao_ativa is not None:
            if atual == previsao_ativa:
                acertos += 1
            elif atual != 0:
                erros += 1
            previsao_ativa = None

        modelo = treinar_modelo(dados[:50])
        if modelo:
            entrada = np.array(dados[-3:]).reshape(1, -1)
            if 0 not in entrada:
                previsao = modelo.predict(entrada)[0]
                if previsao in [1, 2]:
                    previsao_ativa = previsao
                    total = acertos + erros
                    assertiv = (acertos / total) * 100 if total else 0
                    enviar_sinal(previsao, dados[-5:], assertiv)
        ultimo = atual

    time.sleep(20)
