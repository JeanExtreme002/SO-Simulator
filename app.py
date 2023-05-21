from app import Application, MenuWindow

if __name__ == "__main__":
    menu = MenuWindow(title = "Simulador - Configurações")
    menu.build()
    menu.run()

    if not menu.closed:
        algorithm, quantum = menu.get_config()

        application = Application(title = f"Simulador - {algorithm.name} Algorithm")
        application.build()
        application.run(algorithm, quantum)
