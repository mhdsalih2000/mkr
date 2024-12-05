class SimpleLogger:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    RESET = '\033[0m'
    ORANGE = '\033[38;5;214m'  
    def log(self, level, message):
        if level == "INFO":
            print(f"{self.GREEN}[INFO]{self.RESET} {message}")
        elif level == "WARNING":
            print(f"{self.YELLOW}[WARNING]{self.RESET} {message}")
        elif level == "ERROR":
            print(f"{self.RED}[ERROR]{self.RESET} {message}")
        elif level == "VD0":
            print(f"{self.CYAN}VD0 PUBLISHED{self.RESET} {message}")
        elif level == "CRITICAL":
            print(f"{self.MAGENTA}[CRITICAL]{self.RESET} {message}")
        elif level == "SUCCESS":
            print(f"{self.BLUE}CONNECTION ESTABLISHED{self.RESET} {message}")
        elif level == "INPROGRESS":
            print(f"{self.ORANGE}IN PROGRESS{self.RESET} {message}") 
        elif level == "VD1":
            print(f"{self.GREEN}VD1 PUBLISHED{self.RESET} {message}")  
        else:
            print(message)  


