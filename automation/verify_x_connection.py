import sys
import os

# Add the current directory to sys.path to ensure we can import sns_client
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sns_client import SNSClient

def verify_connection():
    print("Initializing SNSClient...")
    client = SNSClient()
    
    if not client.x_client:
        print("Error: X Client failed to initialize. Check .env variables.")
        return

    print("Attempting to fetch authenticated user details (get_me)...")
    try:
        # get_me() fetches the authenticated user's information
        user_response = client.x_client.get_me()
        
        if user_response.data:
            user = user_response.data
            print("\n✅ Verification Successful!")
            print(f"Connected as: {user.name} (@{user.username})")
            print(f"User ID: {user.id}")
        else:
            print("❌ Verification Failed: No user data returned.")
            
    except Exception as e:
        print(f"❌ Verification Failed: {str(e)}")
        print("Please check your API Keys, Secrets, and Tokens in .env")

if __name__ == "__main__":
    verify_connection()
