import discord
from discord.ext import commands, tasks
import aiohttp
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import os
from typing import List, Dict
import re
from . import helpers

class CTFTimeCalendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "data/ctftime.db"
        self.ensure_db_exists()
        self.check_ctftime.start()
        
    def ensure_db_exists(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                title TEXT,
                start_date TEXT,
                end_date TEXT,
                format TEXT,
                url TEXT,
                ctftime_url TEXT,
                weight REAL,
                location TEXT,
                onsite BOOLEAN,
                restrictions TEXT,
                description TEXT,
                posted_date TEXT
            )
        ''')
        conn.commit()
        conn.close()
        
    def is_event_posted(self, event_id: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT 1 FROM events WHERE event_id = ?', (event_id,))
        result = c.fetchone() is not None
        conn.close()
        return result
        
    def save_event(self, event: Dict):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO events (
                event_id, title, start_date, end_date, format, url, 
                ctftime_url, weight, location, onsite, restrictions, description, posted_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event['id'],
            event['title'],
            event['start_date'],
            event['end_date'],
            event['format'],
            event['url'],
            event['ctftime_url'],
            event['weight'],
            event.get('location', ''),
            event['onsite'],
            event['restrictions'],
            event.get('description', ''),
            datetime.now(timezone.utc).isoformat()
        ))
        conn.commit()
        conn.close()
        
    def is_this_week(self, start_date: datetime) -> bool:
        now = datetime.now(timezone.utc)
        monday = now - timedelta(days=now.weekday())
        sunday = monday + timedelta(days=6)
        monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)
        sunday = sunday.replace(hour=23, minute=59, second=59, microsecond=999999)
        return monday <= start_date <= sunday
        
    def create_event_embed(self, event: Dict) -> discord.Embed:
        start_date = helpers.parse_ctftime_date(event['start_date'])
        end_date = helpers.parse_ctftime_date(event['end_date'])
        
        embed = discord.Embed(
            title=event['title'],
            url=f"https://ctftime.org{event['ctftime_url']}",
            description=event.get('description', 'No description available.'),
            color=discord.Color.blue(),
            timestamp=start_date
        )
        
        # Format duration
        duration = end_date - start_date
        hours = duration.total_seconds() / 3600
        duration_str = f"{int(hours)} hours" if hours < 24 else f"{int(hours/24)} days"
        
        embed.add_field(name="Format", value=event['format'], inline=True)
        embed.add_field(name="Weight", value=f"{event['weight']:.2f}", inline=True)
        embed.add_field(name="Duration", value=duration_str, inline=True)
        
        if event['onsite']:
            embed.add_field(name="Location", value=event['location'], inline=True)
        else:
            embed.add_field(name="Type", value="Online", inline=True)
            
        embed.add_field(name="Restrictions", value=event['restrictions'], inline=True)
        
        if event['url']:
            embed.add_field(name="Official URL", value=event['url'], inline=False)
            
        embed.set_footer(text="Data from CTFtime.org")
        
        return embed
        
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
    
                    onsite = item.find('onsite').text.lower() == 'true'
                    restrictions = item.find('restrictions').text or 'Unknown'
    
                    # Filter: skip if onsite or not open
                    if onsite or restrictions.lower() != 'open':
                        continue
    
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
                        'onsite': onsite,
                        'restrictions': restrictions
                    }
    
                    # Make sure event is this year, if not, skip
                    if helpers.parse_ctftime_date(event['start_date']).year != datetime.now().year:
                        print(f"[CTFTime] Skipping event {event['title']} - it's for {helpers.parse_ctftime_date(event['start_date']).year}")
                        continue
    
                    events.append(event)
    
                return events
                
    @tasks.loop(hours=24)
    async def check_ctftime(self):
        try:
            events = await self.fetch_ctftime_events()
            
            channel = discord.utils.get(self.bot.get_all_channels(), name='ctftime')
            if not channel:
                print("Could not find `#ctftime` channel")
                return

            # Get current week's date range
            now = datetime.now(timezone.utc)
            monday = now - timedelta(days=now.weekday())
            sunday = monday + timedelta(days=6)
            
            # Format dates in a nice way
            date_format = "%B %d, %Y"  # Example: January 01, 2024
            week_range = f"CTFs for the week of {monday.strftime(date_format)} - {sunday.strftime(date_format)}"
            
            events_this_week = []
            for event in events:
                # Skip if already posted
                if self.is_event_posted(event['id']):
                    continue
                    
                # Check if event is this week
                start_date = helpers.parse_ctftime_date(event['start_date'])
                if not self.is_this_week(start_date):
                    continue
                
                # Fetch event description
                description = await helpers.fetch_event_description(event['id'])
                # Truncate for Discord embed
                description = helpers.truncate_description(description, max_length=1000)
                event['description'] = description
                events_this_week.append(event)

            if events_this_week:
                # Send the header message first
                await channel.send(f"🚩 **{week_range}** 🚩")
                
                # Then send all event embeds
                for event in events_this_week:
                    embed = self.create_event_embed(event)
                    await channel.send(embed=embed)
                    self.save_event(event)
                
        except Exception as e:
            print(f"Error in CTFtime calendar check: {str(e)}")
            
    @check_ctftime.before_loop
    async def before_check_ctftime(self):
        await self.bot.wait_until_ready()
        
    # force check ctftime
    @commands.slash_command(name="ctftime")
    async def ctftime(self, ctx: discord.ApplicationContext):
        await self.check_ctftime()
        
def setup(bot):
    bot.add_cog(CTFTimeCalendar(bot))
