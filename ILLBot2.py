# ILL Bot 2 Source Code Release
# This source code is licensed under a Creative Commons Attribution 4.0 International License.
# For more details see https://creativecommons.org/licenses/by/4.0/

#ILL Bot 2

#IMPORTS

import discord
import asyncio
import re
from time import gmtime, strftime
import datetime
from random import randint
import sqlite3
import sys

#CONFIGURATION

version = "v0.1.0"
date = datetime.date



#ROLE VARIABLES
#Team Staff
rHC = None #Head Coaches
rAC = None #Assistant Coaches
rFO = None #Franchise Owners

#Server Staff
rCO = None #Commissioner
rBA = None #Bae
rCOw = None #Co-Owner
rCC = None #Co-CEOs
rDI = None #Directors
rOV = None #Overseers

#Server Assistants
rBO = None #Bot
rIN = None #Initiate
rRF = None #Referee
rSC = None #SportsCenter Crew
rEC = None #ESPN Crew

#Players
rFA = None #Free Agent

#Server
sILL = None #Server

#Contract Channel
cCon = None #Contracts
cPro = None #Promotions


client = discord.Client()
illDb = sqlite3.connect("ill.db") #one database, multiple tables
now = datetime.datetime.now()

#TABLES:
#xp: id|value
#pval: id|value
#tmoney: id|value
#contracts: id|value|weeks

#STARTUP

@client.event
async def on_ready():
    print("ILL Bot 2 Source is now loading...")
    print("Username: " + client.user.name)
    print("User ID: " + client.user.id)
    print("API Version: " + discord.__version__)

    #Set bot status
    await client.change_presence(game=discord.Game(name="tell feven to work his minecraft"))

    #Check existance of Player Value table
    c = illDb.cursor()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='pval'")
    if c.fetchone()[0] == 1:
        c.close()
        print("Player Value table has been found!")
    else:
        print("Player Value table not found!")
        c.execute("CREATE TABLE pval(id TEXT, value INT)")
        illDb.commit()
        c.close()
        print("Player Value table has been created.")

    #Check existance of Team Money table
    c = illDb.cursor()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='tmoney'")
    if c.fetchone()[0] == 1:
        c.close()
        print("Team Money table has been found!")
    else:
        print("Team Money table not found!")
        c.execute("CREATE TABLE tmoney(id TEXT, value INT)")
        illDb.commit()
        c.close()
        print("Team Money table has been created.")

    #Check existance of Contract table
    c = illDb.cursor()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' and name='contracts'")
    if c.fetchone()[0] == 1:
        c.close()
        print("Contract table has been found!")
    else:
        print("Contract table not found!")
        c.execute("CREATE TABLE contracts(id TEXT, value INT, weeks INT, signweek INT, endweek INT, team TEXT)")
        illDb.commit()
        c.close()
        print("Contract table has been created.")

    #Initiate role search
    global rHC
    global rAC
    global rFO
    global rCO
    global rBA
    global rCOw
    global rCC
    global rDI
    global rOV
    global rBO
    global rIN
    global rRF
    global rSC
    global rEC
    global rFA
    global sILL
    sILL = discord.utils.find(lambda a: a.id == '473221683952746496', client.servers)
    rHC = discord.utils.find(lambda b: b.name == 'Head Coach', sILL.roles)
    rAC = discord.utils.find(lambda c: c.name == 'Assistant Coach', sILL.roles)
    rFO = discord.utils.find(lambda d: d.name == 'Franchise Owner', sILL.roles)
    rCO = discord.utils.find(lambda e: e.name == 'Commissioner', sILL.roles)
    rBA = discord.utils.find(lambda f: f.name == 'Bae', sILL.roles)
    rCOw = discord.utils.find(lambda g: g.name == 'Co-Owner', sILL.roles)
    rCC = discord.utils.find(lambda h: h.name == 'Co-CEOs', sILL.roles)
    rDI = discord.utils.find(lambda i: i.name == 'Directors', sILL.roles)
    rOV = discord.utils.find(lambda j: j.name == 'Overseers', sILL.roles)
    rBO = discord.utils.find(lambda k: k.name == 'Bot', sILL.roles)
    rIN = discord.utils.find(lambda l: l.name == 'Initiate', sILL.roles)
    rRF = discord.utils.find(lambda m: m.name == 'Referee', sILL.roles)
    rSC = discord.utils.find(lambda n: n.name == 'SportsCenter Crew', sILL.roles)
    rEC = discord.utils.find(lambda o: o.name == 'ESPN Crew', sILL.roles)
    rFA = discord.utils.find(lambda p: p.name == 'Free Agents', sILL.roles)
    print("Roles have been loaded.")
    print("Searching for contracts channel...")
    
    # Source note: All variables for settings are set here.
    global cCon
    cCon = discord.utils.find(lambda q: q.id == '488407155616251936', sILL.channels)
    print("Contract channel has been found.")
    print("Searching for promotions channel...")
    global cPro
    cPro = discord.utils.find(lambda q: q.id == '494632859768979471', sILL.channels)
    print("Promotions channel has been found.")

    print("Bot startup is complete.")

#MESSAGE PROCESSOR

@client.event
async def on_message(message):
    if message.author.bot is False:

        #ABSTRACTIONS

        #DATABASE PROCESSING


        if re.match(r"!\btestweek\b", message.content, re.IGNORECASE):
            d = await curWeek()
            await client.send_message(message.channel, "current week: " + str(d))

        #Pval GET
        async def getPval(id):
            c = illDb.cursor()
            p = (id, )
            o = []
            for row in c.execute("SELECT value FROM pval WHERE id = ?", p):
                o.append(list(row))
            if not o:
                return("250")
            else:
                return(int(o[0][0]))

        #Tmoney GET
        async def getTmoney(id):
            c = illDb.cursor()
            p = (id, )
            o = []
            for row in c.execute("SELECT value FROM tmoney WHERE id = ?", p):
                o.append(list(row))
            if not o:
                return("null")
            else:
                return(int(o[0][0]))

        #Cont GET
        async def getCont(id):
            c = illDb.cursor()
            p = (id, )
            o = []
            for row in c.execute("SELECT * FROM contracts WHERE id = ?", p):
                o.append(list(row))
            if not o:
                return("null")
            else:
                print(o)
                return([int(o[0][1]), int(o[0][2]), str(o[0][3]), str(o[0][4]), str(o[0][5])]) #SHOULD BE WORKING?

        #Pval SET
        async def setPval(id, value):
            c = illDb.cursor()
            p = (id, )
            i = (id, value)
            u = (value, id)
            o = []
            for row in c.execute("SELECT value FROM pval WHERE id = ?", p):
                o.append(list(row))
            if not o:
                c.execute("INSERT INTO pval VALUES(?, ?)", i)
                illDb.commit()
                c.close()
            else:
                c.execute("UPDATE pval SET value = ? WHERE id = ?", u)
                illDb.commit()
                c.close

        #Tmoney SET
        async def setTmoney(id, value):
            c = illDb.cursor()
            p = (id, )
            i = (id, value)
            u = (value, id)
            o = []
            for row in c.execute("SELECT value FROM tmoney WHERE id = ?", p):
                o.append(list(row))
            if not o:
                c.execute("INSERT INTO tmoney VALUES(?, ?)", i)
                illDb.commit()
                c.close()
            else:
                c.execute("UPDATE tmoney SET value = ? WHERE id = ?", u)
                illDb.commit()
                c.close

        #Cont SET


        #Pval ADD
        async def addPval(id, value):
            c = illDb.cursor()
            x = await getPval(id)
            i = (id, )
            a = (id, value) #new value
            n = x + value
            u = (n, id)
            o = []
            for row in c.execute("SELECT value FROM pval WHERE id = ?", i):
                o.append(list(row))
            if not o:
                c.execute("INSERT INTO pval VALUES(?, ?)", a)
                illDb.commit()
                c.close()
            else:
                c.execute("UPDATE pval SET value = ? WHERE id = ?", u)
                illDb.commit()
                c.close()

        #Tmoney ADD
        async def addTmoney(id, value):
            c = illDb.cursor()
            x = await getTmoney(id)
            i = (id, )
            a = (id, value) #new value
            n = x + value
            u = (n, id)
            o = []
            for row in c.execute("SELECT value FROM tmoney WHERE id = ?", i):
                o.append(list(row))
            if not o:
                c.execute("INSERT INTO tmoney VALUES(?, ?)", a)
                illDb.commit()
                c.close()
            else:
                c.execute("UPDATE tmoney SET value = ? WHERE id = ?", u)
                illDb.commit()
                c.close()

        async def getInts(s):
            return(re.findall("[-\d]+", s))

      
        #COMMANDS

        if re.match(r"!\bkill\b", message.content, re.IGNORECASE):
            if message.channel.permissions_for(message.author).administrator:
                sys.exit("Bot force closed by user " + message.author.name + " " + message.author.id)

        if re.match(r"!\bstaff\b", message.content, re.IGNORECASE):
            if len(message.raw_role_mentions) == 1:
                tHC = ""
                tFO = ""
                tAC = ""
                for member in message.server.members:
                    if rHC in [role for role in member.roles] and message.role_mentions[0] in [role for role in member.roles]:
                        tHC = member.mention
                    if rFO in [role for role in member.roles] and message.role_mentions[0] in [role for role in member.roles]:
                        tFO = member.mention
                    if rAC in [role for role in member.roles] and message.role_mentions[0] in [role for role in member.roles]:
                        tAC = member.mention
                await client.send_message(message.channel, "Franchise Owner: " + tFO + "\nHead Coach: " + tHC + "\nAssistant Coach: " + tAC)
            else:
                await client.send_message(message.channel, "Sorry, you need to tag one role to use this command.")

        if re.match(r"!\b(msgrole|rolemsg)\b", message.content, re.IGNORECASE):
            if message.channel.permissions_for(message.author).administrator or rDI in [role for role in message.author.roles] or rOV in [role for role in message.author.roles] or rRF in [role for role in message.author.roles]:
                if len(message.raw_role_mentions) > 0:
                    pl = message.clean_content
                    pl = re.sub(r"!\b(msgrole|rolemsg)\b","",pl,re.IGNORECASE)
                    pl = pl.lstrip()
                    sl = ""
                    fl = ""
                    for member in message.server.members:
                        for role in message.role_mentions:
                            if role in member.roles:
                                try:
                                    sl = sl + member.name + "\n"
                                    await client.send_message(member, pl)
                                except discord.Forbidden:
                                    fl = fl + member.name + "\n"
                    if not fl:
                        fl = "None"
                    if not sl:
                        sl = "None"
                    await client.send_message(message.channel, "The message has been sent.\n\n`Successful messages:`\n" + sl + "\n`Failed messages:`\n" + fl)

        if re.match(r"!\b(mem|member|members)\b", message.content, re.IGNORECASE):
            if len(message.role_mentions) == 1:
                pl = ""
                for member in message.server.members:
                    if message.role_mentions[0] in member.roles:
                        pl = pl + member.mention + " - " + member.top_role.name + "\n"
                await client.send_message(message.channel, pl)

        if re.match(r"!\b(version|ver|info)\b", message.content, re.IGNORECASE):
            await client.send_message(message.channel, "ILL Bot 2, " + version)

        #PLAYER VALUE CONTROL

        if re.match(r"!\b(s|set)pval\b", message.content, re.IGNORECASE):
            if message.channel.permissions_for(message.author).administrator:
                if len(message.raw_mentions) == 1:
                    if len(await getInts(message.content)) == 2:
                        i = await getInts(message.content)
                        await setPval(message.mentions[0].id, int(i[1]))
                        await client.send_message(message.channel, "Player Value for " + message.mentions[0].name + " has been set to " + str(await getPval(message.mentions[0].id)))

        if re.match(r"!\b(g|get)pval\b", message.content, re.IGNORECASE):
            if message.channel.permissions_for(message.author).administrator:
                if len(message.raw_mentions) == 1:
                    await client.send_message(message.channel, "Player Value for " + message.mentions[0].name + " is currently set to " + str(await getPval(message.mentions[0].id)))

        if re.match(r"!\b(a|add)pval\b", message.content, re.IGNORECASE):
            if message.channel.permissions_for(message.author).administrator:
                if len(message.raw_mentions) == 1:
                    if len(await getInts(message.content)) == 2:
                        i = await getInts(message.content)
                        await addPval(message.mentions[0].id, int(i[1]))
                        await client.send_message(message.channel, "Player Value for " + message.mentions[0].name + " has been increased by " + i[1] + " and is now set to " + str(await getPval(message.mentions[0].id)))

        #TEAM MONEY CONTROL

        if re.match(r"!\b(s|set)t(mon|money)\b", message.content, re.IGNORECASE):
            if message.channel.permissions_for(message.author).administrator:
                if len(message.raw_role_mentions) == 1:
                    if len(await getInts(message.content)) == 2:
                        i = await getInts(message.content)
                        print(i)
                        await setTmoney(message.role_mentions[0].id, int(i[1]))
                        await client.send_message(message.channel, "Team Money for " + message.role_mentions[0].name + " has been set to " + str(await getTmoney(message.role_mentions[0].id)))

        if re.match(r"!\b(g|get)t(mon|money)\b", message.content, re.IGNORECASE):
            if message.channel.permissions_for(message.author).administrator:
                if len(message.raw_role_mentions) == 1:
                    await client.send_message(message.channel, "Team Money for " + message.role_mentions[0].name + " is currently set to " + str(await getTmoney(message.role_mentions[0].id)))

        if re.match(r"!\b(a|add)t(mon|money)\b", message.content, re.IGNORECASE):
            if message.channel.permissions_for(message.author).administrator:
                if len(message.raw_role_mentions) == 1:
                    if len(await getInts(message.content)) == 2:
                        i = await getInts(message.content)
                        await addTmoney(message.role_mentions[0].id, int(i[1]))
                        await client.send_message(message.channel, "Team Money for " + message.role_mentions[0].name + " has been increased by " + i[1] + " and is now set to " + str(await getTmoney(message.role_mentions[0].id)))

        if re.match(r"!\b(reset)t(mon)\b", message.content, re.IGNORECASE):
            if message.author.id == "275388086815555585" or message.author.id == "276531286443556865":
                for role in sILL.roles:
                    await setTmoney(role.id, 16000)
                await client.send_message(message.channel, "Process complete. All teams set to $16000")

        #CONTRACT CONTROL

        if re.match(r"!\b(s|set)con\b", message.content, re.IGNORECASE):
            if message.channel.permissions_for(message.author).administrator:
                if len(message.raw_mentions) == 1:
                    if len(message.raw_role_mentions) == 1:
                        if len(await getInts(message.content)) == 3:
                            o = await getInts(message.content)
                            print(o)
                            await setCont(message.mentions[0].id, o[2], o[3])
                            o = await getCont(message.mentions[0].id)
                            print("var o")
                            print(o)
                            await client.send_message(message.channel, "Contract for " + message.mentions[0].name + " has been set to $" + str(o[0]) + " for " + str(o[1]) + " weeks.")

        if re.match(r"!\b(g|get)con\b", message.content, re.IGNORECASE):
            if message.channel.permissions_for(message.author).administrator:
                if len(message.raw_mentions) == 1:
                    o = await getCont(message.mentions[0].id)
                    await client.send_message(message.channel, "Contract for " + message.mentions[0].name + " is currently set to $" + str(o[0]) + " for " + str(o[1]) + " weeks")

        #PLAYER CONTROL

        if re.match(r"!\b(sign)\b", message.content, re.IGNORECASE):
            if message.channel == cCon or message.channel.permissions_for(message.author).administrator:
                if len(message.raw_role_mentions) == 1 and len(message.raw_mentions) == 1:
                    if message.channel.permissions_for(message.author).administrator or (rHC in [role for role in message.author.roles] and message.role_mentions[0] in [role for role in message.author.roles]) or (rAC in [role for role in message.author.roles] and message.role_mentions[0] in [role for role in message.author.roles]) or (rFO in [role for role in message.author.roles] and message.role_mentions[0] in [role for role in message.author.roles]):
                        if rFA in [role for role in message.mentions[0].roles]:
                            if len(await getInts(message.content)) == 4:
                                o = await getInts(message.content)
                                if int(o[3])>=8 and int(o[3])>0:
                                    if int(o[2]) < int(await getTmoney(message.role_mentions[0].id)):
                                        if int(o[2]) >= int(await getPval(message.mentions[0].id)):
                                            await addTmoney(message.role_mentions[0].id, (int(o[2])*-1))
                                            while (rFA in [role for role in message.mentions[0].roles]):
                                                await client.remove_roles(message.mentions[0], rFA)
                                            while (message.role_mentions[0] not in [role for role in message.mentions[0].roles]):
                                                await client.add_roles(message.mentions[0], message.role_mentions[0])
                                            await client.send_message(message.channel, message.mentions[0].mention + " has been signed to " + message.role_mentions[0].mention + " for $" + o[2] + ". Contract expires in " + o[3] + " weeks.")
                                        else:
                                            await client.send_message(message.channel, "Sorry! That player has a minimum value of $" + str(await getPval(message.mentions[0].id)))
                                    else:
                                        await client.send_message(message.channel, "That team does not have enough money! " + message.role_mentions[0].mention + "'s balance: $" + str(await getTmoney(message.role_mentions[0].id)))
                                else:
                                    await client.send_message(message.channel, "You can sign for a maximum of 8 weeks!")
                            else:
                                await client.send_message(message.channel, "You must provide 2 numbers, a contract amount and a contract term length.")
                        else:
                            await client.send_message(message.channel, "That user is not a free agent.")
                    else:
                        await client.send_message(message.channel, "Sorry, you do not have permission.")
                else:
                    await client.send_message(message.channel, "Sorry, you must tag one user and one team.")
            else:
                await client.send_message(message.channel, "Sorry, you can only sign players in the contracts channel.")

        if re.match(r"!\b(release|rel)\b", message.content, re.IGNORECASE):
            if message.channel == cCon or message.channel.permissions_for(message.author).administrator:
                if len(message.raw_role_mentions) == 1 and len(message.raw_mentions) == 1:
                    if message.channel.permissions_for(message.author).administrator or (rHC in [role for role in message.author.roles] and message.role_mentions[0] in [role for role in message.author.roles]) or (rAC in [role for role in message.author.roles] and message.role_mentions[0] in [role for role in message.author.roles]) or (rFO in [role for role in message.author.roles] and message.role_mentions[0] in [role for role in message.author.roles]):
                        if message.role_mentions[0] in [role for role in message.mentions[0].roles]:
                            while (message.role_mentions[0] in [role for role in message.mentions[0].roles]):
                                await client.remove_roles(message.mentions[0], message.role_mentions[0])
                            while (rAC in [role for role in message.mentions[0].roles]):
                                await client.remove_roles(message.mentions[0], rAC)
                            while (rHC in [role for role in message.mentions[0].roles]):
                                await client.remove_roles(message.mentions[0], rHC)
                            while (rFO in [role for role in message.mentions[0].roles]):
                                await client.remove_roles(message.mentions[0], rFO)
                            while (rFA not in [role for role in message.mentions[0].roles]):
                                await client.add_roles(message.mentions[0], rFA)
                            await client.send_message(message.channel, message.mentions[0].mention + " has been released from " + message.role_mentions[0].mention + "!")
                        else:
                            await client.send_message(message.channel, "That user is not on that team.")
                    else:
                        await client.send_message(message.channel, "Sorry, you do not have permission.")
                else:
                    await client.send_message(message.channel, "Sorry, you must tag one user and one team.")
            else:
                await client.send_message(message.channel, "Sorry, you can only release players in the contracts channel.")

        if re.match(r"!\b(s|set)ac\b", message.content, re.IGNORECASE):
            if message.channel == cPro or message.channel.permissions_for(message.author).administrator:
                if len(message.raw_role_mentions) == 1 and len(message.raw_mentions) == 1:
                    if message.channel.permissions_for(message.author).administrator or (rFO in [role for role in message.author.roles] and message.role_mentions[0] in [role for role in message.author.roles]):
                        if message.role_mentions[0] in [role for role in message.mentions[0].roles]:
                            while (rAC not in [role for role in message.mentions[0].roles]):
                                await client.add_roles(message.mentions[0], rAC)
                            await client.send_message(message.channel, message.mentions[0].mention + " has been assigned as Assistant Coach for the " + message.role_mentions[0].mention)
                        else:
                            await client.send_message(message.channel, "Sorry, that user is not on that team.")
                    else:
                        await client.send_message(message.channel, "Sorry, you do not have permission to do that.")
                else:
                    await client.send_message(message.channel, "Sorry, you must tag one user and one team.")
            else:
                await client.send_message(message.channel, "Sorry, you can only assign team staff in the promotions channel.")

        if re.match(r"!\b(s|set)hc\b", message.content, re.IGNORECASE):
            if message.channel == cPro or message.channel.permissions_for(message.author).administrator:
                if len(message.raw_role_mentions) == 1 and len(message.raw_mentions) == 1:
                    if message.channel.permissions_for(message.author).administrator or (rFO in [role for role in message.author.roles] and message.role_mentions[0] in [role for role in message.author.roles]):
                        if message.role_mentions[0] in [role for role in message.mentions[0].roles]:
                            while (rHC not in [role for role in message.mentions[0].roles]):
                                await client.add_roles(message.mentions[0], rHC)
                            await client.send_message(message.channel, message.mentions[0].mention + " has been assigned as Head Coach for the " + message.role_mentions[0].mention)
                        else:
                            await client.send_message(message.channel, "Sorry, that user is not on that team.")
                    else:
                        await client.send_message(message.channel, "Sorry, you do not have permission to do that.")
                else:
                    await client.send_message(message.channel, "Sorry, you must tag one user and one team.")
            else:
                await client.send_message(message.channel, "Sorry, you can only assign team staff in the promotions channel.")

        if re.match(r"!\b(r|rem)ac\b", message.content, re.IGNORECASE):
            if message.channel == cPro or message.channel.permissions_for(message.author).administrator:
                if len(message.raw_role_mentions) == 1 and len(message.raw_mentions) == 1:
                    if message.channel.permissions_for(message.author).administrator or (rFO in [role for role in message.author.roles] and message.role_mentions[0] in [role for role in message.author.roles]):
                        if message.role_mentions[0] in [role for role in message.mentions[0].roles]:
                            while (rAC in [role for role in message.mentions[0].roles]):
                                await client.remove_roles(message.mentions[0], rAC)
                            await client.send_message(message.channel, message.mentions[0].mention + " has been demoted from Assistant Coach for the " + message.role_mentions[0].mention)
                        else:
                            await client.send_message(message.channel, "Sorry, that user is not on that team.")
                    else:
                        await client.send_message(message.channel, "Sorry, you do not have permission to do that.")
                else:
                    await client.send_message(message.channel, "Sorry, you must tag one user and one team.")
            else:
                await client.send_message(message.channel, "Sorry, you can only assign team staff in the promotions channel.")

        if re.match(r"!\b(r|rem)hc\b", message.content, re.IGNORECASE):
            if message.channel == cPro or message.channel.permissions_for(message.author).administrator:
                if len(message.raw_role_mentions) == 1 and len(message.raw_mentions) == 1:
                    if message.channel.permissions_for(message.author).administrator or (rFO in [role for role in message.author.roles] and message.role_mentions[0] in [role for role in message.author.roles]):
                        if message.role_mentions[0] in [role for role in message.mentions[0].roles]:
                            while (rHC in [role for role in message.mentions[0].roles]):
                                await client.remove_roles(message.mentions[0], rHC)
                            await client.send_message(message.channel, message.mentions[0].mention + " has been demoted from Head Coach for the " + message.role_mentions[0].mention)
                        else:
                            await client.send_message(message.channel, "Sorry, that user is not on that team.")
                    else:
                        await client.send_message(message.channel, "Sorry, you do not have permission to do that.")
                else:
                    await client.send_message(message.channel, "Sorry, you must tag one user and one team.")
            else:
                await client.send_message(message.channel, "Sorry, you can only assign team staff in the promotions channel.")

        if re.match(r"!\b(pc|playercard)\b", message.content, re.IGNORECASE):
            if len(message.raw_mentions) > 0:
                await client.send_message(message.channel, message.mentions[0].mention + "'s Player Card:\nCurrent Contract: $" + str([await getCont(message.mentions[0].id)][0][0]) + "\nPlayer Value: $" + str(await getPval(message.mentions[0].id)))
            else:
                await client.send_message(message.channel, message.author.mention + "'s Player Card:\nCurrent Contract: $" + str([await getCont(message.author.id)][0][0]) + "\nPlayer Value: $" + str(await getPval(message.author.id)))



#CLIENT KEY
client.run("Mzg0NzcxMjczOTQ4OTIxODU4.Dp7Ylg.XYQ7srynXgP6G4OzzEX50Uiysgs")
