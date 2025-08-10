import re
from datetime import datetime

import requests
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, ListItem, ListView, Static

GITHUB_API = "https://api.github.com"


class RepoStats(Static):

    def get_date(self, date_str):
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        now = datetime.now()
        diff = now - date
        days = diff.days
        if days == 0:
            if diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f"{minutes} minutes ago"
            else:
                hours = diff.seconds // 3600
                return f"{hours} hours ago"
        elif days < 30:
            return f"{days} days ago"
        elif days < 365:
            months = days // 30
            return f"{months} months ago"
        else:
            years = days // 365
            return f"{years} years ago"

    def update_stats(self, stats):
        created = self.get_date(stats["created_at"])
        updated = self.get_date(stats["updated_at"])

        self.update(
            f"⭐ Stars: {stats['stargazers_count']}\n"
            f"👀 Watchers: {stats['subscribers_count']}\n"
            f"🍴 Forks: {stats['forks_count']}\n"
            f"💻 Commits: {stats.get('commits_count', 'N/A')}\n"
            f"🐞 Open Issues: {stats['open_issues_count']}\n"
            f"📅 Created: {created}\n"
            f"🔄 Updated: {updated}\n"
        )


class StatsScreen(Screen):
    def compose(self):
        with Vertical(classes="left-group"):
            with Container(classes="username"):
                yield Input(placeholder="Enter GitHub username...", id="username_input")
            with Horizontal(classes="buttons"):
                yield Button("Fetch Repos", variant="primary", id="fetch")
                yield Button("Back", id="back")
        with Vertical(classes="right-group"):
            yield Static("Repositories :", classes="addon-label")
            yield ListView(id="repo_list")
            yield RepoStats(id="repo_stats")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "fetch":
            username = self.query_one("#username_input", Input).value.strip()
            await self.fetch_repos(username)
        elif event.button.id == "back":
            self.app.pop_screen()

    async def fetch_repos(self, username):
        self.app.notify("Fetching repositories...")
        repo_list = self.query_one("#repo_list", ListView)
        repo_list.clear()
        self.query_one("#repo_stats", RepoStats).update()
        
        resp = requests.get(f"{GITHUB_API}/users/{username}/repos")
        if resp.status_code == 200:
                repos = [repo for repo in resp.json() if not repo["fork"]]
                if repos:
                    for repo in repos:
                        id = repo["name"].replace(".", "_").replace("-", "_")
                        repo_list.append(
                            ListItem(Static(repo["name"]), id=id)
                        )
                    repo_list.focus()
                else:
                    self.app.notify("User has no repositories", severity="warning")
                    repo_list.append(
                        ListItem(Static("No repositories found!"), id="empty")
                    )
        else:
                self.app.notify(resp.json()["message"], severity="error")
                repo_list.append(
                    ListItem(Static("User not found or error!"), id="error")
                )

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        repo_name = event.item.children[0].render()
        username = self.query_one("#username_input", Input).value.strip()
        if repo_name and repo_name not in ["User not found or error!", "No repositories found!"]:
            resp = requests.get(f"{GITHUB_API}/repos/{username}/{repo_name}")
            if resp.status_code == 200:
                    stats = resp.json()
                    commits_resp = requests.get(
                        f"{GITHUB_API}/repos/{username}/{repo_name}/commits",
                        params={"per_page": 100},
                    )
                    if commits_resp.status_code == 200:
                        total_commits = 0
                        if "Link" in commits_resp.headers:
                            links = commits_resp.headers["Link"].split(",")
                            last_link = [l for l in links if 'rel="last"' in l][0]
                            page_match = re.search(r"page=(\d+)", last_link)
                            if page_match:
                                last_page = int(page_match.group(1))
                                total_commits = (last_page - 1) * 100 + len(
                                    commits_resp.json()
                                )
                        else:
                            total_commits = len(commits_resp.json())

                        stats["commits_count"] = total_commits
                    self.query_one("#repo_stats", RepoStats).update_stats(stats)
            else:
                    self.query_one("#repo_stats", RepoStats).update(
                        "Repo not found or error!"
                    )
