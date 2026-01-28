# Splitwise Integration for Omi

This plugin enables Omi to interact with Splitwise for expense management and bill-splitting functionality.

## Features

- **Add Expenses**: Record shared expenses directly from conversations
  - "Add a $50 expense for dinner to Splitwise"
  - "Split the grocery bill with John and Jane"
  
- **Check Balances**: Query your debts and credits
  - "What's my Splitwise balance?"
  - "How much do I owe Sarah?"
  
- **Manage Groups**: Create and list expense groups
  - "Create a Splitwise group for our vacation"
  - "What groups do I have on Splitwise?"

## Setup

### 1. Register a Splitwise Application

1. Go to [Splitwise Developer Portal](https://secure.splitwise.com/apps)
2. Create a new application
3. Note your API Key and Secret

### 2. Configure Environment Variables

Add to your `.env` file:

```env
SPLITWISE_API_KEY=your_api_key
SPLITWISE_API_SECRET=your_api_secret
```

### 3. Register the Plugin in main.py

Add to `plugins/example/main.py`:

```python
from splitwise import main as splitwise_router
from splitwise import oauth as splitwise_oauth_router

app.include_router(splitwise_router.router)
app.include_router(splitwise_oauth_router.router)
```

### 4. Create Omi App

In the Omi mobile app:
1. Go to Explore → Create App
2. Select "External Integration" capability
3. Set Home URL to your server URL
4. Set Chat Tools Manifest URL to: `https://your-server.com/splitwise/.well-known/omi-tools.json`
5. Enable OAuth and set Setup URL to: `https://your-server.com/splitwise/oauth/setup`

## Architecture

```
splitwise/
├── __init__.py       # Package exports
├── main.py           # Chat tools implementation
├── oauth.py          # OAuth authentication flow
└── README.md         # This file
```

## API Endpoints

### Chat Tools

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/splitwise/add-expense` | POST | Add an expense |
| `/splitwise/get-balance` | POST | Get balance info |
| `/splitwise/list-groups` | POST | List user's groups |
| `/splitwise/create-group` | POST | Create a new group |
| `/splitwise/.well-known/omi-tools.json` | GET | Tools manifest |

### OAuth

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/splitwise/oauth/setup` | GET | OAuth setup page |
| `/splitwise/oauth/callback` | GET | OAuth callback |
| `/splitwise/oauth/status` | GET | Check connection |
| `/splitwise/oauth/disconnect` | POST | Disconnect account |

## Usage Examples

Once connected, users can interact with Splitwise through natural language:

### Adding Expenses
```
User: "Add a $30 lunch expense to Splitwise, split with Mike"
Omi: "Added expense: lunch for $30.00 split with Mike"
```

### Checking Balances
```
User: "How much do I owe on Splitwise?"
Omi: "Your overall balance: You owe $45.50 total
       - John: You owe $25.00
       - Sarah: She owes you $10.50
       - Apartment group: You owe $31.00"
```

### Managing Groups
```
User: "Create a Splitwise group called 'Road Trip' with john@email.com and jane@email.com"
Omi: "Created Splitwise group 'Road Trip' with members: john@email.com, jane@email.com"
```

## Security Notes

- OAuth tokens are stored securely per-user
- All API calls require valid user authentication
- Tokens should be encrypted at rest in production

## Dependencies

Add to `requirements.txt`:
```
splitwise>=2.0.0
```

## Future Enhancements

- [ ] Expense receipt image processing from Omi photos
- [ ] Automatic expense extraction from conversation transcripts
- [ ] Memory trigger for expense-related conversations
- [ ] Recurring expense support
- [ ] Multi-currency support with conversion
