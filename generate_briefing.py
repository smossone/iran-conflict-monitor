#!/usr/bin/env python3
import json, os, sys
from datetime import datetime, timezone

try:
    import anthropic
except ImportError:
    print("ERROR: 'anthropic' package not installed. Run: pip install anthropic")
    sys.exit(1)

PROMPT = """You are an expert OSINT analyst producing a concise intelligence briefing
on the Iran conflict situation. Based on your knowledge of recent events, produce a
structured briefing covering:

1. **Current Situation Overview** - 2-3 sentences on the latest state of affairs
2. **Key Developments** (last 24-48 hours) - bullet points of significant events
3. **Military & Strategic Activity** - troop movements, strikes, deployments, posturing
4. **Diplomatic Channels** - negotiations, statements, UN activity, backchannel signals
5. **Regional Impact** - effects on neighboring countries, proxy groups, shipping lanes
6. **Risk Assessment** - current threat level and escalation/de-escalation indicators
7. **Outlook** - what to watch for in the next 24-48 hours

Format your response in clean HTML (use <h2>, <h3>, <p>, <ul>, <li>, <strong>, <em> tags).
Do NOT include <html>, <body>, or <head> tags - only the inner content.
Keep total length between 400-700 words. Be analytical, not sensational.
Include a disclaimer that this is AI-generated analysis based on available information."""

def generate_briefing():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)
    client = anthropic.Anthropic(api_key=api_key)
    print("Generating briefing...")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": PROMPT}],
    )
    html_content = message.content[0].text
    now = datetime.now(timezone.utc)
    briefing_data = {
        "html": html_content,
        "timestamp": now.strftime("%Y-%m-%d %H:%M UTC"),
        "generated_at": now.isoformat(),
        "model": "claude-sonnet-4-20250514",
        "tokens_used": message.usage.input_tokens + message.usage.output_tokens,
    }
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "briefing.json")
    with open(output_path, "w") as f:
        json.dump(briefing_data, f, indent=2)
    print(f"Briefing generated at {briefing_data['timestamp']}")
    print(f"Tokens used: {briefing_data['tokens_used']}")

if __name__ == "__main__":
    generate_briefing()
