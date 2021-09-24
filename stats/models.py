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
    currentwickets=models.IntegerField(default=0)
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
    def currentwicketszero(self):
        self.currentwickets=0
        self.save()
    def setcurrentwickets(self):
        self.currentwickets=self.currentwickets+1
        self.save()
    def fourw(self):
        if self.currentwickets>=3 and self.currentwickets<5:
            self.threehaul=self.threehaul+1
            self.save()
        if self.currentwickets>=5:
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
    currentwickets=models.IntegerField(default=0)
    threehaul=models.IntegerField(default=0)
    fivehaul=models.IntegerField(default=0)
    def fourw(self):
        if self.currentwickets>=3 and self.currentwickets<5:
            self.threehaul=self.threehaul+1
            self.save()
        if self.currentwickets>=5:
            self.fivehaul=self.fivehaul+1
            self.save()
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
    def currentwicketszero(self):
        self.currentwickets=0
        self.save()
    def setcurrentwickets(self):
        self.currentwickets=self.currentwickets+1
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
    #currentwickets=models.IntegerField(default=0)
    cwicks=models.IntegerField(default=0)
    threehaul=models.IntegerField(default=0)
    fivehaul=models.IntegerField(default=0)
    def fourw(self):
        if self.currentwickets>=3 and self.currentwickets<5:
            self.threehaul=self.threehaul+1
            self.save()
        if self.currentwickets>=5:
            self.fivehaul=self.fivehaul+1
            self.save()
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
    def currentwicketszero(self):
        self.cwicks=0
        self.save()
    def setcurrentruns(self,runs):
        self.currentruns=self.currentruns+runs
        self.save()
    def setcurrentwickets(self):
        self.cwicks=self.cwicks+1
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
        if self.cwicks>=3 and self.cwicks<5:
            self.threehaul=self.threehaul+1
            self.save()
        if self.cwicks>=5:
            self.fivehaul=self.fivehaul+1
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
    currentwickets=models.IntegerField(default=0)

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
    def currentwicketszero(self):
        self.currentwickets=0
        self.save()
    def setcurrentwickets(self):
        self.currentwickets=self.currentwickets+1
        self.save()
    def fourw(self):
        if self.currentwickets>=3 and self.currentwickets<5:
            self.threehaul=self.threehaul+1
            self.save()
        if self.currentwickets>=5:
            self.fivehaul=self.fivehaul+1
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


class Form(models.Model):
    name=models.ForeignKey(Player,  on_delete=models.CASCADE)
    currentform= models.FloatField(default=0)
    i=models.IntegerField(default=1)
    currentruns=models.IntegerField(default=0)
    currentballsfaced=models.IntegerField(default=0)
    currentwickets=models.IntegerField(default=0)
    currentrunsgiven=models.IntegerField(default=0)
    currentballsbowled=models.IntegerField(default=0)
    currentcatches=models.IntegerField(default=0)

    runs1=models.FloatField(default=0)
    runs2=models.FloatField(default=0)
    runs3=models.FloatField(default=0)
    runs4=models.FloatField(default=0)
    runs5=models.FloatField(default=0)

    sr1=models.FloatField(default=0)
    sr2=models.FloatField(default=0)
    sr3=models.FloatField(default=0)
    sr4=models.FloatField(default=0)
    sr5=models.FloatField(default=0)

    wicket1=models.FloatField(default=0)
    wicket2=models.FloatField(default=0)
    wicket3=models.FloatField(default=0)
    wicket4=models.FloatField(default=0)
    wicket5=models.FloatField(default=0)

    economy1=models.FloatField(default=0)
    economy2=models.FloatField(default=0)
    economy3=models.FloatField(default=0)
    economy4=models.FloatField(default=0)
    economy5=models.FloatField(default=0)

    catches1=models.FloatField(default=0)
    catches2=models.FloatField(default=0)
    catches3=models.FloatField(default=0)
    catches4=models.FloatField(default=0)
    catches5=models.FloatField(default=0)

    

    def setcurrentzero(self):
        self.currentruns=0
        self.currentwickets=0
        self.currentcatches=0
        self.currentballsfaced=0
        self.currentballsbowled=0
        self.currentrunsgiven=0
        self.save()
    def updateruns(self,runs):
        self.currentruns=self.currentruns+runs
        self.save()
    def updateballsfaced(self):
        self.currentballsfaced= self.currentballsfaced+1
        self.save()
    def updateballsbowled(self):
        self.currentballsbowled=self.currentballsbowled+1
        self.save()
    def updatecatches(self):
        self.currentcatches=self.currentcatches+1
        self.save()
    def updatewickets(self):
        self.currentwickets=self.currentwickets+1
        self.save()
    def updaterunsgiven(self,runs):
        
        self.currentrunsgiven=self.currentrunsgiven+runs
        self.save()

    def updatepointer(self):
        if self.i==1:
            self.runs1=self.currentruns
            if self.currentballsfaced>0:
                self.sr1=(self.currentruns*100)/(self.currentballsfaced)
                self.sr1=float("{:.2f}".format(self.sr1))
            self.wicket1=self.currentwickets
            if self.currentballsbowled>0:
                self.economy1=(self.currentrunsgiven)/(self.currentballsbowled/6)
                self.economy1=float("{:.1f}".format(self.economy1))
            self.catches1=self.currentcatches
            self.i=2
            self.save()
        elif self.i==2:
            self.runs2=self.currentruns
            if self.currentballsfaced>0:
                self.sr2=(self.currentruns*100)/(self.currentballsfaced)
                self.sr2=float("{:.2f}".format(self.sr2))
            self.wicket2=self.currentwickets
            if self.currentballsbowled>0:
                self.economy2=(self.currentrunsgiven)/(self.currentballsbowled/6)
                self.economy2=float("{:.1f}".format(self.economy2))
            self.catches2=self.currentcatches
            self.i=3
            self.save()
        elif self.i==3:
            self.runs3=self.currentruns
            if self.currentballsfaced>0:
                self.sr3=(self.currentruns*100)/(self.currentballsfaced)
                self.sr3=float("{:.2f}".format(self.sr3))
            self.wicket3=self.currentwickets
            if self.currentballsbowled>0:
                self.economy3=(self.currentrunsgiven)/(self.currentballsbowled/6)
                self.economy3=float("{:.1f}".format(self.economy3))
            self.catches3=self.currentcatches
            self.i=4
            self.save()
        elif self.i==4:
            self.runs4=self.currentruns
            if self.currentballsfaced>0:
                self.sr4=(self.currentruns*100)/(self.currentballsfaced)
                self.sr4=float("{:.2f}".format(self.sr4))
            self.wicket4=self.currentwickets
            if self.currentballsbowled>0:
                self.economy4=(self.currentrunsgiven)/(self.currentballsbowled/6)
                self.economy4=float("{:.1f}".format(self.economy4))
            self.catches4=self.currentcatches
            self.i=5
            self.save()
        else :
            self.runs5=self.currentruns
            if self.currentballsfaced>0:
                self.sr5=(self.currentruns*100)/(self.currentballsfaced)
                self.sr5=float("{:.2f}".format(self.sr5))
            self.wicket5=self.currentwickets
            if self.currentballsbowled>0:
                self.economy5=(self.currentrunsgiven)/(self.currentballsbowled/6)
                self.economy5=float("{:.1f}".format(self.economy5))
            self.catches5=self.currentcatches
            self.i=1
            self.save()

        self.currentform= (self.runs1+self.runs2+self.runs3+self.runs4+self.runs5)/5 + (self.wicket1+self.wicket2+self.wicket3+self.wicket4+self.wicket5)*5 + 8/5*(self.catches1+self.catches2+self.catches3+self.catches4+self.catches5) 
        if (self.sr1+self.sr2+self.sr3+self.sr4+self.sr5)/5 > 150:
            self.currentform=self.currentform+3
        if (self.sr1+self.sr2+self.sr3+self.sr4+self.sr5)/5 < 70:
            self.currentform=self.currentform-3
        if (self.economy1+ self.economy2+self.economy3+self.economy4+self.economy5)/5 <6:
            self.currentform=self.currentform+3
        if (self.economy1+ self.economy2+self.economy3+self.economy4+self.economy5)/5 >10:
            self.currentform=self.currentform-3

        self.save()

def createcategory():
        c=[]
        p=Player.objects.all()
        
        for i in p:
            t=(i.name,i.name)
            c.append(t)
        
        c.append(('OTHER','OTHER'))
        return c
def creategroundcategory():
        c=[]
        p=City.objects.all()
        
        for i in p:
            t=(i.City,i.City)
            
            c.append(t)
        
        c.append(('OTHER','OTHER'))
        return set(c)
class FantasyPrediction(models.Model):
    
    
    CATEGORY = (
        ('Batsman', 'Batsman'),
        ('Bowler', 'Bowler'),
        ('Allrounder', 'Allrounder'),
        ('WicketKeeper','WicketKeeper')
    )
    CATEGORY1 = (
        ('Sunrisers Hyderabad', 'Sunrisers Hyderabad'),
        ('Royal Challengers Bangalore', 'Royal Challengers Bangalore'),
        ('Kolkata Knight Riders', 'Kolkata Knight Riders'),
        ('Chennai Super Kings','Chennai Super Kings'),
        ('Kings XI Punjab','Kings XI Punjab'),
        ('Delhi Daredevils','Delhi Daredevils'),
        ('Rajasthan Royals','Rajasthan Royals'),
        ('Mumbai Indians','Mumbai Indians')

    )
    
    players=createcategory()
    id= models.IntegerField(default=0,primary_key=True)
    grounds=creategroundcategory()
    ground = models.CharField(max_length=300,choices=grounds)
    otherground=models.CharField(max_length=300,blank=True)
    
    team1=models.CharField(max_length=300, choices=CATEGORY1)
    team2=models.CharField(max_length=300, choices=CATEGORY1)
    CATEGORY2= (
        ('Team1','Team1'),
        ('Team2','Team2')
    )
    player1=models.CharField(max_length=250,choices=players)
    other1=models.CharField(max_length=300,blank=True)
    roleofplayer1=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer1=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer1=models.FloatField(default=0)
    player2=models.CharField(max_length=250,choices=players)
    other2=models.CharField(max_length=300,blank=True)
    roleofplayer2=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer2=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer2=models.FloatField(default=0)
    player3=models.CharField(max_length=250,choices=players)
    other3=models.CharField(max_length=300,blank=True)
    roleofplayer3=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer3=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer3=models.FloatField(default=0)
    player4=models.CharField(max_length=250,choices=players)
    other4=models.CharField(max_length=300,blank=True)
    roleofplayer4=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer4=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer4=models.FloatField(default=0)
    player5=models.CharField(max_length=250,choices=players)
    other5=models.CharField(max_length=300,blank=True)
    roleofplayer5=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer5=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer5=models.FloatField(default=0)
    player6=models.CharField(max_length=250,choices=players)
    other6=models.CharField(max_length=300,blank=True)
    roleofplayer6=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer6=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer6=models.FloatField(default=0)
    player7=models.CharField(max_length=250,choices=players)
    other7=models.CharField(max_length=300,blank=True)
    roleofplayer7=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer7=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer7=models.FloatField(default=0)
    player8=models.CharField(max_length=250,choices=players)
    other8=models.CharField(max_length=300,blank=True)
    roleofplayer8=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer8=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer8=models.FloatField(default=0)
    player9=models.CharField(max_length=250,choices=players)
    other9=models.CharField(max_length=300,blank=True)
    roleofplayer9=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer9=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer9=models.FloatField(default=0)
    player10=models.CharField(max_length=250,choices=players)
    other10=models.CharField(max_length=300,blank=True)
    roleofplayer10=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer10=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer10=models.FloatField(default=0)
    player11=models.CharField(max_length=250,choices=players)
    other11=models.CharField(max_length=300,blank=True)
    roleofplayer11=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer11=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer11=models.FloatField(default=0)
    player12=models.CharField(max_length=250,choices=players)
    other12=models.CharField(max_length=300,blank=True)
    roleofplayer12=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer12=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer12=models.FloatField(default=0)
    player13=models.CharField(max_length=250,choices=players)
    other13=models.CharField(max_length=300,blank=True)
    roleofplayer13=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer13=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer13=models.FloatField(default=0)
    player14=models.CharField(max_length=250,choices=players)
    other14=models.CharField(max_length=300,blank=True)
    roleofplayer14=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer14=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer14=models.FloatField(default=0)
    player15=models.CharField(max_length=250,choices=players)
    other15=models.CharField(max_length=300,blank=True)
    roleofplayer15=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer15=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer15=models.FloatField(default=0)
    player16=models.CharField(max_length=250,choices=players)
    other16=models.CharField(max_length=300,blank=True)
    roleofplayer16=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer16=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer16=models.FloatField(default=0)
    player17=models.CharField(max_length=250,choices=players)
    other17=models.CharField(max_length=300,blank=True)
    roleofplayer17=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer17=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer17=models.FloatField(default=0)
    player18=models.CharField(max_length=250,choices=players)
    other18=models.CharField(max_length=300,blank=True)
    roleofplayer18=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer18=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer18=models.FloatField(default=0)
    player19=models.CharField(max_length=250,choices=players)
    other19=models.CharField(max_length=300,blank=True)
    roleofplayer19=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer19=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer19=models.FloatField(default=0)
    player20=models.CharField(max_length=250,choices=players)
    other20=models.CharField(max_length=300,blank=True)
    roleofplayer20=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer20=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer20=models.FloatField(default=0)
    player21=models.CharField(max_length=250,choices=players)
    other21=models.CharField(max_length=300,blank=True)
    roleofplayer21=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer21=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer21=models.FloatField(default=0)
    player22=models.CharField(max_length=250,choices=players)
    other22=models.CharField(max_length=300,blank=True)
    roleofplayer22=models.CharField(max_length=300, choices=CATEGORY)
    teamofplayer22=models.CharField(max_length=300, choices=CATEGORY2)
    creditsofplayer22=models.FloatField(default=0)

    def addintolist(self,p,o,name):
        if name=='OTHER':
            p.append(o)
        else:
            p.append(name)
        return p

    def teamfind(self,team):
        tf={}
        for i in team:
            if team[i]=='Team1':
                tf[i]=self.team1
            else:
                tf[i]=self.team2
        return tf

    def getplayers(self):
        p=[]
        p=self.addintolist(p,self.other1,self.player1)
        p=self.addintolist(p,self.other2,self.player2)
        p=self.addintolist(p,self.other3,self.player3)
        p=self.addintolist(p,self.other4,self.player4)
        p=self.addintolist(p,self.other5,self.player5)
        p=self.addintolist(p,self.other6,self.player6)
        p=self.addintolist(p,self.other7,self.player7)
        p=self.addintolist(p,self.other8,self.player8)
        p=self.addintolist(p,self.other9,self.player9)
        p=self.addintolist(p,self.other10,self.player10)
        p=self.addintolist(p,self.other11,self.player11)
        p=self.addintolist(p,self.other12,self.player12)
        p=self.addintolist(p,self.other13,self.player13)
        p=self.addintolist(p,self.other14,self.player14)
        p=self.addintolist(p,self.other15,self.player15)
        p=self.addintolist(p,self.other16,self.player16)
        p=self.addintolist(p,self.other17,self.player17)
        p=self.addintolist(p,self.other18,self.player18)
        p=self.addintolist(p,self.other19,self.player19)
        p=self.addintolist(p,self.other20,self.player20)
        p=self.addintolist(p,self.other21,self.player21)
        p=self.addintolist(p,self.other22,self.player22)
        return p

    def getplayercredits(self):
        p=[]
        p.append(self.creditsofplayer1)
        p.append(self.creditsofplayer2)
        p.append(self.creditsofplayer3)
        p.append(self.creditsofplayer4)
        p.append(self.creditsofplayer5)
        p.append(self.creditsofplayer6)
        p.append(self.creditsofplayer7)
        p.append(self.creditsofplayer8)
        p.append(self.creditsofplayer9)
        p.append(self.creditsofplayer10)
        p.append(self.creditsofplayer11)
        p.append(self.creditsofplayer12)
        p.append(self.creditsofplayer13)
        p.append(self.creditsofplayer14)
        p.append(self.creditsofplayer15)
        p.append(self.creditsofplayer16)
        p.append(self.creditsofplayer17)
        p.append(self.creditsofplayer18)
        p.append(self.creditsofplayer19)
        p.append(self.creditsofplayer20)
        p.append(self.creditsofplayer21)
        p.append(self.creditsofplayer22)
        return p

    def getroles(self):
        p=[]
        p.append(self.roleofplayer1)
        p.append(self.roleofplayer2)
        p.append(self.roleofplayer3)
        p.append(self.roleofplayer4)
        p.append(self.roleofplayer5)
        p.append(self.roleofplayer6)
        p.append(self.roleofplayer7)
        p.append(self.roleofplayer8)
        p.append(self.roleofplayer9)
        p.append(self.roleofplayer10)
        p.append(self.roleofplayer11)
        p.append(self.roleofplayer12)
        p.append(self.roleofplayer13)
        p.append(self.roleofplayer14)
        p.append(self.roleofplayer15)
        p.append(self.roleofplayer16)
        p.append(self.roleofplayer17)
        p.append(self.roleofplayer18)
        p.append(self.roleofplayer19)
        p.append(self.roleofplayer20)
        p.append(self.roleofplayer21)
        p.append(self.roleofplayer22)
        return p

    def setteams(self):
        pt={}
        pt[self.player1]=self.teamofplayer1
        pt[self.player2]=self.teamofplayer2
        pt[self.player3]=self.teamofplayer3
        pt[self.player4]=self.teamofplayer4
        pt[self.player5]=self.teamofplayer5
        pt[self.player6]=self.teamofplayer6
        pt[self.player7]=self.teamofplayer7
        pt[self.player8]=self.teamofplayer8
        pt[self.player9]=self.teamofplayer9
        pt[self.player10]=self.teamofplayer10
        pt[self.player11]=self.teamofplayer11
        pt[self.player12]=self.teamofplayer12
        pt[self.player13]=self.teamofplayer13
        pt[self.player14]=self.teamofplayer14
        pt[self.player15]=self.teamofplayer15
        pt[self.player16]=self.teamofplayer16
        pt[self.player17]=self.teamofplayer17
        pt[self.player18]=self.teamofplayer18
        pt[self.player19]=self.teamofplayer19
        pt[self.player20]=self.teamofplayer20
        pt[self.player21]=self.teamofplayer21
        pt[self.player22]=self.teamofplayer22
        
        tf=self.teamfind(pt)
        
        return tf

    



    
