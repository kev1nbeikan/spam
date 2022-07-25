def check_file_name(name: str):
    if '/' in name:
        return False
    return name.endswith('.json') or name.endswith('.session')
