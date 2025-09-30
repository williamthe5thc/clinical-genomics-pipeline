#!/bin/bash

# =============================================================================
# VEP MASTER CLINICAL ANNOTATION PIPELINE v115
# =============================================================================
# Consolidated from all previous versions - Best of everything
# Enhanced logging + AlphaMissense + Error capture + Clinical standards
# Created: 2025-09-17 | Clinical Genomics Pipeline v4.1+
# =============================================================================

set -euo pipefail

# =============================================================================
# CONFIGURATION AND VERSIONING
# =============================================================================

SCRIPT_VERSION="v115-master-clinical"
SCRIPT_DATE="2025-09-17"
REQUIRED_VEP_VERSION="114"

# Base directories
BASE_DIR="/mnt/d/Genome"
DATABASE_DIR="${BASE_DIR}/databases"
LOGS_DIR="${BASE_DIR}/DATA/LOGS"

# VEP configuration
VEP_CACHE_DIR="${DATABASE_DIR}/vep_cache"
VEP_PLUGINS_DIR="${BASE_DIR}/COMPONENTS/ANNOTATION"
REFERENCE_FASTA="${DATABASE_DIR}/reference/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz"

# Database paths
CLINVAR_VCF="${DATABASE_DIR}/clinvar/clinvar.vcf.gz"
GNOMAD_DIR="${DATABASE_DIR}/gnomad"
CADD_DIR="${DATABASE_DIR}/cadd"
DBNSFP_DIR="${DATABASE_DIR}/dbnsfp"
ALPHAMISSENSE_FILE="${DATABASE_DIR}/alphamissense/AlphaMissense_hg38.tsv.gz"

# Email notification setup
EMAIL_NOTIFIER="${BASE_DIR}/UTILITIES/email_notifications/pipeline_notifier.py"
EMAIL_CONFIG="${BASE_DIR}/UTILITIES/email_notifications/email_config.json"
EMAIL_ENABLED=true

# Create logs directory
mkdir -p "${LOGS_DIR}"

# =============================================================================
# ENHANCED LOGGING FUNCTIONS
# =============================================================================

log_message() {
    local message="$1"
    local timestamp="[$(date '+%Y-%m-%d %H:%M:%S')]"
    echo "${timestamp} $message" | tee -a "${LOGS_DIR}/vep_annotation.log"
}

log_info() { log_message "ℹ️  INFO: $1"; }
log_success() { log_message "✅ SUCCESS: $1"; }
log_warning() { log_message "⚠️  WARNING: $1"; }
log_error() { log_message "❌ ERROR: $1"; }

error_exit() {
    log_error "$1"
    
    # Show recent error logs if available
    if [[ -f "${LOGS_DIR}/vep_stderr.log" ]]; then
        log_error "VEP Error Details (last 20 lines):"
        tail -20 "${LOGS_DIR}/vep_stderr.log" | while read line; do
            log_error "  $line"
        done
    fi
    
    if [[ -f "${LOGS_DIR}/vep_command_debug.txt" ]]; then
        log_error "Failed VEP Command:"
        head -5 "${LOGS_DIR}/vep_command_debug.txt" | while read line; do
            log_error "  CMD: $line"
        done
    fi
    
    exit 1
}

log_separator() { log_message "======================================================"; }

# =============================================================================
# EMAIL NOTIFICATION FUNCTIONS
# =============================================================================

send_email_notification() {
    local notification_type="$1"
    local sample_id="$2"
    local start_time="$3"
    local end_time="$4"
    local output_file="${5:-}"
    local file_size="${6:-}"
    local variant_count="${7:-0}"
    local error_message="${8:-}"
    
    if [[ "${EMAIL_ENABLED}" == "true" && -f "${EMAIL_NOTIFIER}" ]]; then
        log_info "📧 Sending ${notification_type} notification..."
        python3 "${EMAIL_NOTIFIER}" --type "${notification_type}" \
            --sample-id "${sample_id}" --start-time "${start_time}" \
            --end-time "${end_time}" --output-file "${output_file}" \
            --file-size "${file_size}" --variant-count "${variant_count}" \
            --error-message "${error_message}" --config "${EMAIL_CONFIG}" || {
            log_warning "Email notification failed (non-critical)"
        }
    fi
}

# =============================================================================
# SYSTEM VALIDATION FUNCTIONS
# =============================================================================

check_system_environment() {
    log_separator
    log_message "VEP MASTER CLINICAL PIPELINE STARTUP"
    log_separator
    
    log_info "Script: VEP Master Clinical v115"
    log_info "Date: $SCRIPT_DATE"
    log_info "Environment check starting..."
    
    # Check VEP installation
    if command -v vep &> /dev/null; then
        VEP_VERSION=$(vep --help 2>&1 | grep -o "ensembl-vep : [0-9]\+" | cut -d' ' -f3 2>/dev/null || echo "unknown")
        log_success "VEP found - Version: $VEP_VERSION"
        
        if [[ "$VEP_VERSION" != "unknown" && "$VEP_VERSION" -ge "$REQUIRED_VEP_VERSION" ]]; then
            log_success "VEP version meets clinical requirements (>=$REQUIRED_VEP_VERSION)"
        else
            log_warning "VEP version may not meet requirements (need >=$REQUIRED_VEP_VERSION)"
        fi
    else
        error_exit "VEP not found in PATH - please install VEP v114+"
    fi
    
    # Check essential tools
    for tool in bcftools tabix bgzip; do
        if command -v "$tool" &> /dev/null; then
            local version=$($tool --version 2>&1 | head -1 | grep -o "[0-9]\+\.[0-9]\+" | head -1 || echo "unknown")
            log_success "$tool found - Version: $version"
        else
            log_warning "$tool not found - may cause issues"
        fi
    done
    
    # System resources
    local ram_gb=$(free -g | awk 'NR==2{printf "%.0f", $7}' || echo "unknown")
    local disk_gb=$(df "${DATABASE_DIR}" 2>/dev/null | awk 'NR==2 {printf "%.0f", $4/1024/1024}' || echo "unknown")
    
    log_info "Available RAM: ${ram_gb}GB"
    log_info "Available disk: ${disk_gb}GB"
    
    if [[ "$ram_gb" != "unknown" && "$ram_gb" -lt 8 ]]; then
        log_warning "Low RAM detected - consider reducing buffer size"
    fi
    
    log_separator
}

check_file_exists() {
    local file="$1"
    local description="$2"
    
    if [[ ! -f "$file" ]]; then
        log_warning "$description not found: $file"
        return 1
    else
        local size=$(du -h "$file" 2>/dev/null | cut -f1 || echo "unknown")
        log_success "$description found ($size): $file"
        return 0
    fi
}

validate_databases() {
    log_separator
    log_message "DATABASE VALIDATION"
    log_separator
    
    local critical_ok=true
    
    # Critical databases
    check_file_exists "$REFERENCE_FASTA" "Reference genome (GRCh38)" || critical_ok=false
    check_file_exists "$CLINVAR_VCF" "ClinVar database" || critical_ok=false
    
    # VEP cache
    if [[ -d "${VEP_CACHE_DIR}/homo_sapiens/114_GRCh38" ]]; then
        local cache_size=$(du -sh "${VEP_CACHE_DIR}/homo_sapiens/114_GRCh38" 2>/dev/null | cut -f1 || echo "unknown")
        log_success "VEP cache v114 found ($cache_size)"
    else
        log_error "VEP cache v114 not found"
        critical_ok=false
    fi
    
    # AlphaMissense validation
    if check_file_exists "$ALPHAMISSENSE_FILE" "AlphaMissense database"; then
        if [[ -f "${ALPHAMISSENSE_FILE}.tbi" ]]; then
            log_success "AlphaMissense index found"
        else
            log_warning "AlphaMissense index missing - creating..."
            if command -v tabix &> /dev/null; then
                tabix -s 1 -b 2 -e 2 -f "$ALPHAMISSENSE_FILE" 2>/dev/null || log_warning "Failed to create AlphaMissense index"
            fi
        fi
        
        # Validate AlphaMissense format
        local header_check=$(zcat "$ALPHAMISSENSE_FILE" 2>/dev/null | head -1)
        if [[ "$header_check" == *"am_pathogenicity"* ]]; then
            log_success "AlphaMissense format validated"
        else
            log_warning "AlphaMissense format may be incorrect"
        fi
    else
        log_warning "AlphaMissense not available - structure-based predictions disabled"
    fi
    
    # Optional databases
    local cadd_files=$(find "$CADD_DIR" -name "*.tsv.gz" 2>/dev/null | wc -l || echo "0")
    local dbnsfp_files=$(find "$DBNSFP_DIR" -name "*.gz" 2>/dev/null | wc -l || echo "0")
    
    log_info "CADD files available: $cadd_files"
    log_info "dbNSFP files available: $dbnsfp_files"
    
    if [[ "$critical_ok" == false ]]; then
        error_exit "Critical databases missing - cannot continue"
    fi
    
    log_separator
}

# =============================================================================
# VEP COMMAND BUILDER FUNCTIONS
# =============================================================================

build_core_vep_command() {
    local input_vcf="$1"
    local output_vcf="$2"
    local threads="$3"
    
    local vep_cmd="vep"
    
    # Input/Output
    vep_cmd+=" --input_file '$input_vcf'"
    vep_cmd+=" --output_file '$output_vcf'"
    vep_cmd+=" --format vcf --vcf --force_overwrite --compress_output bgzip"
    
    # Core settings
    vep_cmd+=" --offline --cache --dir_cache '$VEP_CACHE_DIR'"
    vep_cmd+=" --cache_version 114"  # Force use of v114 cache with v115 VEP
    vep_cmd+=" --assembly GRCh38 --species homo_sapiens"
    vep_cmd+=" --fork $threads --buffer_size 25000"
    
    # Reference genome
    if [[ -f "$REFERENCE_FASTA" ]]; then
        vep_cmd+=" --fasta '$REFERENCE_FASTA'"
    fi
    
    # Comprehensive annotations
    vep_cmd+=" --everything --symbol --hgvs --hgvsg --canonical --mane_select"
    vep_cmd+=" --biotype --domains --numbers --tsl --appris --ccds --uniprot"
    vep_cmd+=" --gene_phenotype --regulatory --nearest symbol"
    
    # Population frequencies
    vep_cmd+=" --af --af_gnomade --af_gnomadg --max_af --check_existing --allele_number"
    
    # Basic predictions
    vep_cmd+=" --sift b --polyphen b"
    vep_cmd+=" --pick_order mane_select,canonical,appris,tsl,biotype,ccds,length"
    
    echo "$vep_cmd"
}

add_plugins_to_command() {
    local vep_cmd="$1"
    local plugins_enabled=0
    
    if [[ -d "$VEP_PLUGINS_DIR" ]]; then
        vep_cmd+=" --dir_plugins '$VEP_PLUGINS_DIR'"
        
        # CADD plugin
        local cadd_file=$(find "$CADD_DIR" -name "*SNVs*.tsv.gz" | head -1)
        if [[ -n "$cadd_file" && -f "$cadd_file" ]]; then
            vep_cmd+=" --plugin CADD,'$cadd_file'"
            ((plugins_enabled++))
        fi
        
        # AlphaMissense plugin (FIXED: moved from custom to plugin)
        if [[ -f "$ALPHAMISSENSE_FILE" ]]; then
            vep_cmd+=" --plugin AlphaMissense,file='$ALPHAMISSENSE_FILE'"
            ((plugins_enabled++))
        fi
        
        # dbNSFP plugin (REVEL + others)
        local dbnsfp_combined="${DBNSFP_DIR}/dbNSFP4.9a_combined.gz"
        if [[ -f "$dbnsfp_combined" ]]; then
            vep_cmd+=" --plugin dbNSFP,'$dbnsfp_combined',"
            vep_cmd+="SIFT_score,SIFT_pred,LRT_score,REVEL_score,Polyphen2_HDIV_score,"
            vep_cmd+="Polyphen2_HDIV_pred,MutationTaster_score,MutationTaster_pred,"
            vep_cmd+="CADD_raw,CADD_phred,GERP++_RS,phyloP100way_vertebrate"
            ((plugins_enabled++))
        fi
    fi
    
    echo "$vep_cmd"
}

add_custom_annotations() {
    local vep_cmd="$1"
    
    # ClinVar
    if [[ -f "$CLINVAR_VCF" ]]; then
        vep_cmd+=" --custom '$CLINVAR_VCF',ClinVar,vcf,exact,0,"
        vep_cmd+="CLNSIG,CLNREVSTAT,CLNDN,CLNDISDB,CLNHGVS,CLNVI"
    fi
    
    # AlphaMissense moved to add_plugins_to_command() function
    # Now using proper --plugin AlphaMissense,file=... syntax
    
    echo "$vep_cmd"
}

finalize_vep_command() {
    local vep_cmd="$1"
    local output_vcf="$2"
    
    # Output files
    vep_cmd+=" --stats_file '${output_vcf%.vcf.gz}_stats.html'"
    vep_cmd+=" --warning_file '${output_vcf%.vcf.gz}_warnings.txt'"
    
    # Performance optimizations
    vep_cmd+=" --max_sv_size 10000000"
    vep_cmd+=" --no_check_variants_order"
    
    echo "$vep_cmd"
}

# =============================================================================
# MAIN VEP EXECUTION FUNCTION
# =============================================================================

run_master_vep_annotation() {
    local input_vcf="$1"
    local output_vcf="$2"
    local sample_id="$3"
    local threads="$4"
    
    log_separator
    log_message "VEP MASTER ANNOTATION EXECUTION"
    log_separator
    
    log_info "Sample: $sample_id"
    log_info "Input: $input_vcf"
    log_info "Output: $output_vcf"
    log_info "Threads: $threads"
    
    # Validate input
    if [[ ! -f "$input_vcf" ]]; then
        error_exit "Input VCF not found: $input_vcf"
    fi
    
    # Input analysis
    local input_size=$(du -h "$input_vcf" 2>/dev/null | cut -f1 || echo "unknown")
    local input_variants=$(zcat "$input_vcf" 2>/dev/null | grep -v "^#" | wc -l 2>/dev/null || echo "unknown")
    log_info "Input size: $input_size, variants: $input_variants"
    
    # Create output directory
    mkdir -p "$(dirname "$output_vcf")"
    
    # Build comprehensive VEP command
    log_info "Building comprehensive VEP command..."
    
    local vep_cmd
    vep_cmd=$(build_core_vep_command "$input_vcf" "$output_vcf" "$threads")
    vep_cmd=$(add_plugins_to_command "$vep_cmd")
    vep_cmd=$(add_custom_annotations "$vep_cmd")
    vep_cmd=$(finalize_vep_command "$vep_cmd" "$output_vcf")
    
    # Log what was enabled AFTER command construction
    local cadd_file=$(find "$CADD_DIR" -name "*SNVs*.tsv.gz" | head -1)
    if [[ -n "$cadd_file" && -f "$cadd_file" ]]; then
        log_success "CADD plugin enabled: $(basename "$cadd_file")"
    fi
    
    local dbnsfp_combined="${DBNSFP_DIR}/dbNSFP4.9a_combined.gz"
    if [[ -f "$dbnsfp_combined" ]]; then
        log_success "dbNSFP plugin enabled with REVEL"
    fi
    
    if [[ -f "$CLINVAR_VCF" ]]; then
        log_success "ClinVar custom annotation enabled"
    fi
    
    if [[ -f "$ALPHAMISSENSE_FILE" ]]; then
        log_success "AlphaMissense custom annotation enabled (Structure-based predictions)"
        log_info "AlphaMissense thresholds: Pathogenic ≥0.564, Benign ≤0.34"
    fi
    
    # Save command for debugging
    echo "$vep_cmd" > "${LOGS_DIR}/vep_command_debug.txt"
    log_success "VEP command prepared and saved for debugging"
    
    # Execute VEP with comprehensive error capture
    log_separator
    log_message "EXECUTING VEP ANNOTATION"
    log_separator
    
    local start_time=$(date +%s)
    local vep_start_time_formatted=$(date)
    log_info "VEP execution started at ${vep_start_time_formatted}"
    
    # Run VEP with error capture and PERL5LIB fix
    if PERL5LIB="" eval "$vep_cmd" > "${LOGS_DIR}/vep_stdout.log" 2> "${LOGS_DIR}/vep_stderr.log"; then
    local end_time=$(date +%s)
    local vep_end_time_formatted=$(date)
    local duration=$((end_time - start_time))
    local duration_min=$((duration / 60))
    local duration_sec=$((duration % 60))
    
        log_success "VEP annotation completed in ${duration_min}m ${duration_sec}s"
        
        # Validate output
        if [[ -f "$output_vcf" ]]; then
            local output_size=$(du -h "$output_vcf" 2>/dev/null | cut -f1 || echo "unknown")
            local output_variants=$(zcat "$output_vcf" | grep -v "^#" | wc -l)
            
            log_success "Output VCF created: $output_vcf"
            log_info "Output size: $output_size, variants: $output_variants"
            
            # Check for key annotations
            local revel_count=$(zcat "$output_vcf" | grep -c "REVEL_score" || echo "0")
            local alphamissense_count=$(zcat "$output_vcf" | grep -c "AlphaMissense" || echo "0")
            local cadd_count=$(zcat "$output_vcf" | grep -c "CADD_phred" || echo "0")
            
            log_info "REVEL annotations: $revel_count"
            log_info "AlphaMissense annotations: $alphamissense_count"
            log_info "CADD annotations: $cadd_count"
            
            # Send success email notification
            send_email_notification "vep_completion" "${sample_id}" "${vep_start_time_formatted}" "${vep_end_time_formatted}" \
                                   "${output_vcf}" "${output_size}" "${output_variants}"
            
            # Create index
            if [[ ! -f "${output_vcf}.tbi" ]]; then
                tabix -p vcf "$output_vcf"
                log_success "VCF index created"
            fi
            
            # Check warnings
            if [[ -f "${output_vcf%.vcf.gz}_warnings.txt" ]]; then
                local warning_count=$(wc -l < "${output_vcf%.vcf.gz}_warnings.txt" || echo "0")
                if [[ "$warning_count" -gt 0 ]]; then
                    log_warning "VEP warnings: $warning_count (see warnings file)"
                else
                    log_success "No VEP warnings"
                fi
            fi
            
            return 0
        else
            # Output file missing - send failure notification
            local error_msg="VEP completed but output file ${output_vcf} not found"
            send_email_notification "vep_failure" "${sample_id}" "${vep_start_time_formatted}" "${vep_end_time_formatted}" \
                                   "" "" "0" "${error_msg}"
            error_exit "VEP output file not created"
        fi
    else
        # VEP command failed - send failure notification
        local vep_end_time_formatted=$(date)
        local error_msg="VEP annotation command failed. Check log files: ${LOGS_DIR}/vep_stderr.log"
        
        # Extract last error from log if available
        if [[ -f "${LOGS_DIR}/vep_stderr.log" ]]; then
            local last_error=$(tail -5 "${LOGS_DIR}/vep_stderr.log" | grep -i "error\|fail\|exception" | tail -1)
            if [[ -n "${last_error}" ]]; then
                error_msg="${error_msg}. Last error: ${last_error}"
            fi
        fi
        
        send_email_notification "vep_failure" "${sample_id}" "${vep_start_time_formatted}" "${vep_end_time_formatted}" \
                               "" "" "0" "${error_msg}"
        
        log_error "VEP command failed"
        
        # Show stdout/stderr for debugging
        if [[ -f "${LOGS_DIR}/vep_stdout.log" ]]; then
            log_error "VEP Standard Output (last 10 lines):"
            tail -10 "${LOGS_DIR}/vep_stdout.log" | while read line; do
                log_error "  OUT: $line"
            done
        fi
        
        error_exit "VEP annotation failed - see error details above"
    fi
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

# Usage check
if [[ $# -lt 3 ]]; then
    cat << EOF

=============================================================================
VEP MASTER CLINICAL ANNOTATION PIPELINE v115
=============================================================================

🧬 CLINICAL-GRADE VEP ANNOTATION WITH 2024-2025 STANDARDS

Usage: $0 <input.vcf.gz> <output.vcf.gz> <sample_id> [threads]

Features:
  ✅ Enhanced logging & error capture
  ✅ AlphaMissense structure-based predictions  
  ✅ REVEL + CADD + comprehensive pathogenicity predictors
  ✅ Clinical databases (ClinVar + gnomAD v4.1)
  ✅ Comprehensive system validation
  ✅ Professional error handling

Example:
  $0 /mnt/d/Genome/processed_vcfs/sample.vcf.gz \\
     /mnt/d/Genome/annotation_results/sample_annotated.vcf.gz \\
     SAMPLE_001 8

Clinical Standards:
  - REVEL ≥0.644: Supporting pathogenic evidence
  - AlphaMissense ≥0.564: Pathogenic classification
  - Multi-tool evidence integration for ACMG/AMP

=============================================================================

EOF
    exit 1
fi

# Parse arguments
INPUT_VCF="$1"
OUTPUT_VCF="$2"
SAMPLE_ID="$3"
THREADS="${4:-8}"

# Start pipeline
log_separator
log_message "VEP MASTER CLINICAL PIPELINE STARTUP"
log_separator
log_info "Sample: $SAMPLE_ID"
log_info "Version: $SCRIPT_VERSION ($SCRIPT_DATE)"

# Comprehensive validation
check_system_environment
validate_databases

# Execute annotation
run_master_vep_annotation "$INPUT_VCF" "$OUTPUT_VCF" "$SAMPLE_ID" "$THREADS"

# Final summary
log_separator
log_message "VEP MASTER PIPELINE COMPLETED"
log_separator
log_success "Sample $SAMPLE_ID annotated successfully"
log_info "Output: $OUTPUT_VCF"
log_info "Statistics: ${OUTPUT_VCF%.vcf.gz}_stats.html"
log_info "Logs: ${LOGS_DIR}/"

echo ""
echo "=============================================================================="
echo "🧬 VEP Master Clinical Pipeline v115 - COMPLETED"
echo "=============================================================================="
echo "✅ Sample: $SAMPLE_ID"
echo "📊 Output: $OUTPUT_VCF"
echo "🎯 Features: REVEL + AlphaMissense + CADD + ClinVar"
echo "📈 2024-2025 Clinical Genomics Gold Standard"
echo "=============================================================================="
