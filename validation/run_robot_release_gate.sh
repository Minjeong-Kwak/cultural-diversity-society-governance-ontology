#!/usr/bin/env bash
# CDSG release gate: OWL 2 DL profile, HermiT consistency/classification,
# positive-inference fixture and four inconsistency fixtures.
# Usage: bash validation/run_robot_release_gate.sh [path/to/robot.jar]
set -euo pipefail
PKG="$(cd "$(dirname "$0")/.." && pwd)"
JAR="${1:-$PKG/validation/external/robot.jar}"
CAT="$PKG/validation/catalog-v001.xml"
OUT="$PKG/validation/results"
MERGED="$PKG/data/cdsg_v1.0.0-rc.2_active_merged.ttl"
CORE="$PKG/ontology/cdsg_core_v1.0.0-rc.2.owl"
R="java -Xmx6g -jar $JAR"
mkdir -p "$OUT"
{
echo "ROBOT: $($R --version 2>/dev/null | tail -1)"
echo "== OWL 2 DL profile: core";   $R validate-profile --profile DL --catalog "$CAT" --input "$CORE"
echo "== OWL 2 DL profile: merged"; $R validate-profile --profile DL --catalog "$CAT" --input "$MERGED"
echo "== HermiT: core";   $R reason --reasoner HermiT --catalog "$CAT" --input "$CORE"   --equivalent-classes-allowed all --output "$OUT/core-hermit-reasoned.owl" && echo "consistent, no unsatisfiable classes"
echo "== HermiT: merged"; $R reason --reasoner HermiT --catalog "$CAT" --input "$MERGED" --equivalent-classes-allowed all --output "$OUT/merged-hermit-reasoned.owl" && echo "consistent, no unsatisfiable classes"
echo "== HermiT: class assertions of the merged graph (results/merged-inferred-class-assertions.ttl)"
$R reason --reasoner HermiT --catalog "$CAT" --input "$MERGED" --axiom-generators "ClassAssertion" --include-indirect true --output "$OUT/merged-inferred-class-assertions.ttl"
TMP="$PKG/validation/.gate_tmp.ttl"
cat "$MERGED" "$PKG/validation/reasoning/positive_fixture.ttl" > "$TMP"
echo "== HermiT: positive fixture (class assertions written to results/positive-fixture-inferred.ttl)"
$R reason --reasoner HermiT --catalog "$CAT" --input "$TMP" --axiom-generators "ClassAssertion" --include-indirect true --output "$OUT/positive-fixture-inferred.ttl"
cat "$MERGED" "$PKG/validation/reasoning/inconsistent_identity_fixture.ttl" > "$TMP"
echo "== HermiT: inconsistency fixture (must be reported inconsistent)"
NEG="$($R reason --reasoner HermiT --catalog "$CAT" --input "$TMP" --output "$OUT/.discard.owl" 2>&1 || true)"
if echo "$NEG" | grep -q "inconsistent"; then echo "PASS: reasoner reports inconsistency"; else echo "FAIL: fixture not detected"; fi
cat "$MERGED" "$PKG/validation/reasoning/inconsistent_curated_source_fixture.ttl" > "$TMP"
echo "== HermiT: curated-and-source fixture (must be reported inconsistent)"
NEG="$($R reason --reasoner HermiT --catalog "$CAT" --input "$TMP" --output "$OUT/.discard.owl" 2>&1 || true)"
if echo "$NEG" | grep -q "inconsistent"; then echo "PASS: reasoner reports inconsistency"; else echo "FAIL: fixture not detected"; fi
cat "$MERGED" "$PKG/validation/reasoning/inconsistent_document_version_fixture.ttl" > "$TMP"
echo "== HermiT: document-and-version fixture (must be reported inconsistent)"
NEG="$($R reason --reasoner HermiT --catalog "$CAT" --input "$TMP" --output "$OUT/.discard.owl" 2>&1 || true)"
if echo "$NEG" | grep -q "inconsistent"; then echo "PASS: reasoner reports inconsistency"; else echo "FAIL: fixture not detected"; fi
cat "$MERGED" "$PKG/validation/reasoning/inconsistent_two_statements_fixture.ttl" > "$TMP"
echo "== HermiT: category with two specifying statements of different types (must be reported inconsistent)"
NEG="$($R reason --reasoner HermiT --catalog "$CAT" --input "$TMP" --output "$OUT/.discard.owl" 2>&1 || true)"
if echo "$NEG" | grep -q "inconsistent"; then echo "PASS: reasoner reports inconsistency"; else echo "FAIL: fixture not detected"; fi
rm -f "$TMP" "$OUT/.discard.owl"
} 2>&1 | grep -v JAVA_TOOL_OPTIONS | tee "$OUT/robot-release-gate.txt"
