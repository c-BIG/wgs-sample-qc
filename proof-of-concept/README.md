# Proof of concept

As a first step towards defining the scope of the project, we encourage interested initiatives to run their existing sample QC pipeline on publicly available data, and submit its outputs and metric definitions here. This will allow us to assess how much overlap there is across workflows and kick off discussions on which outputs are “directly comparable” vs. which remain “functionally equivalent”.

**Submission instructions**

1. Run your sample QC pipeline on the following NA12878 build:

```
# BAM and VCF:
s3://1000genomes-dragen/data/dragen-3.5.7b/hg38_altaware_nohla-cnv-anchored/NA12878/

# reference:
aws s3 ls s3://1000genomes-dragen-3.7.6/references/fasta/hg38.fa

# from https://registry.opendata.aws/ilmn-dragen-1kgp/
```

2. Upload results and metric definitions to the present repository.
