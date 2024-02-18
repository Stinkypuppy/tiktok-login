import requests
import json
import os
import logging
from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text
from art import text2art
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.styles import Style as PromptStyle

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StreamConfigurator:
    def __init__(self):
        self.session = requests.Session()
        self.config = {
            "sid_guard_cookie": "",
            "title": "",
            "game_tag_id": "",
            "gen_replay": False,
            "close_room_when_close_stream": True
        }
        self.game_list_url = 'https://webcast16-normal-c-useast2a.tiktokv.com/webcast/room/hashtag/list/'
        self.config_file_path = "stream_config.json"
        self.console = Console()

    def start(self):
        while True:
            options = [
                ("Insert Cookie", "1"),
                ("Select Game", "2"),
                ("Edit Title", "3"),
                ("Toggle Replay Generation", "4"),
                ("Toggle Room Closure on Stream End", "5"),
                ("Create Stream", "6"),
                ("Save Configuration", "7"),
                ("Load Configuration", "8"),
                ("Exit", "9")
            ]
            menu_style = PromptStyle.from_dict({
                "dialog.title": "ansiyellow",
                "dialog.body": "ansiblue",
                "dialog shadow": "bg:#440044",
                "dialog frame.label": "bg:#ffffff #000000",
                "dialog.body label": "bg:#ffffff #000000",
                "dialog": "bg:#88ff88",
            })

            choice = radiolist_dialog(
                title="Stream Configuration Menu",
                text="Choose an option:",
                values=options,
                style=menu_style
            ).run()

            if choice:
                if choice == "1":
                    self.config["sid_guard_cookie"] = prompt("Enter your sid_guard cookie: ")
                elif choice == "2":
                    self.select_game()
                elif choice == "3":
                    self.config["title"] = prompt("Enter stream title: ")
                elif choice == "4":
                    self.config["gen_replay"] = not self.config["gen_replay"]
                    self.console.print(f"Replay Generation {'Enabled' if self.config['gen_replay'] else 'Disabled'}.")
                elif choice == "5":
                    self.config["close_room_when_close_stream"] = not self.config["close_room_when_close_stream"]
                    self.console.print(f"Close Room When Stream Ends {'Enabled' if self.config['close_room_when_close_stream'] else 'Disabled'}.")
                elif choice == "6":
                    self.create_stream()
                elif choice == "7":
                    self.save_configuration()
                elif choice == "8":
                    self.load_configuration()
                elif choice == "9":
                    logging.info("Exiting...")
                    break
            else:
                self.console.print("Invalid option. Please try again.", style="bold red")

    def select_game(self):
        game_tags = self.get_game_hashtags()
        if game_tags:
            for idx, (name, id) in enumerate(game_tags, start=1):
                self.console.print(f"{idx}. {name} - {id}")
            choice = int(prompt("Select a game by number: ")) - 1
            if 0 <= choice < len(game_tags):
                selected_game = game_tags[choice]
                self.config["game_tag_id"] = selected_game[1]
                self.console.print(f"Selected game: {selected_game[0]}")
            else:
                logging.error("Invalid selection.")
        else:
            logging.error("Failed to fetch games.")

    def get_game_hashtags(self):
        try:
            response = self.session.get(self.game_list_url)
            response.raise_for_status()
            data = response.json()
            game_tag_list = data.get('data', {}).get('game_tag_list', [])
            return [(game.get('full_name'), game.get('id')) for game in game_tag_list]
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            return []
        except json.JSONDecodeError:
            logging.error("Failed to parse JSON response")
            return []

    def create_stream(self):
        url = "https://webcast16-normal-c-useast2a.tiktokv.com/webcast/room/create/"
        params = {"aid": "8311"}
        headers = {
            "Cookie": f"sid_guard={self.config['sid_guard_cookie']}",
            "User-Agent": "Your User-Agent Here"
        }
        response = self.session.post(url, params=params, json=self.config, headers=headers)
        try:
            response.raise_for_status()
            stream_info = response.json()
            if stream_info:
                logging.info("Stream created successfully.")
                logging.info(f"Stream URL: {stream_info['data']['stream_url']['rtmp_push_url']}")
                logging.info(f"Share URL: {stream_info['data']['share_url']}")
        except requests.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}")

    def save_configuration(self):
        if not os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'w') as file:
                json.dump(self.config, file, indent=4)
            logging.info("Configuration saved.")
        else:
            with open(self.config_file_path, 'w') as file:
                json.dump(self.config, file, indent=4)
            logging.info("Configuration updated.")

    def load_configuration(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r') as file:
                self.config = json.load(file)
            logging.info("Configuration loaded.")
        else:
            logging.error("No configuration file found. Creating a new one.")
            self.save_configuration()

if __name__ == "__main__":
    configurator = StreamConfigurator()
    configurator.start()
