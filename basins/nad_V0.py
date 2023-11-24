from basins.region import BathymetricPolygon
from basins.basin import SimpleBathymetricBasin

def generate_basins_for_adriatic(bathymetry):
    basins = []

    # ZONE 1  5 and 9
    zone_1_5_9_lon = [12.22265625, 13.30859375, 13.30859375, 12.22265625]
    zone_1_5_9_lat = [44.61328125, 44.61328125, 45.10546875, 45.10546875]

    z1 = BathymetricPolygon(zone_1_5_9_lon, zone_1_5_9_lat, bathymetry, shallower_than=20)
    z5 = BathymetricPolygon(zone_1_5_9_lon, zone_1_5_9_lat, bathymetry, shallower_than=30, deeper_than=20)
    z9 = BathymetricPolygon(zone_1_5_9_lon, zone_1_5_9_lat, bathymetry, shallower_than=35, deeper_than=30)

    z1 = SimpleBathymetricBasin("zone1", z1)
    z5 = SimpleBathymetricBasin("zone5", z5)
    z9 = SimpleBathymetricBasin("zone9", z9)

    basins.append(z1)
    basins.append(z5)
    basins.append(z9)


    # ZONE 2 6
    zone_2_6_lon = [12.22265625, 13.07421875, 13.07421875, 12.22265625]
    zone_2_6_lat = [45.11328125, 45.11328125, 45.18359375, 45.22265625]

    z2 = BathymetricPolygon(zone_2_6_lon, zone_2_6_lat, bathymetry, shallower_than=20)
    z6 = BathymetricPolygon(zone_2_6_lon, zone_2_6_lat, bathymetry, shallower_than=30, deeper_than=20)

    z2 = SimpleBathymetricBasin("zone2", z2)
    z6 = SimpleBathymetricBasin("zone6", z6)

    basins.append(z2)
    basins.append(z6)

    # ZONE 3 7
    zone_3_7_lon = [12.22265625, 13.07421875, 12.80078125, 12.22265625]
    zone_3_7_lat = [45.22265625, 45.18359375, 45.30078125, 45.49609375]

    z3 = BathymetricPolygon(zone_3_7_lon, zone_3_7_lat, bathymetry, shallower_than=20)
    z7 = BathymetricPolygon(zone_3_7_lon, zone_3_7_lat, bathymetry, shallower_than=30, deeper_than=20)

    z3 = SimpleBathymetricBasin("zone3", z3)
    z7 = SimpleBathymetricBasin("zone7", z7)

    basins.append(z3)
    basins.append(z7)

    # ZONE 4 8
    zone_4_8_lon = [12.22265625, 12.80078125, 13.27734375, 13.27734375, 12.22265625]
    zone_4_8_lat = [45.49609375, 45.30078125, 45.30078125, 45.73046875, 45.49609375]

    z4 = BathymetricPolygon(zone_4_8_lon, zone_4_8_lat, bathymetry, shallower_than=20)
    z8 = BathymetricPolygon(zone_4_8_lon, zone_4_8_lat, bathymetry, shallower_than=30, deeper_than=20)

    z4 = SimpleBathymetricBasin("zone4", z4)
    z8 = SimpleBathymetricBasin("zone8", z8)

    basins.append(z4)
    basins.append(z8)

    # ZONE 10
    zone_10_lon = [12.22265625, 13.27734375, 13.27734375, 12.22265625, 12.22265625]
    zone_10_lat = [45.11328125, 45.11328125, 45.73046875, 45.73046875, 45.11328125]

    z10 = BathymetricPolygon(zone_10_lon, zone_10_lat, bathymetry, shallower_than=35, deeper_than=30)

    z10 = SimpleBathymetricBasin("zone10", z10)

    basins.append(z10)


    # ZONE 11
    zone_11_lon = [12.22265625, 13.40234375, 13.40234375, 12.22265625, 12.22265625]
    zone_11_lat = [44.61328125, 44.61328125, 45.73046875, 45.73046875, 44.61328125]

    z11 = BathymetricPolygon(zone_11_lon, zone_11_lat, bathymetry, shallower_than=80, deeper_than=35)

    z11 = SimpleBathymetricBasin("zone11", z11)

    basins.append(z11)

    # ZONE 12 13 GULF OF TRIESTE
    zone_12_13_lon = [13.28515625, 13.91796875, 13.91796875, 13.28515625]
    zone_12_13_lat = [45.49609375, 45.49609375, 45.80859375, 45.80859375]

    z12 = BathymetricPolygon(zone_12_13_lon, zone_12_13_lat, bathymetry, shallower_than=20)
    z13 = BathymetricPolygon(zone_12_13_lon, zone_12_13_lat, bathymetry, shallower_than=35, deeper_than=20)

    z12 = SimpleBathymetricBasin("zone12", z12)
    z13 = SimpleBathymetricBasin("zone13", z13)

    basins.append(z12)
    basins.append(z13)

    # ZONE 14 15 16 ISTRIAN COAST
    zone_14_15_16_lon = [13.28515625, 13.91015625, 13.91015625, 13.28515625]
    zone_14_15_16_lat = [44.69921875, 44.69921875, 45.48828125, 45.48828125]

    z14 = BathymetricPolygon(zone_14_15_16_lon, zone_14_15_16_lat, bathymetry, shallower_than=20)
    z15 = BathymetricPolygon(zone_14_15_16_lon, zone_14_15_16_lat, bathymetry, shallower_than=30, deeper_than=20)
    z16 = BathymetricPolygon(zone_14_15_16_lon, zone_14_15_16_lat, bathymetry, shallower_than=35, deeper_than=30)

    z14 = SimpleBathymetricBasin("zone14", z14)
    z15 = SimpleBathymetricBasin("zone15", z15)
    z16 = SimpleBathymetricBasin("zone16", z16)

    basins.append(z14)
    basins.append(z15)
    basins.append(z16)


    # ZONE 17 ISTRIA PROFONDA
    zone_17_lon = [13.41015625, 13.91015625, 13.91015625, 13.41015625]
    zone_17_lat = [44.61328125, 44.61328125, 45.09765625, 45.09765625]

    z17 = BathymetricPolygon(zone_17_lon, zone_17_lat, bathymetry, shallower_than=80, deeper_than=35)

    z17 = SimpleBathymetricBasin("zone17", z17)

    basins.append(z17)

    # ZONE 18-21  WEST MIDDLE ADRI
    zone_18_19_20_21_lon = [12.22265625, 14.01171875, 13.16796875, 12.22265625]
    zone_18_19_20_21_lat = [43.93359375, 43.93359375, 44.60546875, 44.60546875]


    z18 = BathymetricPolygon(zone_18_19_20_21_lon, zone_18_19_20_21_lat, bathymetry, shallower_than=20)
    z19 = BathymetricPolygon(zone_18_19_20_21_lon, zone_18_19_20_21_lat, bathymetry, shallower_than=30, deeper_than=20)
    z20 = BathymetricPolygon(zone_18_19_20_21_lon, zone_18_19_20_21_lat, bathymetry, shallower_than=35, deeper_than=30)
    z21 = BathymetricPolygon(zone_18_19_20_21_lon, zone_18_19_20_21_lat, bathymetry, shallower_than=80, deeper_than=35)

    z18 = SimpleBathymetricBasin("zone18", z18)
    z19 = SimpleBathymetricBasin("zone19", z19)
    z20 = SimpleBathymetricBasin("zone20", z20)
    z21 = SimpleBathymetricBasin("zone21", z21)

    basins.append(z18)
    basins.append(z19)
    basins.append(z20)
    basins.append(z21)

    # ZONE 22 MIDDLE MIDDLE ADRI
    zone_22_lon = [14.01171875, 14.76171875, 13.91796875, 13.16796875]
    zone_22_lat = [43.93359375, 43.93359375, 44.60546875, 44.60546875]

    z22 = BathymetricPolygon(zone_22_lon, zone_22_lat, bathymetry, shallower_than=80, deeper_than=35)

    z22 = SimpleBathymetricBasin("zone22", z22)

    basins.append(z22)

    # ZONE 23 - 26  EAST MIDDLE ADRI
    zone_23_24_25_26_lon = [14.76171875, 15.80859375, 15.80859375, 13.91796875, 13.91796875]
    zone_23_24_25_26_lat = [43.93359375, 43.93359375, 45.41796875, 45.41796875, 44.60546875]

    z23 = BathymetricPolygon(zone_23_24_25_26_lon, zone_23_24_25_26_lat, bathymetry, shallower_than=20)
    z24 = BathymetricPolygon(zone_23_24_25_26_lon, zone_23_24_25_26_lat, bathymetry, shallower_than=30, deeper_than=20)
    z25 = BathymetricPolygon(zone_23_24_25_26_lon, zone_23_24_25_26_lat, bathymetry, shallower_than=35, deeper_than=30)
    z26 = BathymetricPolygon(zone_23_24_25_26_lon, zone_23_24_25_26_lat, bathymetry, shallower_than=80, deeper_than=35)

    z23 = SimpleBathymetricBasin("zone23", z23)
    z24 = SimpleBathymetricBasin("zone24", z24)
    z25 = SimpleBathymetricBasin("zone25", z25)
    z26 = SimpleBathymetricBasin("zone26", z26)

    basins.append(z23)
    basins.append(z24)
    basins.append(z25)
    basins.append(z26)


    return tuple(basins)

