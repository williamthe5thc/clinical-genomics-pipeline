# Clinical Genomics Pipeline v4.1 - System Requirements
# Generated: September 18, 2025
# Platform: WSL Ubuntu 22.04+ (Primary), Linux (Compatible)

# =============================================================================
# OPERATING SYSTEM REQUIREMENTS
# =============================================================================

# Primary Platform (Tested)
- WSL Ubuntu 22.04 LTS on Windows
- Linux kernel 6.6+ recommended
- 64-bit architecture required

# Alternative Platforms (Compatible)
- Ubuntu 20.04+ LTS
- CentOS 8+ / RHEL 8+
- Debian 11+ (Bullseye)

# =============================================================================
# HARDWARE REQUIREMENTS
# =============================================================================

# Minimum (Targeted Panels)
- RAM: 16GB
- Storage: 100GB available
- CPU: 4 cores

# Recommended (Exome Analysis)  
- RAM: 32-64GB
- Storage: 500GB available
- CPU: 8-16 cores

# Optimal (Whole Genome Analysis)
- RAM: 64-128GB 
- Storage: 1TB+ available
- CPU: 16-20 cores
- SSD storage recommended

# =============================================================================
# CORE SYSTEM TOOLS
# =============================================================================

# Essential Tools (Required)
sudo apt update && sudo apt install -y \
    build-essential \
    wget \
    curl \
    git \
    unzip \
    tabix \
    bcftools \
    samtools \
    bgzip \
    python3 \
    python3-pip \
    python3-dev \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libncurses5-dev \
    libcurl4-openssl-dev \
    libssl-dev

# Package Versions (Tested)
- bcftools: 1.21+
- samtools: 1.21+  
- tabix: 1.21+
- Python: 3.8+ (tested with 3.12.3)

# =============================================================================
# VEP DEPENDENCIES
# =============================================================================

# Perl Environment
- Perl 5.32+
- DBI module
- Archive::Zip
- LWP::Simple

# VEP Installation via Conda (Recommended)
# conda create -n vep_v114 -c bioconda -c conda-forge ensembl-vep=115
# conda activate vep_v114

# =============================================================================
# DATABASE STORAGE REQUIREMENTS
# =============================================================================

# Critical Databases (Required - 600GB Total)
/mnt/d/Genome/databases/
├── vep_cache/           # 26GB - VEP v114 GRCh38
├── gnomad/              # 184GB - Population frequencies v4.1
├── clinvar/             # 162MB - Clinical significance (monthly updates)
├── reference/           # 761MB - GRCh38 primary assembly
├── alphamissense/       # 614MB - Structure-based predictions  
├── dbnsfp/              # 73GB - REVEL + pathogenicity predictors
└── cadd/                # 82GB - Deleteriousness scores

# Processing Space (Additional 400GB)
/mnt/d/Genome/
├── processed_vcfs/      # 100GB - Intermediate VCF files
├── annotation_results/  # 200GB - Annotated results
├── logs/                # 10GB - Processing logs
└── temp/                # 90GB - Temporary processing files

# =============================================================================
# NETWORK REQUIREMENTS
# =============================================================================

# Initial Setup (Database Downloads)
- Stable internet connection for database downloads
- 500GB+ download capacity for initial setup
- No network required for processing (offline operation)

# Update Schedule
- ClinVar: Monthly updates (~200MB)
- gnomAD: Annual major releases (~200GB)
- VEP Cache: Quarterly updates (~30GB)

# =============================================================================
# PERFORMANCE BENCHMARKS
# =============================================================================

# Processing Times (Tested Configuration)
# System: WSL Ubuntu 22.04, 30GB RAM, 20 cores
- Whole Genome (4.7M variants): 3h 15m
- Exome (50K variants): 20-40 minutes  
- Targeted Panel (1K variants): 5-15 minutes

# Memory Usage Patterns
- VCF Preprocessing: 2-8GB
- VEP Annotation: 8-32GB peak
- Clinical Analysis: 4-16GB
- Concurrent Processing: 64GB+ recommended

# =============================================================================
# SECURITY CONSIDERATIONS  
# =============================================================================

# Data Protection
- Patient data encryption at rest recommended
- Secure file permissions (chmod 600 for sensitive files)
- Network isolation for processing environment
- Regular security updates for system packages

# HIPAA Compliance (If Applicable)
- Encrypted storage for PHI data
- Access logging and audit trails
- User authentication and authorization
- Data retention and disposal policies

# =============================================================================
# BACKUP REQUIREMENTS
# =============================================================================

# Critical Components to Backup
- Processing scripts: ~/Genome/scripts/
- Configuration files: ~/Genome/config/
- Results: ~/Genome/annotation_results/
- Processed samples: ~/Genome/processed_vcfs/

# Database Backup Strategy  
- Databases can be re-downloaded (not backed up due to size)
- Custom annotations and modifications should be backed up
- Version control for scripts and configurations

# =============================================================================
# MONITORING AND MAINTENANCE
# =============================================================================

# System Monitoring
- Disk space alerts (< 100GB available)
- Memory usage monitoring during processing
- Log rotation for processing logs
- Database integrity checks

# Maintenance Schedule
- Weekly: Log cleanup and disk space check
- Monthly: ClinVar database updates
- Quarterly: VEP cache updates, system package updates
- Annually: Major database updates (gnomAD, etc.)

# =============================================================================
# TROUBLESHOOTING RESOURCES
# =============================================================================

# Common Issues
1. VEP Perl environment conflicts -> Use PERL5LIB=""
2. Memory issues -> Reduce buffer_size and fork count
3. Disk space -> Clean temp files and old results
4. Permission issues -> Check file ownership and chmod

# Support Documentation
- Pipeline logs: logs/master_pipeline.log
- VEP logs: logs/annotation_logs/vep_annotation.log  
- Database status: Check with ls -la databases/*/
- System resources: Use htop, df -h, free -h

# =============================================================================
# VERSION COMPATIBILITY
# =============================================================================

# Tested Versions (September 2025)
- Ubuntu: 22.04 LTS
- Python: 3.12.3
- VEP: 115.1 
- bcftools: 1.21
- gnomAD: v4.1
- ClinVar: September 2025
- Assembly: GRCh38 (required)

# Upgrade Path
- Minor versions: Generally compatible
- Major versions: Test thoroughly before deployment
- Database versions: Follow official migration guides
- Pipeline versions: Maintain compatibility with existing data
