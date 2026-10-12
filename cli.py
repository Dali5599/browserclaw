#!/usr/bin/env python3
"""
BrowserClaw CLI - Enterprise Autonomous AI Web Automation Interface
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

# Ensure package import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.backend.services.browser import BrowserEngine
from src.backend.services.agent import CognitiveAgent

async def run_inspection(url: str, task: str, headless: bool, json_output: bool):
    print(f"🦈 [BrowserClaw] Initializing Autonomous Browser Engine...")
    print(f"🌐 Target: {url}")
    print(f"🎯 Objective: {task}")
    print(f"⚙️ Mode: { Headless if headless else Headed}")
    print("-" * 65)

    engine = BrowserEngine(headless=headless)
    try:
        await engine.start()
        print("  ✓ Chromium instance launched with anti-detection stealth patches.")
        print(f"  → Navigating to {url}...")
        state = await engine.navigate(url)

        print(f"  ✓ Page Loaded: \"{state.title}\"")
        print(f"  ✓ Interactive Elements Detected: {len(state.elements)}")

        if json_output:
            elements_data = [
                {
                    "index": el.index,
                    "role": el.role,
                    "name": el.name,
                    "selector": el.selector,
                    "box": el.bounding_box
                }
                for el in state.elements[:15]
            ]
            print("\n" + json.dumps({
                "status": "success",
                "title": state.title,
                "url": state.url,
                "elements_count": len(state.elements),
                "sample_elements": elements_data
            }, indent=2))
        else:
            print("\n📋 Top Interactive Elements (Set-of-Marks):")
            for el in state.elements[:10]:
                print(f"  [{el.index}] <{el.role}> \"{el.name or el.text[:30]}\" -> {el.selector}")

        print("-" * 65)
        print("✅ Autonomous inspection completed successfully.")
    except Exception as e:
        print(f"[-] Execution error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await engine.close()

def main():
    parser = argparse.ArgumentParser(
        description="BrowserClaw CLI - Autonomous AI Web Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  browserclaw https://news.ycombinator.com --task "Inspect headlines"
  browserclaw https://github.com --task "Analyze landing page" --json
        """
    )
    parser.add_argument("url", nargs="?", default="https://news.ycombinator.com", help="Target URL to automate")
    parser.add_argument("--task", default="Autonomous web inspection", help="Agent goal or instruction")
    parser.add_argument("--headed", action="store_true", help="Run browser with visible UI window")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    asyncio.run(run_inspection(args.url, args.task, headless=not args.headed, json_output=args.json))

if __name__ == "__main__":
    main()
