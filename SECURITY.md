# 🔒 Security Guidelines for CineScope

## API Key Management

### ❌ NEVER Do This
```python
# DO NOT hardcode API keys in code!
OPENAI_API_KEY = "sk-proj-xxxxx"  # WRONG!
```

### ✅ Correct Way to Handle API Keys

#### 1. Create a .env file (locally only)
```bash
# In project root, create .env file
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

#### 2. Load environment variables in Python
```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use the key
api_key = os.getenv('OPENAI_API_KEY')
```

#### 3. Install python-dotenv
```bash
pip install python-dotenv
```

## What's Already Protected

✅ `.env` files are in `.gitignore` - they won't be committed  
✅ `.env.example` shows the format without real keys  
✅ No API keys in source code

## If You Accidentally Exposed a Key

**Immediate Steps:**
1. **Revoke the key** at https://platform.openai.com/api-keys
2. **Generate a new key** (keep it secret!)
3. **Update your local .env file** with the new key
4. **Never share the key** in chat, email, or any public place

## GitHub Repository Security

Before pushing changes:
```bash
# Check what files will be committed
git status

# Make sure .env is NOT listed!
# .gitignore should prevent this

# If .env appears, run:
git reset HEAD .env
```

## Environment Variables for Production

For deployment (Heroku, AWS, etc.):
- Use their environment variable settings
- Never commit production keys
- Use different keys for development and production

## Best Practices

1. ✅ Use `.env` files for local development
2. ✅ Keep `.env` in `.gitignore`
3. ✅ Share `.env.example` (template only)
4. ✅ Rotate API keys regularly
5. ✅ Use different keys for different environments
6. ❌ Never hardcode secrets in code
7. ❌ Never commit `.env` files
8. ❌ Never share keys in screenshots or chat

## Current Project Status

🔒 **Protected**: Your repository is configured to ignore sensitive files  
⚠️ **Action Required**: Revoke any keys you've shared publicly  
✅ **Safe**: Follow this guide for future API key usage

---

**Remember**: An exposed API key can lead to unauthorized usage and charges on your account!
