import subprocess


class ReactCreator:

    @staticmethod
    def create(
        name: str,
        typescript: str = "typescript",
        selected_addons: list = [],
    ) -> None:

        cmd = ["npx", "create-next-app@latest", name]

        if typescript == "typescript":
            cmd.append("--typescript")
        else:
            cmd.append("--js")

        if "eslint" in selected_addons:
            cmd.append("--eslint")
        else:
            cmd.append("--no-eslint")

        if "tailwindcss" in selected_addons:
            cmd.append("--tailwind")
        else:
            cmd.append("--no-tailwind")

        if "src_directory" in selected_addons:
            cmd.append("--src-dir")
        else:
            cmd.append("--no-src-dir")

        if "app_router" in selected_addons:
            cmd.append("--app")
        else:
            cmd.append("--pages")

        if "turbopack" in selected_addons:
            cmd.append("--turbopack")

        cmd.extend(["--import-alias", "'@/*'"])
        cmd.append("--yes")

        subprocess.run(
            " ".join(cmd),
            text=True,
            capture_output=True,
            shell=True,
        )
