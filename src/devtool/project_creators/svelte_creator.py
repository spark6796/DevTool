import subprocess

from config import svelte_addons


class SvelteCreator:

    @staticmethod
    def create(
        name: str,
        template: str = "demo",
        typescript: str = "typescript",
        selected_addons: list = [],
    ) -> str:

        types_map = {"typescript": "ts", "javascript": "jsdoc"}

        cmd = ["npx", "sv", "create", name]
        cmd.append(f"--template={template}")
        cmd.append(f"--types={types_map[typescript]}")
        cmd.append("--no-add-ons")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            shell=True,
        )

        if result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode, cmd, result.stdout, result.stderr
            )

        if selected_addons:

            for addon in selected_addons:
                if addon in svelte_addons and svelte_addons[addon]:
                    install_cmd = f"npm install -D {svelte_addons[addon]}"
                    addon_result = subprocess.run(
                        install_cmd,
                        shell=True,
                        cwd=name,
                        capture_output=True,
                        text=True,
                    )

                    if addon_result.returncode != 0:
                        print(f"Warning: Failed to install {addon}")

        return result
