from .app import DevTools


def main():
    app = DevTools()
    app.run(headless=False)


if __name__ == "__main__":
    main()
