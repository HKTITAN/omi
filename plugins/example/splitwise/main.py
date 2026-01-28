"""
Splitwise Integration for Omi

This plugin enables Omi to interact with Splitwise for expense management
and bill-splitting functionality via Chat Tools.

Features:
- Add expenses to Splitwise groups from conversations
- Check balances with friends
- Create expense splits based on conversation context
- Get a summary of debts and credits

The plugin extracts expense information from conversations and allows
users to add them to Splitwise via natural language commands in Omi chat.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os

router = APIRouter(prefix="/splitwise", tags=["splitwise"])

# Splitwise API client placeholder
# In production, use the official splitwise SDK: pip install splitwise
SPLITWISE_API_KEY = os.getenv("SPLITWISE_API_KEY", "")
SPLITWISE_API_SECRET = os.getenv("SPLITWISE_API_SECRET", "")


class AddExpenseRequest(BaseModel):
    """Request model for adding an expense to Splitwise."""

    uid: str
    app_id: str
    tool_name: str
    description: str
    amount: float
    currency: Optional[str] = "USD"
    group_name: Optional[str] = None
    split_with: Optional[List[str]] = None  # List of friend names or emails
    paid_by: Optional[str] = None  # "me" or friend name


class GetBalanceRequest(BaseModel):
    """Request model for getting balance with a friend."""

    uid: str
    app_id: str
    tool_name: str
    friend_name: Optional[str] = None  # If None, get all balances


class CreateGroupRequest(BaseModel):
    """Request model for creating a Splitwise group."""

    uid: str
    app_id: str
    tool_name: str
    group_name: str
    members: List[str]  # List of friend emails


class ToolResponse(BaseModel):
    """Standard response model for chat tools."""

    result: Optional[str] = None
    error: Optional[str] = None


def get_user_splitwise_token(uid: str) -> Optional[str]:
    """
    Retrieve the Splitwise OAuth token for a user from the database.

    In production, this should query your secure database.
    """
    # TODO: Implement actual token storage/retrieval
    # This would integrate with the OAuth flow from oauth/splitwise.py
    return None


def validate_splitwise_connection(uid: str) -> Optional[str]:
    """
    Check if user has connected their Splitwise account.
    Returns error message if not connected, None if connected.
    """
    token = get_user_splitwise_token(uid)
    if not token:
        return "Splitwise account not connected. " "Please connect your Splitwise account in the app settings."
    return None


@router.post("/add-expense", response_model=ToolResponse)
async def add_expense(request: AddExpenseRequest):
    """
    Add an expense to Splitwise.

    This tool is called when users say things like:
    - "Add a $50 expense for dinner to Splitwise"
    - "Split the $100 grocery bill with John"
    - "Add expense for coffee $12.50"
    """
    # Validate connection
    connection_error = validate_splitwise_connection(request.uid)
    if connection_error:
        return ToolResponse(error=connection_error)

    # Validate amount
    if request.amount <= 0:
        return ToolResponse(error="Expense amount must be greater than zero")

    if not request.description:
        return ToolResponse(error="Please provide a description for the expense")

    try:
        # TODO: Implement actual Splitwise API call
        # from splitwise import Splitwise
        # sw = Splitwise(SPLITWISE_API_KEY, SPLITWISE_API_SECRET, access_token=token)
        # expense = Expense()
        # expense.setDescription(request.description)
        # expense.setCost(str(request.amount))
        # ...
        # sw.createExpense(expense)

        # Placeholder response
        split_info = ""
        if request.split_with:
            split_info = f" split with {', '.join(request.split_with)}"
        if request.group_name:
            split_info += f" in group '{request.group_name}'"

        return ToolResponse(result=f"Added expense: {request.description} for ${request.amount:.2f}{split_info}")

    except Exception as e:
        return ToolResponse(error=f"Failed to add expense: {str(e)}")


@router.post("/get-balance", response_model=ToolResponse)
async def get_balance(request: GetBalanceRequest):
    """
    Get balance information from Splitwise.

    This tool is called when users say things like:
    - "What's my Splitwise balance?"
    - "How much do I owe John?"
    - "Who owes me money?"
    """
    # Validate connection
    connection_error = validate_splitwise_connection(request.uid)
    if connection_error:
        return ToolResponse(error=connection_error)

    try:
        # TODO: Implement actual Splitwise API call
        # from splitwise import Splitwise
        # sw = Splitwise(SPLITWISE_API_KEY, SPLITWISE_API_SECRET, access_token=token)
        # friends = sw.getFriends()
        # ...

        # Placeholder response
        if request.friend_name:
            return ToolResponse(
                result=f"Balance with {request.friend_name}: You owe $0.00 (placeholder - connect Splitwise to see actual balance)"
            )
        else:
            return ToolResponse(
                result="Overall balance: You are settled up! (placeholder - connect Splitwise to see actual balance)"
            )

    except Exception as e:
        return ToolResponse(error=f"Failed to get balance: {str(e)}")


@router.post("/list-groups", response_model=ToolResponse)
async def list_groups(request: GetBalanceRequest):
    """
    List all Splitwise groups for the user.

    This tool is called when users say things like:
    - "What Splitwise groups do I have?"
    - "List my expense groups"
    """
    # Validate connection
    connection_error = validate_splitwise_connection(request.uid)
    if connection_error:
        return ToolResponse(error=connection_error)

    try:
        # TODO: Implement actual Splitwise API call
        # from splitwise import Splitwise
        # sw = Splitwise(SPLITWISE_API_KEY, SPLITWISE_API_SECRET, access_token=token)
        # groups = sw.getGroups()
        # ...

        # Placeholder response
        return ToolResponse(result="Your Splitwise groups:\n- (Connect Splitwise to see your groups)")

    except Exception as e:
        return ToolResponse(error=f"Failed to list groups: {str(e)}")


@router.post("/create-group", response_model=ToolResponse)
async def create_group(request: CreateGroupRequest):
    """
    Create a new Splitwise group.

    This tool is called when users say things like:
    - "Create a Splitwise group called 'Vacation' with John and Jane"
    - "Make a new expense group for the roommates"
    """
    # Validate connection
    connection_error = validate_splitwise_connection(request.uid)
    if connection_error:
        return ToolResponse(error=connection_error)

    if not request.group_name:
        return ToolResponse(error="Please provide a name for the group")

    try:
        # TODO: Implement actual Splitwise API call
        # from splitwise import Splitwise, Group
        # sw = Splitwise(SPLITWISE_API_KEY, SPLITWISE_API_SECRET, access_token=token)
        # group = Group()
        # group.setName(request.group_name)
        # ...
        # sw.createGroup(group)

        members_str = ""
        if request.members:
            members_str = f" with members: {', '.join(request.members)}"

        return ToolResponse(
            result=f"Created Splitwise group '{request.group_name}'{members_str} (placeholder - connect Splitwise)"
        )

    except Exception as e:
        return ToolResponse(error=f"Failed to create group: {str(e)}")


@router.get("/.well-known/omi-tools.json")
async def get_omi_tools_manifest():
    """
    Return the Omi chat tools manifest for Splitwise integration.

    This endpoint is used by Omi to discover available chat tools
    when the app is registered.
    """
    return {
        "tools": [
            {
                "name": "add_splitwise_expense",
                "description": (
                    "Add an expense to Splitwise. Use this when the user wants to "
                    "record a shared expense, split a bill, or add costs that need to "
                    "be divided among friends or group members. Requires: description and amount. "
                    "Optional: currency, group_name, split_with (list of people), paid_by."
                ),
                "endpoint": "/splitwise/add-expense",
                "method": "POST",
                "parameters": {
                    "properties": {
                        "description": {
                            "type": "string",
                            "description": "Description of the expense (e.g., 'Dinner at restaurant', 'Groceries')",
                        },
                        "amount": {"type": "number", "description": "The expense amount in the specified currency"},
                        "currency": {
                            "type": "string",
                            "description": "Currency code (default: USD). Examples: USD, EUR, GBP",
                        },
                        "group_name": {
                            "type": "string",
                            "description": "Name of the Splitwise group to add the expense to",
                        },
                        "split_with": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of friend names or emails to split with",
                        },
                        "paid_by": {
                            "type": "string",
                            "description": "Who paid for the expense: 'me' or a friend's name",
                        },
                    },
                    "required": ["description", "amount"],
                },
                "auth_required": True,
                "status_message": "Adding expense to Splitwise...",
            },
            {
                "name": "get_splitwise_balance",
                "description": (
                    "Get balance information from Splitwise. Use this when the user wants "
                    "to know how much they owe or are owed, check balances with specific friends, "
                    "or get an overview of their debts and credits."
                ),
                "endpoint": "/splitwise/get-balance",
                "method": "POST",
                "parameters": {
                    "properties": {
                        "friend_name": {
                            "type": "string",
                            "description": "Optional friend name to check balance with. If not provided, returns overall balance.",
                        }
                    },
                    "required": [],
                },
                "auth_required": True,
                "status_message": "Checking Splitwise balance...",
            },
            {
                "name": "list_splitwise_groups",
                "description": (
                    "List all Splitwise groups the user is a member of. Use this when "
                    "the user wants to see their expense groups or find a group to add an expense to."
                ),
                "endpoint": "/splitwise/list-groups",
                "method": "POST",
                "parameters": {"properties": {}, "required": []},
                "auth_required": True,
                "status_message": "Fetching Splitwise groups...",
            },
            {
                "name": "create_splitwise_group",
                "description": (
                    "Create a new Splitwise group. Use this when the user wants to "
                    "create a new expense group for tracking shared costs with friends, "
                    "roommates, or for a specific event like a vacation."
                ),
                "endpoint": "/splitwise/create-group",
                "method": "POST",
                "parameters": {
                    "properties": {
                        "group_name": {
                            "type": "string",
                            "description": "Name for the new group (e.g., 'Roommates', 'Vacation 2024')",
                        },
                        "members": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of friend emails to add to the group",
                        },
                    },
                    "required": ["group_name"],
                },
                "auth_required": True,
                "status_message": "Creating Splitwise group...",
            },
        ]
    }
