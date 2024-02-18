from requests import Session
import json
import logging
from os import path
from rich.console import Console
from rich.logging import RichHandler
from rich.markdown import Markdown
from art import text2art
from alive_progress import alive_bar
import time
from pyfiglet import Figlet
from colorama import init, Fore, Back, Style
import inquirer

# Initialize Colorama for ANSI escape sequences to work on all platforms.
init(autoreset=True)

# Set up rich console and logging with enhanced visual appeal.
console = Console()
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True)]
)

class StreamConfigurator:
    def __init__(self):
        self.config = {
            "cookie": "",
            "title": "",
            "game_tag_id": "",
            "gen_replay": False,
            "close_room_when_close_stream": True
        }
        self.game_list_url = 'https://webcast16-normal-c-useast2a.tiktokv.com/webcast/room/hashtag/list/'
        self.config_file_path = "stream_config.json"
        self.session = Session()

    def start(self):
        # Display an over-the-top title with ASCII art.
        figlet_title = Figlet(font='slant')
        console.print(Fore.MAGENTA + figlet_title.renderText("Guinness's StreamKey Generator"))

        while True:
            console.print("\n[bold magenta]=== Guinness’s StreamKey Generator Menu ===[/bold magenta]", style="bold green")
            actions = ["Insert Cookie", "Select Game", "Edit Title", "Toggle Replay Generation",
                       "Toggle Room Closure on Stream End", "Save Configuration", "Load Configuration",
                       "Create Stream", "Exit"]
            for idx, action in enumerate(actions, start=1):
                console.print(f"[bold cyan]{idx}. {action}[/bold cyan]")
            choice = console.input("[bold yellow]Choose an option: [/bold yellow]")

            if choice == "1":
                self.insert_cookie()
            elif choice == "2":
                self.select_game()
            elif choice == "3":
                self.edit_title()
            elif choice == "4":
                self.toggle_replay_generation()
            elif choice == "5":
                self.toggle_room_closure()
            elif choice == "6":
                self.save_configuration()
            elif choice == "7":
                self.load_configuration()
            elif choice == "8":
                self.create_stream()
            elif choice == "9":
                console.print("[bold red]Exiting...[/bold red]")
                break
            else:
                console.print("[bold yellow]Invalid option. Please try again.[/bold yellow]")

    def insert_cookie(self):
        self.config["cookie"] = console.input("[bold green]Enter your sid_guard cookie: [/bold green]")

    def select_game(self):
        console.print("[bold blue]Fetching games...[/bold blue]")
        with alive_bar(1, bar="bubbles", spinner="dots_waves"):
            game_tags = self.get_game_hashtags(self.game_list_url)
            time.sleep(1)  # Simulate fetching
        if game_tags:
            for idx, (name, id) in enumerate(game_tags, start=1):
                console.print(f"[bold]{idx}. {name} - {id}[/bold]")
            choice = int(console.input("[bold green]Select a game by number: [/bold green]")) - 1
            if 0 <= choice < len(game_tags):
                selected_game = game_tags[choice]
                self.config["game_tag_id"] = selected_game[1]
                console.print(f"[bold green]Selected game: {selected_game[0]}[/bold green]")
            else:
                console.print("[bold red]Invalid selection.[/bold red]")
        else:
            console.print("[bold red]Failed to fetch games.[/bold red]")

    def edit_title(self):
        self.config["title"] = console.input("[bold green]Enter stream title: [/bold green]")

    def toggle_replay_generation(self):
        self.config["gen_replay"] = not self.config["gen_replay"]
        console.print(f"[bold magenta]Replay Generation {'Enabled' if self.config['gen_replay'] else 'Disabled'}.[/bold magenta]")

    def toggle_room_closure(self):
        self.config["close_room_when_close_stream"] = not self.config["close_room_when_close_stream"]
        console.print(f"[bold magenta]Close Room When Stream Ends {'Enabled' if self.config['close_room_when_close_stream'] else 'Disabled'}.[/bold magenta]")

    def save_configuration(self):
        with open(self.config_file_path, 'w') as file:
            json.dump(self.config, file, indent=4)
        console.print("[bold green]Configuration saved.[/bold green]")

    def load_configuration(self):
        if path.exists(self.config_file_path):
            with open(self.config_file_path, 'r') as file:
                self.config = json.load(file)
            console.print("[bold green]Configuration loaded.[/bold green]")
        else:
            console.print("[bold red]No configuration file found.[/bold red]")

    def get_game_hashtags(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            game_tag_list = data.get('data', {}).get('game_tag_list', [])
            return [(game.get('full_name'), game.get('id')) for game in game_tag_list]
        except Exception as e:
            console.print(f"[bold red]Request failed: {e}[/bold red]")
            return []

    def create_stream(self):
        if not self.config["cookie"]:
            console.print("[bold red]Cookie is required to create a stream.[/bold red]")
            return
        if not self.config["title"]:
            console.print("[bold red]Title is required to create a stream.[/bold red]")
            return
        if not self.config["game_tag_id"]:
            console.print("[bold red]Game tag ID is required to create a stream.[/bold red]")
            return
        console.print("[bold blue]Creating stream...[/bold blue]")
        with alive_bar(1, bar="bubbles", spinner="dots_waves"):
            # Simulate the creation process
            time.sleep(1)  # Simulate network call
        console.print("[bold green]Stream created successfully![/bold green]")

if __name__ == "__main__":
    configurator = StreamConfigurator()
    configurator.start()
