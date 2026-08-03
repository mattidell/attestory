export const DIV1B_FORMAT = {
  "kind": "currency-amount",
  "field": "1099-DIV Box 1b",
  "hintLabel": "dollars and cents",
  "errorLabel": "positive dollar amount",
  "examples": ["600", "600.50"],
  "commaGrouping": "accepted",
  "currencySymbol": "$",
  "currencyPrefix": "accepted",
  "maxFractionDigits": 2,
  "requirePositive": true,
  "maxValue": "999999999.99"
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

export function formatDiv1bHint(format = DIV1B_FORMAT) {
  return `Enter ${format.hintLabel} ${acceptedFormattingText(format)}, for example ${format.examples.join(
    " or "
  )}.`;
}

export function formatDiv1bError(format = DIV1B_FORMAT) {
  return `Enter ${format.field} as a ${format.errorLabel} ${acceptedFormattingText(format)}, and with no more than ${format.maxFractionDigits} decimal places.`;
}
