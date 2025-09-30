# Clinical Genomics Pipeline - Installation Guide
# Complete dependency setup for replicating the environment

## System Requirements
- **OS:** Linux (Ubuntu 22.04 or similar) or WSL2 on Windows
- **RAM:** 32GB+ recommended (minimum 16GB)
- **Storage:** 1TB+ available space
- **CPU:** Multi-core processor recommended

## Installation Steps

### 1. Install Conda/Mamba
```bash
# Install miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Or install mamba (faster package manager)
conda install -c conda-forge mamba
```

### 2. Create Environment
```bash
# Using conda
conda env create -f environment.yml
conda activate clinical_genomics_pipeline

# Or using mamba (recommended)
mamba env create -f environment.yml
mamba activate clinical_genomics_pipeline
```

### 3. Install Python Dependencies
```bash
# After activating the environment
pip install -r requirements.txt
```

### 4. Verify Core Tools
```bash
# Check installations
vep --help
bcftools --version
tabix --version
python --version
```

## Large Database Downloads Required

### VEP Cache (26GB)
```bash
# Download VEP cache v114 for GRCh38
vep_install -a cf -s homo_sapiens -y GRCh38 -c /path/to/vep_cache --CONVERT
```

### ClinVar (162MB)
```bash
# Download current ClinVar
wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
wget https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi
```

### gnomAD v4.1 (184GB total)
```bash
# Download gnomAD genome files (all chromosomes)
# This is a large download - plan accordingly
for chr in {1..22} X Y; do
    wget https://gnomad-public-us-east-1.s3.amazonaws.com/release/4.1/vcf/genomes/gnomad.genomes.v4.1.sites.chr${chr}.vcf.bgz
    wget https://gnomad-public-us-east-1.s3.amazonaws.com/release/4.1/vcf/genomes/gnomad.genomes.v4.1.sites.chr${chr}.vcf.bgz.tbi
done
```

### CADD v1.6/v1.7 (83GB)
```bash
# Download CADD scores
wget https://krishna.gs.washington.edu/download/CADD/v1.6/GRCh38/whole_genome_SNVs.tsv.gz
wget https://krishna.gs.washington.edu/download/CADD/v1.6/GRCh38/whole_genome_SNVs.tsv.gz.tbi
```

### dbNSFP v4.9a (73GB)
```bash
# Download dbNSFP database with REVEL scores
wget -c https://sites.google.com/site/jpopgen/dbNSFP/dbNSFP4.9a.zip
unzip dbNSFP4.9a.zip
```

### AlphaMissense (614MB) - 2024 Gold Standard
```bash
# Download AlphaMissense predictions
wget https://storage.googleapis.com/dm_alphamissense/AlphaMissense_hg38.tsv.gz
tabix -s 1 -b 2 -e 2 -f AlphaMissense_hg38.tsv.gz
```

### Reference Genome (761MB)
```bash
# Download GRCh38 reference
wget http://ftp.ensembl.org/pub/release-104/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
```

## Directory Structure Setup
```bash
# Create organized directory structure
mkdir -p /mnt/d/Genome/{databases,scripts,input_data,processed_vcfs,annotation_results,logs}
mkdir -p /mnt/d/Genome/databases/{vep_cache,clinvar,gnomad,cadd,dbnsfp,alphamissense,reference}
mkdir -p /mnt/d/Genome/scripts/{annotation,filtering}
mkdir -p /mnt/d/Genome/vep_setup/plugins
```

## Environment Validation
```bash
# Test the complete pipeline setup
cd /mnt/d/Genome
bash master_pipeline_enhanced_logging.sh --help
```

## Troubleshooting Notes
- **VEP Version Issues:** If VEP shows "unknown" version, use `PERL5LIB="" vep --version`
- **Memory Issues:** Reduce VEP buffer size if running out of RAM
- **Permission Issues:** Ensure write permissions in all directories
- **WSL2 Issues:** May need to adjust paths for Windows/Linux compatibility

## Total Storage Requirements
- **Databases:** ~600GB
- **Processing Space:** ~500GB
- **Results Storage:** Variable based on usage
- **Total Recommended:** 1TB+

## Performance Notes
- **Full genome analysis:** 3-4 hours (4.7M variants)
- **Exome analysis:** 30-60 minutes (50K variants)
- **Memory usage:** 16-32GB during VEP annotation
- **Parallel processing:** Uses all available CPU cores
