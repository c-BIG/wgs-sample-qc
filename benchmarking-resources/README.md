# Benchmarking Resources

## 1000 Genomes Phase 3 Reanalysis with DRAGEN at Registry of Open Data on AWS

"1000 Genomes Phase 3 Reanalysis with DRAGEN 3.5 and 3.7" available from Registry of Open Data on AWS is a good first resource of BAM/CRAM and VCF pubklically available WGS data. 

This collection contains (amongst other) alignment files (.bam) and short nucleotide variant call files (.hard-filtered.gvcf.gz & .hard-filtered.vcf.gz formatted) from n=3202 "1000 Genomes Project 
Phase 3" samples dataset, reprocessed by Illumina using DRAGEN v3.5.7b and v3.7.6 software as part of the PrecisionFDA Truth Challenge V2.

The v3.7.6 dataset also includes results from joint small variant, de novo structural variant, de novo copy number variant and repeat expansion calls on 602 trio families 
comprised of members from the 1000 Genomes Project Phase 3 dataset, as well as DRAGEN gVCF Genotyper (v3.8.3) analysis on the entire dataset (n=3202). 

See https://registry.opendata.aws/ilmn-dragen-1kgp/ for more details.

---

**Resource type** public S3 Bucket

**Amazon Resource Name (ARN)** arn:aws:s3:::1000genomes-dragen-3.7.6

**AWS Region** us-west-2

**AWS CLI Access (No AWS account required)** `aws s3 ls --no-sign-request s3://1000genomes-dragen-3.7.6/`

---

**Prototypical path and (WGS sample QC relevant) data content**
```
s3://1000genomes-dragen-3.7.6/data/individuals/hg38-graph-based/NA21130/NA21130.bam
s3://1000genomes-dragen-3.7.6/data/individuals/hg38-graph-based/NA21130/NA21130.bam.bai
s3://1000genomes-dragen-3.7.6/data/individuals/hg38-graph-based/NA21130/NA21130.hard-filtered.gvcf.gz
s3://1000genomes-dragen-3.7.6/data/individuals/hg38-graph-based/NA21130/NA21130.hard-filtered.gvcf.gz.tbi
s3://1000genomes-dragen-3.7.6/data/individuals/hg38-graph-based/NA21130/NA21130.hard-filtered.vcf.gz
s3://1000genomes-dragen-3.7.6/data/individuals/hg38-graph-based/NA21130/NA21130.hard-filtered.vcf.gz.tbi
```

