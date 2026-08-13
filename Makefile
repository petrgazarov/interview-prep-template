PYTHON ?= python3
LIMIT ?= 10

.PHONY: help today_snapshot leetcode_attempt_history leetcode_recent_attempts leetcode_active_redos validate_leetcode_attempts validate_today_snapshot validate

help:
	@printf 'Targets:\n'
	@printf '  today_snapshot              Build read-only JSON inputs for the $$today docket\n'
	@printf '  leetcode_attempt_history    Show all attempts for URL=<problem URL>\n'
	@printf '  leetcode_recent_attempts    Show recent attempts, newest first (LIMIT=10)\n'
	@printf '  leetcode_active_redos       Show active redos and per-date capacity\n'
	@printf '  validate_leetcode_attempts  Validate leetcode_attempts.csv\n'
	@printf '  validate_today_snapshot     Run docket-snapshot regression checks\n'
	@printf '  validate                    Run all validation and regression checks\n'

today_snapshot:
	@$(PYTHON) scripts/today_snapshot.py

leetcode_attempt_history:
	@$(PYTHON) scripts/leetcode_queries.py history --url "$(URL)"

leetcode_recent_attempts:
	@$(PYTHON) scripts/leetcode_queries.py recent --limit "$(LIMIT)"

leetcode_active_redos:
	@$(PYTHON) scripts/leetcode_queries.py active-redos

validate_leetcode_attempts:
	$(PYTHON) scripts/validate_leetcode_attempts.py
	$(PYTHON) -m unittest scripts/test_validate_leetcode_attempts.py scripts/test_leetcode_queries.py

validate_today_snapshot:
	$(PYTHON) -m unittest scripts/test_today_snapshot.py

validate: validate_leetcode_attempts validate_today_snapshot
