/*
 * owner-review-embed.js — renders the per-page owner review UI into
 * #owner-review-root and composes the structured mailto submission.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-07-29 · Initial version: one card per screen with N questions x M
 *   options, a "no action required" default, a free-text field, and a client-side
 *   page_open_date_time per screen (no tracking beacon — the view record travels
 *   with the submission).
 */

(() => {
  // Set to false to disable the owner review UI for this client without touching the HTML pages.
  const OWNER_REVIEW_ENABLED = true;
  if (!OWNER_REVIEW_ENABLED) return;

  const root = document.getElementById("owner-review-root");
  if (!root) return;

  const screens = (typeof ownerReviewScreens !== "undefined" && ownerReviewScreens) || [];
  const questions = (typeof ownerReviewQuestions !== "undefined" && ownerReviewQuestions) || [];
  const options = (typeof ownerReviewOptions !== "undefined" && ownerReviewOptions) || [];
  const recipient = (typeof ownerReviewRecipient !== "undefined" && ownerReviewRecipient) || "";
  const businessName = (typeof garageConfig !== "undefined" && garageConfig.businessName) || document.title;

  // page_open_date_time per screen: recorded client-side only, the first
  // time each screen's card is expanded. No live ping anywhere -- this
  // rides along in the eventual submission, and reminders are driven by
  // absence of a submission at all, not by this partial data.
  const openedAt = {};

  function markOpened(screenName) {
    if (!openedAt[screenName]) openedAt[screenName] = new Date().toISOString();
  }

  function buildScreenCard(screen) {
    const card = document.createElement("details");
    card.className = "owner-review-card";
    card.addEventListener("toggle", () => { if (card.open) markOpened(screen.screenName); });

    const summary = document.createElement("summary");
    summary.textContent = screen.label;
    card.append(summary);

    const noActionRow = document.createElement("label");
    noActionRow.className = "owner-review-no-action";
    const noActionInput = document.createElement("input");
    noActionInput.type = "checkbox";
    noActionInput.dataset.screen = screen.screenName;
    noActionInput.dataset.role = "no-action";
    noActionRow.append(noActionInput, document.createTextNode(" No action required for this page"));
    card.append(noActionRow);

    const questionList = document.createElement("div");
    questionList.className = "owner-review-questions";
    questions.forEach((questionText, questionIndex) => {
      const qNumber = questionIndex + 1;
      const fieldset = document.createElement("fieldset");
      const legend = document.createElement("legend");
      legend.textContent = `${qNumber}. ${questionText}`;
      fieldset.append(legend);
      options.forEach((optionText, optionIndex) => {
        const optNumber = optionIndex + 1;
        const label = document.createElement("label");
        label.className = "owner-review-option";
        const input = document.createElement("input");
        input.type = "radio";
        input.name = `${screen.screenName}__q${qNumber}`;
        input.value = String(optNumber);
        input.dataset.screen = screen.screenName;
        input.dataset.question = String(qNumber);
        if (optNumber === 1) input.defaultChecked = true; // "Keep as-is" is the sensible default
        label.append(input, document.createTextNode(" " + optionText));
        fieldset.append(label);
      });
      questionList.append(fieldset);
    });
    card.append(questionList);

    const freeTextLabel = document.createElement("label");
    freeTextLabel.className = "owner-review-anything-else";
    freeTextLabel.textContent = "Anything else for this page?";
    const freeText = document.createElement("textarea");
    freeText.rows = 2;
    freeText.dataset.screen = screen.screenName;
    freeText.dataset.role = "anything-else";
    freeTextLabel.append(freeText);
    card.append(freeTextLabel);

    return card;
  }

  function composeSubmission() {
    const lines = [`${businessName}`, "{"];
    screens.forEach((screen) => {
      const parts = [`  screen_name: ${screen.screenName}`];
      parts.push(`page_open_date_time: ${openedAt[screen.screenName] || "not opened"}`);
      const noAction = root.querySelector(
        `input[data-role="no-action"][data-screen="${screen.screenName}"]`,
      );
      if (noAction && noAction.checked) {
        parts.push("no_action_required: true");
      } else {
        questions.forEach((_, questionIndex) => {
          const qNumber = questionIndex + 1;
          const checked = root.querySelector(
            `input[data-screen="${screen.screenName}"][data-question="${qNumber}"]:checked`,
          );
          parts.push(`${qNumber}:${checked ? checked.value : ""}`);
        });
      }
      const anythingElse = root.querySelector(
        `textarea[data-role="anything-else"][data-screen="${screen.screenName}"]`,
      );
      const anythingElseValue = (anythingElse && anythingElse.value.trim()) || "nothing to add";
      parts.push(`anything_else: "${anythingElseValue}"`);
      lines.push("  " + parts.join(", "));
    });
    lines.push("}");
    return lines.join("\n");
  }

  function render() {
    const heading = document.createElement("h3");
    heading.textContent = "Review each page and suggest any changes";
    root.append(heading);

    const intro = document.createElement("p");
    intro.textContent = "Open each page below. Pick \"No action required\" if you're happy with it, or choose an option for each question. Add anything else in the free-text box.";
    root.append(intro);

    const list = document.createElement("div");
    list.className = "owner-review-list";
    screens.forEach((screen) => list.append(buildScreenCard(screen)));
    root.append(list);

    const submitButton = document.createElement("button");
    submitButton.type = "button";
    submitButton.className = "btn btn-primary";
    submitButton.textContent = "Submit review";
    submitButton.addEventListener("click", () => {
      const body = composeSubmission();
      const subject = `Website review — ${businessName}`;
      window.location.href =
        `mailto:${encodeURIComponent(recipient)}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    });
    root.append(submitButton);
  }

  render();
})();
