from app import Application, MenuWindow

if __name__ == "__main__":
    menu = MenuWindow(title = "Simulador - Configurações")
    menu.build()
    menu.run()

    if not menu.closed:
        process_scheduler = menu.get_process_scheduler()
        memory_manager = menu.get_memory_manager()

        application = Application(title = f"Simulador - {process_scheduler.name} Algorithm")
        application.build()
        application.run(process_scheduler, memory_manager, generate_log_file = True)
