import traceback
import logging
from aiogram import Bot, Dispatcher, executor, types

import re
import json

import compiler
import ping_users

with open("config.json", "r", encoding="utf-8") as f:
    # Read the config file
    config_keys = json.loads(f.read())

# Get the API token
API_TOKEN = config_keys['API_KEY']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def helper(args):
    print(args)
    if "start" in args:
        return {"status": False}
    if len(args) > 1:
        args = args[1:]
        if "/compilar" in args or "compilar" in args:
            return "Uso: \nUse /compilar [linguagem] [codigo] ou mencionando um código para executar. O código será executado remotamente e a saída será enviada para o chat"
        if "/pingme" in args or "pingme" in args:
            return "Uso: \nUse /pingme para ser adicionado(a) na lista de ping. Todos os usuários que deram esse comando serão mencionados com /pingall. Para sair, dê /unpingme"
        if "/pingall" in args or "pingall" in args:
            return "Uso: \nUse /pingall para pingar todos os usuarios na lista que deram /pignme."
        if "/unpingme" in args or "unpingme" in args:
            return "Uso: \nUse /unpingme para sair da lista de menções do comando /pingall"
        if "/help" in args or "help" in args:
            return "Uso: \nMostra a mensagem de ajuda ou, caso algum parametro seja passado, mostra a ajuda específica daquele item."
        if "/download" in args or "download" in args:
            return "Em andamento!"
        if '/search' in args or "search" in args:
            return "Em andamento!"
    text = "Olá! Sou um simples bot multiuso. Algumas das minhas funções são: "
    text += "\n/compilar [linguagem] [codigo]: compila e roda um snnipet de codigo e manda a saida no chat"
    text += "\n/pingme, /pingall e /unpingme: cria uma lista de ping para as pessoas que derem /pingme"
    text += "\n/help [arg (optional)]: mostra essa mensagem e, caso algum comando seja passado, mostra a ajuda dele"
    text += "\nMeu repositório: github.com/kamuridesu/não existe ainda!"
    return text


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    # Send message to the chat
    args = message['text'].split(" ")
    text = helper(args)
    #text = "Olá! Sou um simples bot multiuso. Algumas das minhas funções são: "
    #text += "\n/compilar [linguagem] [codigo]: compila e roda um snnipet de codigo e manda a saida no chat"
    #text += "\n/ping, /pingall e /unpingme: cria uma lista de ping para as pessoas que derem /pingme"
    #text += "\n/help [arg (optional)]: mostra essa mensagem e, caso algum comando seja passado, mostra a ajuda dele"
    #text += "\nMeu repositório: github.com/kamuridesu/não existe ainda!"
    await message.reply(text)


def processSpace(args: str):
    args = args.split(" ")[1:] # Remove the command
    if len(args) >= 2: # Check if there is a language and a code
        lang = args[0] # Get the language
        if not "\n" in lang: # Check if the language is a valid one
            return {"status": True, "lang": lang, "code": " ".join(args[1:])} # Return the code
    return {"status": False, "msg": "Preciso da linguagem e do codigo!"}


def processNewLine(args: str):
    args = args.split("\n") # Split the code by new lines
    if len(args) >= 2: # Check if there is a language and a code
        lang = args[0].split(" ") # Get the language
        if len(lang) > 1: # Check if the language is a valid one
            lang = lang[1] # Get the language
            code = "\n".join(args[1:]) # Get the code
            return {"status": True, "lang": lang, "code": code} # Return the code
    return {"status": False, "msg": "Preciso da linguagem e do codigo!"}


def replyCompile(message: types.Message):
    # Get the code
    text = message['text'] # Get the text
    mentioned_msg = message["reply_to_message"] # Get the message that was replied
    mentioned_code = mentioned_msg[text] # Get the code
    return mentioned_code


@dp.message_handler(commands=["compilar"]) # Compile the code
async def compilar(message: types.Message):
    data = None
    lang = ""
    code = ""
    err = "Algum erro ocorreu!"
    to_compile = {"status": False}
    msg = await message.reply("Processando...")
    if message["reply_to_message"]: # Check if the message was replied
        data = replyCompile(message) # Get the code
        args = message['text'].split(" ") # Get the args
        if len(args) > 1: # Check if there is a language and a code
            lang = args[1] # Get the language
            to_compile["status"] = True
            to_compile["lang"] = lang
            to_compile["code"] = data
        else: # Check if there is a language and a code
            err = "Preciso da linguagem!"
    else: # Check if the message was replied
        args = message["text"]
        to_compile = processSpace(args) # Get the code
        if not to_compile["status"]: # Check if there is a language and a code
            err = to_compile["msg"]
            to_compile = processNewLine(args) # Get the code
    if to_compile["status"]:  # Check if there is a language and a code
        await bot.edit_message_text(text="Rodando codigo...", chat_id=msg['chat']['id'], message_id=msg["message_id"]) # Edit the message
        comp = compiler.Compiler(to_compile['lang'], to_compile['code']) # Compile the code
        success = comp.postData() # Post the data
        if success:
            res = comp.getResponse() # Get the response
            response = ["✅", "❌"][res['exit_code'] == 0] + "Codigo executado\!" # Get the response
            response += "\nSaida: \n\n```\n" + res['body']
            response += "\n```"
            return await bot.edit_message_text(text=response, chat_id=msg['chat']['id'], message_id=msg["message_id"], parse_mode="MarkdownV2") # Edit the message
        else:
            err = "Erro! Linguagem não suportada ou algum problema ocorreu!"
    return await bot.edit_message_text(text=err, chat_id=msg['chat']['id'], message_id=msg["message_id"])


@dp.message_handler(commands=["pingme"])
async def pingme(message: types.Message):
    # Ping the user
    """{"message_id": 894, "from": {"id": 1253085705, "is_bot": false, "first_name": "Kamuri", "last_name": "SG;r02 ☄️", "username": "kamuridesu", "language_code": "en"}, "chat": {"id": 1253085705, "first_name": "Kamuri", "last_name": "SG;r02 ☄️", "username": "kamuridesu", "type": "private"}, "date": 1631712271, "text": "/pingme", "entities": [{"type": "bot_command", "offset": 0, "length": 7}]}"""
    chat_id = message["chat"]["id"]
    user_id = message["from"]["id"]
    username = ""
    try: # Check if the user has a username
        username = message["from"]["username"]
    except Exception: # If not, get first_name
        username = message["from"]["first_name"]
    users = ping_users.UsersToPing() # Get the users to ping
    # users.clearFile()
    success = users.addUser(chat_id, username, user_id) # Add the user to the list
    response = "Usuario já na lista!"
    if success:
        response = "Usuario adicionado com sucesso!"
    await message.reply(response)


def checkUsername(username):
    get_out = ["[", "]", "_", "*", "`"]
    new_username = ""
    for char in username:
        if char in get_out:
            char = "\\" + char
        new_username += char
    return new_username


@dp.message_handler(commands=['pingall'])
async def pingall(message: types.Message):
    chat_id = message["chat"]["id"] # Get the chat id
    msg = "Erro! Algo deu errado"
    users = ping_users.UsersToPing() # Get the users to ping
    all_users = users.getAllUsers(chat_id)
    if all_users is None: # Check if there is users to ping
        msg = "Nenhum usuario para pingar\!"
    else:
        rep = ""
        for user in all_users: # For each user
            username = checkUsername(user['username']) # Get the username
            user_id = user['id']
            rep += f"[{username}](tg://user?id={user_id}) " # Add the username to the response
        msg = rep
    if msg == "":
        msg = "Nenhum usuario para pingar\!"
    await message.reply(msg, parse_mode="MarkdownV2")


@dp.message_handler(commands=['unpingme'])
async def unpingme(message: types.Message):
    # Unping the user
    chat_id = message['chat']['id']
    user_id = message["from"]["id"]
    username = ""
    try:
        username = message["from"]["username"]
    except Exception:
        username = message["from"]["first_name"]
    users = ping_users.UsersToPing() # Get the users to ping
    status = users.removeUser(chat_id, username, user_id) # Remove the user from the list
    await message.reply(status['message'])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

