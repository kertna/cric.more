from django.shortcuts import render
import glob
from .models import Player,PowerPlay,PlayerTeam,MiddleOvers,DeathOvers
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
def home(request):
    return render(request, '../templates/html/home.html')


def Fantasy(request):
    return render(request, '../templates/html/Fantasy.html')


def PlayerStats(request):
    return render(request, '../templates/html/PlayerStats.html')


def About(request):
    return render(request, '../templates/html/About.html')


def Contact(request):
    return render(request, '../templates/html/Contact.html')


def Disclaimer(request):
    return render(request, '../templates/html/Disclaimer.html')


def playerProfile(request,id):
    print(id)
    player=Player.objects.get(name=id)
    return render(request, '../templates/html/playerProfile.html',context={'player':player})


def login(request):
    return render(request, '../templates/html/login.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, '../templates/html/register.html', {'form': form})

def createprofile(request):
    all=glob.glob("./stats/*.yaml")
    for f in all:
        with open(f,'r') as file:
            every=Player.objects.all()
            for z in every:
                z.currentrunszero()
            every1=PlayerTeam.objects.all()
            for z in every1:
                z.currentrunszero()
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
                if k[0]<7:
                    pp.append(k[0])
                if k[0]>=7 and k[0]<16:
                    mid.append(k[0])
                if k[0]>16:
                    death.append(k[0])
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
            if not plat:
                profileteam=PlayerTeam(name=pla,Team=team1)
                profileteam.save()
            prot=PlayerTeam.objects.get(name=pla,Team=team1)
            prot.updateruns(runs)
            prot.setcurrentruns(runs)
            pla.updateruns(runs)
            pla.setcurrentruns(runs)
            if wide==0:
                pla.updateballsfaced()
                prot.updateballsfaced()
                if i<7:
                    play.ppupdateballsfaced()
                if i>=7 and i<16:
                    player.midupdateballsfaced()
                if i>=16:
                    players.deathupdateballsfaced()
            if runs==6:
                pla.updatesixes()
                prot.updatesixes()
            if runs==4:
                pla.updatefours()
                prot.updatefours()

            pla=Player.objects.filter(name=bo)
            if not pla:
                profile=Player(name=bo)
                profile.save()
            pla=Player.objects.get(name=bo)
            plat=PlayerTeam.objects.filter(name=pla,Team=team2)
            if not plat:
                profileteam=PlayerTeam(name=pla,Team=team2)
                profileteam.save()
            prot=PlayerTeam.objects.get(name=pla,Team=team2)
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
            if legbyes==0:
                pla.updaterunsgiven(total)
                prot.updaterunsgiven(total)

            if "wicket" in p.keys():
                    wi=list_cricket["innings"][0]["1st innings"]["deliveries"][k][i]["wicket"]["player_out"]
                    #print(wi,end=":")
                    outupdate=Player.objects.get(name=wi)
                    outupdate.out()
                    outupdate1=PlayerTeam.objects.get(name=wi,Team=team1)
                    outupdate1.out()
                    if i<7:
                        playoutupdate=Player.objects.get(name=wi)
                        ppoutupdate=PowerPlay.objects.get(name=playoutupdate)
                        ppoutupdate.ppout()
                    if i>=7 and i<16:
                        playoutupdate=Player.objects.get(name=wi)
                        midoutupdate=MiddleOvers.objects.get(name=playoutupdate)
                        midoutupdate.midout()
                    if i>=16:
                        playoutupdate=Player.objects.get(name=wi)
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
                        fiel.updatecatches()
                        pla.updatewickets()
                        prot.updatewickets()
                        if i<7:
                            play.ppupdatewickets()
                        if i>=7 and i<16:
                            player.midupdatewickets()
                        if i>=16:
                            players.deathupdatewickets()
                       
                    else:
                        if ki!="run out":
                            pla.updatewickets()
                            prot.updatewickets()
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
            pint=PlayerTeam.objects.get(name=some,Team=team1)
            pin.updateinnings() 
            pint.updateinnings()
        every=Player.objects.all()
        for i in every:
            i.seteco()
            i.setaverage()
            i.setsr()
            i.fourw()
        every1=PlayerTeam.objects.all()
        for i in every1:
            i.seteco()
            i.setaverage()
            i.setsr()
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
        
        every=Player.objects.all()
        for z in every:
            z.currentrunszero()
        every1=PlayerTeam.objects.all()
        for z in every1:
            z.currentrunszero()
        
        ls=[]
        batlist=[]
        pp=[]
        team1=list_cricket["innings"][0]["1st innings"]["team"]
        team2=list_cricket["innings"][1]["2nd innings"]["team"]
        
        
        
        
            
        for x in list_cricket["innings"][1]["2nd innings"]["deliveries"]:
            k=[key for key,value in x.items()]
            ls.append(k[0])
            if k[0]<7:
                pp.append(k[0])
        k=0
        for i in ls:
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
            plat=PlayerTeam.objects.filter(name=pla,Team=team2)
            if not plat:
                profileteam=PlayerTeam(name=pla,Team=team2)
                profileteam.save()
            prot=PlayerTeam.objects.get(name=pla,Team=team2)
            prot.updateruns(runs)
            prot.setcurrentruns(runs)
            pla.updateruns(runs)
            pla.setcurrentruns(runs)
            if wide==0:
                pla.updateballsfaced()
                prot.updateballsfaced()
                if i<7:
                    play.ppupdateballsfaced()
            if runs==6:
                pla.updatesixes()
                prot.updatesixes()
            if runs==4:
                pla.updatefours()
                prot.updatefours()

            pla=Player.objects.filter(name=bo)
            if not pla:
                profile=Player(name=bo)
                profile.save()
            pla=Player.objects.get(name=bo)
            plat=PlayerTeam.objects.filter(name=pla,Team=team1)
            if not plat:
                profileteam=PlayerTeam(name=pla,Team=team1)
                profileteam.save()
            prot=PlayerTeam.objects.get(name=pla,Team=team1)
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
            
            if e==0 or legbyes==1 or bye==1:
                pla.updateballsbowled()
                prot.updateballsbowled()
            if legbyes==0:
                pla.updaterunsgiven(total)
                prot.updaterunsgiven(total)

            if "wicket" in p.keys():
                    wi=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]["player_out"]
                    #print(wi,end=":")
                    outupdate=Player.objects.get(name=wi)
                    outupdate.out()
                    outupdate1=PlayerTeam.objects.get(name=wi,Team=team2)
                    outupdate1.out()
                    if i<7:
                        playoutupdate=Player.objects.get(name=wi)
                        ppoutupdate=PowerPlay.objects.get(name=playoutupdate)
                        ppoutupdate.ppout()
                    
                        
                    ki=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]["kind"]
            
                    x=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]
            
                    if "fielders" in x.keys():
                        c=list_cricket["innings"][1]["2nd innings"]["deliveries"][k][i]["wicket"]["fielders"][0]
                        fiel=Player.objects.filter(name=c)
                        if not fiel:
                            profile=Player(name=c)
                            profile.save()

                        fiel=Player.objects.get(name=c)
                        fiel.updatecatches()
                        pla.updatewickets()
                        prot.updatewickets()
                        if i<7:
                            play.ppupdatewickets()
                        
                    else:
                        if ki!="run out":
                            pla.updatewickets()
                            prot.updatewickets()
                            if i<7:
                                play.ppupdatewickets()

            k=k+1
        res=N.array(batlist)

        unique_res=N.unique(res)
        for some in unique_res:
            pin=Player.objects.get(name=some)
            pint=PlayerTeam.objects.get(name=some,Team=team2)
            pin.updateinnings() 
            pint.updateinnings()
        every=Player.objects.all()
        for i in every:
            i.seteco()
            i.setaverage()
            i.setsr()
        every1=PlayerTeam.objects.all()
        for i in every1:
            i.seteco()
            i.setaverage()
            i.setsr()
        ppevery=PowerPlay.objects.all()
        for j in ppevery:
            j.setppeco()
            j.setppsr()
            j.setppaverage()
    return HttpResponse("updated")
def search_players(request):
    query=request.GET.get('q1')
    ls=query.split(' ')
    l=len(ls)
    if query:
        posts = Player.objects.all()
        if l==1:
            results=posts.filter(Q(name__icontains=ls[0]))
        if l==2:
            results=posts.filter(Q(name__icontains=ls[0])|Q(name__icontains=ls[1]))

	
    return render(request, '../templates/html/playerslist.html',context={'players':results})