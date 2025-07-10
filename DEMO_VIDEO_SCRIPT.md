# Spark AI Shopping Assistant - Demo Video Script (1:50 seconds)

## Part 1: Problem Statement (45-50 seconds)
**[Full Screen - Narrator Voice]**

"Online shopping is great — fast, convenient, and full of options. But let's be honest — sometimes, it's overwhelming.

Take buying a phone, for example. You set a budget. You find a few options. But then the questions begin:
- Which one has the best camera?
- Is the battery reliable?
- Should I go for a newer model or the one with better reviews?

You open tab after tab — YouTube reviews, comparison sites, store locators, price trackers.
Before you know it, you've spent 40 minutes researching… and you're more confused than when you started.

And just when you think you've decided — you wonder if it's cheaper in a nearby store.
Or if you're missing a better deal.
Or if the reviews are even real.

It's exhausting. It's not the experience online shopping promised us."

## Part 2: Solution Demo (60 seconds)
**[Split Screen - Left: Commands | Right: Website]**

### Demo Commands in Sequence:

1. **Enable AI Mode** (5 seconds)
   - Click the AI toggle
   - *"Meet Spark AI - your smart shopping assistant"*

2. **Budget Recommendation Flow** (20 seconds)
   ```
   "I have 25k budget, need best phone for camera and gaming"
   ```
   - Shows 3 recommendations with scores
   - *"AI analyzes 15+ phones instantly"*

3. **Check Store Prices** (10 seconds)
   ```
   "Check nearby stores"
   ```
   - Shows 4 stores with prices
   - *"Save ₹501 at TechZone Express!"*

4. **Cart Comparison Flow** (15 seconds)
   ```
   "Show me iPhone 13"
   ```
   → Add to cart
   ```
   "Show me OnePlus 11"
   ```
   → Add to cart
   ```
   "Compare phones in my cart for battery and camera"
   ```
   - Shows comparison table with review ratings
   - *"Winner: OnePlus 11 for battery (4.5/5 stars)"*

5. **Quick Review Check** (10 seconds)
   ```
   "What do reviews say?"
   ```
   - Shows review summary
   - *"86% users recommend, great camera quality"*

## Sequential Demo Commands for "Try Saying" Section:

```javascript
// Update the suggestions in agent.py
suggestions = [
    // Demo Flow 1: Budget Shopping
    "I have 25k budget, need best phone for camera and gaming",
    "Check nearby stores",
    
    // Demo Flow 2: Comparison
    "Show me iPhone 13",
    "Show me OnePlus 11", 
    "Compare phones in my cart for battery and camera",
    
    // Demo Flow 3: Quick Actions
    "Add it to my cart",
    "What do reviews say?",
    "Show my recent orders",
    
    // Demo Flow 4: Navigation
    "Take me to my cart",
    "Go to products page"
]
```

## Key Visual Elements:

### Split Screen Layout:
- **Left Side (30%)**: Command input with suggestions
- **Right Side (70%)**: Website showing results

### Highlight Features:
1. **Scores Display**: Camera: 85/100, Gaming: 90/100
2. **Store Savings**: Green highlight on savings amount
3. **Comparison Winner**: Trophy icon for best choice
4. **Review Stars**: Visual 5-star ratings

## Closing (10 seconds):
*"From 40 minutes of confusion to 2 minutes of confidence. Spark AI - Shopping made simple."*

## Technical Notes for Demo:

1. **Pre-load Data**: Ensure products are in cart before comparison demo
2. **Clear Navigation**: Each command should visibly navigate to the right page
3. **Response Time**: Keep AI responses under 1 second
4. **Visual Feedback**: Show loading states for commands

## Commands Copy-Paste List:

```
I have 25k budget, need best phone for camera and gaming
Check nearby stores
Show me iPhone 13
Show me OnePlus 11
Compare phones in my cart for battery and camera
What do reviews say?
Add it to my cart
Show my recent orders
Take me to my cart
```