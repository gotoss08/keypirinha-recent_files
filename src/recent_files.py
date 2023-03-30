# Keypirinha launcher (keypirinha.com)

import keypirinha as kp
import keypirinha_util as kpu
import keypirinha_net as kpnet

import os
from pathlib import Path

class recent_files(kp.Plugin):
    """
    Quick open recent files or folders
    """

    def __init__(self):
        super().__init__()

    def on_catalog(self):
        self.set_catalog([self.create_item(
            category=kp.ItemCategory.KEYWORD,
            label='Open recent',
            short_desc='Open recent file or directory',
            target='open_recent',
            args_hint=kp.ItemArgsHint.REQUIRED,
            hit_hint=kp.ItemHitHint.IGNORE)])

    def on_suggest(self, user_input, items_chain):
        if not items_chain or items_chain[-1].category() != kp.ItemCategory.KEYWORD:
            return

        recent_files = self.get_recent_files()

        suggestions = []

        for f in recent_files:
            suggestions.append(self.create_item(
                category=kp.ItemCategory.FILE,
                label=f.name,
                short_desc=f._str,
                target=f._str,
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.IGNORE))

        self.set_suggestions(suggestions, kp.Match.FUZZY, kp.Sort.NONE)

    def on_execute(self, item, action):
        if item:
            kpu.shell_execute(item.target())

    def get_recent_files(self):
        
        recent_files_path = Path(f"{os.getenv('AppData')}/Microsoft/Windows/Recent/")
        
        if not recent_files_path.exists():
            return []

        files = ((f.stat().st_atime, f) for f in recent_files_path.iterdir() if f.is_file())

        recent_files = []

        for cdate, f in sorted(files, reverse=True):
            recent_files.append(f)

        return recent_files
