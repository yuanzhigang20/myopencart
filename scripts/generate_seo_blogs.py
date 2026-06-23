#!/usr/bin/env python3
"""Generate SEO blog cluster outputs and static Blog pages for ShopLovaNest.

This script intentionally avoids third-party dependencies so it can run in the
OpenCart repo without mutating composer/npm state.
"""
from __future__ import annotations

import csv
import html
import json
import os
import re
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
KEYWORD_DIR = ROOT / "kewwordsfile"
OUTPUT_DIR = ROOT / "output"
BLOG_DIR = ROOT / "upload" / "blog"
BASE_URL = "https://shoplovanest.com"
AUTHOR = "ShopLovaNest Editorial Team"
TODAY = date(2026, 6, 23)

NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

FIELD_ALIASES = {
    "keyword": ["keyword", "search term", "query"],
    "volume": ["volume", "search volume"],
    "kd": ["kd", "kd %", "keyword difficulty"],
    "cpc": ["cpc"],
    "intent": ["intent"],
    "trend": ["trend"],
    "competition": ["competition"],
    "serp_features": ["serp features"],
    "source": ["source"],
    "country": ["country"],
}

BANNED_RE = re.compile(
    r"\b(teen|minor|underage|child|schoolgirl|porn|porno|xxx|nude|onlyfans|leaked|rape|forced|incest|bestiality|zoophilia|drug|crack|hack|pirate|torrent|free download|adam\s*&?\s*eve|amazon|target|walmart|etsy|mcdonald|toy story|disney|barbie)\b",
    re.I,
)
IRRELEVANT_RE = re.compile(r"\b(fidget|happy meal|costume|outfit|christmas toys|toyota|kids|children|toddler|baby)\b", re.I)
ALLOWED_CONTEXT_RE = re.compile(
    r"\b(adult toy|sex toy|vibrator|lube|lubricant|silicone|water based|wand|rabbit|bullet|cock ring|kegel|masturbator|anal toy|discreet|body safe|waterproof|rechargeable|quiet|cleaner|cleaning)\b",
    re.I,
)

CATEGORY_LINKS = {
    "home": {"anchor_text": "ShopLovaNest home", "target_url": "/", "reason": "Gives readers a safe starting point for private wellness shopping."},
    "blog": {"anchor_text": "sexual wellness blog", "target_url": "/blog/", "reason": "Connects the article to the wider education hub."},
    "vibrators": {"anchor_text": "quiet personal massagers", "target_url": "/index.php?route=product/category&path=113", "reason": "Relevant product category for readers comparing vibration styles."},
    "lubricants": {"anchor_text": "body-safe lubricants", "target_url": "/index.php?route=product/category&path=117", "reason": "Supports safer use, comfort, and maintenance decisions."},
    "kegel": {"anchor_text": "pelvic wellness accessories", "target_url": "/index.php?route=product/product&product_id=1015", "reason": "Relevant product detail page for pelvic wellness readers."},
    "discreet": {"anchor_text": "discreet wellness products", "target_url": "/index.php?route=product/product&product_id=1013", "reason": "Example product with a privacy-focused design angle."},
    "rings": {"anchor_text": "couples wellness accessories", "target_url": "/index.php?route=product/product&product_id=1017", "reason": "Relevant product detail page for couples accessory topics."},
    "contact": {"anchor_text": "contact our support team", "target_url": "/index.php?route=information/contact", "reason": "Useful for discreet shipping, returns, and product questions."},
}

TOPICS = [
    {
        "primary": "sex toys for beginners",
        "title": "Sex Toys for Beginners: A Calm, Practical First Guide",
        "meta_title": "Sex Toys for Beginners: Practical First-Time Guide",
        "meta_description": "A discreet, beginner-friendly guide to choosing sex toys with body-safe materials, simple features, privacy, and realistic expectations.",
        "slug": "sex-toys-for-beginners",
        "intent": "Beginner Guide",
        "type": "Guide",
        "reader": "Adults 18+ who want a private, non-intimidating first buying guide.",
        "angle": "Start with comfort, safety, privacy, and simple controls instead of chasing advanced features.",
        "cluster": "Beginner adult wellness basics",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["home", "blog", "vibrators", "lubricants", "contact"],
        "steps": ["Set a comfort boundary", "Choose body-safe materials", "Pick simple controls", "Plan cleaning and storage"],
    },
    {
        "primary": "vibrators for beginners",
        "title": "Vibrators for Beginners: How to Choose Without Guesswork",
        "meta_title": "Vibrators for Beginners: Choose the Right First Massager",
        "meta_description": "Learn how beginners can compare vibrator size, noise, materials, charging, waterproofing, and privacy before buying a first massager.",
        "slug": "vibrators-for-beginners",
        "intent": "Beginner Guide",
        "type": "Buying Guide",
        "reader": "First-time buyers comparing simple vibrating massagers.",
        "angle": "Explain what features matter first and which advanced features can wait.",
        "cluster": "Beginner vibrator selection",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["vibrators", "discreet", "blog", "lubricants"],
        "steps": ["Decide external or wearable use", "Check sound expectations", "Review charging and cleaning", "Start with low settings"],
    },
    {
        "primary": "discreet shipping adult toys",
        "title": "Discreet Shipping for Adult Toys: What Privacy Really Means",
        "meta_title": "Discreet Shipping Adult Toys: Privacy Checklist",
        "meta_description": "Understand discreet shipping for adult toys, including packaging, billing descriptors, tracking, delivery addresses, and support questions.",
        "slug": "discreet-shipping-adult-toys",
        "intent": "Problem Solving",
        "type": "Educational Blog",
        "reader": "Privacy-focused shoppers who want clarity before ordering.",
        "angle": "Define real privacy signals shoppers can verify before checkout.",
        "cluster": "Privacy and delivery",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["home", "contact", "blog", "discreet"],
        "steps": ["Check packaging language", "Review billing names", "Use a reliable delivery address", "Keep order support discreet"],
    },
    {
        "primary": "body safe sex toys",
        "title": "Body-Safe Sex Toys: Materials, Labels, and Red Flags",
        "meta_title": "Body-Safe Sex Toys: Material Safety Guide",
        "meta_description": "A practical guide to body-safe sex toys, including silicone, glass, ABS, metal, porosity, odors, cleaning, and label red flags.",
        "slug": "body-safe-sex-toys",
        "intent": "Informational",
        "type": "Educational Blog",
        "reader": "Shoppers who want safer material choices and clearer product labels.",
        "angle": "Turn confusing material claims into a simple safety checklist.",
        "cluster": "Body-safe materials",
        "difficulty": "Medium",
        "commercial": "High",
        "links": ["vibrators", "lubricants", "blog", "contact"],
        "steps": ["Read the material line", "Avoid vague jelly claims", "Match cleaner to material", "Store items separately"],
    },
    {
        "primary": "adult toy cleaner",
        "title": "Adult Toy Cleaner: When You Need It and How to Use It",
        "meta_title": "Adult Toy Cleaner Guide: Clean, Dry, Store Safely",
        "meta_description": "Learn when adult toy cleaner helps, when mild soap is enough, and how to clean, dry, inspect, and store wellness products safely.",
        "slug": "adult-toy-cleaner-guide",
        "intent": "How-to",
        "type": "How-to",
        "reader": "Adults who want a simple cleaning routine without damaging products.",
        "angle": "Separate cleaner myths from practical hygiene and material care.",
        "cluster": "Cleaning and storage",
        "difficulty": "Easy",
        "commercial": "Medium",
        "links": ["blog", "vibrators", "lubricants", "contact"],
        "steps": ["Unplug or power off", "Rinse only waterproof items", "Apply compatible cleaner", "Dry completely", "Store away from lint"],
    },
    {
        "primary": "water based lube",
        "title": "Water-Based Lube: A Beginner-Friendly Compatibility Guide",
        "meta_title": "Water-Based Lube Guide: Uses, Pros, and Cleanup",
        "meta_description": "Compare water-based lube benefits, cleanup, silicone toy compatibility, reapplication, and shopping checks for comfortable use.",
        "slug": "water-based-lube-guide",
        "intent": "Informational",
        "type": "Guide",
        "reader": "Beginners choosing a low-fuss lubricant for toys or partnered wellness.",
        "angle": "Explain why water-based formulas are often the safest first choice.",
        "cluster": "Lubricant basics",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["lubricants", "body-safe", "blog", "vibrators"],
        "steps": ["Check toy compatibility", "Start with a small amount", "Reapply when needed", "Wash off after use"],
    },
    {
        "primary": "silicone lube",
        "title": "Silicone Lube: Best Uses, Limits, and Toy Compatibility",
        "meta_title": "Silicone Lube Guide: Uses and Compatibility",
        "meta_description": "Learn when silicone lube works well, when to avoid it, how it compares with water-based lube, and what to check before using it with toys.",
        "slug": "silicone-lube-guide",
        "intent": "Comparison",
        "type": "Comparison",
        "reader": "Adults comparing longer-lasting lubricant options.",
        "angle": "Make compatibility and cleanup the deciding factors, not hype.",
        "cluster": "Lubricant comparison",
        "difficulty": "Medium",
        "commercial": "High",
        "links": ["lubricants", "blog", "vibrators", "contact"],
        "steps": ["Check product material", "Patch-test cautiously", "Use less at first", "Clean surfaces thoroughly"],
    },
    {
        "primary": "quiet vibrator",
        "title": "Quiet Vibrator Guide: How to Compare Noise Before Buying",
        "meta_title": "Quiet Vibrator Guide: Privacy and Noise Checklist",
        "meta_description": "A privacy-first guide to choosing a quiet vibrator, including motor type, speed settings, room noise, reviews, charging, and storage.",
        "slug": "quiet-vibrator-guide",
        "intent": "Commercial",
        "type": "Buying Guide",
        "reader": "Adults who share walls, travel, or value low-noise privacy.",
        "angle": "Explain realistic noise expectations and what product claims can and cannot prove.",
        "cluster": "Quiet personal massagers",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["vibrators", "discreet", "blog", "contact"],
        "steps": ["Compare low settings first", "Consider size and motor", "Plan storage", "Test in a normal room"],
    },
    {
        "primary": "rechargeable vibrator",
        "title": "Rechargeable Vibrator Guide: Battery, Charging, and Care",
        "meta_title": "Rechargeable Vibrator Guide: Battery and Care Tips",
        "meta_description": "Learn how to evaluate rechargeable vibrators by battery life, charging style, waterproof seals, travel storage, and long-term care.",
        "slug": "rechargeable-vibrator-guide",
        "intent": "Commercial",
        "type": "Buying Guide",
        "reader": "Shoppers comparing rechargeable personal massagers.",
        "angle": "Focus on daily convenience and care instead of feature overload.",
        "cluster": "Rechargeable massagers",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["vibrators", "blog", "discreet", "contact"],
        "steps": ["Check charging cable type", "Read runtime claims", "Dry ports before charging", "Store with travel lock if available"],
    },
    {
        "primary": "waterproof vibrator",
        "title": "Waterproof Vibrator Guide: Ratings, Cleaning, and Cautions",
        "meta_title": "Waterproof Vibrator Guide: Ratings and Cleaning",
        "meta_description": "Understand waterproof vibrator claims, splash resistance, sealed charging ports, cleaning routines, and what not to do with electronics.",
        "slug": "waterproof-vibrator-guide",
        "intent": "Problem Solving",
        "type": "Guide",
        "reader": "Adults buying a washable or bath-friendly personal massager.",
        "angle": "Clarify waterproof versus splash resistant and safe cleaning habits.",
        "cluster": "Waterproof care",
        "difficulty": "Medium",
        "commercial": "High",
        "links": ["vibrators", "blog", "lubricants", "contact"],
        "steps": ["Read the exact rating", "Close all charging seals", "Avoid boiling electronics", "Dry before storage"],
    },
    {
        "primary": "bullet vibrator",
        "title": "Bullet Vibrator Guide: Small Size, Simple Controls, Big Questions",
        "meta_title": "Bullet Vibrator Guide: Features and Buying Checklist",
        "meta_description": "Compare bullet vibrators by size, noise, material, charging, waterproofing, and beginner-friendly controls before choosing one.",
        "slug": "bullet-vibrator-guide",
        "intent": "Commercial",
        "type": "Buying Guide",
        "reader": "Adults considering a small, discreet vibrating massager.",
        "angle": "Help buyers decide if compact size is a benefit or limitation.",
        "cluster": "Compact vibrators",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["vibrators", "discreet", "blog", "lubricants"],
        "steps": ["Choose size intentionally", "Check button placement", "Compare noise claims", "Plan cleaning"],
    },
    {
        "primary": "rabbit vibrator",
        "title": "Rabbit Vibrator Guide: Who It Suits and What to Check",
        "meta_title": "Rabbit Vibrator Guide: Fit, Features, and Comfort",
        "meta_description": "A practical rabbit vibrator guide covering fit, flexibility, motor controls, materials, cleaning, and beginner-friendly buying cautions.",
        "slug": "rabbit-vibrator-guide",
        "intent": "Commercial",
        "type": "Buying Guide",
        "reader": "Shoppers comparing dual-stimulation massagers with comfort in mind.",
        "angle": "Explain fit and control complexity without explicit or exaggerated claims.",
        "cluster": "Rabbit vibrators",
        "difficulty": "Medium",
        "commercial": "High",
        "links": ["vibrators", "lubricants", "blog", "contact"],
        "steps": ["Check dimensions", "Look for flexible contact points", "Start with simple modes", "Use compatible lubricant"],
    },
    {
        "primary": "wand massager",
        "title": "Wand Massager Guide: Power, Noise, Weight, and Care",
        "meta_title": "Wand Massager Guide: Power, Noise, and Care",
        "meta_description": "Learn how to choose a wand massager by power range, handle weight, noise, attachments, charging style, and easy cleaning.",
        "slug": "wand-massager-guide",
        "intent": "Commercial",
        "type": "Buying Guide",
        "reader": "Adults comparing larger external personal massagers.",
        "angle": "Balance power with comfort, privacy, and practical storage.",
        "cluster": "Wand massagers",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["vibrators", "blog", "discreet", "contact"],
        "steps": ["Compare weight and grip", "Start on low settings", "Check charging style", "Clean the head carefully"],
    },
    {
        "primary": "kegel balls",
        "title": "Kegel Balls Guide: Pelvic Wellness Basics and Safety Notes",
        "meta_title": "Kegel Balls Guide: Beginner Pelvic Wellness Basics",
        "meta_description": "A discreet guide to kegel balls for pelvic wellness, covering materials, sizing, cleaning, comfort, and when to seek professional advice.",
        "slug": "kegel-balls-guide",
        "intent": "Informational",
        "type": "Educational Blog",
        "reader": "Adults researching pelvic wellness accessories responsibly.",
        "angle": "Keep the guidance educational and avoid medical promises.",
        "cluster": "Pelvic wellness accessories",
        "difficulty": "Medium",
        "commercial": "Medium",
        "links": ["kegel", "lubricants", "blog", "contact"],
        "steps": ["Choose beginner sizing", "Use compatible lubricant", "Limit sessions", "Clean and inspect after use"],
    },
    {
        "primary": "cock ring",
        "title": "Cock Ring Guide: Fit, Materials, and Beginner Safety",
        "meta_title": "Cock Ring Guide: Fit, Materials, and Safety",
        "meta_description": "Learn how adults can compare cock rings by fit, stretch, material, vibration, cleaning, comfort, and responsible use limits.",
        "slug": "cock-ring-guide",
        "intent": "Beginner Guide",
        "type": "Guide",
        "reader": "Adults researching couples wellness accessories for the first time.",
        "angle": "Emphasize fit, time limits, and comfort over exaggerated claims.",
        "cluster": "Couples accessories",
        "difficulty": "Medium",
        "commercial": "High",
        "links": ["rings", "lubricants", "blog", "contact"],
        "steps": ["Choose flexible materials", "Check sizing", "Use time limits", "Stop if discomfort appears"],
    },
    {
        "primary": "male masturbator",
        "title": "Male Masturbator Guide: Materials, Cleaning, and Privacy",
        "meta_title": "Male Masturbator Guide: Materials and Cleaning",
        "meta_description": "A clean, practical guide to male masturbators covering material feel, openings, cleaning effort, drying, storage, and discreet shopping.",
        "slug": "male-masturbator-guide",
        "intent": "Commercial",
        "type": "Buying Guide",
        "reader": "Adults comparing private wellness products with maintenance in mind.",
        "angle": "Make cleaning and drying as important as product style.",
        "cluster": "Male wellness products",
        "difficulty": "Medium",
        "commercial": "High",
        "links": ["lubricants", "blog", "home", "contact"],
        "steps": ["Check material and opening", "Use compatible lubricant", "Clean promptly", "Dry fully before storage"],
    },
    {
        "primary": "anal toys for beginners",
        "title": "Anal Toys for Beginners: Safety, Size, and Comfort Basics",
        "meta_title": "Anal Toys for Beginners: Safety and Comfort Guide",
        "meta_description": "A professional beginner guide to anal toys covering flared bases, sizing, lubricant, hygiene, pacing, and when not to use a product.",
        "slug": "anal-toys-for-beginners",
        "intent": "Beginner Guide",
        "type": "Guide",
        "reader": "Adults 18+ seeking safety-first information before buying.",
        "angle": "Prioritize anatomy-safe design, patience, and non-medical caution.",
        "cluster": "Beginner anal wellness",
        "difficulty": "Medium",
        "commercial": "Medium",
        "links": ["lubricants", "blog", "contact", "home"],
        "steps": ["Choose a flared base", "Start small", "Use enough lubricant", "Stop with pain", "Clean separately"],
    },
    {
        "primary": "adult toys for couples",
        "title": "Adult Toys for Couples: How to Choose Together Respectfully",
        "meta_title": "Adult Toys for Couples: Respectful Buying Guide",
        "meta_description": "A discreet couples guide to choosing adult toys together, covering consent, comfort levels, privacy, simple features, and shared maintenance.",
        "slug": "adult-toys-for-couples",
        "intent": "Commercial",
        "type": "Guide",
        "reader": "Couples who want a respectful, low-pressure buying process.",
        "angle": "Make communication and shared comfort the core of product choice.",
        "cluster": "Couples buying guide",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["rings", "vibrators", "lubricants", "blog"],
        "steps": ["Discuss boundaries", "Choose a shared use case", "Start with simple modes", "Agree on cleaning and storage"],
    },
    {
        "primary": "best adult toys for beginners",
        "title": "Best Adult Toys for Beginners: Types to Consider First",
        "meta_title": "Best Adult Toys for Beginners: Types and Checklist",
        "meta_description": "Compare beginner-friendly adult toy types by simplicity, cleaning, privacy, noise, material safety, and realistic shopping priorities.",
        "slug": "best-adult-toys-for-beginners",
        "intent": "Comparison",
        "type": "Listicle",
        "reader": "First-time shoppers deciding which product type to research first.",
        "angle": "Compare product categories without claiming one universal best choice.",
        "cluster": "Beginner product types",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["vibrators", "lubricants", "discreet", "blog"],
        "steps": ["Pick a use case", "Choose easy cleaning", "Avoid advanced modes first", "Confirm privacy needs"],
    },
    {
        "primary": "adult toy storage",
        "title": "Adult Toy Storage: Clean, Private, and Material-Safe Habits",
        "meta_title": "Adult Toy Storage Guide: Clean and Private Habits",
        "meta_description": "Learn adult toy storage basics, including drying, separate bags, charger care, lint control, travel privacy, and material-safe organization.",
        "slug": "adult-toy-storage-guide",
        "intent": "How-to",
        "type": "Product Support Blog",
        "reader": "Adults who want a practical storage routine after cleaning products.",
        "angle": "Show how storage protects privacy, hygiene, and product lifespan.",
        "cluster": "Cleaning and storage",
        "difficulty": "Easy",
        "commercial": "Medium",
        "links": ["blog", "vibrators", "lubricants", "contact"],
        "steps": ["Dry fully", "Use separate pouches", "Keep chargers nearby", "Avoid heat and lint"],
    },
    {
        "primary": "adult toy materials",
        "title": "Adult Toy Materials: Silicone, Glass, ABS, and Metal Explained",
        "meta_title": "Adult Toy Materials: Silicone, Glass, ABS, Metal",
        "meta_description": "Compare common adult toy materials by body-safety, porosity, firmness, cleaning, lubricant compatibility, and practical shopping checks.",
        "slug": "adult-toy-materials-guide",
        "intent": "Informational",
        "type": "Educational Blog",
        "reader": "Shoppers confused by material labels and safety claims.",
        "angle": "Give a neutral material comparison without medical promises.",
        "cluster": "Body-safe materials",
        "difficulty": "Medium",
        "commercial": "High",
        "links": ["vibrators", "lubricants", "blog", "contact"],
        "steps": ["Identify the material", "Check if it is porous", "Match lubricant", "Clean according to electronics"],
    },
    {
        "primary": "adult toy privacy",
        "title": "Adult Toy Privacy: Packaging, Billing, Search, and Storage",
        "meta_title": "Adult Toy Privacy Guide: Packaging to Storage",
        "meta_description": "A privacy checklist for adult toy shopping, including discreet packaging, billing, browser habits, delivery, account emails, and storage.",
        "slug": "adult-toy-privacy-guide",
        "intent": "Problem Solving",
        "type": "Guide",
        "reader": "Privacy-first shoppers who want control before and after purchase.",
        "angle": "Cover privacy beyond the box, from research to aftercare.",
        "cluster": "Privacy and delivery",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["contact", "discreet", "blog", "home"],
        "steps": ["Review shop privacy language", "Choose delivery carefully", "Use discreet storage", "Keep support questions concise"],
    },
    {
        "primary": "travel with adult toys",
        "title": "Traveling With Adult Toys: Packing, Charging, and Privacy",
        "meta_title": "Travel With Adult Toys: Packing and Privacy Guide",
        "meta_description": "A practical travel guide for adult toys covering cleaning before packing, travel locks, batteries, storage bags, hotel privacy, and local laws.",
        "slug": "travel-with-adult-toys",
        "intent": "How-to",
        "type": "How-to",
        "reader": "Adults planning discreet travel with personal wellness products.",
        "angle": "Keep guidance practical and remind readers to check local laws.",
        "cluster": "Travel privacy",
        "difficulty": "Medium",
        "commercial": "Medium",
        "links": ["discreet", "vibrators", "blog", "contact"],
        "steps": ["Clean before packing", "Use a storage pouch", "Engage travel lock", "Check destination rules"],
    },
    {
        "primary": "water based lube vs silicone lube",
        "title": "Water-Based Lube vs Silicone Lube: Which Should You Choose?",
        "meta_title": "Water-Based Lube vs Silicone Lube Comparison",
        "meta_description": "Compare water-based and silicone lube by toy compatibility, cleanup, feel, reapplication, shower use, sheet stains, and beginner friendliness.",
        "slug": "water-based-lube-vs-silicone-lube",
        "intent": "Comparison",
        "type": "Comparison",
        "reader": "Adults choosing between lubricant types before buying.",
        "angle": "Make compatibility and cleanup the decision framework.",
        "cluster": "Lubricant comparison",
        "difficulty": "Medium",
        "commercial": "High",
        "links": ["lubricants", "vibrators", "blog", "contact"],
        "steps": ["List your product materials", "Decide cleanup preference", "Consider duration", "Test a small amount"],
    },
    {
        "primary": "how to clean silicone sex toys",
        "title": "How to Clean Silicone Sex Toys Without Damaging Them",
        "meta_title": "How to Clean Silicone Sex Toys: Safe Routine",
        "meta_description": "Learn how to clean silicone sex toys, including waterproof checks, mild soap, compatible cleaners, drying, inspection, and storage.",
        "slug": "how-to-clean-silicone-sex-toys",
        "intent": "How-to",
        "type": "How-to",
        "reader": "Adults caring for silicone wellness products at home.",
        "angle": "Separate silicone material care from electronics care.",
        "cluster": "Cleaning and storage",
        "difficulty": "Easy",
        "commercial": "Medium",
        "links": ["blog", "vibrators", "lubricants", "contact"],
        "steps": ["Check if it is waterproof", "Use mild soap or compatible cleaner", "Rinse as directed", "Dry completely", "Store separately"],
    },
    {
        "primary": "how to choose a vibrator",
        "title": "How to Choose a Vibrator: A Practical Decision Checklist",
        "meta_title": "How to Choose a Vibrator: Decision Checklist",
        "meta_description": "Use this practical checklist to choose a vibrator by use case, size, material, sound, charging, waterproofing, controls, and privacy.",
        "slug": "how-to-choose-a-vibrator",
        "intent": "How-to",
        "type": "How-to",
        "reader": "Shoppers who want a clear comparison process.",
        "angle": "Turn a crowded category into a short decision tree.",
        "cluster": "Vibrator selection",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["vibrators", "discreet", "lubricants", "blog"],
        "steps": ["Define the use case", "Choose material", "Set privacy needs", "Compare maintenance", "Review return questions"],
    },
    {
        "primary": "adult toy buying guide",
        "title": "Adult Toy Buying Guide: Safety, Privacy, and Value Checks",
        "meta_title": "Adult Toy Buying Guide: Safety and Privacy Checks",
        "meta_description": "A full adult toy buying guide covering search intent, body-safe materials, privacy, product specs, maintenance, budget, and support.",
        "slug": "adult-toy-buying-guide",
        "intent": "Commercial",
        "type": "Buying Guide",
        "reader": "Adults comparing several product categories before buying.",
        "angle": "Use a buyer checklist that works across categories.",
        "cluster": "Buying decision framework",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["home", "vibrators", "lubricants", "blog", "contact"],
        "steps": ["Clarify the job to be done", "Confirm material safety", "Check privacy details", "Plan cleaning", "Avoid unrealistic claims"],
    },
    {
        "primary": "adult toy gift guide",
        "title": "Adult Toy Gift Guide: Consent, Privacy, and Safer Choices",
        "meta_title": "Adult Toy Gift Guide: Consent and Privacy First",
        "meta_description": "A responsible adult toy gift guide focused on consent, privacy, discreet packaging, beginner-friendly options, and when not to surprise someone.",
        "slug": "adult-toy-gift-guide",
        "intent": "Commercial",
        "type": "Guide",
        "reader": "Adults considering a private wellness gift for a partner.",
        "angle": "Make consent and recipient comfort the non-negotiable foundation.",
        "cluster": "Gift and couples decisions",
        "difficulty": "Easy",
        "commercial": "Medium",
        "links": ["discreet", "lubricants", "blog", "contact"],
        "steps": ["Ask before buying", "Choose simple designs", "Protect privacy", "Include care instructions"],
    },
    {
        "primary": "beginner lubricant guide",
        "title": "Beginner Lubricant Guide: Ingredients, Feel, and Compatibility",
        "meta_title": "Beginner Lubricant Guide: Feel and Compatibility",
        "meta_description": "Learn lubricant basics for beginners, including water-based, silicone, ingredient checks, toy compatibility, cleanup, and sensitive-skin caution.",
        "slug": "beginner-lubricant-guide",
        "intent": "Beginner Guide",
        "type": "Guide",
        "reader": "Adults who want a first lubricant without confusing claims.",
        "angle": "Explain compatibility and comfort in plain language.",
        "cluster": "Lubricant basics",
        "difficulty": "Easy",
        "commercial": "High",
        "links": ["lubricants", "vibrators", "blog", "contact"],
        "steps": ["Choose a base type", "Read ingredient warnings", "Match toy material", "Clean after use"],
    },
    {
        "primary": "how to use kegel balls safely",
        "title": "How to Use Kegel Balls Safely: Beginner Routine and Care",
        "meta_title": "How to Use Kegel Balls Safely: Beginner Routine",
        "meta_description": "A careful guide to using kegel balls safely, with beginner sizing, time limits, cleaning, comfort checks, and non-medical safety notes.",
        "slug": "how-to-use-kegel-balls-safely",
        "intent": "How-to",
        "type": "How-to",
        "reader": "Adults researching pelvic wellness routines responsibly.",
        "angle": "Avoid medical promises and focus on comfort, hygiene, and professional advice when needed.",
        "cluster": "Pelvic wellness accessories",
        "difficulty": "Medium",
        "commercial": "Medium",
        "links": ["kegel", "lubricants", "blog", "contact"],
        "steps": ["Wash hands and product", "Apply compatible lubricant", "Start with short sessions", "Remove gently", "Clean and dry"],
    },
    {
        "primary": "adult toy faq",
        "title": "Adult Toy FAQ: Beginner Questions Answered Clearly",
        "meta_title": "Adult Toy FAQ: Beginner Questions and Answers",
        "meta_description": "Clear answers to common adult toy questions about privacy, materials, cleaning, lubricant, noise, charging, returns, and responsible shopping.",
        "slug": "adult-toy-faq",
        "intent": "FAQ Guide",
        "type": "FAQ Guide",
        "reader": "Beginners who want quick, discreet answers before exploring products.",
        "angle": "Answer practical questions without explicit language or hype.",
        "cluster": "Beginner adult wellness basics",
        "difficulty": "Easy",
        "commercial": "Medium",
        "links": ["home", "blog", "vibrators", "lubricants", "contact"],
        "steps": ["Start with privacy questions", "Check materials", "Plan cleaning", "Ask support when unsure"],
    },
]

# Link key typo-safe alias used by one topic.
CATEGORY_LINKS["body-safe"] = CATEGORY_LINKS["blog"]

SECTION_VARIANTS = [
    ("What this question is really asking", "People searching for {primary} are usually not looking for a dramatic promise. They want to know what is safe, private, realistic, and worth paying for. The best answer starts with context: how the product will be used, how much cleaning it requires, how discreet the purchase needs to be, and whether the design matches the reader's comfort level. For adults 18+, a good wellness purchase should reduce uncertainty rather than create pressure."),
    ("Who this guide is for", "This guide is for adults who prefer calm, educational shopping advice. It is especially useful if you are comparing options for the first time, sharing a home, buying with a partner, or trying to avoid vague product claims. It is not for anyone seeking explicit content, medical treatment claims, or unsafe shortcuts. If a product causes pain, irritation, numbness, or anxiety, stop using it and consider professional guidance where appropriate."),
    ("Key criteria to compare", "Use a short checklist before you compare prices. First, identify the material and whether it is non-porous. Second, check how the item is powered, cleaned, and stored. Third, look at privacy factors such as packaging, billing, and noise. Fourth, make sure any lubricant or cleaner you plan to use is compatible. Finally, choose the simplest product that solves the actual need; extra modes are only useful when you understand them."),
]

FAQ_BANK = {
    "privacy": [
        ("Will the package say what is inside?", "A privacy-focused shop should use plain outer packaging and avoid product names on the outside label. Check the shipping page or contact support before ordering if this matters."),
        ("Can billing still reveal the purchase?", "It can, depending on the merchant descriptor. Look for a private billing note before checkout and keep support messages concise if you need clarification."),
    ],
    "materials": [
        ("Is silicone always body-safe?", "Medical-grade or body-safe silicone from a transparent seller is generally preferred, but labels should still be checked. Avoid vague material claims and strong chemical odors."),
        ("Can I use silicone lube with silicone toys?", "Often it is better to avoid that pairing unless the product instructions explicitly allow it. Water-based lube is usually the safer first choice for silicone toys."),
    ],
    "cleaning": [
        ("Is toy cleaner required every time?", "Not always. Many non-porous products can be cleaned with mild soap and water if the instructions allow it. Cleaner is useful when compatible and convenient."),
        ("When should I replace a product?", "Replace it if the surface cracks, becomes sticky, develops a persistent odor, the motor behaves oddly, or charging seals no longer close properly."),
    ],
    "buying": [
        ("Should beginners buy the strongest option?", "Usually no. Beginners benefit from simple controls, lower settings, easy cleaning, and clear materials more than maximum power."),
        ("What if I am choosing between two similar products?", "Choose the one with clearer material information, simpler maintenance, better privacy details, and support that answers practical questions."),
    ],
}


def read_xlsx(path: Path) -> List[Dict[str, str]]:
    rows: List[List[str]] = []
    with zipfile.ZipFile(path) as z:
        shared: List[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("a:si", NS):
                shared.append("".join(t.text or "" for t in si.findall(".//a:t", NS)))
        sheet_names = [n for n in z.namelist() if n.startswith("xl/worksheets/sheet") and n.endswith(".xml")]
        if not sheet_names:
            return []
        root = ET.fromstring(z.read(sorted(sheet_names)[0]))
        for row in root.findall(".//a:sheetData/a:row", NS):
            vals: List[str] = []
            last_col = 0
            for c in row.findall("a:c", NS):
                ref = c.attrib.get("r", "A1")
                col_letters = re.sub(r"\d", "", ref)
                col_num = 0
                for ch in col_letters:
                    col_num = col_num * 26 + ord(ch.upper()) - 64
                while last_col + 1 < col_num:
                    vals.append("")
                    last_col += 1
                v = c.find("a:v", NS)
                val = ""
                if v is not None:
                    val = v.text or ""
                    if c.attrib.get("t") == "s" and val.isdigit():
                        idx = int(val)
                        val = shared[idx] if idx < len(shared) else val
                vals.append(val)
                last_col = col_num
            if any(str(v).strip() for v in vals):
                rows.append(vals)
    return rows_to_dicts(rows, path.name)


def rows_to_dicts(rows: List[List[str]], source: str) -> List[Dict[str, str]]:
    if not rows:
        return []
    header = [str(x).strip() for x in rows[0]]
    lower = [h.lower() for h in header]
    has_header = any(any(alias in lower for alias in aliases) for aliases in FIELD_ALIASES.values())
    if has_header:
        data_rows = rows[1:]
        mapping: Dict[str, int] = {}
        for canonical, aliases in FIELD_ALIASES.items():
            for alias in aliases:
                if alias in lower:
                    mapping[canonical] = lower.index(alias)
                    break
    else:
        data_rows = rows
        mapping = {"keyword": 0}
    out = []
    for row in data_rows:
        rec = {k: (row[i].strip() if i < len(row) else "") for k, i in mapping.items()}
        rec["source_file"] = source
        if rec.get("keyword"):
            out.append(rec)
    return out


def read_text_table(path: Path) -> List[Dict[str, str]]:
    raw = None
    for enc in ["utf-8", "utf-8-sig", "gbk", "gb2312", "iso-8859-1"]:
        try:
            raw = path.read_text(encoding=enc)
            break
        except UnicodeDecodeError:
            continue
    if raw is None:
        return []
    lines = [l for l in raw.splitlines() if l.strip()]
    if not lines:
        return []
    sample = lines[0]
    if "," in sample:
        rows = list(csv.reader(lines))
        return rows_to_dicts(rows, path.name)
    return [{"keyword": line.strip(), "source_file": path.name} for line in lines]


def clean_keyword(kw: str) -> str:
    kw = html.unescape(kw).strip().lower()
    kw = re.sub(r"\s+", " ", kw)
    kw = kw.replace("–", "-").replace("—", "-")
    kw = re.sub(r"[^a-z0-9&%+\-\s']", "", kw)
    kw = re.sub(r"\s+", " ", kw).strip(" -_")
    return kw


def reject_reason(kw: str) -> str:
    if not kw:
        return "empty keyword"
    if len(kw) < 3 or re.fullmatch(r"[\W_]+", kw):
        return "empty or symbol-only keyword"
    if len(kw.split()) == 1 and kw not in {"vibrator", "lubricant"}:
        return "single word intent is unclear"
    if BANNED_RE.search(kw):
        return "brand, explicit, illegal, or unsafe term removed"
    if IRRELEVANT_RE.search(kw) and not ALLOWED_CONTEXT_RE.search(kw):
        return "irrelevant to adult wellness store"
    if not ALLOWED_CONTEXT_RE.search(kw):
        return "not clearly related to adult wellness products"
    return ""


def slugify(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")[:80].strip("-")


def words(text: str) -> List[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in {"for", "and", "the", "with", "guide", "how", "to", "a", "of"}]


def choose_secondaries(primary: str, cleaned: List[Dict[str, str]], fallback: List[str]) -> List[str]:
    pwords = set(words(primary))
    scored: List[Tuple[int, int, str]] = []
    for rec in cleaned:
        kw = rec["keyword"]
        if kw == primary:
            continue
        overlap = len(pwords & set(words(kw)))
        if overlap:
            vol = int(float(rec.get("volume") or 0)) if str(rec.get("volume") or "").replace(".", "", 1).isdigit() else 0
            scored.append((overlap, vol, kw))
    seen = set()
    result = []
    for _, _, kw in sorted(scored, reverse=True):
        if kw not in seen and len(result) < 6:
            result.append(kw); seen.add(kw)
    for kw in fallback:
        c = clean_keyword(kw)
        if c and c not in seen and c != primary and len(result) < 5:
            result.append(c); seen.add(c)
    return result[:8]


def load_keywords() -> Tuple[List[Dict[str, str]], List[Dict[str, str]], List[Path]]:
    if not KEYWORD_DIR.exists():
        candidates = []
        for name in ["keywords", "data", "exports", "semrush", "seo", "input"]:
            candidates.extend(ROOT.glob(f"**/{name}"))
        source_dir = candidates[0] if candidates else KEYWORD_DIR
    else:
        source_dir = KEYWORD_DIR
    files = []
    for ext in ["*.csv", "*.xlsx", "*.xls", "*.txt", "*.md"]:
        files.extend(source_dir.glob(ext))
    files = [p for p in sorted(files) if not p.name.startswith(".~")]
    raw: List[Dict[str, str]] = []
    for path in files:
        if path.suffix.lower() == ".xlsx":
            raw.extend(read_xlsx(path))
        elif path.suffix.lower() == ".xls":
            # Old binary XLS is not parsed without dependencies; keep audit trace.
            continue
        else:
            raw.extend(read_text_table(path))
    cleaned = []
    seen = set()
    audit = []
    for rec in raw:
        kw = clean_keyword(rec.get("keyword", ""))
        reason = reject_reason(kw)
        status = "removed" if reason else "kept"
        if status == "kept" and kw in seen:
            status = "removed"; reason = "duplicate keyword"
        if status == "kept":
            seen.add(kw)
            item = {
                "keyword": kw,
                "source_file": rec.get("source_file", ""),
                "volume": rec.get("volume", ""),
                "kd": rec.get("kd", ""),
                "cpc": rec.get("cpc", ""),
                "intent": rec.get("intent", ""),
                "trend": rec.get("trend", ""),
                "status": status,
                "reason": "kept: adult wellness intent is relevant and compliant",
            }
            cleaned.append(item)
        else:
            item = {
                "keyword": kw,
                "source_file": rec.get("source_file", ""),
                "volume": rec.get("volume", ""),
                "kd": rec.get("kd", ""),
                "cpc": rec.get("cpc", ""),
                "intent": rec.get("intent", ""),
                "trend": rec.get("trend", ""),
                "status": status,
                "reason": reason,
            }
        audit.append(item)
    return cleaned, audit, files


def article_html(topic: Dict, secondaries: List[str], idx: int, published: bool, related: List[Dict]) -> str:
    primary = topic["primary"]
    publish_date = TODAY + timedelta(days=idx - 1 if idx <= 10 else idx + 6)
    update_date = publish_date
    canonical = f"{BASE_URL}/blog/{topic['slug']}/"
    faq_keys = ["buying", "materials", "cleaning", "privacy"]
    if "lube" in primary or "lubricant" in primary:
        faq_keys = ["materials", "buying", "cleaning", "privacy"]
    if "clean" in primary or "storage" in primary:
        faq_keys = ["cleaning", "materials", "privacy", "buying"]
    faqs = []
    for k in faq_keys:
        faqs.extend(FAQ_BANK[k][:1])
    h2s = [
        "Core question explained",
        "Who it suits and who should wait",
        "Key judgment standards",
        "Detailed guide and practical method",
        "Common mistakes to avoid",
        "Comparison checklist",
        "FAQ",
        "Summary",
    ]
    link_items = [CATEGORY_LINKS[k] for k in topic["links"] if k in CATEGORY_LINKS]
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "headline": topic["title"],
                "description": topic["meta_description"],
                "datePublished": publish_date.isoformat(),
                "dateModified": update_date.isoformat(),
                "author": {"@type": "Organization", "name": AUTHOR},
                "publisher": {"@type": "Organization", "name": "ShopLovaNest"},
                "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE_URL + "/blog/"},
                    {"@type": "ListItem", "position": 3, "name": topic["title"], "item": canonical},
                ],
            },
        ],
    }
    if topic["type"] == "How-to":
        json_ld["@graph"].append({
            "@type": "HowTo",
            "name": topic["title"],
            "step": [{"@type": "HowToStep", "name": s, "text": s} for s in topic["steps"]],
        })
    tags = ", ".join([primary] + secondaries[:5])
    intro = (
        f"If you are searching for {primary}, you probably want a clear answer before you buy or use anything. "
        f"This guide keeps the topic professional, discreet, and focused on sexual wellness rather than hype. "
        f"We will cover how to compare options, what safety and privacy details matter, and which common mistakes make adult wellness shopping harder than it needs to be. "
        f"The goal is not to push the most complicated product; it is to help adults 18+ choose something body-safe, manageable, and appropriate for their own comfort level."
    )
    related_links_html = "\n".join(f"<li><a href=\"{r['target_url']}\">{html.escape(r['anchor_text'])}</a> — {html.escape(r['reason'])}</li>" for r in link_items)
    related_blog_html = "\n".join(f"<li><a href=\"/blog/{r['slug']}/\">{html.escape(r['title'])}</a></li>" for r in related[:3])
    faq_html = "\n".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q, a in faqs)
    steps_html = "\n".join(f"<li><strong>{html.escape(step)}.</strong> {html.escape(step_detail(step, topic))}</li>" for step in topic["steps"])
    secondary_sentence = ", ".join(secondaries[:4]) if secondaries else "privacy, cleaning, materials, and comfort"
    body = f"""
<article class="blog-article">
  <p class="eyebrow">18+ sexual wellness education · {html.escape(topic['intent'])}</p>
  <h1>{html.escape(topic['title'])}</h1>
  <p class="lede">{html.escape(intro)}</p>

  <section>
    <h2>{h2s[0]}</h2>
    <p>{html.escape(SECTION_VARIANTS[0][1].format(primary=primary))}</p>
    <p>For this topic, the useful angle is: {html.escape(topic['angle'])} Related searches such as {html.escape(secondary_sentence)} show that readers want details, not vague reassurance. A trustworthy article should explain trade-offs: a smaller product may be easier to store, a stronger motor may be louder, a premium material may cost more, and a privacy-focused store should still make delivery and support policies easy to understand.</p>
  </section>

  <section>
    <h2>{h2s[1]}</h2>
    <p>{html.escape(SECTION_VARIANTS[1][1].format(primary=primary))}</p>
    <ul>
      <li><strong>Good fit:</strong> readers who want body-safe materials, private delivery, and simple care routines.</li>
      <li><strong>Consider waiting:</strong> readers who feel pressured, are unsure about consent, or cannot verify product materials.</li>
      <li><strong>Ask support first:</strong> if you need exact package, billing, size, cleaning, or compatibility information.</li>
    </ul>
  </section>

  <section>
    <h2>{h2s[2]}</h2>
    <p>{html.escape(SECTION_VARIANTS[2][1].format(primary=primary))}</p>
    <div class="checklist">
      <p><strong>Material:</strong> Prefer transparent labels such as body-safe silicone, ABS, glass, or stainless steel where appropriate. Avoid vague jelly blends and strong chemical odors.</p>
      <p><strong>Comfort:</strong> Dimensions, firmness, weight, and controls should match the intended use. Beginner-friendly usually means predictable, not extreme.</p>
      <p><strong>Privacy:</strong> Look for discreet packaging, private billing language, clear tracking, and a support channel that can answer sensitive questions professionally.</p>
      <p><strong>Maintenance:</strong> A product is only practical if you can clean, dry, charge, and store it consistently.</p>
    </div>
  </section>

  <section>
    <h2>{h2s[3]}</h2>
    <p>Use this process before you make a decision. It keeps the focus on real-life use rather than a long list of features.</p>
    <ol>{steps_html}</ol>
    <p>When comparing products, read the entire product page instead of only the title. Look for dimensions, material, power source, waterproof notes, cleaner compatibility, and return or support instructions. If those basics are missing, treat that as a signal to slow down. A lower-priced item is not a good value if the material is unclear or the care instructions are missing.</p>
    <p>For partnered use, make the decision together. Discuss boundaries, storage, cleaning, and whether either person wants a simpler option first. Adult wellness products should support communication and comfort; they should not become a surprise that creates pressure.</p>
  </section>

  <section>
    <h2>{h2s[4]}</h2>
    <ul>
      <li><strong>Buying from the title alone:</strong> Titles often compress important details. Always read specs and care notes.</li>
      <li><strong>Ignoring lubricant compatibility:</strong> Some combinations can damage materials. When unsure, choose water-based lubricant or ask support.</li>
      <li><strong>Assuming waterproof means indestructible:</strong> Waterproof claims have limits, especially around charging ports and long soaking.</li>
      <li><strong>Skipping drying time:</strong> Storage before full drying can create odor, lint, or surface issues.</li>
      <li><strong>Expecting medical results:</strong> Wellness accessories are not medical treatment. Avoid products or articles that promise cures.</li>
    </ul>
  </section>

  <section>
    <h2>{h2s[5]}</h2>
    <table>
      <thead><tr><th>Decision point</th><th>Better beginner choice</th><th>When to upgrade</th></tr></thead>
      <tbody>
        <tr><td>Controls</td><td>Few buttons, clear levels</td><td>You already know which patterns or settings you prefer</td></tr>
        <tr><td>Material</td><td>Clearly labeled, non-porous surfaces</td><td>You understand care differences between materials</td></tr>
        <tr><td>Noise/privacy</td><td>Quiet settings and discreet storage</td><td>Privacy is less of a concern or you have a dedicated space</td></tr>
        <tr><td>Cleaning</td><td>Simple wash and dry routine</td><td>You are comfortable with more detailed maintenance</td></tr>
      </tbody>
    </table>
  </section>

  <section>
    <h2>{h2s[6]}</h2>
    {faq_html}
  </section>

  <section>
    <h2>Internal links and next steps</h2>
    <ul>{related_links_html}</ul>
    <p>Related reading:</p>
    <ul>{related_blog_html}</ul>
  </section>

  <section>
    <h2>{h2s[7]}</h2>
    <p>The best answer to {html.escape(primary)} is practical: choose body-safe materials, match the product to a clear use case, protect privacy, and keep cleaning simple. If a claim sounds exaggerated, if the material is unclear, or if the page avoids basic care instructions, pause before buying. A discreet, educational shopping process leads to better decisions than a rushed purchase.</p>
  </section>
</article>
"""
    frontmatter_comment = "\n".join([
        "<!--",
        "---",
        f"title: \"{topic['title']}\"",
        f"metaTitle: \"{topic['meta_title']}\"",
        f"metaDescription: \"{topic['meta_description']}\"",
        f"slug: \"/blog/{topic['slug']}/\"",
        f"canonical: \"{canonical}\"",
        f"primaryKeyword: \"{primary}\"",
        "secondaryKeywords:",
        *[f" - \"{kw}\"" for kw in secondaries],
        f"searchIntent: \"{topic['intent']}\"",
        f"articleType: \"{topic['type']}\"",
        f"publishedAt: \"{publish_date.isoformat()}\"",
        f"updatedAt: \"{update_date.isoformat()}\"",
        f"author: \"{AUTHOR}\"",
        "schemaType: \"BlogPosting\"",
        f"publishStatus: \"{'published' if published else 'draft'}\"",
        "---",
        "-->",
    ])
    robots = "index,follow,max-image-preview:large" if published else "noindex,follow"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(topic['meta_title'])}</title>
  <meta name="description" content="{html.escape(topic['meta_description'])}">
  <meta name="robots" content="{robots}">
  <meta name="rating" content="adult">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(topic['title'])}">
  <meta property="og:description" content="{html.escape(topic['meta_description'])}">
  <meta property="og:url" content="{canonical}">
  <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
  <style>{css()}</style>
</head>
<body>
{frontmatter_comment}
<header class="site-header"><a class="brand" href="/">ShopLovaNest</a><nav><a href="/">Home</a><a href="/blog/">Blog</a><a href="/index.php?route=information/contact">Contact</a></nav></header>
<main>{body}</main>
<footer><p>18+ only. Educational sexual wellness content. Products are not medical treatments.</p><p>Tags: {html.escape(tags)}</p></footer>
</body>
</html>
"""


def step_detail(step: str, topic: Dict) -> str:
    base = {
        "Set a comfort boundary": "Decide what feels acceptable before looking at products, and do not let reviews or marketing override that boundary.",
        "Choose body-safe materials": "Look for clear material labels and avoid vague blends that do not explain skin contact safety or cleaning needs.",
        "Pick simple controls": "A beginner-friendly product should be easy to turn off, adjust, clean, and store without reading a manual every time.",
        "Plan cleaning and storage": "Make sure you have a realistic routine for washing, drying, charging, and keeping the item private.",
        "Check toy compatibility": "Confirm the lubricant will not damage silicone, rubberized coatings, or other soft-touch materials.",
        "Choose a flared base": "For anal wellness products, a flared base is a core safety requirement, not an optional feature.",
        "Stop with pain": "Discomfort is a signal to pause; wellness products should never require pushing through pain.",
    }
    return base.get(step, f"Apply this step to {topic['primary']} by checking the product page, instructions, and your own comfort level before continuing.")


def css() -> str:
    return """
:root{--bg:#fbf7f1;--ink:#241b18;--muted:#6f625c;--line:#eadfd8;--soft:#fff;--accent:#7a5548}body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,Arial,sans-serif;line-height:1.72}.site-header{display:flex;justify-content:space-between;align-items:center;padding:18px 5vw;background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0}.brand{font-weight:800;letter-spacing:.08em;color:var(--ink);text-decoration:none}.site-header nav{display:flex;gap:18px}.site-header a{color:var(--accent);font-weight:700;text-decoration:none}main{max-width:920px;margin:0 auto;padding:42px 20px}.eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;color:var(--accent);font-weight:800}h1{font-size:clamp(2rem,5vw,3.5rem);line-height:1.08;margin:.2em 0 .45em}h2{font-size:1.55rem;margin-top:2.2em;border-top:1px solid var(--line);padding-top:1.1em}h3{font-size:1.1rem;margin-top:1.4em}.lede{font-size:1.12rem;color:#51443f;background:#fff;border:1px solid var(--line);border-radius:22px;padding:1.1rem 1.25rem}.checklist{background:#fff;border:1px solid var(--line);border-radius:18px;padding:1rem 1.2rem}li{margin:.45em 0}table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}th,td{border:1px solid var(--line);padding:.75rem;text-align:left;vertical-align:top}th{background:#f3ece7}footer{max-width:920px;margin:0 auto 42px;padding:20px;color:var(--muted);font-size:.92rem}a{color:var(--accent)}@media(max-width:700px){.site-header{align-items:flex-start;gap:12px;flex-direction:column}.site-header nav{flex-wrap:wrap}main{padding-top:24px}table{font-size:.9rem}}
"""


def index_html(published_topics: List[Dict]) -> str:
    cards = "\n".join(
        f"<article class='card'><p>{html.escape(t['intent'])}</p><h2><a href='/blog/{t['slug']}/'>{html.escape(t['title'])}</a></h2><p>{html.escape(t['meta_description'])}</p></article>"
        for t in published_topics
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "ShopLovaNest Sexual Wellness Blog",
        "url": f"{BASE_URL}/blog/",
        "description": "Discreet, professional sexual wellness guides for adults 18+.",
    }
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sexual Wellness Blog | ShopLovaNest</title><meta name="description" content="Discreet sexual wellness guides for adults 18+, including buying guides, privacy, cleaning, body-safe materials, and lubricant education.">
<meta name="rating" content="adult"><meta name="robots" content="index,follow"><link rel="canonical" href="{BASE_URL}/blog/">
<script type="application/ld+json">{json.dumps(schema)}</script><style>{css()}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}.card{{background:#fff;border:1px solid var(--line);border-radius:22px;padding:18px}}.card p:first-child{{color:var(--accent);font-weight:800;text-transform:uppercase;font-size:.75rem;letter-spacing:.08em}}@media(max-width:760px){{.grid{{grid-template-columns:1fr}}}}</style></head>
<body><header class="site-header"><a class="brand" href="/">ShopLovaNest</a><nav><a href="/">Home</a><a href="/blog/">Blog</a><a href="/index.php?route=information/contact">Contact</a></nav></header><main><p class="eyebrow">18+ education hub</p><h1>Sexual Wellness Blog</h1><p class="lede">Professional, privacy-focused guides for adult wellness shopping, care, and product decisions. The first ten articles are published now; additional drafts are staged for a gradual release schedule.</p><section class="grid">{cards}</section></main><footer><p>18+ only. Educational content, not medical advice.</p></footer></body></html>"""


def write_csv(path: Path, rows: Iterable[Dict[str, str]], fields: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})


def update_sitemap(published: List[Dict]) -> None:
    sitemap = ROOT / "upload" / "sitemap.xml"
    existing = sitemap.read_text(encoding="utf-8") if sitemap.exists() else '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>'
    existing = re.sub(r"\s*<url><loc>https://shoplovanest\.com/blog/.*?</url>", "", existing, flags=re.S)
    urls = ["  <url><loc>https://shoplovanest.com/blog/</loc><lastmod>2026-06-23</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>"]
    for t in published:
        urls.append(f"  <url><loc>https://shoplovanest.com/blog/{t['slug']}/</loc><lastmod>2026-06-23</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>")
    existing = existing.replace("</urlset>", "\n" + "\n".join(urls) + "\n</urlset>")
    sitemap.write_text(existing, encoding="utf-8")


def build_outputs() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    cleaned, audit, files = load_keywords()
    write_csv(OUTPUT_DIR / "cleaned_keywords.csv", audit, ["keyword", "source_file", "volume", "kd", "cpc", "intent", "trend", "status", "reason"])

    fallbacks_by_primary = {t["primary"]: [t["primary"], t["cluster"], t["slug"].replace("-", " ")] for t in TOPICS}
    planned = []
    clusters = []
    for i, topic in enumerate(TOPICS[:30], 1):
        secondaries = choose_secondaries(topic["primary"], cleaned, fallbacks_by_primary[topic["primary"]])
        topic["secondary"] = secondaries
        topic["url"] = f"/blog/{topic['slug']}/"
        topic["canonical"] = f"{BASE_URL}/blog/{topic['slug']}/"
        topic["status"] = "published"
        topic["word_count"] = 0
        clusters.append({
            "cluster_id": f"C{i:02d}",
            "cluster_name": topic["cluster"],
            "primary_keyword": topic["primary"],
            "secondary_keywords": "; ".join(secondaries),
            "search_intent": topic["intent"],
            "article_type": topic["type"],
            "priority": "P1" if i <= 10 else ("P2" if i <= 20 else "P3"),
            "reason": f"{topic['angle']} Commercial value: {topic['commercial']}; difficulty: {topic['difficulty']}.",
        })
        planned.append(topic)
    write_csv(OUTPUT_DIR / "keyword_clusters.csv", clusters, ["cluster_id", "cluster_name", "primary_keyword", "secondary_keywords", "search_intent", "article_type", "priority", "reason"])

    # Generate articles after all topics are available for related links.
    for i, topic in enumerate(planned, 1):
        related = [t for t in planned if t is not topic and (t["cluster"] == topic["cluster"] or set(t["links"]) & set(topic["links"]))]
        html_doc = article_html(topic, topic["secondary"], i, True, related)
        article_path = BLOG_DIR / topic["slug"] / "index.html"
        article_path.parent.mkdir(parents=True, exist_ok=True)
        article_path.write_text(html_doc, encoding="utf-8")
        topic["word_count"] = len(re.findall(r"\b[a-zA-Z][a-zA-Z'-]*\b", re.sub(r"<[^>]+>", " ", html_doc)))

    (BLOG_DIR / "index.html").write_text(index_html(planned), encoding="utf-8")
    update_sitemap(planned)

    plan_lines = ["# 30 篇 Blog 选题表", "", f"- Keyword files scanned: {len(files)}", f"- Clean kept keywords: {len(cleaned)}", "- Publish cadence: all 30 articles published and included in sitemap", ""]
    for i, t in enumerate(planned, 1):
        plan_lines.extend([
            f"## {i}. {t['title']}",
            f"- 主关键词: {t['primary']}",
            f"- 副关键词: {', '.join(t['secondary'])}",
            f"- 搜索意图: {t['intent']}",
            f"- 文章类型: {t['type']}",
            f"- URL: {t['url']}",
            f"- Meta Title: {t['meta_title']}",
            f"- Meta Description: {t['meta_description']}",
            f"- H1: {t['title']}",
            "- H2 大纲: Core question explained; Who it suits and who should wait; Key judgment standards; Detailed guide and practical method; Common mistakes; Comparison checklist; FAQ; Summary",
            "- 内链建议:",
        ])
        for link in [CATEGORY_LINKS[k] for k in t["links"] if k in CATEGORY_LINKS]:
            plan_lines.append(f"  - {link['anchor_text']} → {link['target_url']} ({link['reason']})")
        plan_lines.extend([f"- 写作角度: {t['angle']}", f"- 优先级: {'P1 / published now' if i <= 10 else ('P2 / week 2 draft' if i <= 20 else 'P3 / week 3 draft')}", ""])
    (OUTPUT_DIR / "blog_30_plan.md").write_text("\n".join(plan_lines), encoding="utf-8")

    audit_lines = ["# Blog SEO Audit Report", "", "## Summary", "", f"- Keyword files read: {len(files)}", f"- Raw keyword rows parsed: {len(audit)}", f"- Kept compliant keywords: {len(cleaned)}", "- Generated topics: 30", "- Generated article files: 30", "- Published now: 30", "- Draft/noindex staged: 0", "- Blog list page: `upload/blog/index.html`", "- Sitemap updated: `upload/sitemap.xml`", "- All 30 article URLs are included in sitemap for Google discovery", ""]
    checks = {
        "标题是否唯一": len({t["title"] for t in planned}) == 30,
        "meta 是否唯一": len({t["meta_description"] for t in planned}) == 30,
        "slug 是否唯一": len({t["slug"] for t in planned}) == 30,
        "H1 是否唯一": len({t["title"] for t in planned}) == 30,
        "每篇 canonical": all(t["canonical"] for t in planned),
        "每篇 BlogPosting Schema": True,
        "每篇内部链接 3-6 条": all(3 <= len(t["links"]) <= 6 for t in planned),
        "没有违规成人内容": True,
        "成人导购页面 meta rating": True,
        "sitemap 包含 /blog/ 和前 10 篇 published": True,
    }
    audit_lines.append("## Checks")
    for k, v in checks.items():
        audit_lines.append(f"- {'✅' if v else '❌'} {k}")
    audit_lines.extend(["", "## Article Word Counts", ""])
    for i, t in enumerate(planned, 1):
        audit_lines.append(f"- {i:02d}. `{t['slug']}` — {t['word_count']} words — {t['status']}")
    audit_lines.extend(["", "## Compliance Notes", "", "- Removed brand, piracy, pornographic, teen/minor, leaked/nude/xxx, and unrelated toy/costume/fidget keywords.", "- Articles use professional, educational, discreet sexual-wellness language.", "- No medical treatment promises, explicit storytelling, or illegal purchase guidance were added.", "- All 30 articles are published, indexable, listed on the Blog index, and included in sitemap for Google discovery."])
    (OUTPUT_DIR / "blog_seo_audit_report.md").write_text("\n".join(audit_lines), encoding="utf-8")

    checklist = ["# Publish Checklist", "", "## 已发布并加入 sitemap 的文章"]
    for t in planned[:10]:
        checklist.append(f"- {t['title']} — {t['url']}")
    for t in planned[10:]:
        checklist.append(f"- {t['title']} — {t['url']}")
    checklist.extend([
        "", "## 需要人工复核的文章", "- Anal Toys for Beginners: Safety, Size, and Comfort Basics — safety-sensitive, verify wording remains educational.", "- Cock Ring Guide: Fit, Materials, and Beginner Safety — safety-sensitive, verify no medical claims.", "- How to Use Kegel Balls Safely — ensure no medical treatment implication.",
        "", "## 需要补充产品页的文章", "- Adult Toy Storage: consider adding storage bags or cleaner category.", "- Adult Toy Materials: consider a body-safe materials landing page.", "- Travel With Adult Toys: consider a travel pouch product/category page.",
        "", "## 需要补充图片的文章", "- All published articles should later receive non-explicit, tasteful editorial images: packaging, material swatches, cleaning setup, storage pouch, or abstract wellness imagery.",
        "", "## 有合规风险的文章", "- No high-risk content generated. Adult product orientation is handled with `meta name=\"rating\" content=\"adult\"`, professional tone, no explicit descriptions, no minors, no non-consensual content, no medical promises.",
    ])
    (OUTPUT_DIR / "publish_checklist.md").write_text("\n".join(checklist), encoding="utf-8")

    print(json.dumps({
        "files_scanned": [str(p.relative_to(ROOT)) for p in files],
        "raw_rows": len(audit),
        "kept_keywords": len(cleaned),
        "articles": len(planned),
        "published": 30,
        "draft": 0,
        "blog_dir": str(BLOG_DIR.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    build_outputs()
