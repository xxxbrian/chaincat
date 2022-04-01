from discord.ext import tasks
import discord
from src.config import CHANNELID
from src.job import run_jobs

class Mybot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # channel IDs goes here
        self.channels = None

        # start the task to run in the background
        self.warning_message.start()
        self.status_message.start()

    async def on_ready(self):
        print(f'Login with {self.user.name}({self.user.id})')
        self.channels=[self.get_channel(id) for id in CHANNELID]

    @tasks.loop(minutes=5) # task runs every 5 minutes
    async def warning_message(self):
        print('Task: warning_message')
        resp = run_jobs()
        if resp['status']:
            await self.send_to_all(resp['msg'])
    
    @tasks.loop(hours=6) # task runs every 6 hours
    async def status_message(self):
        print('Task: status_message')
        resp = run_jobs()
        print(resp['msg'])
        await self.send_to_all(resp['msg'])

    @status_message.before_loop
    @warning_message.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

    async def send_to_all(self,msg:str):
        for channel in self.channels:
            await channel.send(msg)
        
if __name__ == '__main__':
    bot = Mybot()
    bot.run('OTU1NDAxODA5OTEwOTgwNjM5.YjhJRQ.WfFcACpX3JWjXPvIDEj46vIFDiM')