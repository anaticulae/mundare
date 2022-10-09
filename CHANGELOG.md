# Changelog

Every noteable change is logged here.

## v0.8.0 (2022-10-09)

### Feature

* remove refs in invalid area (78eb71602c54)

### Chore

* upgrade requirements.txt (cc9f718d59ce)

## v0.7.1 (2022-10-05)

### Chore

* upgrade requirements.txt (8e762ecc0979)
* privileged container is not necessary (28f17f2632db)
* upgrade baw (965825b63ce4)
* upgrade requirements.txt (2447cb02a5b7)
* extend test data generator (9452047697ce)

## v0.7.0 (2022-09-29)

### Feature

* raise ValueError if empty translation is given (308ce6c2d30c)

### Fix

* adjust comparison for linux (2c2c8769a331)
* clarify error message (eb23aa6f24de)

### Chore

* upgrade requirements.txt (7aab57d2e24c)
* increase worker count on CI (99d0794bea56)
* add separate generator step (0e80894db06e)
* add Jenkinsfile (3c76813919ab)
* upgrade requirements.txt (26cbf1f2326d)

## v0.6.0

### Feature

* add select parameter to run a single cleanup (30b06c8c7a7b)

## v0.5.0

### Feature

* add parameter to skip cleanup resources (412e9b2df65b)

### Fix

* increase footnote bounding to catch all footnotes (80efe95f1eb0)

## v0.4.2

### Fix

* fix var access (7932a1b1e319)

## v0.4.1

## v0.4.0

### Feature

* clean footer and header area (70ee6156edbd)
* add headnote loader (452f33dc2336)

### Fix

* skip invalid footnote bounding (bc52ee3ead7b)

## v0.3.0

### Feature

* add footnotes (8497c0a64ab8)
* make hidden state more precise (4708fe4bfa7f)
* run separate invalidation steps (329f846e5e7b)
* add parameter to set different cleaning states (9618663909f0)
* allow single cleaning (ccc5765df0b4)

## v0.2.2

### Fix

* run cleanup without fontstore (acbbc029183a)

## v0.2.1

### Fix

* load hidden data (2ac5651e78c0)

## v0.2.0

### Feature

* hide pagenumber in cleanup step (6775ee1cceb3)
* add pagenumber loader (7bd152b94193)

## v0.1.5

### Feature

* log number of loaded horizontals and lines (bcfcc69d2504)

### Fix

* decrease required min width (52f64c2aa178)

## v0.1.4

### Fix

* do not fail on white page document, single page (0a38e08349ec)

## v0.1.3

## v0.1.2

### Feature

* inform about missing translation (58cc047ba202)

### Fix

* adjust file inputs (7ba14f7a71fe)

## v0.1.1

## v0.1.0

### Feature

* move code from rawmaker project (44a310117f71)

## v0.0.0 Initial release
