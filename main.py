import modules as md
import json

import os, sys, logging

logging.basicConfig(
    filename="/home/ubuntu/ppgcc/ppgcc.log",
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)

logging.debug(f"PWD = {os.getcwd()}")
logging.debug(f"Python = {sys.executable}")
logging.debug(f"Args = {sys.argv}")


def manage_log(response):
	log_config = config['log']
	e = response.get('message', 'Erro desconhecido')

	if response['response'] is False:
		print(f'[LOG] mandando email de log...')
		md.send_email(
			send_from=log_config['email-sender'],
			password=log_config['app-password'],         
			subject="ERROR - PPGCC TELEGRAM",
			text=f"Erro ao enviar mensagem para o canal ppgccmossoro do Telegram.\n\n ERROR: {e}",
			send_to= log_config['email-receiver'] if log_config['email-receiver'] else log_config['email-sender'],
		)

	return

if __name__ == '__main__':
	with open('config.json', 'r') as f:
		config = json.load(f)

	bot = md.BotTelegram(config['telegram']['token'], config['telegram']['chatId'])

	news = md.await_news()
	db = md.DataBase(config['database'])
	new_news = db.save_news(news)

	for item in new_news:
		# 💬 📜 🔗 📅
		
		text = (
			f"*{item['title']}*\n\n"
			f"📅 {item['date']}\n\n"
			f"📜 {item['partial_description']}\n\n"
			f"🔗 {item['link']}"
		)

		if item.get('img'):
			response = bot.sendPhoto(photo_url=item['img'], caption=text)
			manage_log(response)
		else:
			response = bot.sendMessage(message=text)
			manage_log(response)