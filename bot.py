# bot.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands
import CardList as cl
import asyncio




    

class Game():
    def __init__(self):
        self.started = False
        self.game_round = 0
        self.in_round = False

    def start_game(self):
        self.in_round = True
        self.started = True
        setup_rounds(len(player_list))
        self.game_round=1
        deal_cards()
        #start_timer(game.game_round)

class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        ##Not sure what this next thing is
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()


class Player():
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.card = None
        for room in voice_rooms:
            if(room.name == '2r-entry-room'):
                self.voice_rooms = room
        for room in text_rooms:
            if(room.name == '2r-entry-room'):
                self.text_rooms = room
        

class Rounds():
    def __init__(self, round_number, hostages, time):
        self.round_number = round_number
        self.hostages = hostages
        self.time = time
        
class Room():
    def __init__(self, room_id, room_name): 
        self.id = room_id
        self.leader = None
        self.name = room_name
        
    
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='2r ')
client.remove_command('help')
client.case_insensitive = True

current_deck = []
current_card_list = []
player_list = []
rounds = []
game = Game()
voice_rooms = []
text_rooms = []
room_roles = []


#general_room = Room('2r-entry-room')
#room_1 = Room('2r-room-1')
#room_2 = Room('2r-room-a')
#roles are RoomA and Room1


##Need to make sure this still works when switching to bot
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord and is ready!')
    for channel in client.guilds[0].voice_channels:
        if(channel.name.startswith('2r')):
            voice_rooms.append(Room(channel.id,channel.name))
    for channel in client.guilds[0].text_channels:
        if(channel.name.startswith('2r')):
            text_rooms.append(Room(channel.id,channel.name))
    for role in client.guilds[0].roles:
        if(role.name == 'RoomA' or role.name == 'Room1'):
            room_roles.append(role)

#converting to bot commands
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )
    embed.set_author(name="Help")
    embed.add_field(name='**Anytime:**', value='__Commands you can use anytime.__', inline=False)
    embed.add_field(name='2r availablecards', value='shows the cards available in the game, you can add these to the deck', inline=False)
    embed.add_field(name='2r currentdeck', value='shows the cards in the current deck', inline=False)
    embed.add_field(name='2r exit', value='if you or I fucks up you can exit the game with this', inline=False)
    embed.add_field(name='**Before Game:**', value='__Commands you can use before the game starts.__', inline=False)
    embed.add_field(name='2r addcard <card>', value='adds the given card to the game.\n\tIf there are cards linked to this it automatically adds those.\tFor Example, if I add a Red Team, then a Blue Team is also added', inline=False)
    embed.add_field(name='2r removecard <card>', value='this removes a card from the game.\n\tIf there are cards linked to this it automatically removes those.\tFor Example, if I remove a Red Team, then a Blue Team is also removed', inline=False)
    embed.add_field(name='2r default', value='this command automatically adds the President, Bomber, Engineer, Doctor, Blue_Shy_Guy, Red_Shy_Guy, Blue_Spy, Red_Spy, Red_Team, Blue_Team, and Gambler', inline=False)
    embed.add_field(name='2r clear', value='this command automatically clears out all of the cards in the current deck', inline=False)
    embed.add_field(name='2r start', value='begins the game', inline=False)
    embed.add_field(name='**During a round**', value='__Commands you can use during the round.__', inline=False)
    embed.add_field(name='2r color @user', value='reveals the color of your card to the user specified, make sure you ask them if they want to color reveal with you.', inline=False)
    embed.add_field(name='2r full @user', value='fully reveals your card with user you specify, make sure you ask them if they want to fully reveal cards with you.', inline=False)
    embed.add_field(name='2r usurp @user', value='votes for @user to be the new leader for your room.  If no vote has started yet then it begins a new vote.  Majority wins, *I love democracy*', inline=False)
    embed.add_field(name='2r revealall', value='reveals your card to everyone in your room - you maniac, you', inline=False)
    await ctx.message.channel.send(embed=embed)


@client.command(name='exit')
async def exit_command(ctx):
    response = ('Thank you for playing')
    ##revert to original roles & move back to original voice channel
    for i in range(0,len(player_list)):
        member = client.guilds[0].get_member(player_list[i].id)
        for role in member.roles:
            if role.name.startswith('Room'):
                await member.remove_roles(role, reason='Exiting 2r Game')
        await member.move_to(voice_rooms[0])
    
    await client.get_channel(text_rooms[0].id).send(response)
    await client.logout()
    
    
@client.command(name='availablecards')
async def available_cards_command(ctx):
    response = 'Available cards to add to current list:\n'
    response += show(cl.available_cards)
    await ctx.message.channel.send(response)

@client.command(name='currentdeck')
async def current_deck_command(ctx):
    response = f'You can currently play a game with %i people\n' % len(current_card_list)
    response += '__Current Cards in the deck:__\n'
    response += show(current_card_list)
    await ctx.message.channel.send(response)

    
@client.command(name='addcard')
async def addcard_command(ctx):
    if(game.started == False):
        word_list = ctx.message.content.split()
        card_name = word_list[-1]
        if(cl.add_card(card_name,current_card_list) == False):
            response = ('Invalid card name, to see available cards type **2r available cards**')
            await ctx.message.channel.send(response)
        response = f'You can currently play a game with %i people\n' % len(current_card_list)
        response += '__Current Cards:__\n'
        response+=show(current_card_list)
        await ctx.message.channel.send(response)
    else:
        response = 'You can\'t add cards to the deck while the game is in progress.'
        await ctx.message.channel.send(response)
        
        
@client.command(name='removecard')
async def removecard_command(ctx):
    if(game.started == False):
        word_list = message.content.split()
        card_name = word_list[-1]
        if(cl.remove_card(card_name,current_card_list) == False):
            response = ('Invalid card name, to see the current cards type **2r show**')
            await ctx.message.channel.send(response)
        response = f'You can currently play a game with %i people\n' % len(current_card_list)
        response += '__Current Cards:__\n'
        response += show(current_card_list)
        await ctx.message.channel.send(response)
    else:
        response = 'You can\'t remove cards from the deck while the game is in progress.'
        await ctx.message.channel.send(response)

@client.command(name='default')
async def default_command(ctx):
    if(game.started == False):
        default_cards = ['President','Engineer','Blue_Spy','Blue_Shy_Guy','Blue_Team','Gambler']
        for card in default_cards:
            cl.add_card(card,current_card_list)
        response = f'You can currently play a game with %i people\n' % len(current_card_list)        
        response += '__Current Cards:__\n'
        response += show(current_card_list)
        await ctx.message.channel.send(response)
    else:
        response = 'You can\'t add cards to the deck while the game is in progress.'
        await ctx.message.channel.send(response)

@client.command(name='start')
async def start_command(ctx):
    if(game.started == False):
        global player_list
        global current_deck
        for channel in client.guilds[0].voice_channels:
            if(channel.name == '2r-entry-room'):
                print(channel.name)
                print(channel.members)
                for member in channel.members:
                    print(member)
                    player_list.append(Player(member.display_name, member.id))
        print(player_list)
        response = '__Players in game:__\n'
        for player in player_list:
            response += player.name + '\n'
        random.shuffle(player_list)
           
        ##TODO, let's create a new variable for the shuffled cards, that way no one can call current deck and see the shuffle (players are also shuffled so this probably won't be an issue
        current_deck = random.sample(current_card_list, len(current_card_list))
        if(len(player_list) != len(current_card_list)):
            response = 'The player list does not match the number of cards.  Please add or remove cards as necessary.';
            player_list = []
        elif(len(player_list) == 0):
            response = 'There are no players, you can\'t start the game without players.  Everyone needs to join the **2r-entry-room voice channel** to play.'
        else:
            game.start_game()
            await message_cards()
            await assign_rooms()
            warning_timer = Timer(rounds[0].time * 60 - 30, warning_callback)
            timer = Timer(rounds[0].time * 60, timeout_callback)
            response+= f'''\nRound 1 has started, you have {rounds[0].time} minutes before the round ends.  You have been messaged your cards and assigned to your rooms.\nThe first person to use **2r appoint @user**
            appoints that @user as the initial leader.'''
        await client.get_channel(text_rooms[1].id).send(response)
        await client.get_channel(text_rooms[2].id).send(response)
    else:
        response = 'Game is already in progress, type **2r help** to view available commands or **2r exit** to stop the game'
        await ctx.message.channel.send(response)

@client.command(name='appoint')
async def appoint(ctx):
    ##can only appoint if game is going
    if(game.started == False or game.in_round == False):
        response = 'Game and round must have started to use this command\n'
        await ctx.message.channel.send(response)
        return

    
    user_not_found = True
    word_list = ctx.message.content.split()
    
    ##If they enter it correctly, the @ sign makes the user a member id, so I guess no @ sign for now!!!
    designated_appointee = word_list[-1]
    appointee = None
    
    for member in ctx.channel.members:
        if(member.name == designated_appointee):
            user_not_found = False
            appointee = member
            break
           
    for room in text_rooms:    

        if(room.id == ctx.message.channel.id):
            if(room.leader is not None):
                response = 'You can only appoint when no one is the leader\n'
                await ctx.message.channel.send(response)
                return
            room.leader = appointee
            response = f'The new leader of {client.get_channel(room.id)} is {room.leader.name}'            
    if(user_not_found == True):
        response = '@User not in your room, try again'
    await ctx.message.channel.send(response)
    
    
@client.command(name='usurp')
async def usurp(ctx):
    ##can only vote if game is going
    if(game.started == False or game.in_round == False):
        response = 'Game and round must have started to use this command\n'
        await ctx.message.channel.send(response)
        return

    
    user_not_found = True
    word_list = ctx.message.content.split()
    
    ##If they enter it correctly, the @ sign makes the user a member id, so I guess no @ sign for now!!!
    designated_appointee = word_list[-1]
    appointee = None
    
    for member in ctx.channel.members:
        if(member.name == designated_appointee):
            user_not_found = False
            appointee = member
            break
           
    for room in text_rooms:    

        if(room.id == ctx.message.channel.id):
            if(room.leader is not None):
                response = 'You can only appoint when no one is the leader\n'
                await ctx.message.channel.send(response)
                return
            room.leader = appointee
            response = f'The new leader of {client.get_channel(room.id)} is {room.leader.name}'            
    if(user_not_found == True):
        response = '@User not in your room, try again'
    await ctx.message.channel.send(response)
    
@client.event
async def message():
    print(f'{client.user.name} has connected to Discord and is ready!')
    for channel in client.guilds[0].voice_channels:
        if(channel.name.startswith('2r')):
            voice_rooms.append(Room(channel.id,channel.name))
    for channel in client.guilds[0].text_channels:
        if(channel.name.startswith('2r')):
            text_rooms.append(Room(channel.id,channel.name))
    for role in client.guilds[0].roles:
        if(role.name == 'RoomA' or role.name == 'Room1'):
            room_roles.append(role)            
                
        
        
async def message_cards():
    for player in player_list:
        user = client.get_user(player.id)
        response = f'Welcome to the {player.card.team} team!  You have the **{player.card.name}** card. {player.card.description}.  Good luck!'
        await user.send(response)    
        await user.send(file=discord.File(player.card.image))

def show(card_list):
    response = ''
    for card in card_list:
        response += '**' + card.name + '**: ' + 'this card is on the ' + card.team + ' team.  ' + card.description + '\n'
    return response
        
    
##the cards and players are already randomly shuffled, so this just gives the players their cards
##message player what card they have
def deal_cards():
    for i in range(0,len(player_list)):
        print(f'i: {i}, player_list {player_list} current_deck {current_deck}')
        player_list[i].card = current_deck[i]
        print(player_list[i].name + ' has card ' + player_list[i].card.name)
        
        
    
    
##There are different round times and hostages depending on how many players are playing
def setup_rounds(player_count):
    if(player_count <= 10):
        for i in range(0,3):
            rounds.append(Rounds(i + 1, 1, 3 - i))
    elif(player_count >= 11 and player_count <= 13):
        for i in range(0,2):
            rounds.append(Rounds(i + 1, 5 - i))
        for i in range(2,5):
            rounds.append(Rounds(i + 1, 1, 5 - i))
    elif(player_count >= 14 and player_count <= 17):
        rounds[0].append(Rounds(0 + 1, 3, 5))
        for i in range(1,3):
            rounds.append(Rounds(i + 1, 2, 5 - i))
        for i in range(3,5):
            rounds.append(Rounds(i + 1, 1, 5 - i))            
    elif(player_count >= 18 and player_count <= 21):
        for i in range(0,5):
            rounds.append(Rounds(i + 1, 5 - i))
    for round_num in rounds:
        print(f'\nRound: {round_num.round_number} \nTime: {round_num.time} \nHostages: {round_num.hostages}') 

async def timeout_callback():
    await asyncio.sleep(0.1)
    print('Timer ran out.')
    game.in_round = False
    await text_rooms[1].send("Time is up, leaders choose your hostages by typing @user.")
    await text_rooms[2].send("Time is up, leaders choose your hostages by typing @user.")

    

async def warning_callback():
    await asyncio.sleep(0.1)
    await text_rooms[1].send("45 seconds remaining, leaders be ready to choose your hostage(s).")
    await text_rooms[2].send("45 seconds remaining, leaders be ready to choose your hostage(s).")
    
    
##TODO assign permissions to certain rooms and also move players to a particular room
async def assign_rooms():
    for i in range(0,len(player_list)):
        member = client.guilds[0].get_member(player_list[i].id)
        if i % 2 == 0:
            player_list[i].room = '2r-room-1'
            for role in room_roles:
                if role.name == 'Room1':
                    await member.add_roles(role, reason='Starting game')
            await member.move_to(voice_rooms[1])
        else:
            player_list[i].room = '2r-room-a'
            for role in room_roles:
                if role.name == 'RoomA':
                    await member.add_roles(role, reason='Starting game')
            await member.move_to(voice_rooms[2])
        print(f'{player_list[i].name} is in room {player_list[i].room}')
        
def change_room(player):
    player_room = player.room
    if player_room == '2r-room-1':
        player_room == '2r-room-a'
    elif player_room == '2r-room-a':
        player_room == '2r-room-1'
    else:
        print('Unknown Room ' + player_room)
        return 'Unknown Room'
    return player_room
        
##TODO Let's have calling exit stop the game and reset stuff if a game is in-progress
##TODO have timer change to end of round, send Time's Up message
##move to voice channel
##game loop? No I'll just use a flag, should be fine in this instance
##round loops?  No I'll just use a flag, should be fine in this instance
##leader voting
##change leader
##end of round with movement between rooms


client.run(TOKEN)
