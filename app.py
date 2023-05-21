from app import Application, MenuWindow

if __name__ == "__main__":
    menu = MenuWindow()
    menu.build()
    menu.run()

    if not menu.closed:
        algorithm, quantum, switching = menu.get_config()

        application = Application()
        application.build()
        print(algorithm, quantum, switching)
        application.run(algorithm, quantum, switching)
