# `calculate_coverage.py`

## Dependencies

- [mosdepth](https://github.com/brentp/mosdepth)
- [datamash](https://www.gnu.org/software/datamash/)

## Usage

```bash
python calculate_coverage.py -h
# usage: calculate_coverage.py [-h] --bam BAM --out_json OUT_JSON
#                              [--fasta FASTA] [--bed BED] [--mapq MAPQ]
#                              [--scratch_dir SCRATCH_DIR] [--loglevel LOGLEVEL]

# optional arguments:
#   -h, --help            show this help message and exit
#   --bam BAM             Path to input BAM or CRAM.
#   --out_json OUT_JSON   Path to output json.
#   --fasta FASTA         Path to genome fasta. Required when providing an input
#                         CRAM.
#   --bed BED             Path to BED file to be used as a mask for metrics
#                         calculation. Only regions in the provided BED will be
#                         considered.
#   --mapq MAPQ           Mapping quality threshold. Default: 20.
#   --scratch_dir SCRATCH_DIR
#                         Path to scratch directory. Default: ./
#   --loglevel LOGLEVEL   Set logging level to INFO (default), WARNING or DEBUG.

## example run
python calculate_coverage.py \
    --bam /data/NPM-sample-qc/proof_of_concept/NA12878.bam \
    --bed /data/NPM-sample-qc/proof_of_concept/Homo_sapiens_assembly38.autosomes.bed \
    --mapq 20 \
    --scratch_dir /data/NPM-sample-qc/proof_of_concept/work \
    --out_json /data/NPM-sample-qc/proof_of_concept/NA12878.coverage_metrics.json
# 2021-10-19 07:54:33,049 INFO     Input arguments: bam=/data/NPM-sample-qc/proof_of_concept/NA12878.bam,out_json=/data/NPM-sample-qc/proof_of_concept/NA12878.coverage_metrics.json,fasta=None,bed=/data/NPM-sample-qc/proof_of_concept/Homo_sapiens_assembly38.autosomes.bed,mapq=20,scratch_dir=./data/NPM-sample-qc/proof_of_concept/work,loglevel=INFO,mosdepth_version=mosdepth 0.2.6,datamash_version=datamash (GNU datamash) 1.7,sample_id=NA12878,mosdepth_prefix=/data/NPM-sample-qc/proof_of_concept/work/NA12878
# 2021-10-19 07:54:33,049 INFO     Running mosdepth...
# 2021-10-19 07:59:07,263 INFO     Applying bed mask...
# 2021-10-19 07:59:11,855 INFO     Calculating metrics: mean_autosome_coverage...
# 2021-10-19 07:59:12,443 INFO     Calculating metrics: sd_autosome_coverage...
# 2021-10-19 07:59:13,084 INFO     Calculating metrics: median_autosome_coverage...
# 2021-10-19 07:59:14,553 INFO     Calculating metrics: mad_autosome_coverage...
# 2021-10-19 07:59:16,475 INFO     Calculating metrics: total_autosome_bases...
# 2021-10-19 07:59:18,742 INFO     Calculating metrics: pct_autosomes_1x...
# 2021-10-19 07:59:20,928 INFO     Calculating metrics: pct_autosomes_5x...
# 2021-10-19 07:59:23,058 INFO     Calculating metrics: pct_autosomes_10x...
# 2021-10-19 07:59:25,189 INFO     Calculating metrics: pct_autosomes_15x...
# 2021-10-19 07:59:27,313 INFO     Calculating metrics: pct_autosomes_20x...
# 2021-10-19 07:59:29,422 INFO     Calculating metrics: pct_autosomes_25x...
# 2021-10-19 07:59:31,523 INFO     Calculating metrics: pct_autosomes_30x...
# 2021-10-19 07:59:33,295 INFO     Saving metrics report...
# 2021-10-19 07:59:33,296 INFO     DONE: /data/NPM-sample-qc/proof_of_concept/NA12878.coverage_metrics.json
```

## Outputs

```bash
cat NA12878.coverage_metrics.json
# {
#     "sample_id": "NA12878",
#     "qc_metrics": {
#         "mean_autosome_coverage": {
#             "description": "The mean coverage in autosomes, after coverage filters are applied.",
#             "source": "In-house tool based on mosdepth 0.2.6",
#             "implementation_details": {
#                 "REF": "GRCh38 (## refget checksum ##)",
#                 "BED": "/data/NPM-sample-qc/proof_of_concept/Homo_sapiens_assembly38.autosomes.bed",
#                 "MIN_BQ": 0,
#                 "MIN_MQ": "20",
#                 "DUP": false,
#                 "CLP": false,
#                 "UMI": false
#             },
#             "value": 31.7162
#         },
#
#         ...
#
#         "pct_autosomes_30x": {
#             "description": "The percentage of bases that attained at least 30X sequence coverage in autosomes, after coverage # filters are applied.",
#             "source": "In-house tool based on mosdepth 0.2.6",
#             "implementation_details": {
#                 "REF": "GRCh38 (## refget checksum ##)",
#                 "BED": "Homo_sapiens_assembly38.autosomes.bed",
#                 "MIN_BQ": 0,
#                 "MIN_MQ": "20",
#                 "DUP": false,
#                 "CLP": false,
#                 "UMI": false
#             },
#             "value": 75.3728
#         }
#     }
# }
```
