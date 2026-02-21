# We track the cost of every 1,000 tokens based on current provider rates.
INPUT_COST_1K = 0.01 
OUTPUT_COST_1K = 0.03
MAX_BUDGET = 2.00 

class BudgetGuard:
    def __init__(self):
        # We initialize the total spend at zero.
        self.total_spend = 0.0

    def update_and_check(self, input_tokens, output_tokens):
        # We calculate the cost of the current interaction.
        cost = (input_tokens / 1000 * INPUT_COST_1K) + (output_tokens / 1000 * OUTPUT_COST_1K)
        
        # We add the cost to our running total.
        self.total_spend += cost
        print(f"Current session cost: ${self.total_spend:.4f}")

        # If we exceed the $2.00 limit, we trigger an emergency shutdown.
        if self.total_spend >= MAX_BUDGET:
            print("CRITICAL: Budget reached. Killing agent.")
            # We raise a custom error that the main loop cannot ignore.
            raise SystemExit("Budget reached. Hard kill switch activated.")

# How to use it in your loop:
# guard = BudgetGuard()
# guard.update_and_check(usage['input'], usage['output'])
