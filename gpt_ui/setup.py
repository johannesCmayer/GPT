#!/usr/bin/env python

from pathlib import Path
import tempfile

from xdg_base_dirs import xdg_config_home
import openai
import yaml
import argparse
import tiktoken

from gpt_ui.util import timestamp
from gpt_ui.gpt_ui import converse

class Conf:
    def __init__(self):
        self.project_dir = Path(__file__).parent.absolute()

        self.config_dir = xdg_config_home() / 'gpt-ui'
        self.config_file = self.config_dir / "config.yaml"
        self.config_file_local = self.config_dir / "config_local.yaml"
        
        self.config = yaml.load(self.config_file.open(), yaml.FullLoader)
        # Load local config file and overwrite default config
        if self.config_file_local.exists():
            self.config.update(yaml.load(self.config_file_local.open(), yaml.FullLoader))
        openai.api_key = yaml.load((self.config_dir / 'api_key.yaml').open(), yaml.FullLoader).get('api_key')

        # Loading config
        self.model = self.config['default_model']
        self.user = self.config['user']
        self.models_dict = yaml.load((self.project_dir / 'models_metadata.yaml').open(), yaml.FullLoader)
        self.max_tokens = self.models_dict[self.model]['max_tokens']
        self.speak_default = self.config['speak']

        # Setting up paths 2/2
        if self.config["chat_dir"] is not None:
            chat_dir = Path(self.config["chat_dir"]).expanduser()
            if not chat_dir.exists():
                raise FileNotFoundError(f"Chat directory {chat_dir} does not exist.")
        else:
            chat_dir = self.project_dir / "chats"
            chat_dir.mkdir(exist_ok=True)

        chat_dir.mkdir(exist_ok=True)
        self.chat_dir = chat_dir

        # Setting up Paths and looading config 1/2


        self.chat_backup_file = chat_dir / f".backup_{timestamp()}.json"

        prompt_history_dir =  Path(tempfile.mkdtemp())
        self.prompt_history_dir = prompt_history_dir

        self.prompt_dir = self.project_dir / 'prompts'

        voice_precache_dir = Path(tempfile.mkdtemp())
        self.voice_precache_dir = voice_precache_dir

        obsidian_vault_dir = Path(self.config['obsidian_vault_dir']).expanduser()
        if not obsidian_vault_dir.exists():
            raise FileNotFoundError(f"Obsidian vault directory {obsidian_vault_dir} does not exist.")
        self.obsidian_vault_dir = obsidian_vault_dir

        try:
            self.enc = tiktoken.encoding_for_model(self.model)
        except KeyError as e:
            print(f"WARNING: Could not determine encoder for {self.model}. Falling back to gpt-4 encoder.")
            self.enc = tiktoken.encoding_for_model('gpt-4')


        # Parsing Arguments
        parser = argparse.ArgumentParser(description=
            "Press CTRL+C to stop generating the message. "
            "In user role press CTRL+D to exit the chat. You will first be asked to save the chat. "
            "Press CTRL+D in the safe dialog to exit the program without saving the chat. "
            "\n\n"
            "During a chat session there are a number of runtime commands you can enter as the user role. Enter 'help' as the "
            "user role to see all available runtime commands."
            "\n\n"
            "You can use :file:FILENAME: to show the contents of FILENAME to GPT, while in the UI the text will "
            "not be expanded. Similarly you can use :obsidian:FILENAME: in order to search the obsidian vault "
            "(needs to be configured in config.yaml) for the file FILENAME and show the contents to GPT.")
        parser.add_argument('--chat-name', type=str, help='Name of the chat')
        parser.add_argument('--load-chat', type=str, help='Name of the chat to load')
        parser.add_argument('--load-last-chat', action='store_true', help='Name of the chat to load')
        parser.add_argument('--list-chats', action='store_true', help='List all chats')
        parser.add_argument('--list-all-chats', action='store_true', help='List all chats including hidden backup chats')
        parser.add_argument('--list-models', action='store_true', help='List all models')
        parser.add_argument('--list-models-full', action='store_true', help='List all models and their details')
        parser.add_argument('--speak', default=self.speak_default, action='store_true', help='Speak the messages.')
        parser.add_argument('-p', '--personality', default='default', type=str, choices=[x.stem for x in self.prompt_dir.iterdir()], help='Set the system prompt based on predefined file.')
        parser.add_argument('--config', action='store_true', help='Open the config file.')
        parser.add_argument('--debug', action='store_true', help='Run with debug settings. Includes notifications.')
        parser.add_argument('--export-chats-to-markdown', action='store_true', help='Re export all named chats as markdown files into the chat directory.')
        parser.add_argument('user_input',  type=str, nargs='*', help='Initial input the user gives to the chat bot.')
        args = parser.parse_args()
        if args.user_input == []:
            args.user_input = None
        else:
            args.user_input = " ".join(args.user_input)
            if args.user_input == "":
                args.user_input = None

        self.args = args

        self.assistant_name = 'assistant'

    def cleanup(self):
        self.prompt_history_dir.cleanup()
        self.voice_precache_dir.cleanup()

def main():
    conf = Conf()
    converse(conf)
    conf.cleanup()