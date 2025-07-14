class Archiver:
    archiver = None

    def __init__(self):
        self.reset()

    def run(self):
        self.state = "Running"
        self.path = "cr_scraper/static/archive.json"

    def status(self):
        return self.state

    def reset(self):
        self.state = "Waiting"
        self.path = ""
        self._progress = 0

    def archive_file(self):
        return self.path

    def progress(self):
        return self._progress

    @classmethod
    def get(cls):
        if cls.archiver:
            if cls.archiver.status() == "Running":
                if cls.archiver._progress < 1:
                    cls.archiver._progress += 0.1
                    cls.archiver._progress = round(cls.archiver._progress, 1)
                else:
                    cls.archiver.state = "Complete"
            return cls.archiver
        archiver = Archiver()
        cls.archiver = archiver
        return archiver


if __name__ == "__main__":
    Archiver.archiver
    arch_1 = Archiver.get()
    arch_2 = Archiver.get()
    arch_1.run()
    assert arch_1.status() == arch_2.status()
    assert arch_1 is arch_2
