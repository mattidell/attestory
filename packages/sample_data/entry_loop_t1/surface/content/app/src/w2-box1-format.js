export const W2_BOX1_FORMAT = {
  "field": "W-2 Box 1",
  "hintLabel": "dollars and cents",
  "errorLabel": "positive dollar amount",
  "examples": ["90000", "90000.50"],
  "commaGrouping": "refused",
  "maxFractionDigits": 2,
  "requirePositive": true
};

function commaGroupingText(format) {
  return format.commaGrouping === "refused"
    ? "without commas"
    : "with comma grouping";
}

export function formatW2Box1Hint(format = W2_BOX1_FORMAT) {
  return `Enter ${format.hintLabel} ${commaGroupingText(format)}, for example ${format.examples.join(
    " or "
  )}.`;
}

export function formatW2Box1Error(format = W2_BOX1_FORMAT) {
  return `Enter ${format.field} as a ${format.errorLabel} ${commaGroupingText(
    format
  )} and with no more than ${format.maxFractionDigits} decimal places.`;
}
