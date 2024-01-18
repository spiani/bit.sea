from basins.region import BathymetricPolygon, Polygon
from basins.basin import SimpleBathymetricBasin, SimpleBasin, ComposedBasin

def generate_basins_for_adriatic(bathymetry):
    basins = []

    # ZONE 1  5 and 9
    44.60546875
    zone_1_5_9_lon = [12.22265625, 13.30859375, 13.30859375, 12.22265625]
    zone_1_5_9_lat = [44.60546875, 44.60546875, 45.10546875, 45.10546875]

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
    zone_4_8_lat = [45.49609375, 45.30078125, 45.30078125, 45.9       , 45.49609375]

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
    zone_11_lon = [12.22265625,13.27734375,13.27734375,12.22265625,12.22265625]
    zone_11_lat = [44.60546875,44.60546875,45.73046875,45.73046875,44.60546875]

    z11 = BathymetricPolygon(zone_11_lon, zone_11_lat, bathymetry, shallower_than=220, deeper_than=35)

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

    # ZONE 14 ISTRIAN COAST
    zone_14_lon = [13.28515625, 13.91015625, 13.91015625, 13.28515625]
    zone_14_lat = [44.60546875, 44.60546875, 45.49609375, 45.49609375]

    z14_raw = Polygon(zone_14_lon, zone_14_lat)
    z14_raw = BathymetricPolygon(zone_14_lon, zone_14_lat, bathymetry, shallower_than=35)

    z14_raw = SimpleBasin("zone14", z14_raw)

    # Zone14bis defined to fill some irregularities

    zone_14_lon_bis = [13.28515625, 13.91015625, 13.91015625, 13.28515625]
    zone_14_lat_bis = [45.3       , 45.3       , 45.49609375, 45.49609375]

    z14bis=Polygon(zone_14_lon_bis,zone_14_lat_bis)

    z14bis=SimpleBasin("zone14bis", z14bis)

    z14=ComposedBasin("zone14",[z14_raw,z14bis])

    basins.append(z14)


    # ZONE 15 ISTRIA PROFONDA
    zone_15_lon = [13.28515625,13.91015625,13.91015625,13.28515625]
    zone_15_lat = [44.60546875,44.60546875,45.2       ,45.2       ]

    z15 = BathymetricPolygon(zone_15_lon, zone_15_lat, bathymetry, deeper_than=35)

    z15 = SimpleBathymetricBasin("zone15", z15)

    basins.append(z15)

    # ZONE 18-21  WEST MIDDLE ADRI
    zone_18_19_20_21_lon = [12.22265625,14.01171875,13.28515625,12.22265625]
    zone_18_19_20_21_lat = [43.96484375,43.96484375,44.60546875,44.60546875]


    z18 = BathymetricPolygon(zone_18_19_20_21_lon, zone_18_19_20_21_lat, bathymetry, shallower_than=20)
    z19 = BathymetricPolygon(zone_18_19_20_21_lon, zone_18_19_20_21_lat, bathymetry, shallower_than=30, deeper_than=20)
    z20 = BathymetricPolygon(zone_18_19_20_21_lon, zone_18_19_20_21_lat, bathymetry, shallower_than=35, deeper_than=30)
    z21 = BathymetricPolygon(zone_18_19_20_21_lon, zone_18_19_20_21_lat, bathymetry, shallower_than=220, deeper_than=35)

    z18 = SimpleBathymetricBasin("zone18", z18)
    z19 = SimpleBathymetricBasin("zone19", z19)
    z20 = SimpleBathymetricBasin("zone20", z20)
    z21 = SimpleBathymetricBasin("zone21", z21)

    basins.append(z18)
    basins.append(z19)
    basins.append(z20)
    basins.append(z21)

    # ZONE 22 MIDDLE MIDDLE ADRI
    zone_22_lon = [14.01171875,14.75390625,13.91796875,13.28515625]
    zone_22_lat = [43.96484375,43.96484375,44.60546875,44.60546875]

    z22 = BathymetricPolygon(zone_22_lon, zone_22_lat, bathymetry, shallower_than=220, deeper_than=35)

    z22 = SimpleBathymetricBasin("zone22", z22)

    basins.append(z22)

    # ZONE 23  EAST MIDDLE ADRI
    zone_23_lon = [14.75390625,15.80859375,15.80859375,13.91796875,13.91796875]
    zone_23_lat = [43.96484375,43.96484375,45.41796875,45.41796875,44.60546875]
    z23 = Polygon(zone_23_lon,zone_23_lat)
    z23 = SimpleBasin("zone23", z23)

    basins.append(z23)

    # ZONE 27 - 30  WEST MARCHE ADRI
    zone_27_28_29_30_lon = [12.22265625,14.40234375,14.01171875,12.22265625]
    zone_27_28_29_30_lat = [43.60546875,43.60546875,43.96484375,43.96484375]


    z27 = BathymetricPolygon(zone_27_28_29_30_lon, zone_27_28_29_30_lat, bathymetry, shallower_than=20)
    z28 = BathymetricPolygon(zone_27_28_29_30_lon, zone_27_28_29_30_lat, bathymetry, shallower_than=30, deeper_than=20)
    z29 = BathymetricPolygon(zone_27_28_29_30_lon, zone_27_28_29_30_lat, bathymetry, shallower_than=35, deeper_than=30)
    z30 = BathymetricPolygon(zone_27_28_29_30_lon, zone_27_28_29_30_lat, bathymetry, shallower_than=220, deeper_than=35)

    z27 = SimpleBathymetricBasin("zone27", z27)
    z28 = SimpleBathymetricBasin("zone28", z28)
    z29 = SimpleBathymetricBasin("zone29", z29)
    z30 = SimpleBathymetricBasin("zone30", z30)

    basins.append(z27)
    basins.append(z28)
    basins.append(z29)
    basins.append(z30)

    # ZONE 31  MIDDLE MARCHE ADRI
    zone_31_lon = [14.40234375,15.26171875,14.75390625,14.01171875]
    zone_31_lat = [43.60546875,43.60546875,43.96484375,43.96484375]

    z31 = Polygon(zone_31_lon, zone_31_lat)

    z31 = SimpleBasin("zone31", z31)
    basins.append(z31)

    # ZONE 32 - 35  EAST MARCHE ADRI
    zone_32_lon = [15.26171875,16.04296875,16.04296875,14.75390625]
    zone_32_lat = [43.60546875,43.60546875,43.96484375,43.96484375]

    z32 = Polygon(zone_32_lon, zone_32_lat)

    z32 = SimpleBathymetricBasin("zone32", z32)

    basins.append(z32)

    # ZONE 36 - 39  WEST SOUTH BC
    zone_36_37_38_39_lon = [12.22265625,14.59765625,14.40234375,12.22265625]
    zone_36_37_38_39_lat = [43.47265625,43.47265625,43.59765625,43.59765625]

    z36 = BathymetricPolygon(zone_36_37_38_39_lon, zone_36_37_38_39_lat, bathymetry, shallower_than=20)
    z37 = BathymetricPolygon(zone_36_37_38_39_lon, zone_36_37_38_39_lat, bathymetry, shallower_than=30, deeper_than=20)
    z38 = BathymetricPolygon(zone_36_37_38_39_lon, zone_36_37_38_39_lat, bathymetry, shallower_than=35, deeper_than=30)
    z39 = BathymetricPolygon(zone_36_37_38_39_lon, zone_36_37_38_39_lat, bathymetry, shallower_than=220, deeper_than=35)

    z36 = SimpleBathymetricBasin("zone36", z36)
    z37 = SimpleBathymetricBasin("zone37", z37)
    z38 = SimpleBathymetricBasin("zone38", z38)
    z39 = SimpleBathymetricBasin("zone39", z39)

    basins.append(z36)
    basins.append(z37)
    basins.append(z38)
    basins.append(z39)
        
    # ZONE 40  MIDDLE SOUTH ADRI
    zone_40_lon = [14.59765625,15.41796875,15.26171875,14.40234375]
    zone_40_lat = [43.47265625,43.47265625,43.59765625,43.59765625]

    z40 = Polygon(zone_40_lon, zone_40_lat)

    z40 = SimpleBasin("zone40", z40)
    basins.append(z40)
        
    # ZONE 41  EAST SOUTH ADRI
    zone_41_lon = [15.41796875,16.07421875,16.07421875,15.26171875]
    zone_41_lat = [43.47265625,43.47265625,43.59765625,43.59765625]

    z41 = Polygon(zone_41_lon, zone_41_lat)

    z41 = SimpleBathymetricBasin("zone41", z41)

    basins.append(z41)
 
    return tuple(basins)

