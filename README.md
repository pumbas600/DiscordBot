# Discord Joke Bot

A very simple discord joke bot using python.
The bot works by requesting a joke from the a Joke API by 15Dkatz, which you can find [here](https://github.com/15Dkatz/official_joke_api).

## Resources

### Discord Bots:

Feel free to check out [this](https://realpython.com/how-to-make-a-discord-bot-python/) realpython tutorial for a comprehensive guide to getting started with discord bots in python:

### Free Hosting Options:

I am currently hosting my bot off [repl.it](repl.it). A tutorial on how to do this can be found [here](https://repl.it/talk/learn/Hosting-discordpy-bots-with-replit/11008)

**Note:** Unless you are using an upgraded repl.it account, all your repls will be public. For this reason, do NOT hard code your token into your program. Instead you can try:

```python
TOKEN = input('Enter your discord bot token: ')
```
This is the most secure option and is recommended if you don't need to continously restart the bot.
Alternatively, I designed a less secure option to encrypt your token using an easy to remember password:

```python
import os.path
import random

token_file = 'TOKEN.txt'

def get_token(overwrite=False):
    if not overwrite and os.path.isfile(token_file):
        with open(token_file, 'r') as f:
            encrypted_token = f.readline()
            if not encrypted_token:
                return request_user_token()
            else:
                password = input("Enter the password to unencrypt your token: ")
                unencrypted_token = unencrypt_token(encrypted_token, get_encryption_seed(password))
                # They only have one chance to enter the correct password, otherwise they
                # have to re-enter the token or restart the program.
                if not unencrypted_token:
                    request_user_token()
                else:
                    return unencrypted_token
    else:
        return request_user_token()


def get_encryption_seed(password):
    return sum(ord(c) for c in password)


def unencrypt_token(token, encryption_seed):
    unencrypted_token = ""
    random.seed(encryption_seed)

    try:
        for char in token:
            unencrypted_token += chr(ord(char) - random.randint(0,10000))
    # Occurs when chr(i) is out of out the range 0 - 1,114,111
    except ValueError:
        print('Error occured while unencryping token.')
        return False

    return unencrypted_token


def encrypt_token(token, encryption_seed):
    random.seed(encryption_seed)
    encrypted_token = ""

    try:
        for char in token:
            encrypted_token += chr(ord(char) + random.randint(0,10000))
    # Occurs when chr(i) is out of out the range 0 - 1,114,111
    except ValueError:
        print('Error occured while encryping token.')
        return False

    return encrypted_token
    

def request_user_token():
    token = input("Enter discord bot token: ")

    if token:
        password = input("Enter the password to encrypt your token: ")
        encrypted_token = encrypt_token(token, get_encryption_seed(password))
        if not encrypted_token:
            return request_user_token()
        else:
            # Save token to file
            with open(token_file, 'w') as f:
                f.write(encrypted_token)
            return token
    else:
        return request_user_token()
```

You can then use this to get the token in your main program by simply doing:

```python
import token_manager
TOKEN = token_manager.get_token()
```

Example of encrypyting the token: ThisIsAT3stTok3n

```
Enter discord bot token: ThisIsAT3stTok3n
Enter the password to encrypt your token: ThisIsAT3stPassword
...
In the file TOKEN.txt:
⌾ᑄݡ᪱ᙁ፯᣻៻ඇ᣿⊂ሳĂࣂᎏ৲
...
Next time you go to start your server:
Enter the password to unencrypt your token: ThisIsAT3stPassword
```
