// campaign-client.js
class CampaignClient {
    constructor(apiBaseUrl, token) {
        this.apiBaseUrl = apiBaseUrl;
        this.token = token;
    }

    async fetchCampaigns(options = {}) {
        const queryParams = new URLSearchParams({
            platform: options.platform || 'web',
            location: options.location || '',
        }).toString();

        const response = await fetch(
            `${this.apiBaseUrl}/api/v1/marketing-campaigns/?${queryParams}`,
            {
                headers: {
                    'Authorization': `Token ${this.token}`,
                    'Content-Type': 'application/json'
                }
            }
        );

        if (!response.ok) {
            throw new Error('Failed to fetch campaigns');
        }

        return await response.json();
    }
}

// Usage example:
const client = new CampaignClient('http://127.0.0.1:8080/', 'NZX650912mnhtS');

async function displayCampaign() {
    try {
        const campaigns = await client.fetchCampaigns({
            platform: 'web',
            location: 'london'
        });

        if (campaigns.length > 0) {
            const campaign = campaigns[0];
            renderCampaign(campaign);
        }
    } catch (error) {
        console.error('Error fetching campaign:', error);
    }
}

function renderCampaign(campaign) {
    const container = document.getElementById('campaign-container');
    const content = campaign.campaign_content;
    const settings = campaign.campaign_settings;

    // Render based on campaign type
    if (settings.display.type === 'banner') {
        container.innerHTML = `
            <div class="campaign-banner" style="${generateStyles(settings.display.style)}">
                ${renderBlocks(content.blocks)}
            </div>
        `;
    }
    
    // Initialize tracking if enabled
    if (settings.tracking.enabled) {
        initializeTracking(settings.tracking);
    }
}

function generateStyles(styleSettings) {
    return Object.entries(styleSettings)
        .map(([key, value]) => `${key}: ${value}`)
        .join(';');
}

function renderBlocks(blocks) {
    return blocks.map(block => {
        // Render each content block based on its type
        return `<div class="campaign-block">${block.content}</div>`;
    }).join('');
}

function initializeTracking(trackingSettings) {
    trackingSettings.events.forEach(event => {
        // Implement tracking logic
    });
}
