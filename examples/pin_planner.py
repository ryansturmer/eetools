import eetools.pin_planner as planner


# GPIOs
def claim_gpios(pin_map, *funcs):
    gpios = stm.available_like('pa') + stm.available_like('pb') + stm.available_like('pc') + stm.available_like('pd')
    for func in funcs:
        while True:
            pin = gpios.pop(0)
            try:
                print "Claiming %s for %s" % (pin,func)
                stm.claim(pin)
                break
            except:
                print "Nope!"
                continue


def claim(pin_map, function, purpose):
    try:
        pin_map.claim(function)
        print "Claimed %s for %s" % (function, purpose)
        print "    %s" % pin_map.who_shares(function)
    except:
        print "!!!!!!!!Couldn't claim %s for %s" % (function, purpose)

stm = planner.load("data/STM32F1xxC.csv", "LQFP64")

# Power Pins
print stm.claim_like('vdd')
print stm.claim_like('vss')
print stm.claim('vbat')
# External Oscillator
print stm.claim_like('osc')


# SPI1
spi1 = stm.claim_like('spi1')
for f in spi1:
    print f + " : %s" % stm.who_shares(f)

# SPI2 (Internal client SPI)
print stm.claim_like('spi2')

# JTAG
print stm.claim_like('J')
print stm.claim('nrst')

# USB
print stm.claim_like('usb')

# BOOT Pins
print stm.claim_like('boot')

# IOs that appear on the coastline connector
g = 0
for i in range(4, 9):
    claim(stm, 'pc%d' % i, 'GPIO%d' % g)
    g+=1
for i in range(5, 10):
    claim(stm, 'pb%d' % i, 'GPIO%d' % g)
    g+=1

claim(stm, 'pa0', 'CS_MOTOR')
claim(stm, 'pa1', 'CS_MOTOR_CURRENT')
claim(stm, 'pa2', 'CS_LOAD')
#claim(stm, 'pa4', 'KCS_ARM') # Claimed by spi thing above
claim(stm, 'pb0', 'CS_AB')
claim(stm, 'pb1', 'CS_CD')
for d,a in enumerate('ABCD'):
    claim(stm, 'pc%d' % d, 'ADC%s' % a)

print "Available Functions:\n" + '-'*len('Available Functions:')
for p in stm.unclaimed_pins:
    print "%02d : %s" %  (p, stm.functions_of(p))


