"use strict";

// Keep in sync with testgen/models.py (TestType, Priority) and
// testgen/core/generator.py (DEFAULT_MODEL).
const TEST_TYPES = [
  "Functional",
  "Negative",
  "Boundary",
  "Security",
  "Usability",
  "Performance",
];
const PRIORITIES = ["Critical", "High", "Medium", "Low"];
const DEFAULT_MODEL = "claude-opus-4-8";

let suite = null;

const el = {
  requirement: document.getElementById("requirement"),
  instructions: document.getElementById("instructions"),
  model: document.getElementById("model"),
  generateBtn: document.getElementById("generate-btn"),
  errorBanner: document.getElementById("error-banner"),
  resultsSection: document.getElementById("results-section"),
  feature: document.getElementById("feature"),
  summary: document.getElementById("summary"),
  cases: document.getElementById("cases"),
  addCaseBtn: document.getElementById("add-case-btn"),
  exportFormat: document.getElementById("export-format"),
  downloadBtn: document.getElementById("download-btn"),
  caseTemplate: document.getElementById("case-template"),
  stepTemplate: document.getElementById("step-template"),
};

function linesToArray(text) {
  return text
    .split("\n")
    .map((s) => s.trim())
    .filter(Boolean);
}

function showError(message) {
  el.errorBanner.textContent = message;
  el.errorBanner.classList.remove("hidden");
}

function clearError() {
  el.errorBanner.textContent = "";
  el.errorBanner.classList.add("hidden");
}

async function extractError(response) {
  try {
    const data = await response.json();
    return data.detail || response.statusText;
  } catch {
    return response.statusText;
  }
}

async function generate() {
  const requirement = el.requirement.value.trim();
  if (!requirement) {
    showError("Enter a requirement or user story first.");
    return;
  }

  clearError();
  el.generateBtn.disabled = true;
  el.generateBtn.textContent = "Generating...";

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        requirement,
        instructions: el.instructions.value.trim(),
        model: el.model.value.trim() || DEFAULT_MODEL,
      }),
    });

    if (!response.ok) {
      showError(await extractError(response));
      return;
    }

    suite = await response.json();
    renderSuite();
    el.resultsSection.classList.remove("hidden");
  } catch (err) {
    showError(String(err));
  } finally {
    el.generateBtn.disabled = false;
    el.generateBtn.textContent = "Generate";
  }
}

function nextCaseId() {
  let max = 0;
  for (const tc of suite.test_cases) {
    const m = /^TC-(\d+)$/.exec(tc.id);
    if (m) max = Math.max(max, parseInt(m[1], 10));
  }
  return `TC-${String(max + 1).padStart(3, "0")}`;
}

function addCase() {
  suite.test_cases.push({
    id: nextCaseId(),
    title: "",
    type: "Functional",
    priority: "Medium",
    preconditions: [],
    steps: [{ action: "", expected_result: "" }],
    test_data: [],
    tags: [],
  });
  renderSuite();
}

function deleteCase(index) {
  suite.test_cases.splice(index, 1);
  renderSuite();
}

function fillSelect(select, options, value) {
  select.innerHTML = "";
  for (const opt of options) {
    const o = document.createElement("option");
    o.value = opt;
    o.textContent = opt;
    select.appendChild(o);
  }
  select.value = value;
}

function buildStepRow(step, tc, stepIndex) {
  const node = el.stepTemplate.content.firstElementChild.cloneNode(true);
  const action = node.querySelector(".f-step-action");
  const expected = node.querySelector(".f-step-expected");
  const removeBtn = node.querySelector(".remove-step-btn");

  action.value = step.action;
  action.addEventListener("input", (e) => (step.action = e.target.value));

  expected.value = step.expected_result;
  expected.addEventListener(
    "input",
    (e) => (step.expected_result = e.target.value)
  );

  removeBtn.addEventListener("click", () => {
    tc.steps.splice(stepIndex, 1);
    renderSuite();
  });

  return node;
}

function buildCaseCard(tc, caseIndex) {
  const node = el.caseTemplate.content.firstElementChild.cloneNode(true);

  node.querySelector(".case-id").textContent = tc.id;
  node
    .querySelector(".delete-case-btn")
    .addEventListener("click", () => deleteCase(caseIndex));

  const title = node.querySelector(".f-title");
  title.value = tc.title;
  title.addEventListener("input", (e) => (tc.title = e.target.value));

  const type = node.querySelector(".f-type");
  fillSelect(type, TEST_TYPES, tc.type);
  type.addEventListener("change", (e) => (tc.type = e.target.value));

  const priority = node.querySelector(".f-priority");
  fillSelect(priority, PRIORITIES, tc.priority);
  priority.addEventListener("change", (e) => (tc.priority = e.target.value));

  const preconditions = node.querySelector(".f-preconditions");
  preconditions.value = tc.preconditions.join("\n");
  preconditions.addEventListener(
    "input",
    (e) => (tc.preconditions = linesToArray(e.target.value))
  );

  const stepsContainer = node.querySelector(".steps");
  tc.steps.forEach((step, stepIndex) =>
    stepsContainer.appendChild(buildStepRow(step, tc, stepIndex))
  );
  node.querySelector(".add-step-btn").addEventListener("click", () => {
    tc.steps.push({ action: "", expected_result: "" });
    renderSuite();
  });

  const testData = node.querySelector(".f-test-data");
  testData.value = tc.test_data.join("\n");
  testData.addEventListener(
    "input",
    (e) => (tc.test_data = linesToArray(e.target.value))
  );

  const tags = node.querySelector(".f-tags");
  tags.value = tc.tags.join(", ");
  tags.addEventListener(
    "input",
    (e) =>
      (tc.tags = e.target.value
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean))
  );

  return node;
}

function renderSuite() {
  el.feature.value = suite.feature;
  el.summary.value = suite.summary;

  el.cases.innerHTML = "";
  suite.test_cases.forEach((tc, i) =>
    el.cases.appendChild(buildCaseCard(tc, i))
  );
}

async function download() {
  clearError();
  const format = el.exportFormat.value;

  try {
    const response = await fetch("/api/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ suite, format }),
    });

    if (!response.ok) {
      showError(await extractError(response));
      return;
    }

    const blob = await response.blob();
    const disposition = response.headers.get("content-disposition") || "";
    const match = /filename="([^"]+)"/.exec(disposition);
    const filename = match ? match[1] : `testsuite.${format}`;

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  } catch (err) {
    showError(String(err));
  }
}

el.model.value = DEFAULT_MODEL;
el.feature.addEventListener("input", (e) => (suite.feature = e.target.value));
el.summary.addEventListener("input", (e) => (suite.summary = e.target.value));
el.generateBtn.addEventListener("click", generate);
el.addCaseBtn.addEventListener("click", addCase);
el.downloadBtn.addEventListener("click", download);
