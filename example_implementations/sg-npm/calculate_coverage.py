#!/usr/bin/env python3

import logging
import argparse
import subprocess
from pathlib import Path
import json


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--bam", required=True, default=None,
                        help="Path to input BAM or CRAM.")
    parser.add_argument("--out_json", required=True, default=None,
                        help="Path to output json.")
    parser.add_argument("--fasta", required=False, default=None,
                        help="Path to genome fasta. Required when providing an input CRAM.")
    parser.add_argument("--bed", required=False, default=None,
                        help="Path to BED file to be used as a mask for metrics calculation. Only regions in the provided BED will be considered.")
    parser.add_argument("--mapq", required=False, default=20,
                        help="Mapping quality threshold. Default: 20.")
    parser.add_argument("--scratch_dir", required=False, default=".",
                        help="Path to scratch directory. Default: ./")
    parser.add_argument("--loglevel", required=False, default="INFO",
                        help="Set logging level to INFO (default), WARNING or DEBUG.")
    args = parser.parse_args()

    set_logging(args.loglevel)

    # I/O checks
    if not Path(args.bam).exists():
        logging.error(f"Couldn't find input file: {args.bam}")
        exit(1)

    if Path(args.bam).suffix == ".cram" and not args.fasta:
        logging.error("Must provide a fasta file when running from CRAM")
        exit(1)

    if Path(args.bam).suffix == ".cram" and not Path(args.fasta).exists():
        logging.error(f"Couldn't find input file: {args.fasta}")
        exit(1)

    if not Path(args.bed).exists():
        logging.error(f"Couldn't find input file: {args.bed}")
        exit(1)

    if not Path(args.scratch_dir).exists():
        logging.error(f"Couldn't find scratch directory: {args.scratch_dir}")
        exit(1)

    # check software dependencies
    cmd = "mosdepth --version"
    args.mosdepth_version = try_run_command(cmd, return_stdout=True)

    cmd = "datamash --version | head -1"
    args.datamash_version = try_run_command(cmd, return_stdout=True)

    # retrieve sample id
    args.sample_id = Path(args.bam).stem

    # set mosdepth prefix
    args.mosdepth_prefix = f"{args.scratch_dir}/{args.sample_id}"

    # report input args
    input_args = ",".join(f"{k}={v}" for k, v in vars(args).items())
    logging.info(f"Input arguments: {input_args}")

    return args


def set_logging(loglevel):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {loglevel}")
    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s", level=numeric_level)


def try_run_command(cmd, return_stdout=False):
    logging.debug(f"CMD: {cmd}")
    try:
        if return_stdout:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            stdout = p.stdout.read().decode("utf-8").strip()
            return stdout
        else:
            p = subprocess.run(cmd, shell=True)
    except:
        logging.error(f"Error when running command: {cmd}")
        exit(1)


def run_mosdepth(args):
    logging.info("Running mosdepth...")
    mosdepth_options = f"--no-per-base --by 1000 --mapq {args.mapq} --threads 4"
    if Path(args.bam).suffix == ".cram":
        mosdepth_options += f"{mosdepth_options} --fasta {args.fasta}"
    cmd = f"mosdepth {mosdepth_options} {args.mosdepth_prefix} {args.bam}"
    try_run_command(cmd)


def apply_bed_mask(args):
    if args.bed:
        logging.info("Applying bed mask...")
        cmd = f"zcat {args.mosdepth_prefix}.regions.bed.gz"
        cmd += f" | bedtools intersect -a stdin -b {args.bed}"
        cmd += f" | gzip -c > {args.mosdepth_prefix}.regions.masked.bed.gz"
        try_run_command(cmd)


def calculate_metrics(args):
    # general settings
    mosdepth_bed = f"{args.mosdepth_prefix}.regions.masked.bed.gz" if args.bed else f"{args.mosdepth_prefix}.regions.bed.gz"
    metrics_dict = dict()
    source = f"In-house tool based on {args.mosdepth_version}"
    implementation_details = dict(
        REF = "GRCh38 (## refget checksum ##)",
        BED = args.bed,
        MIN_BQ = 0,
        MIN_MQ = args.mapq,
        DUP = False,
        CLP = False,
        UMI = False
    )

    # metric-specific calculations
    id = "mean_autosome_coverage"
    description = "The mean coverage in autosomes, after coverage filters are applied."
    logging.info(f"Calculating metrics: {id}...")
    cmd = f"zcat {mosdepth_bed} | datamash --round 4 mean 4"
    value = round(float(try_run_command(cmd, return_stdout=True)), 4)
    metrics_dict[id] = dict(description=description, source=source, implementation_details=implementation_details, value=value)

    id = "sd_autosome_coverage"
    description = "The standard deviation of coverage in autosomes, after coverage filters are applied."
    logging.info(f"Calculating metrics: {id}...")
    cmd = f"zcat {mosdepth_bed} | datamash --round 4 sstdev 4"
    value = round(float(try_run_command(cmd, return_stdout=True)), 4)
    metrics_dict[id] = dict(description=description, source=source, implementation_details=implementation_details, value=value)

    id = "median_autosome_coverage"
    description = "The median coverage in autosomes, after coverage filters are applied."
    logging.info(f"Calculating metrics: {id}...")
    cmd = f"zcat {mosdepth_bed} | datamash --round 4 median 4"
    value = round(float(try_run_command(cmd, return_stdout=True)), 4)
    metrics_dict[id] = dict(description=description, source=source, implementation_details=implementation_details, value=value)

    id = "mad_autosome_coverage"
    description = "The median absolute deviation of coverage in autosomes, after coverage filters are applied."
    logging.info(f"Calculating metrics: {id}...")
    cmd = f"zcat {mosdepth_bed} | datamash --round 4 madraw 4"
    value = round(float(try_run_command(cmd, return_stdout=True)), 4)
    metrics_dict[id] = dict(description=description, source=source, implementation_details=implementation_details, value=value)

    id = "total_autosome_bases"
    description = "The number of non-N bases in autosomes over which coverage will be evaluated."
    logging.info(f"Calculating metrics: {id}...")
    cmd = "zcat %s | awk -F '\\t' 'BEGIN { SUM=0 } { SUM+=$3-$2 } END { print SUM }'" % mosdepth_bed
    value = int(try_run_command(cmd, return_stdout=True))
    metrics_dict[id] = dict(description=description, source=source, implementation_details=implementation_details, value=value)

    for min_depth in 1, 5, 10, 15, 20, 25, 30:
        id = f"pct_autosomes_{min_depth}x"
        description = f"The percentage of bases that attained at least {min_depth}X sequence coverage in autosomes, after coverage filters are applied."
        logging.info(f"Calculating metrics: {id}...")
        cmd = "zcat %s | awk '$4>=%d' | awk -F '\\t' 'BEGIN { SUM=0 } { SUM+=$3-$2 } END { print SUM }'" % (mosdepth_bed, min_depth)
        min_depth_bases = try_run_command(cmd, return_stdout=True)
        total_bases = metrics_dict["total_autosome_bases"]["value"]
        value = round(int(min_depth_bases)/int(total_bases) * 100, 4)
        metrics_dict[id] = dict(description=description, source=source, implementation_details=implementation_details, value=value)

    return metrics_dict


def report_metrics(args, metrics_dict):
    logging.info("Saving metrics report...")
    output_report = dict(
        sample_id = args.sample_id,
        qc_metrics = metrics_dict
    )
    with open(args.out_json, "w") as out_file:
        json.dump(output_report, out_file, indent=4)


def done(args):
    logging.info(f"DONE: {args.out_json}")


if __name__ == "__main__":
    args = parse_args()
    run_mosdepth(args)
    apply_bed_mask(args)
    metrics_dict = calculate_metrics(args)
    report_metrics(args, metrics_dict)
    done(args)