/**
 * AIPA Gmail Labels Creator
 * This Google Apps Script will create all the Gmail labels needed for your AIPA system
 * 
 * Instructions:
 * 1. Go to https://script.google.com
 * 2. Create a new project
 * 3. Replace the default code with this script
 * 4. Save the project (name it "AIPA Gmail Setup")
 * 5. Click the "Run" button to execute createAllLabels()
 * 6. Grant permissions when prompted
 * 7. Check your Gmail - all labels should be created!
 */

function createAllLabels() {
  console.log('🚀 Creating AIPA Gmail Labels...');
  
  // Define all labels with their colors
  const labels = [
    // Main business labels
    { name: 'WoodysCreations', color: 'green' },
    { name: 'DJ-Business', color: 'red' },
    { name: 'BMF-Work', color: 'orange' },
    { name: 'TheTopOdd', color: 'purple' },
    { name: 'Personal', color: 'blue' },
    
    // WoodysCreations sub-labels
    { name: 'WoodysCreations/Urgent', parent: 'WoodysCreations' },
    { name: 'WoodysCreations/Orders', parent: 'WoodysCreations' },
    { name: 'WoodysCreations/Suppliers', parent: 'WoodysCreations' },
    { name: 'WoodysCreations/Customers', parent: 'WoodysCreations' },
    { name: 'WoodysCreations/Processed', parent: 'WoodysCreations' },
    { name: 'WoodysCreations/AwaitingReply', parent: 'WoodysCreations' },
    
    // DJ-Business sub-labels
    { name: 'DJ-Business/Urgent', parent: 'DJ-Business' },
    { name: 'DJ-Business/Bookings', parent: 'DJ-Business' },
    { name: 'DJ-Business/Inquiries', parent: 'DJ-Business' },
    { name: 'DJ-Business/Contracts', parent: 'DJ-Business' },
    { name: 'DJ-Business/Processed', parent: 'DJ-Business' },
    { name: 'DJ-Business/AwaitingReply', parent: 'DJ-Business' },
    
    // BMF-Work sub-labels
    { name: 'BMF-Work/Urgent', parent: 'BMF-Work' },
    { name: 'BMF-Work/Projects', parent: 'BMF-Work' },
    { name: 'BMF-Work/Timesheets', parent: 'BMF-Work' },
    { name: 'BMF-Work/Processed', parent: 'BMF-Work' },
    { name: 'BMF-Work/AwaitingReply', parent: 'BMF-Work' },
    
    // TheTopOdd sub-labels
    { name: 'TheTopOdd/Urgent', parent: 'TheTopOdd' },
    { name: 'TheTopOdd/Licensing', parent: 'TheTopOdd' },
    { name: 'TheTopOdd/Suppliers', parent: 'TheTopOdd' },
    { name: 'TheTopOdd/Processed', parent: 'TheTopOdd' },
    { name: 'TheTopOdd/AwaitingReply', parent: 'TheTopOdd' },
    
    // Personal sub-labels
    { name: 'Personal/Urgent', parent: 'Personal' },
    { name: 'Personal/Family', parent: 'Personal' },
    { name: 'Personal/Bills', parent: 'Personal' },
    { name: 'Personal/Processed', parent: 'Personal' },
    { name: 'Personal/AwaitingReply', parent: 'Personal' }
  ];
  
  let createdCount = 0;
  let existingCount = 0;
  
  labels.forEach(labelConfig => {
    try {
      // Check if label already exists
      const existingLabels = Gmail.Users.Labels.list('me').labels;
      const exists = existingLabels.some(label => label.name === labelConfig.name);
      
      if (exists) {
        console.log(`✓ Label "${labelConfig.name}" already exists`);
        existingCount++;
        return;
      }
      
      // Create the label
      const labelResource = {
        name: labelConfig.name,
        labelListVisibility: 'labelShow',
        messageListVisibility: 'show'
      };
      
      // Add color if specified (for main labels)
      if (labelConfig.color) {
        const colorMap = {
          'green': '#0b8043',
          'red': '#d93025',
          'orange': '#f29900',
          'purple': '#8430ce',
          'blue': '#1a73e8'
        };
        labelResource.color = {
          backgroundColor: colorMap[labelConfig.color] || '#0b8043'
        };
      }
      
      Gmail.Users.Labels.create(labelResource, 'me');
      console.log(`✅ Created label: ${labelConfig.name}`);
      createdCount++;
      
    } catch (error) {
      console.error(`❌ Error creating label "${labelConfig.name}": ${error.message}`);
    }
  });
  
  console.log(`\n🎉 Gmail Labels Setup Complete!`);
  console.log(`📊 Summary:`);
  console.log(`   ✅ Created: ${createdCount} labels`);
  console.log(`   ↩️  Already existed: ${existingCount} labels`);
  console.log(`   📧 Total labels: ${labels.length}`);
  console.log(`\n🔍 Next steps:`);
  console.log(`   1. Check your Gmail to see all the new labels`);
  console.log(`   2. Continue with your AIPA setup`);
  console.log(`   3. Run getLabelIds() to get the label IDs for n8n`);
}

/**
 * Get all label IDs for n8n configuration
 * Run this after creating labels to get the IDs needed for n8n
 */
function getLabelIds() {
  console.log('📋 Getting Gmail Label IDs for n8n...\n');
  
  const labels = Gmail.Users.Labels.list('me').labels;
  const businessLabels = labels.filter(label => 
    label.name.includes('WoodysCreations') ||
    label.name.includes('DJ-Business') ||
    label.name.includes('BMF-Work') ||
    label.name.includes('TheTopOdd') ||
    label.name.includes('Personal')
  );
  
  console.log('📋 Copy these Label IDs for your n8n configuration:');
  console.log('=' * 60);
  
  businessLabels.forEach(label => {
    console.log(`${label.name}: ${label.id}`);
  });
  
  console.log('\n💾 Save these IDs - you\'ll need them for n8n setup!');
}

/**
 * Test function to verify Gmail API access
 */
function testGmailAccess() {
  try {
    const labels = Gmail.Users.Labels.list('me');
    console.log(`✅ Gmail API access works! Found ${labels.labels.length} existing labels.`);
  } catch (error) {
    console.error(`❌ Gmail API access failed: ${error.message}`);
  }
}