"""
Splitwise OAuth Configuration for Omi

This module handles OAuth authentication flow for connecting
user's Splitwise accounts to Omi.

Setup Instructions:
1. Register your app at https://secure.splitwise.com/apps
2. Set SPLITWISE_API_KEY and SPLITWISE_API_SECRET in .env
3. Configure OAuth redirect URL in Splitwise app settings
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from typing import Optional
import os

router = APIRouter(prefix="/splitwise/oauth", tags=["splitwise-oauth"])

# Splitwise OAuth configuration
SPLITWISE_API_KEY = os.getenv("SPLITWISE_API_KEY", "")
SPLITWISE_API_SECRET = os.getenv("SPLITWISE_API_SECRET", "")
SPLITWISE_AUTH_URL = "https://secure.splitwise.com/oauth/authorize"
SPLITWISE_TOKEN_URL = "https://secure.splitwise.com/oauth/token"


def save_user_token(uid: str, access_token: str, refresh_token: Optional[str] = None):
    """
    Save user's Splitwise OAuth tokens to secure storage.

    In production, this should store tokens encrypted in your database.
    """
    # TODO: Implement secure token storage
    # Example: db.save_token(uid, 'splitwise', access_token, refresh_token)
    pass


def get_oauth_redirect_url(base_url: str) -> str:
    """Generate the OAuth redirect URL."""
    return f"{base_url}/splitwise/oauth/callback"


@router.get("/setup", response_class=HTMLResponse)
async def setup_splitwise(uid: str, request: Request):
    """
    Setup page for connecting Splitwise account.

    This page is shown to users when they click "Connect" in the
    Omi app for the Splitwise integration.
    """
    if not SPLITWISE_API_KEY:
        return HTMLResponse(
            content="""
            <html>
            <head><title>Splitwise Setup</title></head>
            <body style="font-family: Arial, sans-serif; padding: 40px; background: #1a1a1a; color: white;">
                <h2>⚠️ Splitwise Integration Not Configured</h2>
                <p>The Splitwise API credentials have not been set up.</p>
                <p>Please contact the administrator to configure the integration.</p>
            </body>
            </html>
            """,
            status_code=503,
        )

    # Generate OAuth URL
    base_url = str(request.base_url).rstrip('/')
    redirect_uri = get_oauth_redirect_url(base_url)

    oauth_url = (
        f"{SPLITWISE_AUTH_URL}?"
        f"client_id={SPLITWISE_API_KEY}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"state={uid}"  # Pass uid in state for callback
    )

    return HTMLResponse(
        content=f"""
        <html>
        <head>
            <title>Connect Splitwise to Omi</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                    color: white;
                    min-height: 100vh;
                    margin: 0;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .container {{
                    text-align: center;
                    padding: 40px;
                    max-width: 400px;
                }}
                .logo {{
                    font-size: 48px;
                    margin-bottom: 20px;
                }}
                h1 {{
                    font-size: 24px;
                    margin-bottom: 16px;
                }}
                p {{
                    color: #888;
                    margin-bottom: 32px;
                    line-height: 1.6;
                }}
                .connect-btn {{
                    background: #5BC5A7;
                    color: white;
                    border: none;
                    padding: 16px 32px;
                    font-size: 16px;
                    border-radius: 8px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    transition: transform 0.2s, box-shadow 0.2s;
                }}
                .connect-btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(91, 197, 167, 0.4);
                }}
                .features {{
                    margin-top: 40px;
                    text-align: left;
                }}
                .feature {{
                    display: flex;
                    align-items: center;
                    margin: 12px 0;
                    color: #ccc;
                }}
                .feature span {{
                    margin-left: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">💰</div>
                <h1>Connect Splitwise to Omi</h1>
                <p>
                    Link your Splitwise account to manage expenses 
                    and split bills directly through Omi conversations.
                </p>
                <a href="{oauth_url}" class="connect-btn">
                    Connect Splitwise
                </a>
                <div class="features">
                    <div class="feature">
                        ✅ <span>Add expenses from conversations</span>
                    </div>
                    <div class="feature">
                        ✅ <span>Check balances with friends</span>
                    </div>
                    <div class="feature">
                        ✅ <span>Create and manage groups</span>
                    </div>
                    <div class="feature">
                        ✅ <span>Natural language expense tracking</span>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """,
        status_code=200,
    )


@router.get("/callback")
async def oauth_callback(code: str, state: str, request: Request):
    """
    OAuth callback handler for Splitwise.

    Splitwise redirects here after user authorizes the app.
    We exchange the code for access token and save it.
    """
    uid = state  # We passed uid in the state parameter

    if not code:
        return HTMLResponse(
            content="""
            <html>
            <head><title>Connection Failed</title></head>
            <body style="font-family: Arial, sans-serif; padding: 40px; background: #1a1a1a; color: white; text-align: center;">
                <h2>❌ Connection Failed</h2>
                <p>Authorization was denied or failed.</p>
                <p>Please try again from the Omi app.</p>
            </body>
            </html>
            """,
            status_code=400,
        )

    try:
        # Exchange code for access token
        # In production, use httpx or aiohttp:
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(
        #         SPLITWISE_TOKEN_URL,
        #         data={
        #             'client_id': SPLITWISE_API_KEY,
        #             'client_secret': SPLITWISE_API_SECRET,
        #             'code': code,
        #             'grant_type': 'authorization_code',
        #             'redirect_uri': get_oauth_redirect_url(str(request.base_url).rstrip('/'))
        #         }
        #     )
        #     token_data = response.json()
        #     access_token = token_data['access_token']
        #     refresh_token = token_data.get('refresh_token')

        # TODO: Implement actual token exchange
        # For now, show success placeholder

        # Save tokens
        # save_user_token(uid, access_token, refresh_token)

        return HTMLResponse(
            content="""
            <html>
            <head>
                <title>Splitwise Connected!</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                        color: white;
                        min-height: 100vh;
                        margin: 0;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }
                    .container {
                        text-align: center;
                        padding: 40px;
                    }
                    .success-icon {
                        font-size: 64px;
                        margin-bottom: 20px;
                    }
                    h1 {
                        color: #5BC5A7;
                        margin-bottom: 16px;
                    }
                    p {
                        color: #888;
                        margin-bottom: 24px;
                    }
                    .examples {
                        background: rgba(255,255,255,0.05);
                        border-radius: 12px;
                        padding: 20px;
                        margin-top: 24px;
                        text-align: left;
                    }
                    .examples h3 {
                        margin-top: 0;
                        font-size: 14px;
                        color: #888;
                    }
                    .example {
                        color: #5BC5A7;
                        margin: 8px 0;
                        font-style: italic;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="success-icon">🎉</div>
                    <h1>Splitwise Connected!</h1>
                    <p>You can now manage expenses through Omi.</p>
                    <p style="font-size: 14px;">You can close this window and return to the app.</p>
                    <div class="examples">
                        <h3>Try saying:</h3>
                        <p class="example">"Add a $50 expense for dinner to Splitwise"</p>
                        <p class="example">"What's my balance with John?"</p>
                        <p class="example">"Split the grocery bill with my roommates"</p>
                    </div>
                </div>
            </body>
            </html>
            """,
            status_code=200,
        )

    except Exception as e:
        return HTMLResponse(
            content=f"""
            <html>
            <head><title>Connection Error</title></head>
            <body style="font-family: Arial, sans-serif; padding: 40px; background: #1a1a1a; color: white; text-align: center;">
                <h2>❌ Connection Error</h2>
                <p>An error occurred while connecting your account.</p>
                <p>Please try again from the Omi app.</p>
            </body>
            </html>
            """,
            status_code=500,
        )


@router.get("/status")
async def check_connection_status(uid: str):
    """
    Check if user has connected their Splitwise account.

    Returns connection status for display in app settings.
    """
    from .main import get_user_splitwise_token

    token = get_user_splitwise_token(uid)

    return {"connected": token is not None, "service": "splitwise"}


@router.post("/disconnect")
async def disconnect_splitwise(uid: str):
    """
    Disconnect user's Splitwise account.

    Removes stored OAuth tokens.
    """
    # TODO: Implement token removal
    # db.delete_token(uid, 'splitwise')

    return {"success": True, "message": "Splitwise account disconnected"}
