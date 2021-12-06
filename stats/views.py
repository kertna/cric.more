from django.shortcuts import render
import glob
import json
from pulp import *
import random
from .models import FantasyTeam, FantasyPrediction, Player,Form,PowerPlay,PlayerTeam,MiddleOvers,DeathOvers,Matchups,City,Position,AgainstTeam
# Create your views here.
from django.http import HttpResponse
import yaml
import os
from os import listdir
from django.db.models import Q 
from os.path import isfile, join
import numpy as N
from django.templatetags.static import static
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404

def overall(name):

    p= Player.objects.get(name=name)
    points1=0
    if p.innings>0:
        points1= (p.runs+ p.fours + 2*(p.sixes)+ 16*(p.hundreds)+ 8*(p.fifties) + 8*(p.catches))//p.innings
        
    if p.ballsbowled>0:
        wickets= (24*p.wickets)/p.ballsbowled
        threehaul=(24*p.threehaul)/p.ballsbowled
        fivehaul=(24*p.fivehaul)/p.ballsbowled
        points2 = 25*(wickets)+ 5*(p.threehaul) +15*(p.fivehaul)
    else:
        points2=0
    
    points=points1+points2
    if p.strikerate >150:
        points=points+3
    elif p.strikerate<70:
        points=points-3
    
    if p.economy<6:
        points=points+3
    elif p.economy>10:
        points=points-3
    
    return points
def against(name,team):
    
    p=AgainstTeam.objects.filter(name=name,Team=team)
    
    points1=0
    if not p:
        return 0
    p=AgainstTeam.objects.get(name=name,Team=team)
    
    
    if p.innings>0:
        points1= (p.runs+ p.fours + 2*(p.sixes)+ 16*(p.hundreds)+ 8*(p.fifties))//p.innings
        
    if p.ballsbowled>0:
        wickets= (24*p.wickets)/p.ballsbowled
        threehaul=(24*p.threehaul)/p.ballsbowled
        fivehaul=(24*p.fivehaul)/p.ballsbowled
        points2 = 25*(wickets)+ 5*(p.threehaul) +15*(p.fivehaul)
    else:
        points2=0
    points=points1+points2
    if p.strikerate >150:
        points=points+3
    elif p.strikerate<70:
        points=points-3
    
    if p.economy<6:
        points=points+3
    elif p.economy>10:
        points=points-3
    
    return points

def city(name,ground):
    p=City.objects.filter(name=name,City=ground)
   
    points1=0
    if not p:
        return 0
    p=City.objects.get(name=name,City=ground)
    
    
    if p.innings>0:
        points1= (p.runs+ 16*(p.hundreds)+ 8*(p.fifties))//p.innings
    if p.ballsbowled>0:
        wickets= (24*p.wickets)/p.ballsbowled
        threehaul=(24*p.threehaul)/p.ballsbowled
        fivehaul=(24*p.fivehaul)/p.ballsbowled
        points2 = 25*(wickets)+ 5*(p.threehaul) +15*(p.fivehaul)
    else:
        points2=0
    points=points1+points2
    if p.strikerate >150:
        points=points+3
    elif p.strikerate<70:
        points=points-3
    
    if p.economy<6:
        points=points+3
    elif p.economy>10:
        points=points-3
    
    return points

def form(name):
    f=Form.objects.filter(name=name)
    if not f:
        return 0
    f= Form.objects.get(name=name)
    return f.currentform
def calculate1(name,role,ground,againstteam):
    
    p=Player.objects.filter(name=name)
    if not p:
        if role[name]=='Bowler':
            return 10
        if role[name]=='Batsman':
            return 20
        if role[name]=='Allrounder':
            return 25
        if role[name]=='WicketKeeper':
            return 5
    
    overallperformance=overall(name)

    againstteamperformance= against(name,againstteam[name])

    groundperformance=city(name,ground)

    recentperformance = form(name)
    return overallperformance + 0.1*againstteamperformance+ 0.1*groundperformance+0.1*recentperformance

def calculate2(name,role,ground,againstteam):
    
    p=Player.objects.filter(name=name)
    if not p:
        if role[name]=='Bowler':
            return 10
        if role[name]=='Batsman':
            return 20
        if role[name]=='Allrounder':
            return 25
        if role[name]=='WicketKeeper':
            return 5
    
    overallperformance=overall(name)

    againstteamperformance= against(name,againstteam[name])

    groundperformance=city(name,ground)

    recentperformance = form(name)
    return 0.1*overallperformance + 0.1*againstteamperformance+ groundperformance+0.1*recentperformance
def calculate3(name,role,ground,againstteam):
    
    p=Player.objects.filter(name=name)
    if not p:
        if role[name]=='Bowler':
            return 10
        if role[name]=='Batsman':
            return 20
        if role[name]=='Allrounder':
            return 25
        if role[name]=='WicketKeeper':
            return 5
    
    overallperformance=overall(name)

    againstteamperformance= against(name,againstteam[name])

    groundperformance=city(name,ground)

    recentperformance = form(name)
    return 0.1*overallperformance + againstteamperformance+ 0.1*groundperformance+0.1*recentperformance
def calculate4(name,role,ground,againstteam):
    
    p=Player.objects.filter(name=name)
    if not p:
        if role[name]=='Bowler':
            return 10
        if role[name]=='Batsman':
            return 20
        if role[name]=='Allrounder':
            return 25
        if role[name]=='WicketKeeper':
            return 5
    
    overallperformance=overall(name)

    againstteamperformance= against(name,againstteam[name])

    groundperformance=city(name,ground)

    recentperformance = form(name)
    return 0.1*overallperformance + 0.1*againstteamperformance+ 0.1*groundperformance+recentperformance
def calculate5(name,role,ground,againstteam):
    
    p=Player.objects.filter(name=name)
    if not p:
        if role[name]=='Bowler':
            return 10
        if role[name]=='Batsman':
            return 20
        if role[name]=='Allrounder':
            return 25
        if role[name]=='WicketKeeper':
            return 5
    
    overallperformance=overall(name)

    againstteamperformance= against(name,againstteam[name])

    groundperformance=city(name,ground)

    recentperformance = form(name)
    return 0.1*overallperformance + 0.1*againstteamperformance+ 0.1*groundperformance+recentperformance
    
def setagainstteams(teams,team1,team2):
    ans={}
    for i in teams:
        if teams[i]==team1:
            ans[i]=team2
        else:
            ans[i]=team1
    
    return ans
def getbatsmen(players,roles):
    di={}
    for i in players:
        if roles[i]=='Batsman':
            di[i]=1
        else:
            di[i]=0
    return di

def getbowlers(players,roles):
    di={}
    for i in players:
        if roles[i]=='Bowler':
            di[i]=1
        else:
            di[i]=0
    return di
def getar(players,roles):
    di={}
    for i in players:
        if roles[i]=='Allrounder':
            di[i]=1
        else:
            di[i]=0
    return di
def getwk(players,roles):
    di={}
    for i in players:
        if roles[i]=='WicketKeeper':
            di[i]=1
        else:
            di[i]=0
    return di
def t1(players,teams,team1,team2):
    playersinteam1={}
    for i in teams:
        if teams[i]==team1:
            playersinteam1[i]=1
        else:
            playersinteam1[i]=0
    return playersinteam1

def t2(players,teams,team1,team2):
    playersinteam2={}
    for i in teams:
        if teams[i]==team2:
            playersinteam2[i]=1
        else:
            playersinteam2[i]=0
    return playersinteam2
def shortforms(team):
    if team=='Sunrisers Hyderabad':
        return 'SRH'
    elif team=='Mumbai Indians':
        return 'MI'
    elif team=='Royal Challengers Bangalore':
        return 'RCB'
    elif team=='Kolkata Knight Riders':
        return 'KKR'
    elif team=='Chennai Super Kings':
        return 'CSK'
    elif team=='Kings XI Punjab':
        return 'PK'
    elif team=='Delhi Daredevils':
        return 'DD'
    else:
        return 'RR'


def predictOverall(request):
    model = LpProblem("Fantasy Cricket",LpMaximize)
    f=FantasyPrediction.objects.get(id=1)

    ground= f.ground
    team1=f.team1
    team2=f.team2

    player= f.getplayers()
    player_vars = LpVariable.dicts("",player,0,1,LpBinary)
    mapping={}
    for i in player_vars:
        mapping[str(player_vars[i])]=i
    #print(mapping['_AB_Agarkar'])
    #print(player_vars)
    credit=f.getplayercredits()
    credits = {(player[i]): credit[i] for i in range(0,22)} 

    role= f.getroles()
    roles={(player[i]): role[i] for i in range(0,22)} 
    
    teams= f.setteams()
    
    againstteams= setagainstteams(teams,team1,team2)
    
    points={(i): calculate1(i,roles,ground,againstteams) for i in player} 

    batsmen=getbatsmen(player,roles)
    bowlers=getbowlers(player,roles)
    allrounders=getar(player,roles)
    wk=getwk(player,roles)
    playersinteam1=t1(player,teams,team1,team2)
    playersinteam2=t2(player,teams,team1,team2)
    #print(wk)
    model+=lpSum([points[i]*player_vars[i] for i in player]), "Total Points"
    model+= lpSum([player_vars[i] for i in player]) == 11, "Total 11 Players"
    model += lpSum([credits[i] * player_vars[i] for i in player]) <= 100.0, "Total Credits"
    model+= lpSum([batsmen[i]*player_vars[i] for i in player]) >=3 , "Minimum 3 bastmen"
    model+= lpSum([bowlers[i]*player_vars[i] for i in player]) >=3, "Minimum 3 bowlers"
    model+= lpSum([wk[i]*player_vars[i] for i in player]) >=1 , "Minimum 4 wk"
    model+= lpSum([wk[i]*player_vars[i] for i in player]) <=4, "Maximum 4 wk"
    model+= lpSum([allrounders[i]*player_vars[i] for i in player]) >=1, "Minimum 1 allrounders"
    model+= lpSum([batsmen[i]*player_vars[i] for i in player]) <=6 , "Maximum 6 bastmen"
    model+= lpSum([bowlers[i]*player_vars[i] for i in player]) <=6, "Maximum 6 bowlers"
    model+= lpSum([allrounders[i]*player_vars[i] for i in player]) <=4, "Maximum 4 allrounders"
    model+= lpSum([playersinteam1[i]*player_vars[i] for i in player]) <=7 , "Maximum 7 players in team1"
    model+= lpSum([playersinteam2[i] *player_vars[i] for i in player]) <=7, "Maximum 7 players in team2"
    status = model.solve()
    finalprediction=[]
    captainp=0
    vicecaptainp=0
    captain=""
    vicecaptain=""
    for var in model.variables():
        if var.value()==1:
            if points[mapping[var.name]]>captainp:
                vicecaptain=captain
                vicecaptainp=captainp
                captain=mapping[var.name]
                captainp=points[mapping[var.name]]
            elif points[mapping[var.name]]>vicecaptainp:
                vicecaptain=mapping[var.name]
                vicecaptainp=points[mapping[var.name]]

        
            finalprediction.append(var.name)
   
    b=[]
    bo=[]
    ar=[]
    wk=[]
    bt=[]
    bot=[]
    art=[]
    wkt=[]
    bc=[]
    boc=[]
    arc=[]
    wkc=[]
    for i in finalprediction:
        
        if roles[mapping[i]]=='Batsman':
            b.append(mapping[i])
            bt.append(shortforms(teams[mapping[i]]))
            bc.append(credits[mapping[i]])
            
        elif roles[mapping[i]]=='Bowler':
            bo.append(mapping[i])
            bot.append(shortforms(teams[mapping[i]]))
            boc.append(credits[mapping[i]])
        elif roles[mapping[i]]=='Allrounder':
            ar.append(mapping[i])
            art.append(shortforms(teams[mapping[i]]))
            arc.append(credits[mapping[i]])
        else:
            wk.append(mapping[i])
            wkt.append(shortforms(teams[mapping[i]]))
            wkc.append(credits[mapping[i]])

    
    context = {
                'captain':captain,
                'vicecaptain':vicecaptain,
				't1':team1,
                't2':team2,
                'b':b,
                'bo':bo,
                'ar':ar,
                'wk':wk,
                'bt':bt,
                'bot':bot,
                'art':art,
                'wkt':wkt,
                'bc':bc,
                'boc':boc,
                'arc':arc,
                'wkc':wkc
                
                
			}
    #finalans=json.dumps(context)
    ft=FantasyTeam.objects.filter(id=1)
    if not ft:
        ft=FantasyTeam(id=1)
        ft.save()
    ft=FantasyTeam.objects.get(id=1)
    ft.setteam(context)

    return HttpResponse("PREDICTED")

def predictGround(request):
    model = LpProblem("Fantasy Cricket",LpMaximize)
    f=FantasyPrediction.objects.get(id=1)

    ground= f.ground
    team1=f.team1
    team2=f.team2

    player= f.getplayers()
    player_vars = LpVariable.dicts("",player,0,1,LpBinary)
    mapping={}
    for i in player_vars:
        mapping[str(player_vars[i])]=i
    #print(mapping['_AB_Agarkar'])
    #print(player_vars)
    credit=f.getplayercredits()
    credits = {(player[i]): credit[i] for i in range(0,22)} 

    role= f.getroles()
    roles={(player[i]): role[i] for i in range(0,22)} 
    
    teams= f.setteams()
    
    againstteams= setagainstteams(teams,team1,team2)
    
    points={(i): calculate2(i,roles,ground,againstteams) for i in player} 

    batsmen=getbatsmen(player,roles)
    bowlers=getbowlers(player,roles)
    allrounders=getar(player,roles)
    wk=getwk(player,roles)
    playersinteam1=t1(player,teams,team1,team2)
    playersinteam2=t2(player,teams,team1,team2)
    #print(wk)
    model+=lpSum([points[i]*player_vars[i] for i in player]), "Total Points"
    model+= lpSum([player_vars[i] for i in player]) == 11, "Total 11 Players"
    model += lpSum([credits[i] * player_vars[i] for i in player]) <= 100.0, "Total Credits"
    model+= lpSum([batsmen[i]*player_vars[i] for i in player]) >=3 , "Minimum 3 bastmen"
    model+= lpSum([bowlers[i]*player_vars[i] for i in player]) >=3, "Minimum 3 bowlers"
    model+= lpSum([wk[i]*player_vars[i] for i in player]) >=1 , "Minimum 4 wk"
    model+= lpSum([wk[i]*player_vars[i] for i in player]) <=4, "Maximum 4 wk"
    model+= lpSum([allrounders[i]*player_vars[i] for i in player]) >=1, "Minimum 1 allrounders"
    model+= lpSum([batsmen[i]*player_vars[i] for i in player]) <=6 , "Maximum 6 bastmen"
    model+= lpSum([bowlers[i]*player_vars[i] for i in player]) <=6, "Maximum 6 bowlers"
    model+= lpSum([allrounders[i]*player_vars[i] for i in player]) <=4, "Maximum 4 allrounders"
    model+= lpSum([playersinteam1[i]*player_vars[i] for i in player]) <=7 , "Maximum 7 players in team1"
    model+= lpSum([playersinteam2[i] *player_vars[i] for i in player]) <=7, "Maximum 7 players in team2"
    status = model.solve()
    finalprediction=[]
    captainp=0
    vicecaptainp=0
    captain=""
    vicecaptain=""
    for var in model.variables():
        if var.value()==1:
            if points[mapping[var.name]]>captainp:
                vicecaptain=captain
                vicecaptainp=captainp
                captain=mapping[var.name]
                captainp=points[mapping[var.name]]
            elif points[mapping[var.name]]>vicecaptainp:
                vicecaptain=mapping[var.name]
                vicecaptainp=points[mapping[var.name]]

        
            finalprediction.append(var.name)
   
    b=[]
    bo=[]
    ar=[]
    wk=[]
    bt=[]
    bot=[]
    art=[]
    wkt=[]
    bc=[]
    boc=[]
    arc=[]
    wkc=[]
    for i in finalprediction:
        
        if roles[mapping[i]]=='Batsman':
            b.append(mapping[i])
            bt.append(shortforms(teams[mapping[i]]))
            bc.append(credits[mapping[i]])
            
        elif roles[mapping[i]]=='Bowler':
            bo.append(mapping[i])
            bot.append(shortforms(teams[mapping[i]]))
            boc.append(credits[mapping[i]])
        elif roles[mapping[i]]=='Allrounder':
            ar.append(mapping[i])
            art.append(shortforms(teams[mapping[i]]))
            arc.append(credits[mapping[i]])
        else:
            wk.append(mapping[i])
            wkt.append(shortforms(teams[mapping[i]]))
            wkc.append(credits[mapping[i]])

    
    context = {
                'captain':captain,
                'vicecaptain':vicecaptain,
				't1':team1,
                't2':team2,
                'b':b,
                'bo':bo,
                'ar':ar,
                'wk':wk,
                'bt':bt,
                'bot':bot,
                'art':art,
                'wkt':wkt,
                'bc':bc,
                'boc':boc,
                'arc':arc,
                'wkc':wkc
                
                
			}
    #finalans=json.dumps(context)
    ft=FantasyTeam.objects.filter(id=2)
    if not ft:
        ft=FantasyTeam(id=2)
        ft.save()
    ft=FantasyTeam.objects.get(id=2)
    ft.setteam(context)

    return HttpResponse("PREDICTED")

def predictAgainst(request):
    model = LpProblem("Fantasy Cricket",LpMaximize)
    f=FantasyPrediction.objects.get(id=1)

    ground= f.ground
    team1=f.team1
    team2=f.team2

    player= f.getplayers()
    player_vars = LpVariable.dicts("",player,0,1,LpBinary)
    mapping={}
    for i in player_vars:
        mapping[str(player_vars[i])]=i
    #print(mapping['_AB_Agarkar'])
    #print(player_vars)
    credit=f.getplayercredits()
    credits = {(player[i]): credit[i] for i in range(0,22)} 

    role= f.getroles()
    roles={(player[i]): role[i] for i in range(0,22)} 
    
    teams= f.setteams()
    
    againstteams= setagainstteams(teams,team1,team2)
    
    points={(i): calculate3(i,roles,ground,againstteams) for i in player} 

    batsmen=getbatsmen(player,roles)
    bowlers=getbowlers(player,roles)
    allrounders=getar(player,roles)
    wk=getwk(player,roles)
    playersinteam1=t1(player,teams,team1,team2)
    playersinteam2=t2(player,teams,team1,team2)
    #print(wk)
    model+=lpSum([points[i]*player_vars[i] for i in player]), "Total Points"
    model+= lpSum([player_vars[i] for i in player]) == 11, "Total 11 Players"
    model += lpSum([credits[i] * player_vars[i] for i in player]) <= 100.0, "Total Credits"
    model+= lpSum([batsmen[i]*player_vars[i] for i in player]) >=3 , "Minimum 3 bastmen"
    model+= lpSum([bowlers[i]*player_vars[i] for i in player]) >=3, "Minimum 3 bowlers"
    model+= lpSum([wk[i]*player_vars[i] for i in player]) >=1 , "Minimum 4 wk"
    model+= lpSum([wk[i]*player_vars[i] for i in player]) <=4, "Maximum 4 wk"
    model+= lpSum([allrounders[i]*player_vars[i] for i in player]) >=1, "Minimum 1 allrounders"
    model+= lpSum([batsmen[i]*player_vars[i] for i in player]) <=6 , "Maximum 6 bastmen"
    model+= lpSum([bowlers[i]*player_vars[i] for i in player]) <=6, "Maximum 6 bowlers"
    model+= lpSum([allrounders[i]*player_vars[i] for i in player]) <=4, "Maximum 4 allrounders"
    model+= lpSum([playersinteam1[i]*player_vars[i] for i in player]) <=7 , "Maximum 7 players in team1"
    model+= lpSum([playersinteam2[i] *player_vars[i] for i in player]) <=7, "Maximum 7 players in team2"
    status = model.solve()
    finalprediction=[]
    captainp=0
    vicecaptainp=0
    captain=""
    vicecaptain=""
    for var in model.variables():
        if var.value()==1:
            if points[mapping[var.name]]>captainp:
                vicecaptain=captain
                vicecaptainp=captainp
                captain=mapping[var.name]
                captainp=points[mapping[var.name]]
            elif points[mapping[var.name]]>vicecaptainp:
                vicecaptain=mapping[var.name]
                vicecaptainp=points[mapping[var.name]]

        
            finalprediction.append(var.name)
   
    b=[]
    bo=[]
    ar=[]
    wk=[]
    bt=[]
    bot=[]
    art=[]
    wkt=[]
    bc=[]
    boc=[]
    arc=[]
    wkc=[]
    for i in finalprediction:
        
        if roles[mapping[i]]=='Batsman':
            b.append(mapping[i])
            bt.append(shortforms(teams[mapping[i]]))
            bc.append(credits[mapping[i]])
            
        elif roles[mapping[i]]=='Bowler':
            bo.append(mapping[i])
            bot.append(shortforms(teams[mapping[i]]))
            boc.append(credits[mapping[i]])
        elif roles[mapping[i]]=='Allrounder':
            ar.append(mapping[i])
            art.append(shortforms(teams[mapping[i]]))
            arc.append(credits[mapping[i]])
        else:
            wk.append(mapping[i])
            wkt.append(shortforms(teams[mapping[i]]))
            wkc.append(credits[mapping[i]])

    
    context = {
                'captain':captain,
                'vicecaptain':vicecaptain,
				't1':team1,
                't2':team2,
                'b':b,
                'bo':bo,
                'ar':ar,
                'wk':wk,
                'bt':bt,
                'bot':bot,
                'art':art,
                'wkt':wkt,
                'bc':bc,
                'boc':boc,
                'arc':arc,
                'wkc':wkc
                
                
			}
    #finalans=json.dumps(context)
    ft=FantasyTeam.objects.filter(id=3)
    if not ft:
        ft=FantasyTeam(id=3)
        ft.save()
    ft=FantasyTeam.objects.get(id=3)
    ft.setteam(context)

    return HttpResponse("PREDICTED")

def predictForm(request):
    model = LpProblem("Fantasy Cricket",LpMaximize)
    f=FantasyPrediction.objects.get(id=1)

    ground= f.ground
    team1=f.team1
    team2=f.team2

    player= f.getplayers()
    player_vars = LpVariable.dicts("",player,0,1,LpBinary)
    mapping={}
    for i in player_vars:
        mapping[str(player_vars[i])]=i
    #print(mapping['_AB_Agarkar'])
    #print(player_vars)
    credit=f.getplayercredits()
    credits = {(player[i]): credit[i] for i in range(0,22)} 

    role= f.getroles()
    roles={(player[i]): role[i] for i in range(0,22)} 
    
    teams= f.setteams()
    
    againstteams= setagainstteams(teams,team1,team2)
    
    points={(i): calculate4(i,roles,ground,againstteams) for i in player} 

    batsmen=getbatsmen(player,roles)
    bowlers=getbowlers(player,roles)
    allrounders=getar(player,roles)
    wk=getwk(player,roles)
    playersinteam1=t1(player,teams,team1,team2)
    playersinteam2=t2(player,teams,team1,team2)
    #print(wk)
    model+=lpSum([points[i]*player_vars[i] for i in player]), "Total Points"
    model+= lpSum([player_vars[i] for i in player]) == 11, "Total 11 Players"
    model += lpSum([credits[i] * player_vars[i] for i in player]) <= 100.0, "Total Credits"
    model+= lpSum([batsmen[i]*player_vars[i] for i in player]) >=3 , "Minimum 3 bastmen"
    model+= lpSum([bowlers[i]*player_vars[i] for i in player]) >=3, "Minimum 3 bowlers"
    model+= lpSum([wk[i]*player_vars[i] for i in player]) >=1 , "Minimum 4 wk"
    model+= lpSum([wk[i]*player_vars[i] for i in player]) <=4, "Maximum 4 wk"
    model+= lpSum([allrounders[i]*player_vars[i] for i in player]) >=1, "Minimum 1 allrounders"
    model+= lpSum([batsmen[i]*player_vars[i] for i in player]) <=6 , "Maximum 6 bastmen"
    model+= lpSum([bowlers[i]*player_vars[i] for i in player]) <=6, "Maximum 6 bowlers"
    model+= lpSum([allrounders[i]*player_vars[i] for i in player]) <=4, "Maximum 4 allrounders"
    model+= lpSum([playersinteam1[i]*player_vars[i] for i in player]) <=7 , "Maximum 7 players in team1"
    model+= lpSum([playersinteam2[i] *player_vars[i] for i in player]) <=7, "Maximum 7 players in team2"
    status = model.solve()
    finalprediction=[]
    captainp=0
    vicecaptainp=0
    captain=""
    vicecaptain=""
    for var in model.variables():
        if var.value()==1:
            if points[mapping[var.name]]>captainp:
                vicecaptain=captain
                vicecaptainp=captainp
                captain=mapping[var.name]
                captainp=points[mapping[var.name]]
            elif points[mapping[var.name]]>vicecaptainp:
                vicecaptain=mapping[var.name]
                vicecaptainp=points[mapping[var.name]]

        
            finalprediction.append(var.name)
   
    b=[]
    bo=[]
    ar=[]
    wk=[]
    bt=[]
    bot=[]
    art=[]
    wkt=[]
    bc=[]
    boc=[]
    arc=[]
    wkc=[]
    for i in finalprediction:
        
        if roles[mapping[i]]=='Batsman':
            b.append(mapping[i])
            bt.append(shortforms(teams[mapping[i]]))
            bc.append(credits[mapping[i]])
            
        elif roles[mapping[i]]=='Bowler':
            bo.append(mapping[i])
            bot.append(shortforms(teams[mapping[i]]))
            boc.append(credits[mapping[i]])
        elif roles[mapping[i]]=='Allrounder':
            ar.append(mapping[i])
            art.append(shortforms(teams[mapping[i]]))
            arc.append(credits[mapping[i]])
        else:
            wk.append(mapping[i])
            wkt.append(shortforms(teams[mapping[i]]))
            wkc.append(credits[mapping[i]])

    
    context = {
                'captain':captain,
                'vicecaptain':vicecaptain,
				't1':team1,
                't2':team2,
                'b':b,
                'bo':bo,
                'ar':ar,
                'wk':wk,
                'bt':bt,
                'bot':bot,
                'art':art,
                'wkt':wkt,
                'bc':bc,
                'boc':boc,
                'arc':arc,
                'wkc':wkc
                
                
			}
    #finalans=json.dumps(context)
    ft=FantasyTeam.objects.filter(id=4)
    if not ft:
        ft=FantasyTeam(id=4)
        ft.save()
    ft=FantasyTeam.objects.get(id=4)
    ft.setteam(context)

    return HttpResponse("PREDICTED")

def predictSuggested(request):
    model = LpProblem("Fantasy Cricket",LpMaximize)
    f=FantasyPrediction.objects.get(id=1)

    ground= f.ground
    team1=f.team1
    team2=f.team2

    player= f.getplayers()
    player_vars = LpVariable.dicts("",player,0,1,LpBinary)
    mapping={}
    for i in player_vars:
        mapping[str(player_vars[i])]=i
    #print(mapping['_AB_Agarkar'])
    #print(player_vars)
    credit=f.getplayercredits()
    credits = {(player[i]): credit[i] for i in range(0,22)} 

    role= f.getroles()
    roles={(player[i]): role[i] for i in range(0,22)} 
    
    teams= f.setteams()
    
    againstteams= setagainstteams(teams,team1,team2)
    
    points={(i): calculate5(i,roles,ground,againstteams) for i in player} 

    batsmen=getbatsmen(player,roles)
    bowlers=getbowlers(player,roles)
    allrounders=getar(player,roles)
    wk=getwk(player,roles)
    playersinteam1=t1(player,teams,team1,team2)
    playersinteam2=t2(player,teams,team1,team2)
    #print(wk)
    model+=lpSum([points[i]*player_vars[i] for i in player]), "Total Points"
    model+= lpSum([player_vars[i] for i in player]) == 11, "Total 11 Players"
    model += lpSum([credits[i] * player_vars[i] for i in player]) <= 100.0, "Total Credits"
    model+= lpSum([batsmen[i]*player_vars[i] for i in player]) >=3 , "Minimum 3 bastmen"
    model+= lpSum([bowlers[i]*player_vars[i] for i in player]) >=3, "Minimum 3 bowlers"
    model+= lpSum([wk[i]*player_vars[i] for i in player]) >=1 , "Minimum 4 wk"
    model+= lpSum([wk[i]*player_vars[i] for i in player]) <=4, "Maximum 4 wk"
    model+= lpSum([allrounders[i]*player_vars[i] for i in player]) >=1, "Minimum 1 allrounders"
    model+= lpSum([batsmen[i]*player_vars[i] for i in player]) <=6 , "Maximum 6 bastmen"
    model+= lpSum([bowlers[i]*player_vars[i] for i in player]) <=6, "Maximum 6 bowlers"
    model+= lpSum([allrounders[i]*player_vars[i] for i in player]) <=4, "Maximum 4 allrounders"
    model+= lpSum([playersinteam1[i]*player_vars[i] for i in player]) <=7 , "Maximum 7 players in team1"
    model+= lpSum([playersinteam2[i] *player_vars[i] for i in player]) <=7, "Maximum 7 players in team2"
    status = model.solve()
    finalprediction=[]
    captainp=0
    vicecaptainp=0
    captain=""
    vicecaptain=""
    for var in model.variables():
        if var.value()==1:
            if points[mapping[var.name]]>captainp:
                vicecaptain=captain
                vicecaptainp=captainp
                captain=mapping[var.name]
                captainp=points[mapping[var.name]]
            elif points[mapping[var.name]]>vicecaptainp:
                vicecaptain=mapping[var.name]
                vicecaptainp=points[mapping[var.name]]

        
            finalprediction.append(var.name)
   
    b=[]
    bo=[]
    ar=[]
    wk=[]
    bt=[]
    bot=[]
    art=[]
    wkt=[]
    bc=[]
    boc=[]
    arc=[]
    wkc=[]
    for i in finalprediction:
        
        if roles[mapping[i]]=='Batsman':
            b.append(mapping[i])
            bt.append(shortforms(teams[mapping[i]]))
            bc.append(credits[mapping[i]])
            
        elif roles[mapping[i]]=='Bowler':
            bo.append(mapping[i])
            bot.append(shortforms(teams[mapping[i]]))
            boc.append(credits[mapping[i]])
        elif roles[mapping[i]]=='Allrounder':
            ar.append(mapping[i])
            art.append(shortforms(teams[mapping[i]]))
            arc.append(credits[mapping[i]])
        else:
            wk.append(mapping[i])
            wkt.append(shortforms(teams[mapping[i]]))
            wkc.append(credits[mapping[i]])

    
    context = {
                'captain':captain,
                'vicecaptain':vicecaptain,
				't1':team1,
                't2':team2,
                'b':b,
                'bo':bo,
                'ar':ar,
                'wk':wk,
                'bt':bt,
                'bot':bot,
                'art':art,
                'wkt':wkt,
                'bc':bc,
                'boc':boc,
                'arc':arc,
                'wkc':wkc
                
                
			}
    #finalans=json.dumps(context)
    ft=FantasyTeam.objects.filter(id=5)
    if not ft:
        ft=FantasyTeam(id=5)
        ft.save()
    ft=FantasyTeam.objects.get(id=5)
    ft.setteam(context)

    return HttpResponse("PREDICTED")

def predictedteam1(request):
    ft=FantasyTeam.objects.filter(id=1)
    if not ft:
        return HttpResponse("NOT AVAILABLE")
    ft=FantasyTeam.objects.get(id=1)
    context=ft.getteam()
    return render(request, '../templates/html/Fantasy.html',context)

def predictedteam2(request):
    ft=FantasyTeam.objects.filter(id=2)
    if not ft:
        return HttpResponse("NOT AVAILABLE")
    ft=FantasyTeam.objects.get(id=2)
    context=ft.getteam()
    return render(request, '../templates/html/Fantasy.html',context)
def predictedteam3(request):
    ft=FantasyTeam.objects.filter(id=3)
    if not ft:
        return HttpResponse("NOT AVAILABLE")
    ft=FantasyTeam.objects.get(id=3)
    context=ft.getteam()
    return render(request, '../templates/html/Fantasy.html',context)
def predictedteam4(request):
    ft=FantasyTeam.objects.filter(id=4)
    if not ft:
        return HttpResponse("NOT AVAILABLE")
    ft=FantasyTeam.objects.get(id=4)
    context=ft.getteam()
    return render(request, '../templates/html/Fantasy.html',context)
def predictedteam5(request):
    ft=FantasyTeam.objects.filter(id=5)
    if not ft:
        return HttpResponse("NOT AVAILABLE")
    ft=FantasyTeam.objects.get(id=5)
    context=ft.getteam()
    return render(request, '../templates/html/Fantasy.html',context)
def home(request):
    return render(request, '../templates/html/home.html')

def Fantasy(request):
    return render(request, '../templates/html/Fantasy.html')


def PlayerStats(request):
    return render(request, '../templates/html/PlayerStats.html')
def filterform(request):
    f= Form.objects.all().order_by('-currentform')
    return render(request, '../templates/html/filterform.html',context={'f':f})
def filterruns(request):
    player=Player.objects.all().order_by('-runs')

    return render(request, '../templates/html/filterruns.html',context={'player':player})
def filterwickets(request):
    player=Player.objects.all().order_by('-wickets')

    return render(request, '../templates/html/filterwickets.html',context={'player':player})
def filtereco(request):
    player=Player.objects.all().order_by('economy')

    return render(request, '../templates/html/filtereco.html',context={'player':player})
def filterinnings(request):
    player=Player.objects.all().order_by('-innings')

    return render(request, '../templates/html/filterinnings.html',context={'player':player})
def filteraverage(request):
    player=Player.objects.all().order_by('-average')

    return render(request, '../templates/html/filteraverage.html',context={'player':player})
def filterstrikerate(request):
    player=Player.objects.all().order_by('-strikerate')

    return render(request, '../templates/html/filtersr.html',context={'player':player})
def filterbowlavg(request):
    player=Player.objects.all().order_by('-bowlavg')

    return render(request, '../templates/html/filterbavg.html',context={'player':player})
def filterbsr(request):
    player=Player.objects.all().order_by('-bowlsr')

    return render(request, '../templates/html/filterbsr.html',context={'player':player})
def filterfours(request):
    player=Player.objects.all().order_by('-fours')

    return render(request, '../templates/html/filterfours.html',context={'player':player})
def filtersixes(request):
    player=Player.objects.all().order_by('-sixes')

    return render(request, '../templates/html/filtersixes.html',context={'player':player})
def filterfifties(request):
    player=Player.objects.all().order_by('-fifties')

    return render(request, '../templates/html/filterfifties.html',context={'player':player})
def filterhundreds(request):
    player=Player.objects.all().order_by('-hundreds')

    return render(request, '../templates/html/filterhundreds.html',context={'player':player})

def mainteamlist(request):
    player=PlayerTeam.objects.values_list('Team',flat='True').distinct()
    
    return render(request, '../templates/html/mainteamlist.html', context={'player':player})

def againstteamlist(request):
    player=AgainstTeam.objects.values_list('Team',flat='True').distinct()
    
    return render(request, '../templates/html/againstteamlist.html', context={'player':player})

def mainwteamlist(request):
    player=PlayerTeam.objects.values_list('Team',flat='True').distinct()
    
    return render(request, '../templates/html/mainwteamlist.html', context={'player':player})

def mainawteamlist(request):
    player=AgainstTeam.objects.values_list('Team',flat='True').distinct()
    
    return render(request, '../templates/html/mainawteamlist.html', context={'player':player})

def cityteamlist(request):
    player=City.objects.values_list('City',flat='True').distinct()
    
    return render(request, '../templates/html/cityteamlist.html', context={'player':player})

def citywteamlist(request):
    player=City.objects.values_list('City',flat='True').distinct()
    
    return render(request, '../templates/html/citywteamlist.html', context={'player':player})

def filterteamruns(request,team):
    player=PlayerTeam.objects.filter(Team=team).order_by('-runs')

    return render(request, '../templates/html/filterteamruns.html',context={'player':player})

def filterateamruns(request,team):
    player=AgainstTeam.objects.filter(Team=team).order_by('-runs')

    return render(request, '../templates/html/filterateamruns.html',context={'player':player})

def filterteamwickets(request,team):
    player=PlayerTeam.objects.filter(Team=team).order_by('-wickets')

    return render(request, '../templates/html/filterteamwickets.html',context={'player':player})

def filterateamwickets(request,team):
    player=AgainstTeam.objects.filter(Team=team).order_by('-wickets')

    return render(request, '../templates/html/filterateamwickets.html',context={'player':player})

def filtercityruns(request, city):
    player=City.objects.filter(City=city).order_by('-runs')

    return render(request, '../templates/html/filtercityruns.html',context={'player':player})

def filtercitywickets(request, city):
    player=City.objects.filter(City=city).order_by('-wickets')

    return render(request, '../templates/html/filtercitywickets.html',context={'player':player})

def filter(request):
    return render(request, '../templates/html/filter1.html')
def About(request):
    return render(request, '../templates/html/About.html')


def Contact(request):
    return render(request, '../templates/html/Contact.html')


def Disclaimer(request):
    return render(request, '../templates/html/Disclaimer.html')

def teamlist(request,id):
    player=PlayerTeam.objects.filter(name=id)
    
    return render(request, '../templates/html/teamlist.html',context={'player':player})
def powerplay(request, id):
    players=PowerPlay.objects.filter(name=id)
    if players:
        player=PowerPlay.objects.get(name=id)
        return render(request, '../templates/html/pp.html',context={'player':player})
    else:
        return render(request,'../templates/html/i.html')
def middleover(request, id):
    players=MiddleOvers.objects.filter(name=id)
    if players:
        players=MiddleOvers.objects.get(name=id)

        return render(request, '../templates/html/mo.html',context={'player':players})
    else:
        return render(request, '../templates/html/i.html')
def deathover(request, id):
    players=DeathOvers.objects.filter(name=id)
    if players:
        players=DeathOvers.objects.get(name=id)
        return render(request, '../templates/html/do.html',context={'player':players})
    else:
        return render(request, '../templates/html/i.html')
def citylist(request,id):
    player=City.objects.filter(name=id)
    
    return render(request, '../templates/html/citylist.html',context={'player':player})
    
def againstlist(request,id):
    player=AgainstTeam.objects.filter(name=id)
    
    return render(request, '../templates/html/againstlist.html',context={'player':player})


def playerProfile(request,id):
    
    player=Player.objects.get(name=id)
    context = {
				'player':player ,
                
			}
    return render(request, '../templates/html/playerProfile.html',context)

def playerProfile1(request,id):
    
    player=PlayerTeam.objects.get(id=id)
    return render(request, '../templates/html/playerProfile1.html',context={'player':player})
def playerProfile2(request,id):
    
    player=City.objects.get(id=id)
    return render(request, '../templates/html/playerProfile2.html',context={'player':player})
def playerProfile3(request,id):
    
    player=AgainstTeam.objects.get(id=id)
    return render(request, '../templates/html/playerProfile3.html',context={'player':player})
def playerProfile4(request,id):
    
    player=Position.objects.get(id=id)
    return render(request, '../templates/html/playerProfile4.html',context={'player':player})
def playerProfile5(request,id):
   
    player=Player.objects.get(name=id)
    return render(request, '../templates/html/playerProfile5.html',context={'player':player})
def playerProfile6(request,id):
   
    player=Player.objects.get(name=id)
    return render(request, '../templates/html/playerProfile6.html',context={'player':player})
def playerProfile7(request,id):
    
    player=Player.objects.get(name=id)
    return render(request, '../templates/html/playerProfile7.html',context={'player':player})
def m(request):
    player=Player.objects.all()

    return render(request, '../templates/html/matchups.html',context={'player':player})

def matchup1(request):
    
    try:
        entry_title = request.POST["drop1"]
    except KeyError:
        entry_title = "x"
    try:
        entry_title1 = request.POST["drop2"]
    except KeyError:
        entry_title1 = "x"
    print(entry_title)
    print(entry_title1)
    
    if entry_title and entry_title1:
        posts=Matchups.objects.filter(name=entry_title,bowler=entry_title1)
        if posts:
            posts = Matchups.objects.get(name=entry_title,bowler=entry_title1)
        else:
            return HttpResponse("THEY HAVE NOT FACED EACH OTHER")
       

    
    return render(request, '../templates/html/m1.html',context={'post':posts})
def matchup2(request):
    
    try:
        entry_title = request.POST["drop1"]
    except KeyError:
        entry_title = "x"
    try:
        entry_title1 = request.POST["drop2"]
    except KeyError:
        entry_title1 = "x"
    print(entry_title)
    print(entry_title1)
    
    if entry_title and entry_title1:
        posts=Player.objects.filter(name=entry_title)
        post=Player.objects.filter(name=entry_title1)
        if posts and post:
            posts = Player.objects.get(name=entry_title)
            post = Player.objects.get(name=entry_title1)
        else:
            return HttpResponse("NOT AVAILABLE")
        
       

    
    return render(request, '../templates/html/m2.html',context={'post':post,'posts':posts})




def login(request):
    return render(request, '../templates/html/login.html')



def createprofile(request):
    all=glob.glob("./stats/*.yaml")
    q=0
    for f in all:
        
    
        print("ayyy")

   
        with open(f,'r') as file:
            #setting currents runs as 0
            q=q+1
            print(q)
            print("------------------------vacharoi-----------------")
            
            curbatlist=[]
            curbowllist=[]


           #every3=Position.objects.all()
           # for z in every3:
                #z.currentrunszero()

            
            list_cricket=yaml.full_load(file)
            ls=[]#list of deliveries
            
            batlist=[]#list of all batsmen
            pp=[]
            mid=[]
            death=[]
            team1=list_cricket["innings"][0]["1st innings"]["team"]
            team2=list_cricket["innings"][1]["2nd innings"]["team"]
            city=list_cricket["info"]["city"]
            
            
            
            
                
            for x in list_cricket["innings"][0]["1st innings"]["deliveries"]:
                k=[key for key,value in x.items()]
                ls.append(k[0])
                if k[0]<7:
                    pp.append(k[0])
                if k[0]>=7 and k[0]<16:
                    mid.append(k[0])
                if k[0]>16:
                    death.append(k[0])
        k=0
        #posi=1
        l=0
        dicti={}
        for i in ls:
            b=list_cricket["innings"][0]["1st innings"]["deliveries"][l][i]["batsman"]
            if b not in curbatlist:
                curbatlist.append(b)
            m=Player.objects.filter(name=b)
            if m:
                mo=Player.objects.get(name=b)
                mo.currentrunszero()
            m=PlayerTeam.objects.filter(name=b)
            if m:
                for y in m:
                    y.currentrunszero()
            m=AgainstTeam.objects.filter(name=b)
            if m:
                for y in m:
                    y.currentrunszero()
            m=City.objects.filter(name=b)
            if m:
                for y in m:
                    y.currentrunszero()

            bo=list_cricket["innings"][0]["1st innings"]["deliveries"][l][i]["bowler"]
            if bo not in curbowllist:
                curbowllist.append(bo)
            m=Player.objects.filter(name=bo)
            #print(m)
            if m:
                #print(m)
                mp=Player.objects.get(name=bo)
                mp.currentwicketszero()
            m=PlayerTeam.objects.filter(name=bo)
            if m:
                for y in m:
                    y.currentwicketszero()
            m=AgainstTeam.objects.filter(name=bo)
            if m:
                for y in m:
                    y.currentwicketszero()
            m=City.objects.filter(name=bo)
            if m:
                for y in m:
                    y.currentwicketszero()

            l=l+1


            
        for i in ls:

            wide=0
            legbyes=0
            e=0
            
            
            bye=0
            p=(list_cricket["innings"][0]["1st innings"]["deliveries"][k][i])
            b=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["batsman"]
            if b not in batlist:
                batlist.append(b)
                #posb=Position.objects.filter(name=b,position=posi)
                #if not posb:
                    
                    #posb=Position(name=b,position=posi)
                    #posb.save()
               # posb=Position.objects.get(name=b,position=posi)
                #print("#")
                #print(b)
                #dicti[b]=posb
                #posi=posi+1
            bo=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["bowler"]
            runs=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["runs"]["batsman"]
            total=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["runs"]["total"]

            if "extras" in p.keys():
                e=1

                var=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["extras"]
                if "wides" in var.keys():
                    wide=1
                if "legbyes" in var.keys():
                    legbyes=1
                if "byes" in var.keys():
                    bye=1
            pla=Player.objects.filter(name=b)
            if not pla:
                profile=Player(name=b)
                
                profile.save()
            
            pla=Player.objects.get(name=b)
            if i<7:
                profile=PowerPlay.objects.filter(name=pla)
                if not profile:
                    pro=PowerPlay(name=pla)
                    pro.save()
                play=PowerPlay.objects.get(name=pla)
                play.ppupdateruns(runs)
            if i>=7 and i<16:
                profile=MiddleOvers.objects.filter(name=pla)
                if not profile:
                    pro=MiddleOvers(name=pla)
                    pro.save()
                player=MiddleOvers.objects.get(name=pla)
                player.midupdateruns(runs)
            if i>=16:
                profile=DeathOvers.objects.filter(name=pla)
                if not profile:
                    pro=DeathOvers(name=pla)
                    pro.save()
                players=DeathOvers.objects.get(name=pla)
                players.deathupdateruns(runs)
                
            plat=PlayerTeam.objects.filter(name=pla,Team=team1)
            ag=AgainstTeam.objects.filter(name=pla,Team=team2)
            cit=City.objects.filter(name=pla, City=city)
            if not cit:
                cite=City(name=pla,City=city)
                cite.save()
            if not plat:
                profileteam=PlayerTeam(name=pla,Team=team1)
                profileteam.save()
            if not ag:
                prot=AgainstTeam(name=pla,Team=team2)
                prot.save()
            prot=PlayerTeam.objects.get(name=pla,Team=team1)
            citi=City.objects.get(name=pla, City=city)
            agi=AgainstTeam.objects.get(name=pla,Team=team2)
            #posb=dicti[b]
            prot.updateruns(runs)
            agi.updateruns(runs)
            #posb.updateruns(runs)
            prot.setcurrentruns(runs)
            agi.setcurrentruns(runs)
            citi.updateruns(runs)
            citi.setcurrentruns(runs)
            #posb.setcurrentruns(runs)
            pla.updateruns(runs)
            pla.setcurrentruns(runs)
            if wide==0:
                pla.updateballsfaced()
                prot.updateballsfaced()
                citi.updateballsfaced()
               # posb.updateballsfaced()
                agi.updateballsfaced()
                if i<7:
                    play.ppupdateballsfaced()
                if i>=7 and i<16:
                    player.midupdateballsfaced()
                if i>=16:
                    players.deathupdateballsfaced()
            if runs==6:
                pla.updatesixes()
                prot.updatesixes()
                agi.updatesixes()
            if runs==4:
                pla.updatefours()
                prot.updatefours()
                agi.updatefours()

            pla=Player.objects.filter(name=bo)
            if not pla:
                profile=Player(name=bo)
                profile.save()
            pla=Player.objects.get(name=bo)
            plat=PlayerTeam.objects.filter(name=pla,Team=team2)
            citu=City.objects.filter(name=pla,City=city)
            aga=AgainstTeam.objects.filter(name=pla, Team=team1)
            if not plat:
                profileteam=PlayerTeam(name=pla,Team=team2)
                profileteam.save()
            if not citu:
                procit=City(name=pla, City=city)
                procit.save()
            if not aga:
                pi=AgainstTeam(name=pla,Team=team1)
                pi.save()
            prot=PlayerTeam.objects.get(name=pla,Team=team2)
            agn=AgainstTeam.objects.get(name=pla,Team=team1)
            citu=City.objects.get(name=pla, City=city)
            if i<7:
                profile=PowerPlay.objects.filter(name=pla)
                if not profile:
                    pro=PowerPlay(name=pla)
                    pro.save()
                play=PowerPlay.objects.get(name=pla)
                if e==0 or legbyes==1 or bye==1:
                    play.ppupdateballsbowled()

                if legbyes==0:
                    play.ppupdaterunsgiven(total)
            if i>=7 and i<16:
                profile=MiddleOvers.objects.filter(name=pla)
                if not profile:
                    pro=MiddleOvers(name=pla)
                    pro.save()
                player=MiddleOvers.objects.get(name=pla)
                if e==0 or legbyes==1 or bye==1:
                    player.midupdateballsbowled()
                if legbyes==0:
                    player.midupdaterunsgiven(total)
            if i>=16:
                profile=DeathOvers.objects.filter(name=pla)
                if not profile:
                    pro=DeathOvers(name=pla)
                    pro.save()
                players=DeathOvers.objects.get(name=pla)
                if e==0 or legbyes==1 or bye==1:
                    players.deathupdateballsbowled()
                if legbyes==0:
                    players.deathupdaterunsgiven(total)
            
            if e==0 or legbyes==1 or bye==1:
                pla.updateballsbowled()
                prot.updateballsbowled()
                citu.updateballsbowled()
                agn.updateballsbowled()
            if legbyes==0:
                pla.updaterunsgiven(total)
                prot.updaterunsgiven(total)
                citu.updaterunsgiven(total)
                agn.updaterunsgiven(total)

            if "wicket" in p.keys():
                    wi=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]["player_out"]
                    #print(wi,end=":")
                    outupdat = Player.objects.filter(name=wi)
                    if not outupdat :
                        outupdate = Player(name=wi)
                        outupdate.save()
                    playeroutupdate=Player.objects.get(name=wi)
                    playeroutupdate.out()
                    #posb=Position.objects.filter(name=wi,position=posi)
                    #if not posb:
                        
                        #posb=Position(name=wi,position=posi)
                        #posb.save()
                       # posb=Position.objects.get(name=wi,position=posi)
                       # dicti[wi]=posb
                        #posi=posi+1
                    outupdat = PlayerTeam.objects.filter(name=playeroutupdate, Team=team1)
                    if not outupdat :
                        outupdate = PlayerTeam(name=playeroutupdate,Team=team1)
                        outupdate.save()
                    outupdate1=PlayerTeam.objects.get(name=playeroutupdate,Team=team1)
                    outupdat = AgainstTeam.objects.filter(name=playeroutupdate,Team=team2)
                    if not outupdat :
                        outupdate = AgainstTeam(name=playeroutupdate,Team=team2)
                        outupdate.save()
                    ou=AgainstTeam.objects.get(name=playeroutupdate, Team=team2)
                    outupdat = City.objects.filter(name=playeroutupdate,City=city)
                    if not outupdat :
                        outupdate = City(name=playeroutupdate,City=city)
                        outupdate.save()
                    procit=City.objects.get(name=playeroutupdate, City=city)
                    
                    outupdate1.out()
                    ou.out()
                    procit.out()
                    #outupdat = Position.objects.filter(name=wi,position=dicti[wi].position)
                    #if not outupdat :
                        #outupdate = Position(name=wi,position=dicti[wi].position)
                        #outupdate.save()
                    #outupdate3=Position.objects.get(name=wi,position=dicti[wi].position)
                    #outupdate3.out()
                    if i<7:
                        playoutupdate=Player.objects.get(name=wi)
                        ppoutupdate= PowerPlay.objects.filter(name=playoutupdate)
                        if not ppoutupdate:
                            ppoutupdate= PowerPlay(name=playoutupdate)
                            ppoutupdate.save()
                        ppoutupdate=PowerPlay.objects.get(name=playoutupdate)
                        ppoutupdate.ppout()
                    if i>=7 and i<16:
                        playoutupdate=Player.objects.get(name=wi)
                        midoutupdate= MiddleOvers.objects.filter(name=playoutupdate)
                        if not midoutupdate:
                            midoutupdate= MiddleOvers(name=playoutupdate)
                            midoutupdate.save()
                        midoutupdate=MiddleOvers.objects.get(name=playoutupdate)
                        midoutupdate.midout()
                    if i>=16:
                        playoutupdate=Player.objects.get(name=wi)
                        deathoutupdate= DeathOvers.objects.filter(name=playoutupdate)
                        if not deathoutupdate:
                            deathoutupdate= DeathOvers(name=playoutupdate)
                            deathoutupdate.save()
                        deathoutupdate=DeathOvers.objects.get(name=playoutupdate)
                        deathoutupdate.deathout()
                    
                        
                    ki=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]["kind"]
           
                    x=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]
           
                    if "fielders" in x.keys():
                        c=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]["fielders"][0]
                        fiel=Player.objects.filter(name=c)
                        if not fiel:
                            profile=Player(name=c)
                            profile.save()
                        
                        fiel=Player.objects.get(name=c)
                        if ki!="run out":
                            fiel.updatecatches()
                            pla.updatewickets()
                            pla.setcurrentwickets()
                            prot.updatewickets()
                            prot.setcurrentwickets()
                            citu.updatewickets()
                            citu.setcurrentwickets()
                            agn.updatewickets()
                            agn.setcurrentwickets()

                            if i<7:
                                play.ppupdatewickets()
                            if i>=7 and i<16:
                                player.midupdatewickets()
                            if i>=16:
                                players.deathupdatewickets()
                       
                    else:
                        if ki!="run out":
                            pla.updatewickets()
                            pla.setcurrentwickets()
                            prot.updatewickets()
                            prot.setcurrentwickets()
                            citu.updatewickets()
                            citu.setcurrentwickets()
                            agn.updatewickets()
                            agn.setcurrentwickets()
                            if i<7:
                                play.ppupdatewickets()
                            if i>=7 and i<16:
                                player.midupdatewickets()
                            if i>=16:
                                players.deathupdatewickets()

            k=k+1
        res=N.array(curbatlist)
        print("hmm")
        unique_res=N.unique(res)

        for some in unique_res:
            print(some)
            pin=Player.objects.get(name=some)
            pin.setfiftiesandhundreds()
            pint=PlayerTeam.objects.get(name=some,Team=team1)
            pin.updateinnings() 
            pint.setfiftiesandhundreds()
            pinto=AgainstTeam.objects.get(name=some,Team=team2)
            pinto.updateinnings() 
            pinto.setfiftiesandhundreds()
            #posb=Position.objects.get(name=some,position=dicti[some].position)
            #posb.updateinnings()
            pint.updateinnings()
            pc=City.objects.get(name=some,City=city)
            pc.updateinnings()
            pc.setfiftiesandhundreds()

        resu=N.array(curbowllist)
        unique_resu=N.unique(resu)
        for some in unique_resu:
        
            pin=Player.objects.get(name=some)
            pin.fourw()
            pint=PlayerTeam.objects.get(name=some,Team=team2)
             
            pint.fourw()
            pinto=AgainstTeam.objects.get(name=some,Team=team1)
            pinto.fourw() 
            
            #posb=Position.objects.get(name=some,position=dicti[some].position)
            #posb.updateinnings()
    
            pc=City.objects.get(name=some,City=city)
        
            pc.fourw()

        print("___________________malli___________")
        
        l=0
        curbatlist=[]
        curbowllist=[]
       
        
        ls=[]
        batlist=[]
        pp=[]
        team1=list_cricket["innings"][0]["1st innings"]["team"]
        team2=list_cricket["innings"][1]["2nd innings"]["team"]
        
        
        
        posi=1
            
        for x in list_cricket["innings"][1]["2nd innings"]["deliveries"]:
            k=[key for key,value in x.items()]
            ls.append(k[0])
            if k[0]<7:
                pp.append(k[0])
        k=0
        dicti1={}
        for i in ls:
            b=list_cricket["innings"][1]["2nd innings"]["deliveries"][l][i]["batsman"]
            if b not in curbatlist:
                curbatlist.append(b)
            m=Player.objects.filter(name=b)
            if m:
                mo=Player.objects.get(name=b)
                mo.currentrunszero()
            m=PlayerTeam.objects.filter(name=b)
            if m:
                for y in m:
                    y.currentrunszero()
            m=AgainstTeam.objects.filter(name=b)
            if m:
                for y in m:
                    y.currentrunszero()
            m=City.objects.filter(name=b)
            if m:
                for y in m:
                    y.currentrunszero()

            bo=list_cricket["innings"][1]["2nd innings"]["deliveries"][l][i]["bowler"]
            if bo not in curbowllist:
                curbowllist.append(bo)
            m=Player.objects.filter(name=bo)
            #print(m)
            if m:
                #print(m)
                mp=Player.objects.get(name=bo)
                mp.currentwicketszero()
            m=PlayerTeam.objects.filter(name=bo)
            if m:
                for y in m:
                    y.currentwicketszero()
            m=AgainstTeam.objects.filter(name=bo)
            if m:
                for y in m:
                    y.currentwicketszero()
            m=City.objects.filter(name=bo)
            if m:
                for y in m:
                    y.currentwicketszero()

            l=l+1
        for i in ls:
            wide=0
            legbyes=0
            
            
            e=0
            bye=0
            p=(list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i])
            b=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["batsman"]
            if b not in batlist:
                batlist.append(b)
                #posb=Position.objects.filter(name=b,position=posi)
               # if not posb:
                    
                    #posb=Position(name=b,position=posi)
                   # posb.save()
                #posb=Position.objects.get(name=b,position=posi)
                #dicti1[b]=posb
                #posi=posi+1
            bo=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["bowler"]
            runs=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["runs"]["batsman"]
            total=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["runs"]["total"]

            if "extras" in p.keys():
                e=1

                var=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["extras"]
                if "wides" in var.keys():
                    wide=1
                if "legbyes" in var.keys():
                    legbyes=1
                if "byes" in var.keys():
                    bye=1
            pla=Player.objects.filter(name=b)
            if not pla:
                profile=Player(name=b)
                
                profile.save()
            
            pla=Player.objects.get(name=b)
            
            if i<7:
                profile=PowerPlay.objects.filter(name=pla)
                if not profile:
                    pro=PowerPlay(name=pla)
                    pro.save()
                play=PowerPlay.objects.get(name=pla)
                play.ppupdateruns(runs)
            if i>=7 and i<16:
                profile=MiddleOvers.objects.filter(name=pla)
                if not profile:
                    pro=MiddleOvers(name=pla)
                    pro.save()
                player=MiddleOvers.objects.get(name=pla)
                player.midupdateruns(runs)
            if i>=16:
                profile=DeathOvers.objects.filter(name=pla)
                if not profile:
                    pro=DeathOvers(name=pla)
                    pro.save()
                players=DeathOvers.objects.get(name=pla)
                players.deathupdateruns(runs)
                            
            plat=PlayerTeam.objects.filter(name=pla,Team=team2)
            at=AgainstTeam.objects.filter(name=pla,Team=team1)
            cit=City.objects.filter(name=pla, City=city)
            if not plat:
                profileteam=PlayerTeam(name=pla,Team=team2)
                profileteam.save()
            if not at:
                profileteam=AgainstTeam(name=pla,Team=team1)
                profileteam.save()
            if not cit:
                procit=City(name=pla, City=city)
                procit.save()

            prot=PlayerTeam.objects.get(name=pla,Team=team2)
            ot=AgainstTeam.objects.get(name=pla,Team=team1)
            citi=City.objects.get(name=pla, City=city)
            #posb=dicti1[b]
            prot.updateruns(runs)
            ot.updateruns(runs)
            prot.setcurrentruns(runs)
            citi.updateruns(runs)
            citi.setcurrentruns(runs)
            ot.setcurrentruns(runs)
            pla.updateruns(runs)
            #posb.updateruns(runs)
            pla.setcurrentruns(runs)
            #posb.setcurrentruns(runs)
            if wide==0:
                pla.updateballsfaced()
                prot.updateballsfaced()
                #posb.updateballsfaced()
                citi.updateballsfaced()
                ot.updateballsfaced()
                if i<7:
                    play.ppupdateballsfaced()
                if i>=7 and i<16:
                    player.midupdateballsfaced()
                if i>=16:
                    players.deathupdateballsfaced()
            if runs==6:
                pla.updatesixes()
                prot.updatesixes()
                ot.updatesixes()
            if runs==4:
                pla.updatefours()
                prot.updatefours()
                ot.updatefours()

            pla=Player.objects.filter(name=bo)
            if not pla:
                profile=Player(name=bo)
                profile.save()
            pla=Player.objects.get(name=bo)
            plat=PlayerTeam.objects.filter(name=pla,Team=team1)
            la=AgainstTeam.objects.filter(name=pla,Team=team2)
            citu=City.objects.filter(name=pla, City=city)
            if not plat:
                profileteam=PlayerTeam(name=pla,Team=team1)
                profileteam.save()
            if not la:
                profileteam=AgainstTeam(name=pla,Team=team2)
                profileteam.save()
            if not citu:
                procit=City(name=pla, City=city)
                procit.save()
            prot=PlayerTeam.objects.get(name=pla,Team=team1)
            ro=AgainstTeam.objects.get(name=pla,Team=team2)
            cite=City.objects.get(name=pla, City=city)
            if i<7:
                profile=PowerPlay.objects.filter(name=pla)
                if not profile:
                    pro=PowerPlay(name=pla)
                    pro.save()
                play=PowerPlay.objects.get(name=pla)
                if e==0 or legbyes==1 or bye==1:
                    play.ppupdateballsbowled()
                if legbyes==0:
                    play.ppupdaterunsgiven(total)
            if i>=7 and i<16:
                profile=MiddleOvers.objects.filter(name=pla)
                if not profile:
                    pro=MiddleOvers(name=pla)
                    pro.save()
                player=MiddleOvers.objects.get(name=pla)
                if e==0 or legbyes==1 or bye==1:
                    player.midupdateballsbowled()
                if legbyes==0:
                    player.midupdaterunsgiven(total)
            if i>=16:
                profile=DeathOvers.objects.filter(name=pla)
                if not profile:
                    pro=DeathOvers(name=pla)
                    pro.save()
                players=DeathOvers.objects.get(name=pla)
                if e==0 or legbyes==1 or bye==1:
                    players.deathupdateballsbowled()
                if legbyes==0:
                    players.deathupdaterunsgiven(total)
            if e==0 or legbyes==1 or bye==1:
                pla.updateballsbowled()
                prot.updateballsbowled()
                cite.updateballsbowled()
                ro.updateballsbowled()

            if legbyes==0:
                pla.updaterunsgiven(total)
                prot.updaterunsgiven(total)
                cite.updaterunsgiven(total)
                ro.updaterunsgiven(total)

            if "wicket" in p.keys():
                    wi=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]["player_out"]
                    #print(wi,end=":")
                    outupdat = Player.objects.filter(name=wi)
                    if not outupdat :
                        outupdate = Player(name=wi)
                        outupdate.save()
                    outupdate=Player.objects.get(name=wi)
                    outupdate.out()
                   # posb=Position.objects.filter(name=wi,position=posi)
                    #if not posb:
                        
                        #posb=Position(name=wi,position=posi)
                        #posb.save()
                        #posb=Position.objects.get(name=wi,position=posi)
                        #dicti1[wi]=posb
                        #posi=posi+1
                    outupdat = PlayerTeam.objects.filter(name=outupdate, Team=team2)
                    if not outupdat :
                        outupdate1 = PlayerTeam(name=outupdate, Team=team2)
                        outupdate1.save()
                    outupdate1=PlayerTeam.objects.get(name=outupdate,Team=team2)
                    outupdat = City.objects.filter(name=outupdate,City=city)
                    if not outupdat :
                        outupdate2 = City(name=outupdate, City=city)
                        outupdate2.save()
                    outupdate2=City.objects.get(name=outupdate, City=city)
                    outupdat = AgainstTeam.objects.filter(name=outupdate,Team=team1)
                    if not outupdat :
                        outupdate4 = AgainstTeam(name=outupdate, Team=team1)
                        outupdate4.save()
                    outupdate4=AgainstTeam.objects.get(name=outupdate,Team=team1)
                   # outupdat = Position.objects.filter(name=wi,position=dicti1[wi].position)
                   # if not outupdat :
                      #  outupdate3 = Position(name=wi,position=dicti1[wi].position )
                       # outupdate3.save()
                   # outupdate3=Position.objects.get(name=wi,position=dicti1[wi].position)
                    outupdate2.out()
                    outupdate1.out()
                    #outupdate3.out()
                    outupdate4.out()
                    if i<7:
                        playoutupdate=Player.objects.get(name=wi)
                        ppoutupdate= PowerPlay.objects.filter(name=playoutupdate)
                        if not ppoutupdate:
                            ppoutupdate= PowerPlay(name=playoutupdate)
                            ppoutupdate.save()
                        ppoutupdate=PowerPlay.objects.get(name=playoutupdate)
                        ppoutupdate.ppout()
                    if i>=7 and i<16:
                        playoutupdate=Player.objects.get(name=wi)
                        midoutupdate= MiddleOvers.objects.filter(name=playoutupdate)
                        if not midoutupdate:
                            midoutupdate= MiddleOvers(name=playoutupdate)
                            midoutupdate.save()
                        midoutupdate=MiddleOvers.objects.get(name=playoutupdate)
                        midoutupdate.midout()
                    if i>=16:
                        playoutupdate=Player.objects.get(name=wi)
                        deathoutupdate= DeathOvers.objects.filter(name=playoutupdate)
                        if not deathoutupdate:
                            deathoutupdate= DeathOvers(name=playoutupdate)
                            deathoutupdate.save()
                        deathoutupdate=DeathOvers.objects.get(name=playoutupdate)
                        deathoutupdate.deathout()
                    
                        
                    ki=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]["kind"]
            
                    x=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]
            
                    if "fielders" in x.keys():
                        c=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]["fielders"][0]
                        fiel=Player.objects.filter(name=c)
                        if not fiel:
                            profile=Player(name=c)
                            profile.save()

                        fiel=Player.objects.get(name=c)
                        if ki!="run out":
                            fiel.updatecatches()
                            pla.updatewickets()
                            pla.setcurrentwickets()
                            prot.updatewickets()
                            prot.setcurrentwickets()
                            cite.updatewickets()
                            cite.setcurrentwickets()
                            ro.updatewickets()
                            ro.setcurrentwickets()
                            if i<7:
                                play.ppupdatewickets()
                            if i>=7 and i<16:
                                player.midupdatewickets()
                            if i>=16:
                                players.deathupdatewickets()
                        
                    else:
                        if ki!="run out":
                            pla.updatewickets()
                            pla.setcurrentwickets()
                            prot.updatewickets()
                            prot.setcurrentwickets()
                            cite.updatewickets()
                            cite.setcurrentwickets()
                            ro.updatewickets()
                            ro.setcurrentwickets()
                            if i<7:
                                play.ppupdatewickets()
                            if i>=7 and i<16:
                                player.midupdatewickets()
                            if i>=16:
                                players.deathupdatewickets()

            k=k+1
        res=N.array(batlist)
      

        unique_res=N.unique(res)
        for some in unique_res:
            pin=Player.objects.get(name=some)
            pint=PlayerTeam.objects.get(name=some,Team=team2)
            pin.updateinnings() 
            pin.setfiftiesandhundreds()
            pint.updateinnings()
            pint.setfiftiesandhundreds()
            pinto=AgainstTeam.objects.get(name=some,Team=team1)
            pinto.updateinnings() 
            pinto.setfiftiesandhundreds()
            #posb=Position.objects.get(name=some,position=dicti1[some].position)
            #posb.updateinnings()
            pc=City.objects.get(name=some,City=city)
            pc.updateinnings()
            pc.setfiftiesandhundreds()
       

        resu=N.array(curbowllist)
        unique_resu=N.unique(resu)
        for some in unique_resu:
        
            pin=Player.objects.get(name=some)
            pin.fourw()
            pint=PlayerTeam.objects.get(name=some,Team=team1)
             
            pint.fourw()
            pinto=AgainstTeam.objects.get(name=some,Team=team2)
            pinto.fourw() 
            
            #posb=Position.objects.get(name=some,position=dicti[some].position)
            #posb.updateinnings()
    
            pc=City.objects.get(name=some,City=city)
        
            pc.fourw()
    return HttpResponse("updated")
def search_players(request):
    query=request.GET.get('q1')
    ls=query.split(' ')
    l=len(ls)
    if query:
        posts = Player.objects.all()
        if l==1:
            results=posts.filter(Q(name__icontains=ls[0]))
        else:
            results=posts.filter(Q(name__icontains=ls[l-1]))

	
    return render(request, '../templates/html/playerslist.html',context={'players':results})

def updatedepends(request):
    print("yes")
    every=Player.objects.all()
    print("hu")
    for i in every:
        i.seteco()
        i.setaverage()
        i.setsr()

            #i.setfiftiesandhundreds()
    every1=PlayerTeam.objects.all()
    for i in every1:
        i.seteco()
        i.setaverage()
        i.setsr()
            #i.setfiftiesandhundreds()
    every6=AgainstTeam.objects.all()
    for i in every6:
        i.seteco()
        i.setaverage()
        i.setsr()
    every7=City.objects.all()
    for i in every7:
        i.seteco()
        i.setaverage()
        i.setsr()
           # i.setfiftiesandhundreds()
            
        #every4=Position.objects.all()
        #for i in every4:
            #i.setaverage()
            #i.setsr()
            
    ppevery=PowerPlay.objects.all()
    for j in ppevery:
        j.setppeco()
        j.setppsr()
        j.setppaverage()
    midevery=MiddleOvers.objects.all()
    for j in midevery:
        j.setmideco()
        j.setmidsr()
        j.setmidaverage()
    deathevery=DeathOvers.objects.all()
    for j in deathevery:
        j.setdeatheco()
        j.setdeathsr()
        j.setdeathaverage()
    return HttpResponse("done")

def matchuprecords(request):
    all=glob.glob("./stats/*.yaml")
    for f in all:
        with open(f,'r') as file:
            every=Player.objects.all()
            
            list_cricket=yaml.full_load(file)
            ls=[]
            
            batlist=[]
            pp=[]
            mid=[]
            death=[]
            team1=list_cricket["innings"][0]["1st innings"]["team"]
            team2=list_cricket["innings"][1]["2nd innings"]["team"]
           
            
            
            
                
            for x in list_cricket["innings"][0]["1st innings"]["deliveries"]:
                k=[key for key,value in x.items()]
                ls.append(k[0])
            
            k=0
            for i in ls:

                wide=0
                legbyes=0
                e=0
                bye=0
                p=(list_cricket["innings"][0]["1st innings"]["deliveries"][k][i])
                b=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["batsman"]
                batlist.append(b)
                bo=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["bowler"]
                runs=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["runs"]["batsman"]
                total=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["runs"]["total"]
                if "extras" in p.keys():
                    e=1
                    var=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["extras"]
                    if "wides" in var.keys():
                        wide=1
                    if "legbyes" in var.keys():
                        legbyes=1
                    if "byes" in var.keys():
                        bye=1
                pla= Player.objects.filter(name=b)
                if not pla:
                    pla=Player(name=b)
                    pla.save()
                pla=Player.objects.get(name=b)
                mat=Matchups.objects.filter(name=pla,bowler=bo)
                if not mat:
                    profile=Matchups(name=pla,bowler=bo)
                    profile.save()
                mat=Matchups.objects.get(name=pla, bowler=bo)
                mat.updateruns(runs)
                if wide==0:
                    mat.updateballsfaced()
                play= Player.objects.filter(name=bo)
                if not play:
                    play=Player(name=bo)
                    play.save()
                play=Player.objects.get(name=bo)
                mats=Matchups.objects.filter(name=play,bowler=b)
                if not mats:
                    profile=Matchups(name=play,bowler=b)
                    profile.save()
                mats=Matchups.objects.get(name=play,bowler=b)
                if e==0 or legbyes==1 or bye==1:
                    mats.updateballsbowled()
                if legbyes==0 :
                    mats.updaterunsgiven(total)

                if "wicket" in p.keys():
                    wi=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]["player_out"]
                    #print(wi,end=":")
                    outupdates= Player.objects.filter(name=wi)
                    if not outupdates:
                        outupdate=Player(name=wi)
                        outupdate.save()

                    outupdate=Player.objects.get(name=wi)

                    outupdates= Matchups.objects.filter(name=wi,bowler=bo)
                    if not outupdates:
                        outupdate1=Matchups(name=outupdate,bowler=bo)
                        outupdate1.save()
                    outupdate1=Matchups.objects.get(name=wi,bowler=bo)
                  
                    ki=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]["kind"]
           
                    x=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]
           
                    if "fielders" in x.keys():
                        c=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]["fielders"][0]
                        
                        if ki != "run out":
                            mats.updatewickets()
                            mat.updateouts()
                    else:
                        mats.updatewickets()
                        mat.updateouts()

                k=k+1
            
            every=Matchups.objects.all()
            for i in every:
                i.seteco()
                i.setaverage()
                i.setsr()
            ls1=[]
            for x in list_cricket["innings"][1]["2nd innings"]["deliveries"]:
                k=[key for key,value in x.items()]
                
                ls1.append(k[0])
            k=0
            for i in ls1:
                wide=0
                legbyes=0
                e=0
                bye=0
                p=(list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i])
                b=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["batsman"]
                batlist.append(b)
                bo=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["bowler"]
                runs=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["runs"]["batsman"]
                total=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["runs"]["total"]
                pla= Player.objects.filter(name=b)
                if not pla:
                    pla=Player(name=b)
                    pla.save()
                pla=Player.objects.get(name=b)
                mat=Matchups.objects.filter(name=pla,bowler=bo)
                if not mat:
                    profile=Matchups(name=pla,bowler=bo)
                    profile.save()
                mat=Matchups.objects.get(name=pla, bowler=bo)
                mat.updateruns(runs)
                if wide==0:
                    mat.updateballsfaced()
                play= Player.objects.filter(name=bo)
                if not play:
                    play=Player(name=bo)
                    play.save()
                play=Player.objects.get(name=bo)
                mats=Matchups.objects.filter(name=play,bowler=b)
                if not mats:
                    profile=Matchups(name=play,bowler=b)
                    profile.save()
                mats=Matchups.objects.get(name=play,bowler=b)
                if e==0 or legbyes==1 or bye==1:
                    mats.updateballsbowled()
                if legbyes==0:
                    mats.updaterunsgiven(total)

                if "wicket" in p.keys():
                    wi=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]["player_out"]
                    #print(wi,end=":")
                    outupdates= Player.objects.filter(name=wi)
                    if not outupdates:
                        outupdate=Player(name=wi)
                        outupdate.save()

                    outupdate=Player.objects.get(name=wi)

                    outupdates= Matchups.objects.filter(name=wi,bowler=bo)
                    if not outupdates:
                        outupdate1=Matchups(name=outupdate,bowler=bo)
                        outupdate1.save()
                    outupdate1=Matchups.objects.get(name=wi,bowler=bo)
                  
                  
                    ki=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]["kind"]
           
                    x=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]
           
                    if "fielders" in x.keys():
                        c=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]["fielders"][0]
                        
                        if ki != "run out":
                            mats.updatewickets()
                            mat.updateouts()
                    else:
                        mats.updatewickets()
                        mat.updateouts()

                k=k+1
            
            every=Matchups.objects.all()
            for i in every:
                i.seteco()
                i.setaverage()
                i.setsr()

        
    return HttpResponse("updated")
                        
def updateform(request):
    all=glob.glob("./stats/1254058.yaml")
    for f in all:
        with open(f,'r') as file:
            every=Player.objects.all()
            everyform=Form.objects.all()
            for formplayer in everyform:
                formplayer.setcurrentzero()
            list_cricket=yaml.full_load(file)
            ls=[]
            listofplayers=[]
            
            
                
            for x in list_cricket["innings"][0]["1st innings"]["deliveries"]:
                k=[key for key,value in x.items()]
                ls.append(k[0])
            
            k=0
            for i in ls:

                wide=0
                legbyes=0
                e=0
                bye=0
                p=(list_cricket["innings"][0]["1st innings"]["deliveries"][k][i])
                b=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["batsman"]
                listofplayers.append(b)
                bo=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["bowler"]
                listofplayers.append(bo)
                runs=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["runs"]["batsman"]
                total=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["runs"]["total"]
                if "extras" in p.keys():
                    e=1
                    var=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["extras"]
                    if "wides" in var.keys():
                        wide=1
                    if "legbyes" in var.keys():
                        legbyes=1
                    if "byes" in var.keys():
                        bye=1
                pla= Player.objects.filter(name=b)
                if not pla:
                    pla=Player(name=b)
                    pla.save()
                pla=Player.objects.get(name=b)
                f=Form.objects.filter(name=pla)
                if not f:
                    f=Form(name=pla)
                    f.save()
                f=Form.objects.get(name=pla)
                f.updateruns(runs)
                if wide==0:
                    f.updateballsfaced()
                play= Player.objects.filter(name=bo)
                if not play:
                    play=Player(name=bo)
                    play.save()
                play=Player.objects.get(name=bo)
                fb=Form.objects.filter(name=play)
                if not fb:
                    fb=Form(name=play)
                    fb.save()
                fb=Form.objects.get(name=play)
                if e==0 or legbyes==1 or bye==1:
                    fb.updateballsbowled()
                if legbyes==0 :
                    fb.updaterunsgiven(total)

                if "wicket" in p.keys():
                    wi=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]["player_out"]
                    #print(wi,end=":")
                    outupdates= Player.objects.filter(name=wi)
                    if not outupdates:
                        outupdate=Player(name=wi)
                        outupdate.save()

                    outupdate=Player.objects.get(name=wi)

                    outupdates= Form.objects.filter(name=wi)
                    if not outupdates:
                        outupdate1=Form(name=outupdate)
                        outupdate1.save()
                    outupdate1=Form.objects.get(name=wi)
                  
                    ki=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]["kind"]
           
                    x=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]
           
                    if "fielders" in x.keys():
                        c=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]["fielders"][0]
                        
                        if ki != "run out":
                            fb.updatewickets()
                            #f.updateouts()
                    else:
                        fb.updatewickets()
                        #f.updateouts()

                k=k+1
            
            
            ls1=[]
            for x in list_cricket["innings"][1]["2nd innings"]["deliveries"]:
                k=[key for key,value in x.items()]
                
                ls1.append(k[0])
            k=0
            for i in ls1:
                wide=0
                legbyes=0
                e=0
                bye=0
                p=(list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i])
                b=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["batsman"]
                listofplayers.append(b)
                bo=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["bowler"]
                listofplayers.append(bo)
                runs=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["runs"]["batsman"]
                total=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["runs"]["total"]
                pla= Player.objects.filter(name=b)
                if not pla:
                    pla=Player(name=b)
                    pla.save()
                pla=Player.objects.get(name=b)
                f=Form.objects.filter(name=pla)
                if not f:
                    f=Form(name=pla)
                    f.save()
                f=Form.objects.get(name=pla)
                f.updateruns(runs)
                if wide==0:
                    f.updateballsfaced()
                play= Player.objects.filter(name=bo)
                if not play:
                    play=Player(name=bo)
                    play.save()
                play=Player.objects.get(name=bo)
                fb=Form.objects.filter(name=play)
                if not fb:
                    fb=Form(name=play)
                    fb.save()
                fb=Form.objects.get(name=play)
                if e==0 or legbyes==1 or bye==1:
                    fb.updateballsbowled()
                if legbyes==0:
                    fb.updaterunsgiven(total)

                if "wicket" in p.keys():
                    wi=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]["player_out"]
                    #print(wi,end=":")
                    outupdates= Player.objects.filter(name=wi)
                    if not outupdates:
                        outupdate=Player(name=wi)
                        outupdate.save()

                    outupdate=Player.objects.get(name=wi)

                    outupdates= Form.objects.filter(name=wi)
                    if not outupdates:
                        outupdate1=Form(name=outupdate)
                        outupdate1.save()
                    outupdate1=Form.objects.get(name=wi)
                  
                  
                    ki=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]["kind"]
           
                    x=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]
           
                    if "fielders" in x.keys():
                        c=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]["fielders"][0]
                        
                        if ki != "run out":
                            fb.updatewickets()
                            #f.updateouts()
                    else:
                        fb.updatewickets()
                        #f.updateouts()

                k=k+1
            
            res=N.array(listofplayers)
            print("hmm")
            unique_res=N.unique(listofplayers)

            for some in unique_res:
                print(some)
                pin=Form.objects.get(name=some)
                pin.updatepointer()

        
    return HttpResponse("updated")
                        
