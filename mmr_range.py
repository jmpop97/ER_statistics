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