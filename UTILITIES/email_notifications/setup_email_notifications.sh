#!/bin/bash
# Quick Email Notification Setup for Clinical Genomics Pipeline
# Run this script to configure email notifications

set -e

GENOME_BASE="/mnt/d/Genome"
CONFIG_DIR="${GENOME_BASE}/UTILITIES/email_notifications"
SCRIPTS_DIR="${GENOME_BASE}/UTILITIES/email_notifications"

echo "🚀 Email Notification Setup for Clinical Genomics Pipeline"
echo "=========================================================="

# Check if files exist
if [[ ! -f "${SCRIPTS_DIR}/pipeline_notifier.py" ]]; then
    echo "❌ ERROR: pipeline_notifier.py not found!"
    echo "   Expected location: ${SCRIPTS_DIR}/pipeline_notifier.py"
    exit 1
fi

if [[ ! -f "${CONFIG_DIR}/email_config_template.json" ]]; then
    echo "❌ ERROR: email_config_template.json not found!"
    echo "   Expected location: ${CONFIG_DIR}/email_config_template.json"
    exit 1
fi

echo "✅ Required files found"

# Make Python script executable
chmod +x "${SCRIPTS_DIR}/pipeline_notifier.py"

# Check if configuration already exists
if [[ -f "${CONFIG_DIR}/email_config.json" ]]; then
    echo ""
    echo "⚠️  Configuration file already exists: ${CONFIG_DIR}/email_config.json"
    read -p "Do you want to reconfigure? (y/N): " reconfigure
    if [[ ! "${reconfigure,,}" =~ ^y ]]; then
        echo "Keeping existing configuration."
        echo ""
        echo "To test existing setup:"
        echo "python3 ${SCRIPTS_DIR}/pipeline_notifier.py --type vep_completion --sample-id TEST --start-time \"\$(date)\" --config ${CONFIG_DIR}/email_config.json"
        exit 0
    fi
fi

echo ""
echo "📧 EMAIL CONFIGURATION SETUP"
echo "============================"
echo ""
echo "For Gmail (most reliable):"
echo "1. Go to https://myaccount.google.com/security"
echo "2. Enable 2-factor authentication if not already enabled"
echo "3. Go to 'App passwords' and create one:"
echo "   - Select 'Mail' and 'Other (custom name)'"
echo "   - Enter any name (e.g., 'Clinical Genomics Pipeline')"
echo "   - Copy the 16-character password"
echo ""
echo "For other email providers:"
echo "- Outlook: smtp-mail.outlook.com, port 587"
echo "- Yahoo: smtp.mail.yahoo.com, port 587"
echo "- Custom SMTP: enter your server details"
echo ""

# Interactive configuration
read -p "Enter your email address: " email_user
echo ""
echo "Enter your email password:"
echo "(For Gmail: use the 16-character App Password)"
echo "(For others: use your regular password or app password)"
read -p "Password: " -s email_password
echo ""
echo ""

read -p "Enter recipient email address (can be same as sender): " recipient_email

# Ask about SMTP settings
echo ""
read -p "Use Gmail SMTP settings? (Y/n): " use_gmail
if [[ "${use_gmail,,}" =~ ^n ]]; then
    read -p "SMTP server: " smtp_server
    read -p "SMTP port: " smtp_port
else
    smtp_server="smtp.gmail.com"
    smtp_port="587"
fi

# Create configuration file
cat > "${CONFIG_DIR}/email_config.json" << EOF
{
    "smtp_server": "${smtp_server}",
    "smtp_port": ${smtp_port},
    "email_user": "${email_user}",
    "email_password": "${email_password}",
    "recipient_email": "${recipient_email}",
    "sender_name": "Clinical Genomics Pipeline",
    "enable_notifications": true
}
EOF

echo ""
echo "✅ Configuration saved to ${CONFIG_DIR}/email_config.json"

# Test the setup
echo ""
echo "🧪 TESTING EMAIL SETUP"
echo "====================="

read -p "Send test email now? (Y/n): " send_test
if [[ ! "${send_test,,}" =~ ^n ]]; then
    echo ""
    echo "Sending test email..."
    
    if python3 "${SCRIPTS_DIR}/pipeline_notifier.py" \
        --type vep_completion \
        --sample-id "TEST_SAMPLE_$(date +%H%M)" \
        --start-time "$(date -d '3 hours ago')" \
        --end-time "$(date)" \
        --variant-count 1234567 \
        --output-file "/mnt/d/Genome/test_output.vcf.gz" \
        --file-size "1.2G" \
        --config "${CONFIG_DIR}/email_config.json"; then
        
        echo ""
        echo "✅ SUCCESS! Test email sent successfully!"
        echo "   📧 Check your inbox for the test notification."
        echo "   📱 Check spam/junk folder if not in inbox."
    else
        echo ""
        echo "❌ FAILED! Test email could not be sent."
        echo "   Please check your configuration and try again."
        echo ""
        echo "Common issues:"
        echo "   - Wrong App Password (Gmail users)"
        echo "   - 2-factor authentication not enabled (Gmail)"
        echo "   - Network/firewall blocking SMTP"
        echo "   - Incorrect SMTP server/port"
        exit 1
    fi
fi

echo ""
echo "🔧 PIPELINE INTEGRATION"
echo "======================"
echo ""
echo "Next, integrate with your VEP pipeline by adding this to"
echo "your comprehensive_vep_v114.sh script:"
echo ""
echo "--- ADD AFTER INITIAL VARIABLES ---"
cat << 'INTEGRATION_CODE'

# Email notification setup
EMAIL_NOTIFIER="/mnt/d/Genome/scripts/pipeline_notifier.py"
EMAIL_CONFIG="/mnt/d/Genome/config/email_config.json"
EMAIL_ENABLED=true

# Function to send email notification
send_email_notification() {
    local notification_type="$1"
    local sample_id="$2" 
    local start_time="$3"
    local end_time="$4"
    local output_file="$5"
    local file_size="$6"
    local variant_count="$7"
    local error_message="$8"
    
    if [[ "${EMAIL_ENABLED}" == "true" && -f "${EMAIL_NOTIFIER}" ]]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 📧 Sending ${notification_type} notification..."
        python3 "${EMAIL_NOTIFIER}" --type "${notification_type}" \
            --sample-id "${sample_id}" --start-time "${start_time}" \
            --end-time "${end_time}" --output-file "${output_file}" \
            --file-size "${file_size}" --variant-count "${variant_count}" \
            --error-message "${error_message}" --config "${EMAIL_CONFIG}" || {
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  Email notification failed (non-critical)"
        }
    fi
}

INTEGRATION_CODE

echo ""
echo "--- ADD BEFORE VEP EXECUTION ---"
echo 'VEP_START_TIME=$(date)'
echo ""
echo "--- ADD AFTER SUCCESSFUL VEP COMPLETION ---"
cat << 'SUCCESS_CODE'
VEP_END_TIME=$(date)
OUTPUT_SIZE=$(du -h "${OUTPUT_VCF}" | cut -f1)
VARIANT_COUNT=$(zcat "${OUTPUT_VCF}" | grep -v "^#" | wc -l)

send_email_notification "vep_completion" "${SAMPLE_ID}" "${VEP_START_TIME}" "${VEP_END_TIME}" \
                       "${OUTPUT_VCF}" "${OUTPUT_SIZE}" "${VARIANT_COUNT}"
SUCCESS_CODE

echo ""
echo "--- ADD FOR VEP FAILURES ---"
cat << 'FAILURE_CODE'
send_email_notification "vep_failure" "${SAMPLE_ID}" "${VEP_START_TIME}" "$(date)" \
                       "" "" "0" "VEP annotation failed - check logs"
FAILURE_CODE

echo ""
echo "🎉 SETUP COMPLETE!"
echo "================"
echo ""
echo "📁 Files created:"
echo "   ${SCRIPTS_DIR}/pipeline_notifier.py"
echo "   ${CONFIG_DIR}/email_config.json"
echo "   ${CONFIG_DIR}/email_config_template.json"
echo ""
echo "✅ Email notifications are ready!"
echo ""
echo "Next steps:"
echo "1. Integrate the code above into your comprehensive_vep_v114.sh script"
echo "2. Run your pipeline as usual"
echo "3. Walk away and wait for the email! 📧"
echo ""
echo "💡 Pro tip: The email includes beautiful HTML formatting with"
echo "   duration, file size, variant counts, and next steps!"
