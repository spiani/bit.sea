OPA_RUNDATE=20171010 # tuesday 

STARTTIME_a=$( date -d " $OPA_RUNDATE -10 days " +%Y%m%d ) 
END__TIME_a=$( date -d " $OPA_RUNDATE  -8 days " +%Y%m%d )

STARTTIME_s=$( date -d " $OPA_RUNDATE -7 days " +%Y%m%d )

STARTTIME_f=$( date -d " $OPA_RUNDATE  -7 days " +%Y%m%d )
END__TIME_f=$( date -d " $OPA_RUNDATE  -4 days " +%Y%m%d )

export MASKFILE=/marconi/home/usera07ogs/a07ogs00/OPA/V3C/etc/static-data/MED24_125/meshmask.nc

WRKDIR=/marconi/home/usera07ogs/a07ogs00/OPA/V3C-dev/wrkdir/2
ARCHIVE_DIR=/marconi/home/usera07ogs/a07ogs00/OPA/V3C-dev/archive

ONLINE_VALIDATION_DIR=/marconi_scratch/usera07ogs/a07ogs01/online_validation_data/


mkdir -p $ONLINE_VALIDATION_DIR/PREVIOUS
mkdir -p $ONLINE_VALIDATION_DIR/ACTUAL

if [ 1 == 0 ]; then

python archive_extractor.py --type analysis -st ${STARTTIME_a} -et ${END__TIME_a}  -a ${ARCHIVE_DIR}  -o ${ONLINE_VALIDATION_DIR}/PREVIOUS
python archive_extractor.py --type forecast -st ${STARTTIME_s} -et ${STARTTIME_s}  -a ${ARCHIVE_DIR}  -o ${ONLINE_VALIDATION_DIR}/PREVIOUS
python archive_extractor.py --type forecast -st ${STARTTIME_f} -et ${END__TIME_f}  -a ${ARCHIVE_DIR}  -o ${ONLINE_VALIDATION_DIR}/PREVIOUS
python archive_extractor.py --type analysis -st ${STARTTIME_f} -et ${END__TIME_f}  -a ${ARCHIVE_DIR}  -o ${ONLINE_VALIDATION_DIR}/ACTUAL


mkdir -p $ONLINE_VALIDATION_DIR/PREVIOUS/output_phys
mkdir -p $ONLINE_VALIDATION_DIR/ACTUAL/output_phys
INGV_MASK=/marconi/home/usera07ogs/a07ogs00/OPA/V3C/etc/static-data/MED24_141/meshmask.nc

#Cutting the physics domain INGV to OGS:
python ingv_cutter.py -i ${ONLINE_VALIDATION_DIR}/PREVIOUS/output_phys_ingv -o  ${ONLINE_VALIDATION_DIR}/PREVIOUS/output_phys -M $INGV_MASK -m $MASKFILE
python ingv_cutter.py -i ${ONLINE_VALIDATION_DIR}/ACTUAL/output_phys_ingv -o ${ONLINE_VALIDATION_DIR}/ACTUAL/output_phys -M $INGV_MASK -m $MASKFILE


PROFILERDIRP=${ONLINE_VALIDATION_DIR}/PREVIOUS/PROFILATORE
IMG_DIR_PREV=${ONLINE_VALIDATION_DIR}/PREVIOUS/IMG
   PHYS_DIRP=${ONLINE_VALIDATION_DIR}/PREVIOUS/output_phys
    BIO_DIRP=${ONLINE_VALIDATION_DIR}/PREVIOUS/output_bio

PROFILERDIRA=${ONLINE_VALIDATION_DIR}/ACTUAL/PROFILATORE
IMG_DIR__ACT=${ONLINE_VALIDATION_DIR}/ACTUAL/IMG
   PHYS_DIRA=${ONLINE_VALIDATION_DIR}/ACTUAL/output_phys
    BIO_DIRA=${ONLINE_VALIDATION_DIR}/ACTUAL/output_bio

# Matchup analysis
mkdir -p $IMG_DIR_PREV
mkdir -p $IMG_DIR__ACT
python float_extractor.py -st ${STARTTIME_a} -et ${END__TIME_a} -i ${BIO_DIRP} -p ${PHYS_DIRP}  -b $PROFILERDIRP  -o $IMG_DIR_PREV -m $MASKFILE
#Matchup forecasts
python float_extractor.py -st ${STARTTIME_f} -et ${END__TIME_f} -i ${BIO_DIRP} -p ${PHYS_DIRP}  -b $PROFILERDIRP  -o $IMG_DIR_PREV -m $MASKFILE
# Matchup actual
python float_extractor.py -st ${STARTTIME_f} -et ${END__TIME_f} -i ${BIO_DIRA} -p ${PHYS_DIRA}  -b $PROFILERDIRA  -o $IMG_DIR__ACT -m $MASKFILE
fi



BACKGROUND=/marconi/home/usera07ogs/a07ogs00/OPA/V3C-dev/etc/static-data/POSTPROC/background_medeaf.png
MODELDIR=/marconi/home/usera07ogs/a07ogs00/OPA/V3C-dev/wrkdir/2/MODEL/AVE_FREQ_1

MAPS=/marconi_scratch/usera07ogs/a07ogs01/MAPS/
XML_FILE=/marconi/home/usera07ogs/a07ogs00/OPA/V3C-dev/HOST/marconi/bit.sea/postproc/Plotlist_bio.xml
mkdir -p $MAPS/ORIG
cp /marconi/home/usera07ogs/a07ogs00/OPA/V3C-dev/etc/static-data/POSTPROC/fonts/TitilliumWeb-Regular.ttf $MAPS

cd $MAPS
BITSEA=/marconi/home/usera07ogs/a07ogs01/MAPPE/bit.sea/
python $BITSEA/build_layer_maps.py -b $BACKGROUND -o $MAPS/ORIG -m $MASKFILE -i $MODELDIR -p $XML_FILE