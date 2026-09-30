# Prompt Streamlining Plan

**Date:** 2026-02-24  
**Goal:** Reduce redundancy while maintaining atomicity and completeness

---

## Reference Documents Created

1. ✅ **00_EXECUTION_ORDER.md** - Dependency-based execution order (10 layers)
2. ✅ **COMMON_PATTERNS.md** - Reusable code patterns (10 patterns)
3. ✅ **AUTHORIZATION_REFERENCE.md** - Central authorization concepts (10 sections)

---

## Streamlining Strategy

### For Each Prompt:

1. **Keep:**
   - Objective statement
   - What it generates (output)
   - Dependencies (brief reference)
   - Core generation logic/code
   - Validation checklist

2. **Remove:**
   - Repeated authorization explanations → Reference AUTHORIZATION_REFERENCE.md
   - Repeated code patterns → Reference COMMON_PATTERNS.md
   - Detailed integration notes → Reference 00_EXECUTION_ORDER.md
   - Redundant examples already shown in other prompts
   - Verbose "Overview" sections that repeat the objective

3. **Replace With:**
   - Brief references: "See AUTHORIZATION_REFERENCE.md #3 for access levels"
   - Pattern references: "Uses soft delete pattern (COMMON_PATTERNS.md #1)"
   - Dependency references: "Dependencies: See 00_EXECUTION_ORDER.md Layer X"

---

## Estimated Reductions by Prompt

| Prompt | Current Lines | Target Lines | Reduction |
|--------|--------------|--------------|-----------|
| 01 | 150 | 120 | 20% |
| 02 | 100 | 80 | 20% |
| 03 | 180 | 100 | 44% |
| 04 | 150 | 90 | 40% |
| 05 | 140 | 90 | 36% |
| 06 | 250 | 130 | 48% |
| 07 | 200 | 120 | 40% |
| 08 | 120 | 100 | 17% |
| 09 | 180 | 120 | 33% |
| 09A | 200 | 140 | 30% |
| 09B | 140 | 100 | 29% |
| 09C | 150 | 110 | 27% |
| 10 | 130 | 110 | 15% |
| 11 | 160 | 120 | 25% |
| 13 | 280 | 150 | 46% |
| 14 | 140 | 120 | 14% |
| 15 | 400 | 250 | 38% |
| 16 | 220 | 130 | 41% |
| 17 | 300 | 160 | 47% |
| 18 | 450 | 220 | 51% |
| 19 | 280 | 150 | 46% |
| 20 | 320 | 170 | 47% |
| 21A | 200 | 140 | 30% |
| 21B | 250 | 160 | 36% |
| 21C | 180 | 120 | 33% |
| 22 | 350 | 200 | 43% |
| 23 | 380 | 210 | 45% |

**Total:** ~5,800 lines → ~3,400 lines (41% reduction)

---

## Implementation Approach

Given the scope (23 prompts), I'll create a streamlining script that:

1. Reads each prompt
2. Identifies redundant sections
3. Replaces with references
4. Maintains core content
5. Adds version note

**Manual Review Required For:**
- PROMPT 15 (authoritative source - minimal changes)
- PROMPT 01, 02 (swfaw_v2 internals - keep detailed)
- Test prompts (21A, 21B, 21C - need complete test code)

---

## Next Steps

1. ✅ Create reference documents
2. ⏳ Update each prompt systematically
3. ⏳ Update 00_INDEX.md with new references
4. ⏳ Update README.md with streamlining notes
5. ⏳ Create CHANGELOG.md documenting changes

---

## Success Criteria

✅ Each prompt is self-contained (atomic)  
✅ Each prompt depends only on previous layers (not explanations)  
✅ No repeated authorization concepts (reference AUTHORIZATION_REFERENCE.md)  
✅ No repeated code patterns (reference COMMON_PATTERNS.md)  
✅ Clear dependency chain (reference 00_EXECUTION_ORDER.md)  
✅ 40%+ reduction in total lines  
✅ All prompts still complete and usable  

---

## User Confirmation

Due to the scope (23 files to update), I recommend:

**Option A:** I create a streamlining script and apply to all prompts automatically  
**Option B:** I manually streamline each prompt with careful review  
**Option C:** I streamline a sample (3-5 prompts) for your review first  

Which approach would you prefer?
