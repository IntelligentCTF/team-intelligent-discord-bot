import discord
from discord.ext import commands
from discord import ApplicationContext, ForumTag, Thread, ForumChannel, PartialEmoji

# We use these tags for thread filtering
TAGS = [
    ForumTag(name="Web Exploitation", emoji=PartialEmoji(name="🌐")),
    ForumTag(name="Cryptography", emoji=PartialEmoji(name="🔑")),
    ForumTag(name="Forensics", emoji=PartialEmoji(name="💽")),    
    ForumTag(name="Reverse Engineering", emoji=PartialEmoji(name="🔄")),
    ForumTag(name="Binary Exploitation", emoji=PartialEmoji(name="📝")),
    ForumTag(name="OSINT", emoji=PartialEmoji(name="🔍")),
    ForumTag(name="Miscellaneous", emoji=PartialEmoji(name="⁉️")),
    ForumTag(name="Solved", emoji=PartialEmoji(name="✅")),
]

# Additional semantic mappings to the above tags
# ie: "web" == "web exploitation"
CATEGORY_MAPPING = {
    "web": "Web Exploitation",
    "web exploitation": "Web Exploitation",
    "crypto": "Cryptography",
    "cryptography": "Cryptography",
    "steganography": "Cryptography",
    "forensics": "Forensics",
    "reverse engineering": "Reverse Engineering",
    "re": "Reverse Engineering",
    "binary exploitation": "Binary Exploitation",
    "pwn": "Binary Exploitation",
    "binex": "Binary Exploitation",
    "binexp": "Binary Exploitation",
    "osint": "OSINT",
    "open source intelligence": "OSINT",
    "solved": "Solved"
}

def get_category_tag(category: str, forum: ForumChannel):
    category = category.lower()
    target_name = CATEGORY_MAPPING.get(category, "Miscellaneous")
    
    for tag in forum.available_tags:
        if tag.name == target_name:
            return tag
            
    # Fallback to Miscellaneous if target tag not found
    print(f"Miscellaneous: {category}")
    return next(tag for tag in forum.available_tags if tag.name == "Miscellaneous")

class Solver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="solved", description="Mark a thread as solved.")
    async def solved(self, ctx: ApplicationContext):
        # Check if the command is being used in a thread
        if not isinstance(ctx.channel, Thread):
            await ctx.respond("This command can only be used in a thread!", ephemeral=True)
            return
            
        thread = ctx.channel
        parent = thread.parent
        
        # Check if the parent channel is a forum and in the Competitions category
        if not isinstance(parent, ForumChannel) or parent.category.name != "Competitions":
            await ctx.respond("This command can only be used in competition threads!", ephemeral=True)
            return
            
        # Get the solved tag
        solved_tag = get_category_tag("solved", parent)
        
        # Get current tags and add solved tag if not already present
        current_tags = list(thread.applied_tags)
        if solved_tag not in current_tags:
            current_tags.append(solved_tag)
            
        # Update thread name and tags
        try:
            new_name = thread.name if thread.name.startswith("solved-") else f"solved-{thread.name}"
            await thread.edit(
                name=new_name,
                applied_tags=current_tags
            )
            await ctx.respond("Thread marked as solved! 🎉")
        except Exception as e:
            await ctx.respond(f"Failed to mark thread as solved: {str(e)}", ephemeral=True)

def setup(bot):
    bot.add_cog(Solver(bot)) 