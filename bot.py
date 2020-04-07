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
        assign_rooms()
        #start_timer(game.game_round)



class Player():
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.room = Room('2r-entry-room')
        self.leader = False
        self.card = None
    ##def color
    
   
class Room():
    def __init__(self, room_name):
        self.room_name = room_name
        #if room_name == '2r-room-1':
            #self.room_id = 
        #elif room_name == '2r-room-a':
            #self.room_id = 
        
    

class Rounds():
    def __init__(self, round_number, hostages, time):
        self.round_number = round_number
        self.hostages = hostages
        self.time = time
        
    
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='2r ')
client.remove_command('help')
client.case_insensitive = True

current_card_list = []
player_list = []
rounds = []
game = Game()
general_room = Room('2r-entry-room')
room_1 = Room('2r-room-1')
room_2 = Room('2r-room-a')



##Need to make sure this still works when switching to bot
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord and is ready!')


#converting to bot commands
@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.orange()
    )
    embed.set_author(name="Help")
    embed.add_field(name='**Anytime:**', value='__Commands you can use anytime.__', inline=False)
    embed.add_field(name='2r currentcards', value='shows the cards in the current deck', inline=False)
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
    embed.add_field(name='2r vote @user', value='votes for a new leader for your room.  If no vote has started yet then it begins a new vote.  Majority wins, *I love democracy*', inline=False)
    embed.add_field(name='2r revealall', value='reveals your card to everyone in your room - you maniac, you', inline=False)
    await ctx.message.channel.send(embed=embed)

@client.command(name='currentcards')
async def current_cards(ctx):
    response = 'Available cards to add to current list:\n'
    response += show(cl.available_cards)
    await ctx.message.channel.send(response)


@client.command(name='exit')
async def current_cards(ctx):
    response = ('Thank you for playing')
    await message.channel.send(response)
    exit()
"""@client.event
async def on_message(message):
    if message.author == client.user:
        return
 

    response = ''
    
    ##Commands anytime
    
    if message.content == '2r exit':
        response = ('Thank you for playing')
        await message.channel.send(response)
        exit()
    elif(message.content == '2r available cards'):
        response = 'Available cards to add to current list:\n'
        response += show(cl.available_cards)
        await message.channel.send(response)
        
        
    

    ##Commands before game
    if(game.started == False):
        if('2r addcard' in message.content):
            word_list = message.content.split()
            card_name = word_list[-1]
            if(cl.add_card(card_name,current_card_list) == False):
                response = ('Invalid card name, to see available cards type **2r available cards**')
                await message.channel.send(response)
            response = f'You can currently play a game with %i people\n' % len(current_card_list)
            response += '__Current Cards:__\n'
            response+=show(current_card_list)
            await message.channel.send(response)
        
        elif('2r removecard' in message.content):
            word_list = message.content.split()
            card_name = word_list[-1]
            if(cl.remove_card(card_name,current_card_list) == False):
                response = ('Invalid card name, to see the current cards type **2r show**')
                await message.channel.send(response)
            response = f'You can currently play a game with %i people\n' % len(current_card_list)
            response += '__Current Cards:__\n'
            response += show(current_card_list)
            await message.channel.send(response)

        ##To more easily manage games, this sets up a default with the President, Bomber, Engineer, Doctor, Red Teamx2, Blue Teamx2, and Gambler
        elif message.content == '2r default' and game.started == False:
            default_cards = ['President','Engineer','Blue_Spy','Blue_Shy_Guy','Blue_Team','Gambler']
            for card in default_cards:
                cl.add_card(card,current_card_list)
            response = f'You can currently play a game with %i people\n' % len(current_card_list)        
            response += '__Current Cards:__\n'
            response += show(current_card_list)
            await message.channel.send(response)
        
        elif('2r currentcards' in message.content):
            response = f'You can currently play a game with %i people\n' % len(current_card_list)
            response += '__Current Cards in the deck:__\n'
            response += show(current_card_list)
            await message.channel.send(response)
    
    
        ##########STARTS THE GAME################################
        elif(message.content == '2r start' and game.started == False):
            global player_list
            for channel in client.guilds[0].voice_channels:
                if(channel.name == '2r-entry-room'):
                    print(channel.name)
                    for member in channel.members:
                        player_list.append(Player(member.display_name, member.id))
            response = '__Players in game:__\n'
            for player in player_list:
                response += player.name + '\n'
            random.shuffle(player_list)
            random.shuffle(current_card_list)
            print(player_list)
            if(len(player_list) != len(current_card_list)):
                response = 'The player list does not match the number of cards.  Please add or remove cards as necessary.';
                player_list = []
            else:
                game.start_game()
        
            await message.channel.send(response)
        
        elif('2r' in message.content):
            await message.channel.send('Invalid command, please see **2r help** for list of commands')
            

    if(game.game_started == True and game.in_round == True):
        if(
        elif('2r' in message.content):
            await message.channel.send('Invalid command, please see **2r help** for list of commands')
    
    #During Game but not During Round
    if(game.game_started == True):
        if(message.content == '2r start'):
            await message.channel.send('Game is in progress, type **2r exit** to stop or **2r help** to view available commands')
        elif('2r' in message.content):
            await message.channel.send('Invalid command, please see **2r help** for list of commands')    
    
    
"""        
        
        
    

def show(card_list):
    response = ''
    for card in card_list:
        response += '**' + card.name + '**: ' + 'this card is on the ' + card.team + ' team.  ' + card.description + '\n'
    return response
        
        

    
##the cards and players are already randomly shuffled, so this just gives the players their cards
def deal_cards():
    for i in range(0,len(player_list)):
        player_list[i].card = current_card_list[i]
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
        
        
        
def assign_rooms():
    for i in range(0,len(player_list)):
        if i % 2 == 0:
            player_list[i].room = '2r-room-1'
        else:
            player_list[i].room = '2r-room-a'
        print(f'{player_list[i].name} is in room {player_list[i].room}')
        
def change_room(player_name):
    player_room = player_list[player_list.index(player_name)].room
    if player_room == '2r-room-1':
        player_room == '2r-room-a'
    elif player_room == '2r-room-a':
        player_room == '2r-room-1'
    else:
        print('Unknown Room ' + player_room)
        return 'Unknown Room'
    return player_room
        

##TODO start_timer
##TODO get_player_list
##implement changing room roles
##move to voice channel
##game loop?
##round loops?
##leader voting
##change leader
##end of round with movement between rooms


client.run(TOKEN)

client.logout()