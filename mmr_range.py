def mmr_charges(mmr):
    if mmr<5000:
        mmr_charge=int(mmr/250)*2+2
    else:
        mmr_charge=int(mmr/250)*3-17
    return mmr_charge
def mmr_line():
    mmr_range=[]
    mmr_charge_range=[]
    i=0
    while i<10000:
        mmr_range+=[i]
        mmr_charge_range+=[mmr_charges(i)]
        i+=250
        mmr_range+=[i]
        mmr_charge_range+=[mmr_charges(i-1)]
    return mmr_range,mmr_charge_range
tier_range={}
tier_range[0]="아이언"
tier_range[1000]="브론즈"
tier_range[2000]="실버"
tier_range[3000]="골드"
tier_range[4000]="플레티넘"
tier_range[5000]="다이아"
tier_range[6000]="데미갓"
tier_range["all"]="all"

getMMR_range={}
getMMR_range[0]="0~25"
getMMR_range[25]="25~50"
getMMR_range[50]="50~75"
getMMR_range[75]="75~100"
getMMR_range[100]="100~125"
getMMR_range[125]="125~150"
getMMR_range[150]="150~175"
getMMR_range[175]="175~200"
getMMR_range[200]="200~225"
getMMR_range[225]="225~"
class Tier:
    def __init__(self):
        self.tier={}
        self.tier["아이언"]={}
        self.tier["브론즈"]={}
        self.tier["실버"]={}
        self.tier["골드"]={}
        self.tier["플레티넘"]={}
        self.tier["다이아"]={}
        self.tier["데미갓"]={}
        self.tier["all"]={}

    def split_getmmr(self,getMMR):
        mmrGain_range=[0,25,50,75,100,125,150,175,200,225]
        while mmrGain_range!=[]:
            getMMR_min=mmrGain_range.pop()
            if getMMR_min<=getMMR:
                return getMMR_range[getMMR_min]
        return "~0"

    def split_tier(self,mmrBefore,getMMR):
        mmrBefore_range=[0,1000,2000,3000,4000,5000,6000]
        mmrGain_range=self.split_getmmr(getMMR)
        self.tier["all"][mmrGain_range]=self.tier["all"].get(mmrGain_range,0)+1
        while mmrBefore_range!=[]:  
            tier_min=mmrBefore_range.pop()
            if tier_min<=mmrBefore:
                
                self.tier[tier_range[tier_min]][mmrGain_range]=self.tier[tier_range[tier_min]].get(mmrGain_range,0)+1
                break



                
