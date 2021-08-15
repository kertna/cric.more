from djongo import models

# Create your models here.reateProfile 

class Player(models.Model):
    name=models.CharField(max_length=250, primary_key=True)
    runs= models.IntegerField(default=0)
    ballsfaced=models.IntegerField(default=0)
    sixes=models.IntegerField(default=0)
    fours=models.IntegerField(default=0)
    catches=models.IntegerField(default=0)
    ballsbowled=models.IntegerField(default=0)
    oversbowled=models.FloatField(default=0)
    runsgiven=models.IntegerField(default=0)
    wickets=models.IntegerField(default=0)
    economy=models.FloatField(default=0)
    strikerate=models.FloatField(default=0)
    fifties=models.IntegerField(default=0)
    hundreds=models.IntegerField(default=0)
    currentruns=models.IntegerField(default=0)
    bowlavg=models.FloatField(default=None)
    bowlsr=models.FloatField(default=None)
    outs=models.IntegerField(default=0)
    average=models.FloatField(default=None)
    innings=models.IntegerField(default=0)
    threehaul=models.IntegerField(default=0)
    fivehaul=models.IntegerField(default=0)
    
    def updateruns(self, runs):
        self.runs=self.runs+runs
        self.save()
    def updateballsfaced(self):
        self.ballsfaced=self.ballsfaced+1
        self.save()
    def updatesixes(self):
        self.sixes=self.sixes+1
        self.save()
    def updatefours(self):
        self.fours=self.fours+1
        self.save()
    
    def updateballsbowled(self):
        self.ballsbowled=self.ballsbowled+1
        self.oversbowled=self.ballsbowled//6 +(0.1)*(self.ballsbowled%6)
        self.oversbowled=float("{:.1f}".format(self.oversbowled))
        self.save()
    def updaterunsgiven(self,runs):
        self.runsgiven=self.runsgiven+runs
        self.save()
    def updatewickets(self):
        self.wickets=self.wickets+1
        self.save()
    def updatecatches(self):
        self.catches=self.catches+1
        self.save()
    def seteco(self):
        if self.ballsbowled>0:
            self.economy=(self.runsgiven)/(self.ballsbowled/6)
            self.economy=float("{:.1f}".format(self.economy))
            if self.wickets>0:
                self.bowlavg=(self.runsgiven)/(self.wickets)
                self.bowlavg=float("{:.2f}".format(self.bowlavg))
                self.bowlsr=(self.ballsbowled)/(self.wickets)
                self.bowlsr=float("{:.2f}".format(self.bowlsr))
            self.save()
    def setsr(self):
        if self.ballsfaced>0:
            self.strikerate=(self.runs*100)/(self.ballsfaced)
            self.strikerate=float("{:.2f}".format(self.strikerate))
            self.save()
    def setfiftiesandhundreds(self):
        if self.currentruns>=100:
            self.hundreds=self.hundreds+1
            self.save()
        elif self.currentruns>=50:
            self.fifties=self.fifties+1
            self.save()
    def currentrunszero(self):
        self.currentruns=0
        self.save()
    def setcurrentruns(self,runs):
        self.currentruns=self.currentruns+runs
        self.save()
    def out(self):
        self.outs=self.outs+1
        self.save()
    def setaverage(self):
        if self.outs==0:
            pass
        else:
            self.average=self.runs/self.outs
            self.average=float("{:.2f}".format(self.average))
            self.save()
    def updateinnings(self):
        self.innings=self.innings+1
        self.save()
    def fourw(self):
        if self.wickets>=3 and self.wickets<5:
            self.threehaul=self.threehaul+1
            self.save()
        if self.wickets>=5:
            self.fivehaul=self.fivehaul+1
            self.save()
class PlayerTeam(models.Model):
    name =models.ForeignKey(Player,  on_delete=models.CASCADE)
    Team = models.CharField(max_length=250)
    runs= models.IntegerField(default=0)
    ballsfaced=models.IntegerField(default=0)
    sixes=models.IntegerField(default=0)
    fours=models.IntegerField(default=0)
    
    ballsbowled=models.IntegerField(default=0)
    oversbowled=models.FloatField(default=0)
    runsgiven=models.IntegerField(default=0)
    wickets=models.IntegerField(default=0)
    economy=models.FloatField(default=0)
    strikerate=models.FloatField(default=0)
    fifties=models.IntegerField(default=0)
    hundreds=models.IntegerField(default=0)
    currentruns=models.IntegerField(default=0)
    bowlavg=models.FloatField(default=None)
    bowlsr=models.FloatField(default=None)
    outs=models.IntegerField(default=0)
    average=models.FloatField(default=None)
    innings=models.IntegerField(default=0)
    def __str__(self):
        return self.name.name+" "+self.Team
    def updateruns(self, runs):
        self.runs=self.runs+runs
        self.save()
    def updateballsfaced(self):
        self.ballsfaced=self.ballsfaced+1
        self.save()
    def updatesixes(self):
        self.sixes=self.sixes+1
        self.save()
    def updatefours(self):
        self.fours=self.fours+1
        self.save()
    
    def updateballsbowled(self):
        self.ballsbowled=self.ballsbowled+1
        self.oversbowled=self.ballsbowled//6 +(0.1)*(self.ballsbowled%6)
        self.oversbowled=float("{:.1f}".format(self.oversbowled))
        self.save()
    def updaterunsgiven(self,runs):
        self.runsgiven=self.runsgiven+runs
        self.save()
    def updatewickets(self):
        self.wickets=self.wickets+1
        self.save()
    def updatecatches(self):
        self.catches=self.catches+1
        self.save()
    def seteco(self):
        if self.ballsbowled>0:
            self.economy=(self.runsgiven)/(self.ballsbowled/6)
            self.economy=float("{:.1f}".format(self.economy))
            if self.wickets>0:
                self.bowlavg=(self.runsgiven)/(self.wickets)
                self.bowlavg=float("{:.2f}".format(self.bowlavg))
                self.bowlsr=(self.ballsbowled)/(self.wickets)
                self.bowlsr=float("{:.2f}".format(self.bowlsr))
            self.save()
    def setsr(self):
        if self.ballsfaced>0:
            self.strikerate=(self.runs*100)/(self.ballsfaced)
            self.strikerate=float("{:.2f}".format(self.strikerate))
            self.save()
    def setfiftiesandhundreds(self):
        if self.currentruns>=100:
            self.hundreds=self.hundreds+1
            self.save()
        elif self.currentruns>=50:
            self.fifties=self.fifties+1
            self.save()
    def currentrunszero(self):
        self.currentruns=0
        self.save()
    def setcurrentruns(self,runs):
        self.currentruns=self.currentruns+runs
        self.save()
    def out(self):
        self.outs=self.outs+1
        self.save()
    def setaverage(self):
        if self.outs==0:
            pass
        else:
            self.average=self.runs/self.outs
            self.average=float("{:.2f}".format(self.average))
            self.save()
    def updateinnings(self):
        self.innings=self.innings+1
        self.save()
class AgainstTeam(models.Model):
    name =models.ForeignKey(Player,  on_delete=models.CASCADE)
    Team = models.CharField(max_length=250)
    runs= models.IntegerField(default=0)
    ballsfaced=models.IntegerField(default=0)
    sixes=models.IntegerField(default=0)
    fours=models.IntegerField(default=0)
    
    ballsbowled=models.IntegerField(default=0)
    oversbowled=models.FloatField(default=0)
    runsgiven=models.IntegerField(default=0)
    wickets=models.IntegerField(default=0)
    economy=models.FloatField(default=0)
    strikerate=models.FloatField(default=0)
    fifties=models.IntegerField(default=0)
    hundreds=models.IntegerField(default=0)
    currentruns=models.IntegerField(default=0)
    bowlavg=models.FloatField(default=None)
    bowlsr=models.FloatField(default=None)
    outs=models.IntegerField(default=0)
    average=models.FloatField(default=None)
    innings=models.IntegerField(default=0)
    def __str__(self):
        return self.name.name+" "+self.Team
    def updateruns(self, runs):
        self.runs=self.runs+runs
        self.save()
    def updateballsfaced(self):
        self.ballsfaced=self.ballsfaced+1
        self.save()
    def updatesixes(self):
        self.sixes=self.sixes+1
        self.save()
    def updatefours(self):
        self.fours=self.fours+1
        self.save()
    
    def updateballsbowled(self):
        self.ballsbowled=self.ballsbowled+1
        self.oversbowled=self.ballsbowled//6 +(0.1)*(self.ballsbowled%6)
        self.oversbowled=float("{:.1f}".format(self.oversbowled))
        self.save()
    def updaterunsgiven(self,runs):
        self.runsgiven=self.runsgiven+runs
        self.save()
    def updatewickets(self):
        self.wickets=self.wickets+1
        self.save()
    def updatecatches(self):
        self.catches=self.catches+1
        self.save()
    def seteco(self):
        if self.ballsbowled>0:
            self.economy=(self.runsgiven)/(self.ballsbowled/6)
            self.economy=float("{:.1f}".format(self.economy))
            if self.wickets>0:
                self.bowlavg=(self.runsgiven)/(self.wickets)
                self.bowlavg=float("{:.2f}".format(self.bowlavg))
                self.bowlsr=(self.ballsbowled)/(self.wickets)
                self.bowlsr=float("{:.2f}".format(self.bowlsr))
            self.save()
    def setsr(self):
        if self.ballsfaced>0:
            self.strikerate=(self.runs*100)/(self.ballsfaced)
            self.strikerate=float("{:.2f}".format(self.strikerate))
            self.save()
    def setfiftiesandhundreds(self):
        if self.currentruns>=100:
            self.hundreds=self.hundreds+1
            self.save()
        elif self.currentruns>=50:
            self.fifties=self.fifties+1
            self.save()
    def currentrunszero(self):
        self.currentruns=0
        self.save()
    def setcurrentruns(self,runs):
        self.currentruns=self.currentruns+runs
        self.save()
    def out(self):
        self.outs=self.outs+1
        self.save()
    def setaverage(self):
        if self.outs==0:
            pass
        else:
            self.average=self.runs/self.outs
            self.average=float("{:.2f}".format(self.average))
            self.save()
    def updateinnings(self):
        self.innings=self.innings+1
        self.save()
	
class PowerPlay(models.Model):
    name = models.ForeignKey(Player,  on_delete=models.CASCADE)
    ppruns= models.IntegerField(default=0)
    ppballsfaced=models.IntegerField(default=0)
    ppballsbowled=models.IntegerField(default=0)
    pprunsgiven=models.IntegerField(default=0)
    ppwickets=models.IntegerField(default=0)
    ppeconomy=models.FloatField(default=0)
    ppstrikerate=models.FloatField(default=0)
    ppouts=models.IntegerField(default=0)
    ppaverage=models.IntegerField(default=None)
    ppbowlavg=models.FloatField(default=0)
    ppbowlsr=models.FloatField(default=0)
    ppoversbowled=models.FloatField(default=0)
    #ppinnings=models.IntegerField(default=0)
    def __str__(self):
        return self.name.name
    def ppupdateruns(self, runs):
        self.ppruns=self.ppruns+runs
        self.save()
    def ppupdateballsfaced(self):
        self.ppballsfaced=self.ppballsfaced+1
        self.save()
    def ppupdateballsbowled(self):
        self.ppballsbowled=self.ppballsbowled+1
        self.ppoversbowled=self.ppballsbowled//6 +(0.1)*(self.ppballsbowled%6)
        self.ppoversbowled=float("{:.1f}".format(self.ppoversbowled))
        self.save()
    def ppupdaterunsgiven(self,runs):
        self.pprunsgiven=self.pprunsgiven+runs
        self.save()
    def ppupdatewickets(self):
        self.ppwickets=self.ppwickets+1
        self.save()
    def setppeco(self):
        if self.ppballsbowled>0:
            self.ppeconomy=(self.pprunsgiven)/(self.ppballsbowled/6)
            self.ppeconomy=float("{:.1f}".format(self.ppeconomy))
            if self.ppwickets>0:
                self.ppbowlavg=(self.pprunsgiven)/(self.ppwickets)
                self.ppbowlavg=float("{:.2f}".format(self.ppbowlavg))
                self.ppbowlsr=(self.ppballsbowled)/(self.ppwickets)
                self.ppbowlsr=float("{:.2f}".format(self.ppbowlsr))
            self.save()
    def setppsr(self):
        if self.ppruns>0 and self.ppballsfaced>0:
            self.ppstrikerate=(self.ppruns*100)/(self.ppballsfaced)
            self.ppstrikerate=float("{:.1f}".format(self.ppstrikerate))
            self.save()
    def ppout(self):
        self.ppouts=self.ppouts+1
        self.save()
    def setppaverage(self):
        if self.ppouts==0:
            pass
        else:
            self.ppaverage=self.ppruns/self.ppouts
            self.ppaverage=float("{:.1f}".format(self.ppaverage))
            self.save()
    
class MiddleOvers(models.Model):
    name = models.ForeignKey(Player,  on_delete=models.CASCADE)
    midruns= models.IntegerField(default=0)
    midballsfaced=models.IntegerField(default=0)
    midballsbowled=models.IntegerField(default=0)
    midrunsgiven=models.IntegerField(default=0)
    midwickets=models.IntegerField(default=0)
    mideconomy=models.FloatField(default=0)
    midstrikerate=models.FloatField(default=0)
    midouts=models.IntegerField(default=0)
    midaverage=models.IntegerField(default=None)
    midbowlavg=models.FloatField(default=0)
    midbowlsr=models.FloatField(default=0)
    midoversbowled=models.FloatField(default=0)
    #ppinnings=models.IntegerField(default=0)
    def __str__(self):
        return self.name.name
    def midupdateruns(self, runs):
        self.midruns=self.midruns+runs
        self.save()
    def midupdateballsfaced(self):
        self.midballsfaced=self.midballsfaced+1
        self.midoversbowled=self.midballsbowled//6 +(0.1)*(self.midballsbowled%6)
        self.midoversbowled=float("{:.1f}".format(self.midoversbowled))
        self.save()
    def midupdateballsbowled(self):
        self.midballsbowled=self.midballsbowled+1
        self.save()
    def midupdaterunsgiven(self,runs):
        self.midrunsgiven=self.midrunsgiven+runs
        self.save()
    def midupdatewickets(self):
        self.midwickets=self.midwickets+1
        self.save()
    def setmideco(self):
        if self.midballsbowled>0:
            self.mideconomy=(self.midrunsgiven)/(self.midballsbowled/6)
            self.mideconomy=float("{:.1f}".format(self.mideconomy))
            if self.midwickets>0:
                self.midbowlavg=(self.midrunsgiven)/(self.midwickets)
                self.midbowlavg=float("{:.2f}".format(self.midbowlavg))
                self.midbowlsr=(self.midballsbowled)/(self.midwickets)
                self.midbowlsr=float("{:.2f}".format(self.midbowlsr))
            self.save()
    def setmidsr(self):
        if self.midballsfaced>0:
            self.midstrikerate=(self.midruns*100)/(self.midballsfaced)
            self.midstrikerate=float("{:.1f}".format(self.midstrikerate))
            self.save()
    def midout(self):
        self.midouts=self.midouts+1
        self.save()
    def setmidaverage(self):
        if self.midouts==0:
            pass
        else:
            self.midaverage=self.midruns/self.midouts
            self.midaverage=float("{:.1f}".format(self.midaverage))
            self.save()


class DeathOvers(models.Model):
    name = models.ForeignKey(Player,  on_delete=models.CASCADE)
    deathruns= models.IntegerField(default=0)
    deathballsfaced=models.IntegerField(default=0)
    deathballsbowled=models.IntegerField(default=0)
    deathrunsgiven=models.IntegerField(default=0)
    deathwickets=models.IntegerField(default=0)
    deatheconomy=models.FloatField(default=0)
    deathstrikerate=models.FloatField(default=0)
    deathouts=models.IntegerField(default=0)
    deathaverage=models.IntegerField(default=None)
    deathbowlavg=models.FloatField(default=0)
    deathbowlsr=models.FloatField(default=0)
    deathoversbowled=models.FloatField(default=0)
    #ppinnings=models.IntegerField(default=0)
    def __str__(self):
        return self.name.name
    def deathupdateruns(self, runs):
        self.deathruns=self.deathruns+runs
        self.save()
    def deathupdateballsfaced(self):
        self.deathballsfaced=self.deathballsfaced+1
        self.save()
    def deathupdateballsbowled(self):
        self.deathballsbowled=self.deathballsbowled+1
        self.deathoversbowled=self.deathballsbowled//6 +(0.1)*(self.deathballsbowled%6)
        self.deathoversbowled=float("{:.1f}".format(self.deathoversbowled))
        self.save()
    def deathupdaterunsgiven(self,runs):
        self.deathrunsgiven=self.deathrunsgiven+runs
        self.save()
    def deathupdatewickets(self):
        self.deathwickets=self.deathwickets+1
        self.save()
    def setdeatheco(self):
        if self.deathballsbowled>0:
            self.deatheconomy=(self.deathrunsgiven)/(self.deathballsbowled/6)
            self.deatheconomy=float("{:.1f}".format(self.deatheconomy))
            if self.deathwickets>0:
                self.deathbowlavg=(self.deathrunsgiven)/(self.deathwickets)
                self.deathbowlavg=float("{:.2f}".format(self.deathbowlavg))
                self.deathbowlsr=(self.deathballsbowled)/(self.deathwickets)
                self.deathbowlsr=float("{:.2f}".format(self.deathbowlsr))
            self.save()
    def setdeathsr(self):
        if self.deathballsfaced>0:
            self.deathstrikerate=(self.deathruns*100)/(self.deathballsfaced)
            self.deathstrikerate=float("{:.1f}".format(self.deathstrikerate))
            self.save()
    def deathout(self):
        self.deathouts=self.deathouts+1
        self.save()
    def setdeathaverage(self):
        if self.deathouts==0:
            pass
        else:
            self.deathaverage=self.deathruns/self.deathouts
            self.deathaverage=float("{:.1f}".format(self.deathaverage))
            self.save()

class Matchups(models.Model):
    name = models.ForeignKey(Player,  on_delete=models.CASCADE)
    bowler=models.CharField(max_length=250)
    runs = models.IntegerField(default=0)
    ballsfaced=models.IntegerField(default=0)
    ballsbowled=models.IntegerField(default=0)
    runsgiven=models.IntegerField(default=0)
    wickets=models.IntegerField(default=0)
    economy=models.FloatField(default=0)
    strikerate=models.FloatField(default=0)
    outs=models.FloatField(default=0)
    average=models.FloatField(default=0)
    bowlavg=models.FloatField(default=0)
    bowlsr=models.FloatField(default=0)
    def setaverage(self, runs):
        if self.outs==0:
            pass
        else:
            self.average=self.runs/self.outs
            self.average=float("{:.1f}".format(self.average))
            self.save()
    def updateruns(self, runs):
        self.runs=self.runs+runs
        self.save()
    def updateballsfaced(self):
        self.ballsfaced=self.ballsfaced+1
        self.save()
    def updateballsbowled(self):
        self.ballsbowled=self.ballsbowled+1
        self.oversbowled=self.ballsbowled//6 +(0.1)*(self.ballsbowled%6)
        self.oversbowled=float("{:.1f}".format(self.oversbowled))
        self.save()
    def updaterunsgiven(self,runs):
        self.runsgiven=self.runsgiven+runs
        self.save()
    def updatewickets(self):
        self.wickets=self.wickets+1
        self.save()
    def updateouts(self):
        self.outs=self.outs+1
        self.save()
    def seteco(self):
        if self.ballsbowled>0:
            self.economy=(self.runsgiven)/(self.ballsbowled/6)
            self.economy=float("{:.1f}".format(self.economy))
            if self.wickets>0:
                self.bowlavg=(self.runsgiven)/(self.wickets)
                self.bowlavg=float("{:.2f}".format(self.bowlavg))
                self.bowlsr=(self.ballsbowled)/(self.wickets)
                self.bowlsr=float("{:.2f}".format(self.bowlsr))
            self.save()
    def setsr(self):
        if self.ballsfaced>0:
            self.strikerate=(self.runs*100)/(self.ballsfaced)
            self.strikerate=float("{:.2f}".format(self.strikerate))
            self.save()

    def setaverage(self):
        if self.outs==0:
            pass
        else:
            self.average=self.runs/self.outs
            self.average=float("{:.2f}".format(self.average))
            self.save()
    def __str__(self):
        return self.name.name+" "+self.bowler
class City(models.Model):
    name=models.ForeignKey(Player,  on_delete=models.CASCADE)
    City=models.CharField(max_length=250)

    runs= models.IntegerField(default=0)
    ballsfaced=models.IntegerField(default=0)
    
    ballsbowled=models.IntegerField(default=0)
    oversbowled=models.FloatField(default=0)
    runsgiven=models.IntegerField(default=0)
    wickets=models.IntegerField(default=0)
    economy=models.FloatField(default=0)
    strikerate=models.FloatField(default=0)
    fifties=models.IntegerField(default=0)
    hundreds=models.IntegerField(default=0)
    currentruns=models.IntegerField(default=0)
    bowlavg=models.FloatField(default=None)
    bowlsr=models.FloatField(default=None)
    outs=models.IntegerField(default=0)
    average=models.FloatField(default=None)
    innings=models.IntegerField(default=0)
    threehaul=models.IntegerField(default=0)
    fivehaul=models.IntegerField(default=0)
    
    def updateruns(self, runs):
        self.runs=self.runs+runs
        self.save()
    def updateballsfaced(self):
        self.ballsfaced=self.ballsfaced+1
        self.save()
    def __str__(self):
        return self.City+" "+self.name.name
    
    def updateballsbowled(self):
        self.ballsbowled=self.ballsbowled+1
        self.oversbowled=self.ballsbowled//6 +(0.1)*(self.ballsbowled%6)
        self.oversbowled=float("{:.1f}".format(self.oversbowled))
        self.save()
    def updaterunsgiven(self,runs):
        self.runsgiven=self.runsgiven+runs
        self.save()
    def updatewickets(self):
        self.wickets=self.wickets+1
        self.save()
    
    def seteco(self):
        if self.ballsbowled>0:
            self.economy=(self.runsgiven)/(self.ballsbowled/6)
            self.economy=float("{:.1f}".format(self.economy))
            if self.wickets>0:
                self.bowlavg=(self.runsgiven)/(self.wickets)
                self.bowlavg=float("{:.2f}".format(self.bowlavg))
                self.bowlsr=(self.ballsbowled)/(self.wickets)
                self.bowlsr=float("{:.2f}".format(self.bowlsr))
            self.save()
    def setsr(self):
        if self.ballsfaced>0:
            self.strikerate=(self.runs*100)/(self.ballsfaced)
            self.strikerate=float("{:.2f}".format(self.strikerate))
            self.save()
    def setfiftiesandhundreds(self):
        if self.currentruns>=100:
            self.hundreds=self.hundreds+1
            self.save()
        elif self.currentruns>=50:
            self.fifties=self.fifties+1
            self.save()
    def currentrunszero(self):
        self.currentruns=0
        self.save()
    def setcurrentruns(self,runs):
        self.currentruns=self.currentruns+runs
        self.save()
    def out(self):
        self.outs=self.outs+1
        self.save()
    def setaverage(self):
        if self.outs==0:
            pass
        else:
            self.average=self.runs/self.outs
            self.average=float("{:.2f}".format(self.average))
            self.save()
    def updateinnings(self):
        self.innings=self.innings+1
        self.save()
    def fourw(self):
        if self.wickets>=3 and self.wickets<5:
            self.threehaul=self.threehaul+1
            self.save()
        if self.wickets>=5:
            self.fivehaul=self.fivehaul+1
            self.save()


class Position(models.Model):
    name=models.CharField(max_length=250, primary_key=True)
    runs= models.IntegerField(default=0)
    position=models.IntegerField(default=0)
   
    ballsfaced=models.IntegerField(default=0)
    
    strikerate=models.FloatField(default=0)
    fifties=models.IntegerField(default=0)
    hundreds=models.IntegerField(default=0)
    currentruns=models.IntegerField(default=0)
    
    outs=models.IntegerField(default=0)
    average=models.FloatField(default=None)
    innings=models.IntegerField(default=0)
    def __str__(self):
        return self.name+"-"+str(self.position)
    
    def updateruns(self, runs):
        self.runs=self.runs+runs
        self.save()
    def updateballsfaced(self):
        self.ballsfaced=self.ballsfaced+1
        self.save()
 
    def setsr(self):
        if self.ballsfaced>0:
            self.strikerate=(self.runs*100)/(self.ballsfaced)
            self.strikerate=float("{:.2f}".format(self.strikerate))
            self.save()
    def setfiftiesandhundreds(self):
        if self.currentruns>=100:
            self.hundreds=self.hundreds+1
            self.save()
        elif self.currentruns>=50:
            self.fifties=self.fifties+1
            self.save()
    def currentrunszero(self):
        self.currentruns=0
        self.save()
    def setcurrentruns(self,runs):
        self.currentruns=self.currentruns+runs
        self.save()
    def out(self):
        self.outs=self.outs+1
        self.save()
    def setaverage(self):
        if self.outs==0:
            pass
        else:
            self.average=self.runs/self.outs
            self.average=float("{:.2f}".format(self.average))
            self.save()
    def updateinnings(self):
        self.innings=self.innings+1
        self.save()
    