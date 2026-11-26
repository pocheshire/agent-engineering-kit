# Tab-separated order export specification

**Document metadata**

| Field | Value |
| --- | --- |
| Template version | 1 |
| Specification version and date | 0.1 · 2026-01-01 |
| Status | Draft example |
| Readers | Export implementer and reviewer |
| Sources | Synthetic brief in the next section. This example describes an invented application. |

## 1. Goal and scope

An operator can export order identifiers and quantities as tab-separated text
from the existing export command. The change covers a new output format for
that command. Changes to stored orders and the existing output are out of scope.

## 2. Current behavior

The example brief describes `orders export` as a command that writes CSV to
standard output. It preserves input row order and returns exit status `0` when
the export succeeds. Automation uses the existing CSV output.

## 3. Required behavior

### R1

- **Conditions** — The order fixture contains `A101` with quantity `2` and
  `A102` with quantity `5`, in that order.
- **Action** — Run `orders export --format tsv`.
- **Observable result** — Exit status is `0`. Standard output contains the
  `order_id` and `quantity` header and one row per order in the fixture order.
  Tabs separate the columns.

### R2

- **Conditions** — The same valid fixture is available.
- **Action** — Run `orders export` without specifying a format.
- **Observable result** — The command emits the existing CSV bytes and returns
  exit status `0`.

### R3

- **Conditions** — The fixture contains order `A101` with no quantity.
- **Action** — Run `orders export --format tsv`.
- **Observable result** — Exit status is `2`. Standard error describes the
  missing quantity for `A101`. Standard output is empty.

## 4. Contracts and constraints

The TSV stream uses UTF-8 and a line feed at the end of each row. In this
example, order IDs contain letters and digits, and quantities are integers.
The command validates all rows before writing TSV to standard output.

## 5. Impact and risks

The export command gains a format option. Existing automation continues to
receive CSV by default. Validating the whole TSV input before writing protects
consumers that would otherwise accept a partial export.

## 6. Acceptance criteria

| Requirement ID | Verification | Expected result |
| --- | --- | --- |
| [R1](#r1) | Run the TSV command on the valid fixture. Compare raw output bytes and exit status. | `order_id\tquantity\nA101\t2\nA102\t5\n`, status `0`. The escaped separators denote single tab and line-feed bytes. |
| [R2](#r2) | Run the command without a format option and compare it with the existing CSV baseline. | Exact baseline bytes and status `0`. |
| [R3](#r3) | Run the TSV command on the fixture with a missing quantity. Inspect both streams and exit status. | Empty standard output, a diagnostic identifying `A101` and the missing quantity on standard error, and status `2`. |

## 7. Decisions and open questions

The example brief specifies TSV as opt-in and preserves CSV by default. It
contains no open product decision for the stated scope.
