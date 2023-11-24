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

    z1 = SimpleBathymetricBasin("z1", z1)
    z5 = SimpleBathymetricBasin("z5", z5)
    z9 = SimpleBathymetricBasin("z9", z9)

    basins.append(z1)
    basins.append(z5)
    basins.append(z9)


    # ZONE 2 6
    zone_2_6_lon = [12.22265625, 13.07421875, 13.07421875, 12.22265625]
    zone_2_6_lat = [45.11328125, 45.11328125, 45.18359375, 45.22265625]

    # ZONE 3 7
    zone_3_7_lon = [12.22265625, 13.07421875, 12.80078125, 12.22265625]
    zone_3_7_lat = [45.22265625, 45.18359375, 45.30078125, 45.49609375]

    # ZONE 4 8
    zone_4_8_lon = [12.22265625, 12.80078125, 13.27734375, 13.27734375, 12.22265625]
    zone_4_8_lat = [45.49609375, 45.30078125, 45.30078125, 45.73046875, 45.49609375]

    # ZONE 10
    zone_10_lon = [12.22265625, 13.27734375, 13.27734375, 12.22265625, 12.22265625]
    zone_10_lat = [45.11328125, 45.11328125, 45.73046875, 45.73046875, 45.11328125]

    # ZONE 11
    zone_11_lon = [12.22265625, 13.40234375, 13.40234375, 12.22265625, 12.22265625]
    zone_11_lat = [44.61328125, 44.61328125, 45.73046875, 45.73046875, 44.61328125]

    # ZONE 12 13 GULF OF TRIESTE
    zone_12_13_lon = [13.28515625, 13.91796875, 13.91796875, 13.28515625]
    zone_12_13_lat = [45.49609375, 45.49609375, 45.80859375, 45.80859375]

    # ZONE 14 15 16 ISTRIAN COAST
    zone_14_15_16_lon = [13.28515625, 13.91015625, 13.91015625, 13.28515625]
    zone_14_15_16_lat = [44.69921875, 44.69921875, 45.48828125, 45.48828125]

    # ZONE 17 ISTRIA PROFONDA
    zone_17_lon = [13.41015625, 13.91015625, 13.91015625, 13.41015625]
    zone_17_lat = [44.61328125, 44.61328125, 45.09765625, 45.09765625]

    # ZONE 18-21  WEST MIDDLE ADRI
    zone_18_19_20_21_lon = [12.22265625, 14.01171875, 13.16796875, 12.22265625]
    zone_18_19_20_21_lat = [43.93359375, 43.93359375, 44.60546875, 44.60546875]

    # ZONE 22 MIDDLE MIDDLE ADRI
    zone_22_lon = [14.01171875, 14.76171875, 13.91796875, 13.16796875]
    zone_22_lat = [43.93359375, 43.93359375, 44.60546875, 44.60546875]

    # ZONE 23 - 26  EAST MIDDLE ADRI
    zone_23_24_25_26_lon = [14.76171875, 15.80859375, 15.80859375, 13.91796875, 13.91796875]
    zone_23_24_25_26_lat = [43.93359375, 43.93359375, 45.41796875, 45.41796875, 44.60546875]

    return tuple(basins)

