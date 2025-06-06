import discord
from discord.ext import commands
from discord import option, ApplicationContext, ForumTag, AllowedMentions, Embed, Color, PartialEmoji, ForumChannel, Thread
import aiohttp
import asyncio
from .general import TAGS, get_category_tag

class rCTF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="rctf", description="Create a thread for a rCTF competition")
    @option("name", description="Name of the CTF competition")
    @option("rctf_url", description="URL of the rCTF instance with team token (e.g., https://rctf.io/)")
    @option("token", description="Bearer token for the rCTF instance")
    async def rctf(self, ctx: ApplicationContext, name: str, rctf_url: str, token: str):
        
        # Defer the response since this might take a while
        await ctx.defer(ephemeral=True)
        
        # Remove trailing slash from URL if present
        rctf_url = rctf_url.rstrip('/')
        
        # Headers for API requests
        headers = {
            'Authorization': f'Bearer {token}',
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
            
            # Fetch challenges from rCTF
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{rctf_url}/api/v1/challs", headers=headers) as response:
                    if response.status != 200:
                        await ctx.followup.send(f"Error: Failed to fetch challenges. Status code: {response.status}", ephemeral=True)
                        return
                        
                    data = await response.json()
                    if not data.get('kind') == 'goodChallenges':
                        await ctx.followup.send("Error: Failed to fetch challenges from rCTF", ephemeral=True)
                        return
                        
                    # "data":[{"files":[],"description":"I made this site where you can upload profile pictures, if you happen to embed caption metadata within your image, I'll try displaying it on your profile page.\n\n[Instancer](https://instancer.tjctf.org/challenge/hidden-canvas)","author":"ansh","points":482,"id":"hidden-canvas","name":"hidden-canvas","category":"web","sortWeight":0,"solves":7}]
                    challenges = data.get('data', [])                    
                    
                    # Create a thread for each challenge
                    for challenge in challenges:
                                                
                        embed = Embed(
                            title=challenge['name'],
                            url=f"{rctf_url}/challenges#{challenge['id']}",
                            color=Color.blue()
                        )
                        
                        # Add challenge details
                        embed.add_field(name="Category", value=get_category_tag(challenge['category'], forum), inline=True)
                        embed.add_field(name="Points", value=str(challenge['points']), inline=True)     
                        embed.description = challenge['description']
                                                     
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
    bot.add_cog(rCTF(bot)) 