import pandas as pd
import math
import random
import csv


def calculate_pdc(ghi,ηpanel,RatedPanelPower):
    print(RatedPanelPower)
    pdc = ghi * ηpanel * RatedPanelPower/100
    return pdc



def find_current(pdc,ratedPanelPower , motorVolatge ):
    i =pdc/ motorVolatge 
    return i

def find_motor_volatage(nominalvoltage,ghi ,max_ghi = 700):
    if ghi > max_ghi:
        ghi = max_ghi
    motor_volatage = nominalvoltage * math.sqrt(ghi/max_ghi)
    return motor_volatage

def find_motorFreq(pdc,ratedPanelPower , max_freq):
    motorfreq =(pdc/ratedPanelPower) * max_freq
    return motorfreq

def dailyGeneratedEnergy(pdc , maxflow ):
    dailyGenerated = pdc/maxflow

    
def dailywaterDischarge():
    pass

def outputPower(dcp , ratio = .84):
    outpower = dcp * ratio 
    return outpower

def findOutputV(pdc,ratedPanelPower,driveOutputV):
    outputV = (pdc/ratedPanelPower ) * driveOutputV
    return outputV


def getlpm(data,hp):
    lp = random.uniform(0.7, 1)
    maxflow = data[0][hp]["MAX-FLOW"] 
    lpm = round((maxflow / 390) * lp, 3)
    return lpm

def get_time_date():
    pass

def findlpm(pdc, maxpanelpower ,maxflow):
    if pdc == 0:
        return 0
    v = (pdc /maxpanelpower)/390 
    lp = random.uniform(0.7, 1)
    lpm = maxflow * v * lp
    return lpm 

