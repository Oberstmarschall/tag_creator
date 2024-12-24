from tag_creator.utils import shell


class Git():

    def __init__(self, repo_dir="."):
        self.repo_dir = repo_dir


    def tag(self, args: str = "") -> shell.subprocess.CompletedProcess:
        return self.__git_cmd(f"tag {args}")

    def rev_list(self, args: str = "") -> shell.subprocess.CompletedProcess:
        return self.__git_cmd(f"rev-list {args}")

    def push(self, reference: str = "") -> shell.subprocess.CompletedProcess:
        return self.__git_cmd(f"push origin {reference}")

    def log(self, args: str = "") -> shell.subprocess.CompletedProcess:
        return self.__git_cmd(f"log {args}")

    def __git_cmd(self, cmd: str) -> shell.subprocess.CompletedProcess:
        return shell.exec(f"git -C {self.repo_dir} {cmd}")
