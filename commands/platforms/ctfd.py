import discord
from discord.ext import commands
from discord import option, ApplicationContext, ForumTag, AllowedMentions, Embed, Color, PartialEmoji, ForumChannel, Thread
import aiohttp
import asyncio
from .general import TAGS, get_category_tag

class CTFd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="ctfd", description="Create a thread for a CTF competition")
    @option("name", description="Name of the CTF competition")
    @option("ctfd_url", description="URL of the CTFd instance (e.g., https://demo.ctfd.io)")
    @option("token", description="Your CTFd API token")
    async def ctf(self, ctx: ApplicationContext, name: str, ctfd_url: str, token: str):
        
        # Defer the response since this might take a while
        await ctx.defer(ephemeral=True)
        
        # Remove trailing slash from URL if present
        ctfd_url = ctfd_url.rstrip('/')
        
        # Headers for API requests
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Create the competition thread in the Competitions category
            competitions_channel = discord.utils.get(ctx.guild.categories, name="Competitions")
            if not competitions_channel:
                await ctx.followup.send("Error: Couldn't find the 'Competitions' category. Please create it first.", ephemeral=True)
                return        
                
            forum = await competitions_channel.create_forum_channel(
                name=f"{name}",
                topic=f"CTF Competition: {name}",
                reason=f"CTF Competition: {name}"
            )        
            
            # Create tags for the forum channel 
            forum = await forum.edit(available_tags=TAGS)
            
            # Fetch challenges from CTFd
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{ctfd_url}/api/v1/challenges", headers=headers) as response:
                    if response.status != 200:
                        await ctx.followup.send(f"Error: Failed to fetch challenges. Status code: {response.status}", ephemeral=True)
                        return
                        
                    data = await response.json()
                    if not data.get('success'):
                        await ctx.followup.send("Error: Failed to fetch challenges from CTFd", ephemeral=True)
                        return
                        
                    challenges = data.get('data', [])                    
                    
                    # Create a thread for each challenge
                    for challenge in challenges:
                                                
                        embed = Embed(
                            title=challenge['name'],
                            url=f"{ctfd_url}/challenges#{challenge['id']}",
                            color=Color.blue()
                        )
                        
                        # Add challenge details
                        embed.add_field(name="Category", value=get_category_tag(challenge['category'], forum), inline=True)
                        embed.add_field(name="Points", value=str(challenge['value']), inline=True)                        
                        
                        # Add tags if available
                        async with session.get(f"{ctfd_url}/api/v1/challenges/{challenge['id']}/tags", headers=headers) as tags_response:
                            if tags_response.status == 200:
                                tags_data = await tags_response.json()
                                if tags_data.get('success'):
                                    tags = tags_data.get('data', [])
                                    if tags:
                                        tag_names = [tag['value'] for tag in tags]
                                        embed.add_field(name="Tags", value=", ".join(tag_names), inline=False)
                        
                        # Get challenge description
                        async with session.get(f"{ctfd_url}/api/v1/challenges/{challenge['id']}", headers=headers) as challenge_response:
                            if challenge_response.status == 200:
                                challenge_data = await challenge_response.json()
                                if challenge_data.get('success'):
                                    description = challenge_data.get('data', {}).get('description', '')
                                    embed.description = description
                                                     
                        thread = await forum.create_thread(
                            name=challenge['name'],
                            embed=embed,
                            reason=f"CTF Challenge: {challenge['name']}",
                            applied_tags=[get_category_tag(challenge['category'], forum)],
                            allowed_mentions=AllowedMentions(
                                everyone=True,
                                users=True,
                                roles=True,
                                replied_user=True
                            )
                        )
                        
                        # Add a small delay to avoid rate limiting
                        await asyncio.sleep(1)
            
            await ctx.followup.send(f"Successfully created CTF thread with {len(challenges)} challenges!", ephemeral=True)
            
        except Exception as e:
            await ctx.followup.send(f"Error: {str(e)}", ephemeral=True)

def setup(bot):
    bot.add_cog(CTFd(bot)) 