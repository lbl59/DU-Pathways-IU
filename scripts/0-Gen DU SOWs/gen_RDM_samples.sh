#!/bin/bash

JAVA_ARGS="-Xmx1g -classpath MOEAFramework-3.5-Demo.jar"
NUM_SAMPLES=250
METHOD=latin

RANGES_FILENAME=rdm_ranges_actions_conf.txt
OUTPUT_FILENAME=rdm_ranges_actions_conf_neg.txt
CSV_FILENAME=rdm_ranges_actions_conf_neg.csv

java ${JAVA_ARGS} org.moeaframework.analysis.sensitivity.SampleGenerator -m ${METHOD} -n ${NUM_SAMPLES} -p ${RANGES_FILENAME} -o ${OUTPUT_FILENAME}

sed 's/ /,/g' ${OUTPUT_FILENAME} > ${CSV_FILENAME}