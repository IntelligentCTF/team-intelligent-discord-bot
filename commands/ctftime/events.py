import discord
from discord.ext import commands, tasks
import aiohttp
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import os
from typing import List, Dict
import re
from . import helpers

class CTFEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "data/events.db"
        self.ensure_db_exists()
        self.create_events.start()
        
    def ensure_db_exists(self):
        """Create the database and events table if they don't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS discord_events (
                event_id TEXT PRIMARY KEY,
                discord_event_id TEXT,
                title TEXT,
                start_date TEXT,
                end_date TEXT,
                url TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()
        conn.close()
        
    def is_event_created(self, event_id: str) -> bool:
        """Check if a Discord event has already been created for this CTF"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT 1 FROM discord_events WHERE event_id = ?', (event_id,))
        result = c.fetchone() is not None
        conn.close()
        return result
        
    def save_event(self, event: Dict, discord_event_id: str):
        """Save the created Discord event to the database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO discord_events (
                event_id, discord_event_id, title, start_date, end_date, url, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            event['id'],
            discord_event_id,
            event['title'],
            event['start_date'],
            event['end_date'],
            f"https://ctftime.org{event['ctftime_url']}",
            datetime.now(timezone.utc).isoformat()
        ))
        conn.commit()
        conn.close()
        
    async def fetch_ctftime_events(self) -> List[Dict]:
        """Fetch and parse CTFtime RSS feed"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://ctftime.org/event/list/upcoming/rss/') as response:
                if response.status != 200:
                    return []
                    
                content = await response.text()
                root = ET.fromstring(content)
                
                events = []
                for item in root.findall('.//item'):
                    ctftime_url = item.find('ctftime_url').text
                    event_id = re.search(r'/event/(\d+)', ctftime_url).group(1)
                    
                    event = {
                        'id': event_id,
                        'title': item.find('title').text,
                        'start_date': item.find('start_date').text,
                        'end_date': item.find('finish_date').text,
                        'format': item.find('format_text').text,
                        'url': item.find('url').text,
                        'ctftime_url': ctftime_url,
                        'weight': float(item.find('weight').text or 0),
                        'location': item.find('location').text or '',
                        'onsite': item.find('onsite').text.lower() == 'true',
                        'restrictions': item.find('restrictions').text or 'Unknown'
                    }
                    
                    # Make sure event is this year, if not, skip
                    if helpers.parse_ctftime_date(event['start_date']).year != datetime.now().year:
                        print(f"[CTFTime] Skipping event {event['title']} - it's for {helpers.parse_ctftime_date(event['start_date']).year}")
                        continue
                    
                    events.append(event)
                    
                return events

    @tasks.loop(hours=24)
    async def create_events(self):
        """Create Discord events for CTF competitions and update Google Sheets"""
        try:
            events = await self.fetch_ctftime_events()
            
            # Update Google Sheets first
            await helpers.update_ctf_spreadsheet(events)
            
            for event in events:
                # Skip if already created
                if self.is_event_created(event['id']):
                    print(f"[Discord Event] Skipping creating for {event['title']} - already created")
                    continue
                
                # Get full description
                description = await helpers.fetch_event_description(event['id'])
                description = helpers.truncate_description(description, max_length=800)
                
                # Parse dates
                start_time = helpers.parse_ctftime_date(event['start_date'])
                end_time = helpers.parse_ctftime_date(event['end_date'])
                
                # Create event description
                full_description = (
                    f"🚩 {event['title']}\n\n"
                    f"Weight: {event['weight']:.2f}\n"
                    f"{'Location: ' + event['location'] if event['onsite'] else 'Type: Online'}\n"
                    f"Restrictions: {event['restrictions']}\n\n"
                    f"Description:\n{description}\n\n"
                    f"Official URL: {event['url']}"
                )
                
                for guild in self.bot.guilds:
                        
                    try:
                        print(f"[Discord Event] Creating event {event['title']} in guild {guild.name}")
                        discord_event = await guild.create_scheduled_event(
                            name=event['title'],
                            description=full_description,
                            start_time=start_time,
                            end_time=end_time,
                            location=f"https://ctftime.org{event['ctftime_url']}"
                        )
                        
                        # Save to database
                        self.save_event(event, str(discord_event.id))
                        print(f"[Discord Event] Created event for {event['title']}")
                        
                    except Exception as e:
                        print(f"[Discord Event] Error creating event in guild {guild.name}: {str(e)}")
                
        except Exception as e:
            print(f"[Discord Event] Error in CTF events creation: {str(e)}")
            
    @create_events.before_loop
    async def before_create_events(self):
        """Wait until the bot is ready before starting the loop"""
        await self.bot.wait_until_ready()
        
    # Command to force event creation
    @commands.slash_command(name="create_ctf_events")
    async def create_ctf_events(self, ctx: discord.ApplicationContext):
        """Force creation of Discord events for CTF competitions"""
        await ctx.defer()
        await self.create_events()
        await ctx.followup.send("Created Discord events for upcoming CTFs!", ephemeral=True)

    # Add command to force spreadsheet update
    @commands.slash_command(name="update_ctf_sheet")
    async def update_ctf_sheet(self, ctx: discord.ApplicationContext):
        """Force update of the CTF events spreadsheet"""
        await ctx.defer()
        events = await self.fetch_ctftime_events()
        await helpers.update_ctf_spreadsheet(events)
        await ctx.followup.send("Updated CTF events spreadsheet!", ephemeral=True)

def setup(bot):
    bot.add_cog(CTFEvents(bot)) 