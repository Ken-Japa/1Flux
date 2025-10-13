import sys
import os

# Adicionar o diretório 'src' ao PYTHONPATH
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
sys.path.insert(0, project_root)

from src.utils.data_storage import (
    init_db,
    insert_brief,
    get_briefs_by_client,
    insert_client_profile,
    get_client_profile,
    get_all_briefs,
    update_brief_feedback,
    export_all_briefs_to_json,
    update_client_profile
)

if __name__ == '__main__':
    init_db()
    export_all_briefs_to_json()