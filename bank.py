import json
import random
import string
from pathlib import Path
from typing import Optional, Dict, Any, List

DATA_FILE = Path("data.json")


class Bank:
    """
    Simple bank backend that stores accounts in a JSON file.
    Each account is a dict:
      {
        "Name": str,
        "Age": int,
        "Address": str,
        "Mobile Number": str,   # store as string for leading zeros
        "Father's / Husband's Name": str,
        "Pin": str,             # store as string to preserve leading zeros
        "Account Number": str,
        "Balance": float
      }
    """

    data: List[Dict[str, Any]] = []

    # load data at import
    try:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
    except Exception as e:
        print("Error loading database:", e)
        data = []

    @classmethod
    def _save(cls) -> None:
        """Persist current data to the JSON file."""
        try:
            with DATA_FILE.open("w", encoding="utf-8") as f:
                json.dump(cls.data, f, indent=2)
        except Exception as e:
            print("Error saving database:", e)
            raise

    @classmethod
    def _generate_account_number(cls) -> str:
        """Generate a unique account number: 10 chars mixed uppercase letters+digits."""
        while True:
            parts = random.choices(string.ascii_uppercase + string.digits, k=10)
            acc = "".join(parts)
            if not any(acc == a["Account Number"] for a in cls.data):
                return acc

    @classmethod
    def _find_user(cls, account_number: str, pin: str) -> Optional[Dict[str, Any]]:
        """Return user dict or None."""
        for acc in cls.data:
            if acc["Account Number"] == account_number and acc["Pin"] == pin:
                return acc
        return None

    @classmethod
    def create_account(
        cls,
        name: str,
        age: int,
        address: str,
        mobile_number: str,
        father_or_husband: str,
        pin: str,
    ) -> Dict[str, Any]:
        """Create and return account dict. Raises ValueError on invalid input."""
        # validations
        if age < 18:
            raise ValueError("Account holder must be at least 18 years old.")
        if not (pin.isdigit() and len(pin) == 4):
            raise ValueError("Pin must be exactly 4 digits.")
        if not (mobile_number.isdigit() and len(mobile_number) == 10):
            raise ValueError("Mobile number must be exactly 10 digits.")

        account = {
            "Name": name.strip(),
            "Age": age,
            "Address": address.strip(),
            "Mobile Number": mobile_number,
            "Father's / Husband's Name": father_or_husband.strip(),
            "Pin": pin,
            "Account Number": cls._generate_account_number(),
            "Balance": 0.0,
        }

        cls.data.append(account)
        cls._save()
        return account

    @classmethod
    def deposit(cls, account_number: str, pin: str, amount: float) -> float:
        """
        Deposit amount to account. Returns new balance.
        Raises ValueError for invalid amount or if account not found.
        """
        if amount <= 0 or amount > 10000:
            raise ValueError("Amount should be > 0 and <= 10000.")

        user = cls._find_user(account_number, pin)
        if user is None:
            raise ValueError("No account found with provided credentials.")

        user["Balance"] = float(user.get("Balance", 0.0)) + float(amount)
        cls._save()
        return user["Balance"]

    @classmethod
    def withdraw(cls, account_number: str, pin: str, amount: float) -> float:
        """
        Withdraw amount from account. Returns new balance.
        Raises ValueError for invalid amount / insufficient funds / no account.
        """
        if amount <= 0 or amount > 10000:
            raise ValueError("Amount should be > 0 and <= 10000.")

        user = cls._find_user(account_number, pin)
        if user is None:
            raise ValueError("No account found with provided credentials.")

        current_balance = float(user.get("Balance", 0.0))
        if amount > current_balance:
            raise ValueError("Insufficient balance.")

        user["Balance"] = current_balance - amount
        cls._save()
        return user["Balance"]

    @classmethod
    def get_details(cls, account_number: str, pin: str) -> Dict[str, Any]:
        """Return user details dictionary (copy to avoid accidental edits)."""
        user = cls._find_user(account_number, pin)
        if user is None:
            raise ValueError("No account found with provided credentials.")
        # return a shallow copy
        return dict(user)

    @classmethod
    def update_details(
        cls,
        account_number: str,
        pin: str,
        *,
        name: Optional[str] = None,
        address: Optional[str] = None,
        mobile_number: Optional[str] = None,
        father_or_husband: Optional[str] = None,
        new_pin: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update allowed fields and return updated record. Validates mobile+pin if provided."""
        user = cls._find_user(account_number, pin)
        if user is None:
            raise ValueError("No account found with provided credentials.")

        if name is not None:
            user["Name"] = name.strip()
        if address is not None:
            user["Address"] = address.strip()
        if mobile_number is not None:
            if not (mobile_number.isdigit() and len(mobile_number) == 10):
                raise ValueError("Mobile number must be exactly 10 digits.")
            user["Mobile Number"] = mobile_number
        if father_or_husband is not None:
            user["Father's / Husband's Name"] = father_or_husband.strip()
        if new_pin is not None:
            if not (new_pin.isdigit() and len(new_pin) == 4):
                raise ValueError("Pin must be exactly 4 digits.")
            user["Pin"] = new_pin

        cls._save()
        return dict(user)

    @classmethod
    def delete_account(cls, account_number: str, pin: str) -> None:
        """Delete account; raises ValueError if not found."""
        user = cls._find_user(account_number, pin)
        if user is None:
            raise ValueError("No account found with provided credentials.")
        cls.data.remove(user)
        cls._save()
