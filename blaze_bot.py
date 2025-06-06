import os
import logging
from telegram import Bot
from telegram.error import TelegramError
from apscheduler.schedulers.blocking import BlockingScheduler
from sklearn.ensemble import RandomForestClassifier
import random
import numpy as np

# Configurações do Telegram via variáveis de ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Inicializa o bot
bot = Bot(token=TELEGRAM_TOKEN)
logging.basicConfig(level=logging.INFO)

# Simulação de dados históricos para IA
historico = [random.choice(['red', 'black', 'white']) for _ in range(100)]
mapeamento = {'red': 0, 'black': 1, 'white': 2}
X = [[mapeamento[cor]] for cor in historico[:-1]]
y = [mapeamento[cor] for cor in historico[1:]]

modelo = RandomForestClassifier()
modelo.fit(X, y)

def prever_cor():
    ultima = X[-1]
    previsao = modelo.predict([ultima])[0]
    prob = modelo.predict_proba([ultima])[0][previsao]
    cor = list(mapeamento.keys())[list(mapeamento.values()).index(previsao)]
    return cor, round(prob * 100, 2)

def enviar_mensagem():
    try:
        cor, assertividade = prever_cor()
        mensagem = f"🎯 Previsão: {cor.upper()}
📊 Assertividade: {assertividade}%"
        bot.send_message(chat_id=CHAT_ID, text=mensagem)
        logging.info(f"Mensagem enviada: {mensagem}")
    except TelegramError as e:
        logging.error(f"Erro ao enviar mensagem: {e}")

# Agenda para enviar mensagem a cada 5 minutos
scheduler = BlockingScheduler()
scheduler.add_job(enviar_mensagem, 'interval', minutes=5)

if __name__ == "__main__":
    logging.info("✅ Robô Blaze com IA (nuvem) iniciado!")
    scheduler.start()