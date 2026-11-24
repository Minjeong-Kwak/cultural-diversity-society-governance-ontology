#!/usr/bin/env python3
"""Obsolete since v1.0.0-rc.2. The rc.1 Pellet route through Owlready2 is retired.
Reasoning, consistency and the fixtures run through ROBOT 1.9.10 with HermiT:
    bash validation/run_robot_release_gate.sh validation/external/robot.jar
    python validation/scripts/check_reasoning_fixture.py
"""
import sys
print(__doc__, file=sys.stderr)
sys.exit(2)
