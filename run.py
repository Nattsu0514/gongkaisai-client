import sunrise

if __name__ == '__main__':
    sunrise.init()
    sunrise.plugin_manager.load_all_plugin("plugins")
    sunrise.run()
