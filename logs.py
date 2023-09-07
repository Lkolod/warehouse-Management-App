import logging

class logging2(logging.Handler):
    def __init__(self, filename, max_entries):
        super().__init__()
        self.filename = filename
        self.max_entries = max_entries
    
    def emit(self, record):
        log_lines = self.get_log_lines()
        
        if len(log_lines) >= self.max_entries:
            log_lines.pop(-1)  
        
        log_lines.insert(0, self.format(record) + '\n')
        with open(self.filename, 'w', encoding="utf-8") as f:
            f.writelines(log_lines)
    
    def get_log_lines(self):
        try:
            with open(self.filename, 'r') as f:
                return f.readlines()
        except FileNotFoundError:
            return []