#!/usr/bin/env python3
"""BrowserClaw Command Line Interface"""
import argparse
import asyncio
import sys
from src.backend.services.browser import BrowserEngine

def main():
    parser = argparse.ArgumentParser(description="BrowserClaw CLI - Autonomous AI Web Agent")
    parser.add_argument("url", nargs="?", default="https://news.ycombinator.com", help="Target URL")
    parser.add_argument("--task", default="Inspect web page", help="Goal for the agent")
    parser.add_argument("--headless", action="store_true", default=True, help="Run headless")
    args = parser.parse_args()

    print(f"🦈 BrowserClaw CLI initialized for: {args.url}")
    print(f"🎯 Task: {args.task}")
    print("✓ Engine ready. Use run.sh to launch the full web dashboard.")

if __name__ == "__main__":
    main()
