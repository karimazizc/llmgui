#!/usr/bin/env python3
"""
Test script for the Puter AI API Processor
Make sure the Flask server is running and browser page is open before running this!
"""

import requests
import time

BASE_URL = "http://localhost:5001"

def check_status():
    """Check if the server is online"""
    print("🔍 Checking server status...")
    response = requests.get(f"{BASE_URL}/api/status")
    data = response.json()
    print(f"✅ Status: {data['status']}")
    print(f"   Pending: {data['pending_requests']}")
    print(f"   Completed: {data['completed_results']}\n")
    return data

def send_prompt(prompt, model="claude"):
    """Send a prompt to be processed"""
    print(f"📤 Sending prompt to {model}...")
    print(f"   Prompt: {prompt[:50]}...\n")
    
    start_time = time.time()
    
    response = requests.post(
        f"{BASE_URL}/api/process",
        json={
            "prompt": prompt,
            "model": model
        }
    )
    
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! (took {elapsed:.2f}s)")
        print(f"   Request ID: {data['request_id']}")
        print(f"   Result: {data['result'][:100]}...")
        print(f"   Full response length: {len(data['result'])} characters\n")
        return data
    else:
        data = response.json()
        print(f"❌ Error: {data['message']}\n")
        return None

def main():
    print("=" * 60)
    print("Puter AI API Processor - Test Script")
    print("=" * 60)
    print()
    
    # Check status
    try:
        check_status()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("   Make sure Flask is running: python app.py")
        return
    
    # Test prompts
    tests = [
        {
            "prompt": "What is 2+2? Answer in one sentence.",
            "model": "claude"
        },
        {
            "prompt": "Write a haiku about Python programming.",
            "model": "claude"
        },
        {
            "prompt": "Explain quantum computing in exactly 3 sentences.",
            "model": "claude"
        }
    ]
    
    print("🚀 Running test prompts...\n")
    
    for i, test in enumerate(tests, 1):
        print(f"Test {i}/{len(tests)}")
        print("-" * 60)
        result = send_prompt(test["prompt"], test["model"])
        
        if result:
            print("✅ Test passed\n")
        else:
            print("❌ Test failed\n")
        
        # Wait a bit between requests
        if i < len(tests):
            print("⏳ Waiting 2 seconds...\n")
            time.sleep(2)
    
    # Final status
    print("=" * 60)
    print("Final Status:")
    check_status()
    print("=" * 60)

if __name__ == "__main__":
    main()
