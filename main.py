from fincore.bootstrap.builder import ApplicationBuilder


def main() -> None:
    controller = ApplicationBuilder().build()
    controller.run()