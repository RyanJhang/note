import asyncio
import flet as ft

class Countdown(ft.UserControl):
    def __init__(self, seconds):
        super().__init__()
        self.seconds = seconds

    async def did_mount_async(self):
        self.running = True
        asyncio.create_task(self.update_timer())

    async def will_unmount_async(self):
        self.running = False

    async def update_timer(self):
        while self.seconds and self.running:
            mins, secs = divmod(self.seconds, 60)
            self.countdown.value = "{:02d}:{:02d}".format(mins, secs)
            await self.update_async()
            await asyncio.sleep(1)
            self.seconds -= 1

    def build(self):
        self.countdown = ft.Text()
        return self.countdown

async def main(page: ft.Page):
    await page.add_async(Countdown(120), Countdown(60))

ft.app(target=main)