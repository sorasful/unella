from rich.progress import Progress


class ProgressBar:
    def __init__(self, total_steps: int):
        self.progress = Progress()
        self.total_steps = total_steps

    def start(self):
        with self.progress:
            task = self.progress.add_task("[green]Processing...", total=self.total_steps)
            for step in range(self.total_steps):
                yield step
                self.progress.update(task, advance=1)
