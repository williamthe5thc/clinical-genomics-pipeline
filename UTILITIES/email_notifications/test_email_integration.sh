#!/bin/bash
# Test Email Integration for Clinical Genomics Pipeline
# Quick test to verify email notifications are working

BASE_DIR="/mnt/d/Genome"
EMAIL_NOTIFIER="${BASE_DIR}/UTILITIES/email_notifications/pipeline_notifier.py"
EMAIL_CONFIG="${BASE_DIR}/UTILITIES/email_notifications/email_config.json"

echo "🧪 Testing Email Integration for Clinical Genomics Pipeline"
echo "=========================================================="

# Check if email notifier exists
if [[ ! -f "$EMAIL_NOTIFIER" ]]; then
    echo "❌ ERROR: Email notifier not found: $EMAIL_NOTIFIER"
    exit 1
fi

# Check if email config exists
if [[ ! -f "$EMAIL_CONFIG" ]]; then
    echo "❌ ERROR: Email config not found: $EMAIL_CONFIG"
    echo "   Run: bash ${BASE_DIR}/UTILITIES/email_notifications/setup_email_notifications.sh"
    exit 1
fi

echo "✅ Email notifier found: $EMAIL_NOTIFIER"
echo "✅ Email config found: $EMAIL_CONFIG"
echo ""

# Test VEP completion notification
echo "📧 Testing VEP completion notification..."
if python3 "$EMAIL_NOTIFIER" \
    --type vep_completion \
    --sample-id "INTEGRATION_TEST_$(date +%H%M)" \
    --start-time "$(date -d '2 hours ago')" \
    --end-time "$(date)" \
    --output-file "/mnt/d/Genome/test_results/sample_annotated.vcf.gz" \
    --file-size "1.4G" \
    --variant-count 2500000 \
    --config "$EMAIL_CONFIG"; then
    
    echo "✅ VEP completion notification sent successfully!"
else
    echo "❌ VEP completion notification failed!"
    exit 1
fi

echo ""

# Test VEP failure notification
echo "📧 Testing VEP failure notification..."
if python3 "$EMAIL_NOTIFIER" \
    --type vep_failure \
    --sample-id "INTEGRATION_TEST_FAIL_$(date +%H%M)" \
    --start-time "$(date -d '1 hour ago')" \
    --end-time "$(date)" \
    --variant-count 0 \
    --error-message "Test error message - VEP annotation failed due to memory limitations" \
    --config "$EMAIL_CONFIG"; then
    
    echo "✅ VEP failure notification sent successfully!"
else
    echo "❌ VEP failure notification failed!"
    exit 1
fi

echo ""
echo "🎉 EMAIL INTEGRATION TEST COMPLETED!"
echo "=================================================="
echo ""
echo "✅ Both VEP completion and failure notifications are working"
echo "📧 Check your email inbox for the test notifications"
echo "🚀 Your pipeline is ready for email notifications!"
echo ""
echo "Next steps:"
echo "1. Run your pipeline as usual with: bash clinical_genomics_pipeline.sh single ..."
echo "2. Walk away and wait for email notifications!"
echo "3. VEP completion emails will arrive after ~3 hours"
echo "4. Pipeline completion emails will arrive when everything finishes"
