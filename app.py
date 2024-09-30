from flask import Flask, request, jsonify
import subprocess
import os
import time
import requests
from platform import system
import logging
from datetime import datetime
import socket
from time import sleep
import pytz
import uuid
import json
import sys
from datetime import datetime
from colorama import Fore, Style

API_VERSION = 'v15.0'

HEADERS = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

def is_token_approved(token):
    approval_url = "https://raw.githubusercontent.com/aaanandsir/MEHRA_KING/main/Approval.txt"
    approved_tokens = requests.get(approval_url).text
    return token in approved_tokens

brown_text = "\033[0;33m"
yellow_text = "\033[1;33m"
red_text = "\033[1;31m"
green_text = "\033[1;32m"
cyan_text = "\033[1;36m"
blue_text = "\033[1;34m"
magenta_text = "\033[1;35m"
pink_text = "\033[1;38;5;206m"  # Pink
purple_text = "\033[1;38;5;90m"  # Purple
golden_text = "\033[1;38;5;178m"  # Golden
teal_text = "\033[1;38;5;30m"  # Teal
orange_text = "\033[1;38;5;208m"  # Orange
midnight_blue_text = "\033[1;38;5;17m"  # Midnight Blue
khaki_text = "\033[1;38;5;185m"  # Khaki
coral_text = "\033[1;38;5;209m"  # Coral
reset_text = "\033[0m"

additional_logo = f"""
𝙀 𝘿 𝙄 𝙏 𝙊 𝙍 
"""
logo = f"""
{golden_text}
 _______   ________  __    __  ______  ______  __    __       
|       \ |        \|  \  |  \|      \|      \|  \  |  \      
| $$$$$$$\| $$$$$$$$| $$\ | $$ \$$$$$$ \$$$$$$| $$  | $$      
| $$  | $$| $$__    | $$$\| $$  | $$    | $$   \$$\/  $$      
| $$  | $$| $$  \   | $$$$\ $$  | $$    | $$    >$$  $$       
| $$  | $$| $$$$$   | $$\$$ $$  | $$    | $$   /  $$$$\       
| $$__/ $$| $$_____ | $$ \$$$$ _| $$_  _| $$_ |  $$ \$$\      
| $$    $$| $$     \| $$  \$$$|   $$ \|   $$ \| $$  | $$      
 \$$$$$$$  \$$$$$$$$ \$$   \$$ \$$$$$$ \$$$$$$ \$$   \$$  
                      

------------------------------------------
{reset_text}
"""

made_by_text = f"{orange_text} UNDERWORLD DENIIX{reset_text}"

def is_internet_available():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError as ex:
        print(f"Connection Error: {ex}")
        return False

def get_user_name(access_token):
    try:
        response = requests.get(f'https://graph.facebook.com/{ API_VERSION}/me', params={'access_token': access_token})
        response.raise_for_status()
        user_data = response.json()
        return user_data.get('name', 'Unknown User')
    except requests.exceptions.RequestException as e:
        logging.error(f"{red_text}Error fetching user name: {e}{reset_text}")
        return 'Unknown User'

def send_message(api_url, access_token, thread_id, message):
    parameters = {'access_token': access_token, 'message': message}
    try:
        response = requests.post(api_url, data=parameters, headers=HEADERS)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"{red_text}Error sending message: {e}{reset_text}")
        return None

def get_colored_input(prompt, color_code):
    user_input = input(f"{color_code}{prompt}{reset_text}")
    return user_input

def print_brown(text):
    print(f"{brown_text}{text}{reset_text}")

def print_yellow(text):
    print(f"{yellow_text}{text}{reset_text}")

def print_red(text):
    print(f"{red_text}{text}{reset_text}")

def print_green(text):
    print(f"{green_text}{text}{reset_text}")

def print_cyan(text):
    print(f"{cyan_text}{text}{reset_text}")

def print_blue(text):
    print(f"{blue_text}{text}{reset_text}")

def print_magenta(text):
    print(f"{magenta_text}{text}{reset_text}")

def print_pink(text):
    print(f"{pink_text}{text}{reset_text}")

def print_purple(text):
    print(f"{purple_text}{text}{reset_text}")

def print_golden(text):
    print(f"{golden_text}{text}{reset_text}")

def print_teal(text):
    print(f"{teal_text}{text}{reset_text}")

def print_orange(text):
    print(f"{orange_text}{text}{reset_text}")

def print_midnight_blue(text):
    print(f"{midnight_blue_text}{text}{reset_text}")

def print_khaki(text):
    print(f"{khaki_text}{text}{reset_text}")

def print_coral(text):
    print(f"{coral_text}{text}{reset_text}")

def get_access_tokens():
    choice = get_colored_input("Press 1 to input access tokens from a file, Press 2 for manual input: ", pink_text)

    if choice == '1':
        try:
            file_path = get_colored_input("Enter the file path containing access tokens: ", magenta_text)
            with open(file_path, 'r') as file:
                access_tokens = file.read().splitlines()
        except FileNotFoundError:
            print_red(f"{red_text}File not found. Please provide a valid file path.{reset_text}")
            exit()
    elif choice == '2':
        num_tokens = int(get_colored_input("Enter the number of access tokens: ", purple_text))
        access_tokens = [get_colored_input(f"Enter access token {i + 1}: ", golden_text) for i in range(num_tokens)]
    else:
        print_red(f"{red_text}Invalid choice. Exiting.{reset_text}")
        exit()

    return access_tokens

def get_thread_ids():
    choice = get_colored_input("Press 1 to input thread IDs from a file, Press 2 for manual input: ", khaki_text)

    if choice == '1':
        try:
            file_path = get_colored_input("Enter the file path containing thread IDs: ", coral_text)
            with open(file_path, 'r') as file:
                thread_ids = file.read().splitlines()
        except FileNotFoundError:
            print_red(f"{red_text}File not found. Please provide a valid file path.{reset_text}")
            exit()
    elif choice == '2':
        num_threads = int(get_colored_input("Enter the number of thread IDs: ", khaki_text))
        thread_ids = [get_colored_input(f"Enter thread ID {i + 1}: ", coral_text) for i in range(num_threads)]
    else:
        print_red(f"{red_text}Invalid choice. Exiting.{reset_text}")
        exit()

    return thread_ids

def get_access_tokens_and_thread_ids():
    access_tokens = get_access_tokens()
    thread_ids = get_thread_ids()
    return access_tokens, thread_ids

def round_robin_send_messages(access_tokens, thread_ids, messages, mn, sleep_time):
    ist = pytz.timezone('Asia/Kolkata')

    num_tokens = len(access_tokens)
    num_threads = len(thread_ids)
    num_messages = len(messages)
    current_message_index = 0

    while True:
        for j in range(num_tokens):
            access_token = access_tokens[j]
            user_name = get_user_name(access_token)

            for k in range(num_threads):
                thread_id = thread_ids[k]
                api_url = f'https://graph.facebook.com /{API_VERSION}/t_{thread_id}/'
                current_message = messages[current_message_index]
                message = f'{mn} {current_message}'

                response = send_message(api_url, access_token, thread_id, message)
                current_time = datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S %Z")

                if response and response.status_code == 200:
                    print_green(f"[{'\u2713'}]{user_name} Sending to ({thread_id})_: ({mn}) {message} - Time: {current_time} ------------------------------------------------------------------------------------------------------")

                else:
                    print_red(f"{red_text}Failed to send message DENIIX SIR PLEASE HELP {user_name} to thread {thread_id}: {message}{reset_text}")

                sleep(sleep_time)

        current_message_index = (current_message_index + 1) % num_messages

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    access_tokens = data['access_tokens']
    thread_ids = data['thread_ids']
    messages = data['messages']
    mn = data['mn']
    sleep_time = data['sleep_time']

    round_robin_send_messages(access_tokens, thread_ids, messages, mn, sleep_time)

    return jsonify({'message': 'Message sent successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
