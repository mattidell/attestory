export const W2_BOX1_FORMAT = {
  "field": "W-2 Box 1",
  "hintLabel": "dollars and cents",
  "errorLabel": "positive dollar amount",
  "examples": ["90000", "90000.50"],
  "commaGrouping": "accepted",
  "currencySymbol": "$",
  "currencyPrefix": "accepted",
  "maxFractionDigits": 2,
  "requirePositive": true
};

function acceptedFormattingText(format) {
  const parts = [];
  parts.push(
    format.commaGrouping === "accepted"
      ? "with or without comma grouping"
      : "without commas"
  );
  parts.push(
    format.currencyPrefix === "accepted"
      ? `an optional ${format.currencySymbol} prefix`
      : `no leading ${format.currencySymbol} prefix`
  );
  return parts.join(" and ");
}

export function formatW2Box1Hint(format = W2_BOX1_FORMAT) {
  return `Enter ${format.hintLabel} ${acceptedFormattingText(format)}, for example ${format.examples.join(
    " or "
  )}.`;
}

export function formatW2Box1Error(format = W2_BOX1_FORMAT) {
  return `Enter ${format.field} as a ${format.errorLabel} ${acceptedFormattingText(format)}, and with no more than ${format.maxFractionDigits} decimal places.`;
}
